import gradio as gr
import requests


def query_model(prompt):
    # Updated API endpoint
    endpoint = "https://ink-concert-snapshot-engage.trycloudflare.com/v1/completions"

    # Prepare the data payload
    data = {
        "prompt": prompt,
        "max_tokens": 200,
        "temperature": 0.7,
        "top_p": 0.9,
        "seed": 666
    }

    # Send a POST request to the API
    response = requests.post(endpoint, json=data)

    # Extract the response text
    if response.status_code == 200:
        return response.json()["choices"][0]["text"]
    else:
        return "Error: " + str(response.status_code)


# Create a Gradio interface
iface = gr.Interface(
    fn=query_model,
    inputs=gr.components.Textbox(lines=2, placeholder="Enter your prompt here..."),
    outputs="text",
    title="DEBUG DAEMON : Custom AI Model Query",
    # description="",
    theme=gr.themes.Monochrome()
)

# Launch the Gradio app
if __name__ == "__main__":
    iface.launch()
