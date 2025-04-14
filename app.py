import PIL.Image
import gradio as gr
import PIL

with gr.Blocks(theme=gr.themes.Soft(primary_hue = "red")) as demo:
    title = gr.Image(value=PIL.Image.open("novaai.png"), show_label=False)
    with gr.Row():
        with gr.Column():
            input_img = gr.Image(label="Input", sources="webcam")
        with gr.Column():
            imput_aud = gr.Audio(sources=["microphone"], streaming=True)
            box = gr.Text("I'm Nova, your alien shape-shifting celebrity study buddy! I can help you solve math problems, explain tough science concepts, or just vibe out with your favorite character voices. Whether you're cramming for finals or casually curious, I'm here to make learning cosmic-level fun. Let's turn your whiteboard chaos into brilliance—one equation at a time.", label="Learn with Nova!")

demo.launch(share=True)