from flask import Flask, render_template, send_from_directory, request, jsonify
import os
import subprocess
from datetime import datetime
from src.storage import DataStorage
import sqlite3
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

app = Flask(__name__)

CAPTURE_FOLDER = "./data/captures"
app.config["CAPTURE_FOLDER"] = CAPTURE_FOLDER

# Initialize DataStorage class
storage = DataStorage()

# Global variable to control the monitoring state
monitoring_process = None

def get_captured_images():
    images = []
    for filename in sorted(os.listdir(CAPTURE_FOLDER), reverse=True):
        if filename.endswith(".jpg") or filename.endswith(".png"):
            try:
                timestamp = filename.split("_")[-1].split(".")[0]
                timestamp = datetime.fromtimestamp(int(timestamp)).strftime("%Y-%m-%d %H:%M:%S")
                images.append({"filename": filename, "timestamp": timestamp})
            except ValueError:
                continue
    return images

@app.route("/")
def index():
    images = get_captured_images()
    return render_template("index.html", images=images)

@app.route("/captures/<filename>")
def get_image(filename):
    return send_from_directory(app.config["CAPTURE_FOLDER"], filename)

@app.route("/save_currency", methods=["POST"])
def save_currency():
    data = request.json
    student_name = data.get("student_name")
    teacher_name = data.get("teacher_name")
    observations = data.get("observations")
    image_src = data.get("image_src")
    timestamp = data.get("timestamp")

    # Save currency data to the database
    storage.save_ocurrency(student_name, teacher_name, observations, image_src, timestamp)

    return jsonify({"status": "success"})

@app.route("/ocorrencias")
def show_ocorrencies():
    """Retrieve and display all occurrences."""
    conn = sqlite3.connect(storage.db_path)
    c = conn.cursor()
    c.execute("SELECT * FROM ocorrencies")
    ocorrencies = c.fetchall()
    conn.close()

    return render_template("ocorrencies.html", ocorrencies=ocorrencies)

@app.route("/start_monitoring", methods=["POST"])
def start_monitoring():
    global monitoring_process
    if monitoring_process is None:
        monitoring_process = subprocess.Popen(['python', 'src/main.py'])
    return jsonify({"status": "monitoring_started"})

@app.route("/stop_monitoring", methods=["POST"])
def stop_monitoring():
    global monitoring_process
    if monitoring_process is not None:
        monitoring_process.terminate()
        monitoring_process = None
    return jsonify({"status": "monitoring_stopped"})

@app.route("/send_email", methods=["POST"])
def send_email():
    email_data = request.json
    student_name = email_data.get("student_name")
    teacher_name = email_data.get("teacher_name")
    observations = email_data.get("observations")
    image_src = email_data.get("image_src")
    timestamp = email_data.get("timestamp")

    # Send email logic
    try:
        sender_email = "your_email@example.com"
        receiver_email = "recipient_email@example.com"
        subject = f"Occurrence for {student_name} ({timestamp})"
        body = f"Details:\n\nStudent: {student_name}\nTeacher: {teacher_name}\nObservations: {observations}\nTimestamp: {timestamp}\n\nImage: {image_src}"

        msg = MIMEMultipart()
        msg['From'] = sender_email
        msg['To'] = receiver_email
        msg['Subject'] = subject
        msg.attach(MIMEText(body, 'plain'))

        # Use SMTP to send the email (change SMTP server settings as needed)
        with smtplib.SMTP('smtp.example.com', 587) as server:
            server.starttls()
            server.login(sender_email, "your_password")
            text = msg.as_string()
            server.sendmail(sender_email, receiver_email, text)

        return jsonify({"status": "success", "message": "Email sent successfully"})
    
    except Exception as e:
        return jsonify({"status": "error", "message": str(e)})

if __name__ == "__main__":
    app.run(debug=True)
