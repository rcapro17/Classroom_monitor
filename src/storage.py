import sqlite3
import cv2
import time
import datetime
import os

class DataStorage:
    def __init__(self, db_path="./data/detections.db", save_dir="./data/captures", cooldown_seconds=5):
        self.db_path = os.path.abspath(db_path)
        self.save_dir = os.path.abspath(save_dir)
        self.cooldown_seconds = cooldown_seconds  # Cooldown to avoid redundant images
        self.last_capture_time = None  # Track last image save time

        os.makedirs(self.save_dir, exist_ok=True)  # Ensure directory exists
        self._init_db()

    def _init_db(self):
        """Initialize the SQLite database and create the detections and occurrences tables if they do not exist."""
        conn = sqlite3.connect(self.db_path)
        c = conn.cursor()

        # Create the detections table if it doesn't exist
        c.execute("""CREATE TABLE IF NOT EXISTS detections (
                     timestamp TEXT,
                     image_path TEXT)""")
        
        # Create the occurrences table to store currency data
        c.execute("""CREATE TABLE IF NOT EXISTS ocorrencies (
                     id INTEGER PRIMARY KEY AUTOINCREMENT,
                     student_name TEXT,
                     teacher_name TEXT,
                     observations TEXT,
                     image_path TEXT,
                     timestamp TEXT)""")

        conn.commit()
        conn.close()

    def save_image(self, frame):
        """Save an image only if cooldown time has passed."""
        current_time = datetime.datetime.now()

        if self.last_capture_time is None or (current_time - self.last_capture_time).total_seconds() > self.cooldown_seconds:
            timestamp = current_time.strftime("%Y%m%d_%H%M%S")
            filename = os.path.join(self.save_dir, f"cellphone_{timestamp}.jpg")

            print(f"[DEBUG] Attempting to save image at: {filename}")

            success = cv2.imwrite(filename, frame)
            if success:
                self.last_capture_time = current_time  # Update last capture time
                print(f"[INFO] Image saved successfully: {filename}")
                self.log_detection(filename)
            else:
                print("[ERROR] Failed to save image!")

            return filename if success else None
        else:
            print("[DEBUG] Skipping image save (cooldown active)")
            return None

    def log_detection(self, filename):
        """Log the image capture event in the SQLite database."""
        if not filename:
            print("[ERROR] No filename received, skipping database entry.")
            return

        conn = sqlite3.connect(self.db_path)
        c = conn.cursor()
        c.execute("INSERT INTO detections VALUES (?, ?)", (time.ctime(), filename))
        conn.commit()
        conn.close()
        print(f"[INFO] Detection logged: {filename}")

    def save_ocurrency(self, student_name, teacher_name, observations, image_path, timestamp):
        """Save the currency (ocorrency) data to the database."""
        conn = sqlite3.connect(self.db_path)
        c = conn.cursor()
        c.execute("""
            INSERT INTO ocorrencies (student_name, teacher_name, observations, image_path, timestamp)
            VALUES (?, ?, ?, ?, ?)
        """, (student_name, teacher_name, observations, image_path, timestamp))
        conn.commit()
        conn.close()
        print(f"[INFO] Ocorrency saved for {student_name}")
