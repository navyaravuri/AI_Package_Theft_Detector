import cv2
import numpy as np
from ultralytics import YOLO
from collections import deque
from config import *

class PackageTheftDetector:
    def __init__(self, model_name="yolov8n.pt"):
        self.model = YOLO(model_name)
        self.reset_state()

    def reset_state(self):
        self.prev_packages = []
        self.prev_persons = []
        self.events = deque(maxlen=100)
        self.suspicion_score = 0.0
        self.package_present = False
        self.last_event = None

    def is_near(self, box1, box2, thresh=APPROACH_DISTANCE_THRESHOLD):
        """Check if two bounding boxes are close"""
        x1, y1, x2, y2 = box1
        cx1, cy1 = (x1 + x2) / 2, (y1 + y2) / 2
        x3, y3, x4, y4 = box2
        cx2, cy2 = (x3 + x4) / 2, (y3 + y4) / 2
        return np.hypot(cx2 - cx1, cy2 - cy1) < thresh

    def detect_objects(self, frame):
        results = self.model(frame, verbose=False)[0]
        persons, packages = [], []
        for box in results.boxes:
            cls_id = int(box.cls[0])
            label = results.names[cls_id]
            conf = float(box.conf[0])
            if conf < DETECTION_CONFIDENCE:
                continue
            xyxy = box.xyxy[0].cpu().numpy().astype(int)
            if label == PERSON_CLASS:
                persons.append(xyxy)
            elif label in PACKAGE_CLASSES:
                packages.append(xyxy)
        return persons, packages

    def process_video(self, video_path):
        cap = cv2.VideoCapture(video_path)
        fps = cap.get(cv2.CAP_PROP_FPS)
        if fps == 0:
            fps = 30
        out_path = video_path.replace(".mp4", "_processed.mp4")
        fourcc = cv2.VideoWriter_fourcc(*"mp4v")
        out = None
        frame_idx = 0
        package_state = "none"  # can be "none", "present", or "removed"

        while True:
            ret, frame = cap.read()
            if not ret:
                break
            frame_idx += 1
            persons, packages = self.detect_objects(frame)

            if out is None:
                h, w = frame.shape[:2]
                out = cv2.VideoWriter(out_path, fourcc, fps, (w, h))

            # Detect package appearance or disappearance
            if not self.prev_packages and packages:
                # Package appeared
                package_state = "present"
                self.last_event = "dropoff"
                self.suspicion_score = max(0.0, self.suspicion_score - 0.2)

            elif self.prev_packages and not packages:
                # Package disappeared
                package_state = "removed"
                nearby = any(self.is_near(p_prev, per) for per in persons for p_prev in self.prev_packages)
                if nearby:
                    self.last_event = "pickup"
                    self.suspicion_score = min(1.0, self.suspicion_score + 0.5)
                else:
                    self.suspicion_score = max(0.0, self.suspicion_score - 0.1)

            # Draw detections
            for box in persons:
                cv2.rectangle(frame, (box[0], box[1]), (box[2], box[3]), (255, 200, 0), 2)
                cv2.putText(frame, "Person", (box[0], box[1] - 10),
                            cv2.FONT_HERSHEY_SIMPLEX, 0.6, (255, 200, 0), 2)

            for box in packages:
                cv2.rectangle(frame, (box[0], box[1]), (box[2], box[3]), (0, 255, 0), 2)
                cv2.putText(frame, "Package", (box[0], box[1] - 10),
                            cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0, 255, 0), 2)

            # Add status overlay
            status = "Suspicious" if self.suspicion_score > SUSPICION_THRESHOLD else "Normal"
            color = (0, 0, 255) if status == "Suspicious" else (0, 255, 0)
            cv2.putText(frame, f"{status} ({self.suspicion_score:.2f})", (20, 40),
                        cv2.FONT_HERSHEY_SIMPLEX, 1, color, 3)

            # Update state
            self.prev_persons = persons
            self.prev_packages = packages
            out.write(frame)

        cap.release()
        if out:
            out.release()

        label = "Suspicious" if self.suspicion_score > SUSPICION_THRESHOLD else "Normal delivery"
        return label, float(self.suspicion_score), out_path
