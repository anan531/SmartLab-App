# SmartLab

SmartLab is a **College Computer Lab Management and Monitoring System** designed to simplify the administration of computer laboratories in educational institutions. The system enables administrators, faculty, and lab assistants to efficiently monitor lab activities, manage resources, and remotely control student systems through an intuitive web and mobile interface.

## Features

* 👨‍🏫 Role-based access for **Admin, Staff, Lab Assistant, and Students**
* 💻 Real-time monitoring of student computer activity
* 📸 Capture desktop screenshots from student systems
* 📷 Capture webcam images of students for monitoring and attendance
* 🖥️ Remote system management (Shutdown, Restart, Process Monitoring)
* 🔔 Notification system for suspicious or important activities
* 📚 Student, Staff, Department, Course, and Subject Management
* 🧑‍💻 Computer and Lab Resource Management
* 🪑 System Allocation for Students
* 📝 Student Feedback Management for Staff Evaluation
* 📊 Lab monitoring and activity logging
* 🔐 Secure authentication and role-based authorization

## Technology Stack

### Backend

* Python
* Django

### Frontend

* HTML
* CSS
* Flutter (Mobile Application)

### Database

* MySQL

## System Modules

* Admin Module
* Staff Module
* Lab Assistant Module
* Student Module
* Computer Monitoring Module
* Screenshot & Webcam Capture Module
* Remote Command Execution Module
* Feedback Management Module
* Notification Module

## Project Structure

```
SmartLab/
│── MyApp/
│── SmartLab/
│── static/
│── templates/
│── manage.py
```

## Installation

### Clone the repository

```bash
git clone https://github.com/anan531/SmartLab-App.git
cd SmartLab-App
```

### Create a virtual environment

```bash
python -m venv venv
```

Activate the virtual environment:

**Windows**

```bash
venv\Scripts\activate
```

**Linux / macOS**

```bash
source venv/bin/activate
```

### Install dependencies

```bash
pip install -r requirements.txt
```

### Configure the database

Create a MySQL database and update the database credentials in `settings.py`.

### Run migrations

```bash
python manage.py makemigrations
python manage.py migrate
```

### Start the server

```bash
python manage.py runserver
```

Visit:

```
http://127.0.0.1:8000/
```

## Screenshots


* Add Course
<img width="752" height="492" alt="image" src="https://github.com/user-attachments/assets/e4e04507-1e3f-4771-9604-6c04e8c23c4b" />
  
* Add Lab
<img width="727" height="404" alt="image" src="https://github.com/user-attachments/assets/676c677b-fe19-43e1-8b4e-471fca5508e6" />


* NOTIFICATION details
<img width="754" height="457" alt="image" src="https://github.com/user-attachments/assets/5444169a-6b9c-4d20-bb0b-3906d5b94498" />

  
* View Complaints
<img width="746" height="292" alt="image" src="https://github.com/user-attachments/assets/836f8a8f-506b-4fb3-b947-a94cd94d52ce" />


* Student Dashboard
<img width="230" height="689" alt="image" src="https://github.com/user-attachments/assets/9f43db1f-031f-4c15-bff8-9ccd6788d38e" />

* View Subjects
<img width="215" height="644" alt="image" src="https://github.com/user-attachments/assets/6ec49719-8f6d-4e25-997c-d4ed1328b708" />


## Future Enhancements

* AI-based student activity analysis
* Cloud-based monitoring
* Biometric authentication
* Mobile application improvements
* Advanced analytics dashboard
* Automated issue detection
* Enhanced security features

## Authors

**Ananya T**

B.Sc. Computer Science

Providence Women's College (Autonomous)

## License

This project was developed for academic and educational purposes.
