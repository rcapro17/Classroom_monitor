from ultralytics import YOLO
import cv2

class ObjectDetector:
    def __init__(self, model_path="../models/yolov8n.pt"):
        self.model = YOLO(model_path)

    def detect(self, frame):
        results = self.model(frame)
        detected_objects = []
        for result in results:
            for box in result.boxes:
                obj_class = result.names[int(box.cls)]
                detected_objects.append(obj_class)
                if obj_class == "cell phone":
                    x1, y1, x2, y2 = map(int, box.xyxy[0])
                    cv2.rectangle(frame, (x1, y1), (x2, y2), (0, 255, 0), 2)
        return detected_objects