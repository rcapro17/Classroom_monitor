Classroom Monitor is a project that uses a camera to detect and capture images of students' devices (like cellphones) in a classroom. It provides functionality to track occurrences and manage them through a simple web interface.

**1.** To get started with the project, follow these steps:

git clone https://github.com/your-username/Classroom_monitor.git

**2.** Navigate into the project directory:

cd Classroom_monitor

**3.** Create and activate a virtual environment (if using Python):
   
python3 -m venv venv
source venv/bin/activate

**4.** Install dependencies:
   
pip install -r requirements.txt

**5.** Start the application:
   
python app.py

**6.** Open your browser and go to http://127.0.0.1:5000 to access the Classroom Monitor.
   
**Features**

***Monitor mode:*** The system monitors the classroom and detects cellphones.
***Ocorrências (Occurrences):**** You can create reports for detected devices and store them in a database.
***View captured images:*** View and manage captured images from the system.

**Example Workflow**

The system monitors the classroom, captures images, and allows you to create reports.
After each image capture, you can add an "Occurrence" by providing student details and observations.

**Project Structure**

Here's a breakdown of the project structure:

<img width="385" alt="Project_Structure" src="https://github.com/user-attachments/assets/6a8f78bb-5c4f-4ee8-aaa0-aae8fd516ba1" />


