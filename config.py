# config.py
import os

PROJECT_DIR = os.path.dirname(os.path.abspath(__file__))
OUTPUT_DIR = os.path.join(PROJECT_DIR, "outputs")
os.makedirs(OUTPUT_DIR, exist_ok=True)

# Detection settings
PACKAGE_CLASSES = ["suitcase", "backpack", "handbag", "box"]
PERSON_CLASS = "person"

DETECTION_CONFIDENCE = 0.35
SUSPICION_THRESHOLD = 0.6

# Tracking / logic thresholds
APPROACH_DISTANCE_THRESHOLD = 120
PACKAGE_MISSING_FRAMES = 20

# of_config.py
from openfilter.filter_runtime import FilterConfig

class PackageTheftFilterConfig(FilterConfig):
    detection_confidence: float = 0.35
    suspicion_threshold: float = 0.6
    approach_distance_threshold: int = 120
    package_classes: list = ["suitcase", "backpack", "handbag", "box"]
    person_class: str = "person"
