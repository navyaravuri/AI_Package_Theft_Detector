import gradio as gr
from package_detector import PackageTheftDetector
import os

detector = PackageTheftDetector()

def analyze_video(video_path):
    if not video_path:
        return None, "Please upload a video"
    label, score, output_path = detector.process_video(video_path)
    result_text = f"**Result:** {label}\n**Confidence:** {score:.2f}"
    return output_path, result_text

with gr.Blocks(title="📦 AI Package Theft Detector") as demo:
    gr.Markdown("## 📦 AI-Powered Package Theft Detection System")
    gr.Markdown("Upload a video of a delivery or doorstep activity. The system will analyze whether it's **suspicious** or **normal**.")

    with gr.Row():
        input_video = gr.Video(label="Upload Delivery Video")
        output_video = gr.Video(label="Processed Output")

    analyze_btn = gr.Button("🚀 Analyze Video", variant="primary")
    result_box = gr.Markdown()

    analyze_btn.click(fn=analyze_video, inputs=[input_video], outputs=[output_video, result_box])

demo.launch()

