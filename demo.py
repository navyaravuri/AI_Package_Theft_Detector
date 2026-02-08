# demo.py
import gradio as gr
from package_detector import PackageTheftDetector
from openfilter.filter_runtime import Filter, Frame

# -----------------------------
# OpenFilter Config (as dict)
# -----------------------------
config = {
    "detection_confidence": 0.35,
    "suspicion_threshold": 0.6,
    "approach_distance_threshold": 120,
    "package_classes": ["suitcase", "backpack", "handbag", "box"],
    "person_class": "person"
}

# -----------------------------
# OpenFilter Wrapper
# -----------------------------
class PackageTheftFilter(Filter):
    def __init__(self, config):
        super().__init__(config)  # config must be a dict
        self.detector = PackageTheftDetector()

    def process(self, frames):
        for frame in frames:
            video_path = frame.data.get("video_path")
            if video_path:
                label, score, output_path = self.detector.process_video(video_path)
                frame.data["label"] = label
                frame.data["score"] = score
                frame.data["output_path"] = output_path
        return frames

# -----------------------------
# Initialize Filter
# -----------------------------
of_filter = PackageTheftFilter(config)

# -----------------------------
# Gradio Video Analysis Function
# -----------------------------
def analyze_video(video_path):
    if not video_path:
        return None, "Please upload a video"

    # Wrap video path in OpenFilter Frame
    frame = Frame(data={"video_path": video_path})

    # Process through OpenFilter
    processed_frame = of_filter.process([frame])[0]

    result_text = f"**Result:** {processed_frame.data['label']}\n**Confidence:** {processed_frame.data['score']:.2f}"
    return processed_frame.data['output_path'], result_text

# -----------------------------
# Gradio UI
# -----------------------------
with gr.Blocks(title="📦 AI Package Theft Detector") as demo:
    gr.Markdown("## 📦 AI-Powered Package Theft Detection System")
    gr.Markdown("Upload a video of a delivery or doorstep activity. The system will analyze whether it's **suspicious** or **normal**.")

    with gr.Row():
        input_video = gr.Video(label="Upload Delivery Video")
        output_video = gr.Video(label="Processed Output")

    analyze_btn = gr.Button("🚀 Analyze Video", variant="primary")
    result_box = gr.Markdown()

    analyze_btn.click(fn=analyze_video, inputs=[input_video], outputs=[output_video, result_box])

# Launch Gradio
demo.launch()
