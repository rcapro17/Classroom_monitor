from camera import VideoStream
from detection import ObjectDetector
from storage import DataStorage
import time

# Initialize components
camera = VideoStream()
detector = ObjectDetector()
storage = DataStorage()

while True:
    frame = camera.get_frame()
    if frame is None:
        break
    
    detections = detector.detect(frame)
    if 'cell phone' in detections:
        filename = storage.save_image(frame)
        storage.log_detection(filename)
    
    camera.show_frame(frame)
    if camera.check_exit():
        break

camera.release()