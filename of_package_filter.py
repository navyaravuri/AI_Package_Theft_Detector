from openfilter.filter_runtime import Filter
from package_detector import PackageTheftDetector

class PackageTheftFilter(Filter):
    def __init__(self, config):
        super().__init__(config)  # MUST call parent constructor with config
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
