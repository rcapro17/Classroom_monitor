import cv2

class VideoStream:
    def __init__(self, src=0):
        self.cap = cv2.VideoCapture(src)

    def get_frame(self):
        ret, frame = self.cap.read()
        return frame if ret else None

    def show_frame(self, frame):
        cv2.imshow("Classroom Monitor", frame)

    def check_exit(self):
        return cv2.waitKey(1) & 0xFF == ord('q')

    def release(self):
        self.cap.release()
        cv2.destroyAllWindows()