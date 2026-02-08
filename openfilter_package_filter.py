from openfilter.filter_runtime import Filter
from config import PackageTheftFilterConfig
from package_detector import PackageTheftDetector

class PackageTheftFilter(Filter):
    def setup(self, config: PackageTheftFilterConfig):
        self.detector = PackageTheftDetector()
        self.config = config

    def process(self, frames):
        for frame in frames:
            video_path = frame.data.get("video_path")
            if video_path:
                label, score, output_path = self.detector.process_video(video_path)
                frame.data["label"] = label
                frame.data["score"] = score
                frame.data["output_path"] = output_path
        return frames
