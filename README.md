💼 Job Board Web Application

A fully functional Job Board Web Application that allows employers to post jobs and candidates to search and apply for them.
Built using Django with a clean UI and deployed on Render.

🌐 Live Demo:
👉 https://django-job-board-4ja4.onrender.com/

🚀 Features

User authentication (Login / Register)

Employer & Job Seeker role-based access

Employers can create and manage companies

Employers can post job listings

Job seekers can browse and search jobs

Job application functionality

Django Admin panel for management

Responsive UI using HTML & CSS

Secure forms with CSRF protection

🛠️ Tech Stack
Backend

Django (Python Web Framework)

Django ORM

SQLite (Development)

PostgreSQL (Production – Render)

Frontend

HTML5

CSS3

Bootstrap (if used)

Authentication

Django Authentication System

Deployment

Render (Web Service Hosting)

Gunicorn (WSGI Server)

📂 Project Structure (Simplified)

accounts – User authentication & roles

companies – Company & job posting management

applications – Job application logic

templates – HTML templates

static – CSS & static files

config – Project settings & URLs                                                                                                                                                                                                                 

⚙️ Installation & Setup (Local)
# Clone the repository
git clone https://github.com/your-username/django-job-board.git

# Move into project folder
cd django-job-board

# Create virtual environment
python -m venv .venv
source .venv/bin/activate   # Windows: .venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Run migrations
python manage.py migrate

# Start server
python manage.py runserver
