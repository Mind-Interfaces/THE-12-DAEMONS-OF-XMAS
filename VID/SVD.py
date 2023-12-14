import customtkinter
from tkinter import filedialog
import torch
from diffusers import StableVideoDiffusionPipeline
from diffusers.utils import load_image, export_to_video
from PIL import Image, ImageTk

class SVDGUI(customtkinter.CTk):
    def __init__(self):
        super().__init__()

        self.title("SVDGUI")
        self.geometry("1620x650")
        self.grid_columnconfigure((0, 1, 2, 3), weight=1)

        self.svd_pipe = StableVideoDiffusionPipeline.from_pretrained("stabilityai/stable-video-diffusion-img2vid-xt", torch_dtype=torch.float16, variant="fp16")
        self.svd_pipe.enable_model_cpu_offload()
        self.seed = 42
        self.fps = 12
        self.motion_bucket_id = 100
        self.noise_aug_strength = 0.1
        self.decode_chunk_size = 4
        self.image = None
        self.frames = []
        self.accumulated_frames = []
        self.savepath = "generate.gif"

        placeholder_image = Image.new("RGB", (1024, 576), color="#181818")
        self.display_photo = customtkinter.CTkImage(light_image=placeholder_image, dark_image=placeholder_image, size=(800, 461))

        self.image_label = customtkinter.CTkLabel(self, text="")  # Label to display the image
        self.image_label.grid(row=0, column=0, padx=5, pady=5, sticky="ew", columnspan=2)
        self.image_label.configure(image=self.display_photo)

        self.gif_label = customtkinter.CTkLabel(self, text="")
        self.gif_label.grid(row=0, column=2, padx=5, pady=5, sticky="ew", columnspan=2)
        self.gif_label.configure(image=self.display_photo)

        self.load_image_button = customtkinter.CTkButton(self, text="Select Image", command=self.load_init_image)
        self.load_image_button.grid(row=1, column=0, padx=5, pady=5, sticky="ew")
        self.load_last_frame_button = customtkinter.CTkButton(self, text="Load Last Frame", command=self.load_last_frame)
        self.load_last_frame_button.grid(row=1, column=1, padx=5, pady=5, sticky="ew")

        self.seed_label = customtkinter.CTkLabel(self, text="Seed:")
        self.seed_label.grid(row=2, column=0, padx=5, pady=5, sticky="w")
        self.seed_entry = customtkinter.CTkEntry(self, placeholder_text=self.seed)
        self.seed_entry.grid(row=2, column=0, padx=5, pady=5, sticky="e")

        self.fps_label = customtkinter.CTkLabel(self, text="Fps:")
        self.fps_label.grid(row=2, column=1, padx=5, pady=5, sticky="w")
        self.fps_entry = customtkinter.CTkEntry(self, placeholder_text=self.fps)
        self.fps_entry.grid(row=2, column=1, padx=5, pady=5, sticky="e")

        self.motion_bucket_id_label = customtkinter.CTkLabel(self, text="Motion strength 1-255:")
        self.motion_bucket_id_label.grid(row=4, column=0, padx=5, pady=5, sticky="w")
        self.motion_bucket_id_entry = customtkinter.CTkEntry(self, placeholder_text=self.motion_bucket_id)
        self.motion_bucket_id_entry.grid(row=4, column=0, padx=5, pady=5, sticky="e")

        self.decode_chunk_label = customtkinter.CTkLabel(self, text="Decode frames:")
        self.decode_chunk_label.grid(row=3, column=0, padx=5, pady=5, sticky="w")
        self.decode_chunk_entry = customtkinter.CTkEntry(self, placeholder_text=self.decode_chunk_size)
        self.decode_chunk_entry.grid(row=3, column=0, padx=5, pady=5, sticky="e")

        self.noise_aug_label = customtkinter.CTkLabel(self, text="Noise:")
        self.noise_aug_label.grid(row=3, column=1, padx=5, pady=5, sticky="w")
        self.noise_aug_entry = customtkinter.CTkEntry(self, placeholder_text=self.noise_aug_strength)
        self.noise_aug_entry.grid(row=3, column=1, padx=5, pady=5, sticky="e")

        self.save_name_label = customtkinter.CTkLabel(self, text="Name:")
        self.save_name_label.grid(row=4, column=2, padx=5, pady=5, sticky="w")
        self.save_name_entry = customtkinter.CTkEntry(self, placeholder_text=self.savepath)
        self.save_name_entry.grid(row=4, column=2, padx=5, pady=5, sticky="e")

        self.save_gif_button = customtkinter.CTkButton(self, text="Save", command=self.save_gif)
        self.save_gif_button.grid(row=4, column=3, padx=5, pady=5, sticky="ew")

        self.accumulated_frames_counter = customtkinter.CTkLabel(self, text=len(self.accumulated_frames))
        self.accumulated_frames_counter.grid(row=2, column=2, padx=5, pady=5, sticky="e")
        self.accumulated_frames_label = customtkinter.CTkLabel(self, text="Accumulated frames:")
        self.accumulated_frames_label.grid(row=2, column=2, padx=5, pady=5, sticky="w")

        self.accumulate_frames_button = customtkinter.CTkButton(self, text="Accumulate", command=self.accumulate_frames)
        self.accumulate_frames_button.grid(row=2, column=3, padx=5, pady=5, sticky="ew")

        self.clear_frames_button = customtkinter.CTkButton(self, text="Clear frames", command=self.clear_frames)
        self.clear_frames_button.grid(row=3, column=2, padx=5, pady=5, sticky="ew", columnspan=2)

        self.generate_button = customtkinter.CTkButton(self, text="Generate", command=self.generate)
        self.generate_button.grid(row=1, column=2, padx=5, pady=5, sticky="ew", columnspan=4)


    def generate(self):

        user_seed = self.seed_entry.get()
        user_fps = self.fps_entry.get()
        user_motion_bucket_id = self.motion_bucket_id_entry.get()
        user_decode_chunk = self.decode_chunk_entry.get()
        user_noise = self.noise_aug_entry.get()

        if user_seed:
            self.seed = int(user_seed)
        if user_fps:
            self.fps = int(user_fps)
        if user_motion_bucket_id:
            self.motion_bucket_id = int(user_motion_bucket_id)
        if user_decode_chunk:
            self.decode_chunk_size = int(user_decode_chunk)
        if user_noise:
            self.noise_aug_strength = float(user_noise)

        generator = torch.manual_seed(self.seed)
        self.frames = self.svd_pipe(self.image, decode_chunk_size=self.decode_chunk_size, generator=generator, motion_bucket_id=self.motion_bucket_id, noise_aug_strength=self.noise_aug_strength).frames[0]

        self.gif_label.image = None
        self.display_frames_as_gif(reset=True)





    def save_gif(self):
        self.update_idletasks()
        user_save_name = self.save_name_entry.get()
        if user_save_name:
            self.savepath = f"{user_save_name}.gif"
        self.accumulated_frames[0].save(self.savepath, save_all=True, append_images=self.accumulated_frames[1:], optimize=False, duration=int(1000 / self.fps), loop=0)
        self.update_idletasks()

    def clear_frames(self):
        self.accumulated_frames = []
        self.accumulated_frames_counter.configure(text=len(self.accumulated_frames))

    def accumulate_frames(self):
        self.accumulated_frames.extend(self.frames)
        self.accumulated_frames_counter.configure(text=len(self.accumulated_frames))

    def load_last_frame(self):
        if self.frames:
            self.image = self.frames[-1]  # Accessing the last image in the list
            self.display_photo = customtkinter.CTkImage(light_image=self.image, dark_image=self.image, size=(800, 461))
            self.image_label.configure(image=self.display_photo)


    def load_init_image(self):
        imagepath = filedialog.askopenfilename()
        if imagepath:
            self.image = load_image(imagepath)
            self.image = self.image.resize((1024, 576))
            self.display_photo = customtkinter.CTkImage(light_image=self.image, dark_image=self.image, size=(800, 461))
            self.image_label.configure(image=self.display_photo)

    def display_frames_as_gif(self, reset=False):
        if reset:
            # Reset GIF playback to the first frame
            self.gif_label.configure(image=self.display_photo)
            self.gif_label.image = self.display_photo
        if self.frames and self.fps:
            def update_label(index):
                if index < len(self.frames):
                    frame = self.frames[index]
                    photo = customtkinter.CTkImage(light_image=frame, dark_image=frame, size=(800, 461))
                    self.gif_label.configure(image=photo)
                    self.gif_label.image = photo
                    self.after(int(1000 / self.fps), update_label, index + 1)
                else:
                    update_label(0)
            update_label(0)


SVD = SVDGUI()
SVD.mainloop()
