# 🧠 Job Portal API

A feature-rich job portal backend built with Django REST Framework. This API allows users to register, post and apply to jobs, with dynamic role-based permissions, background email tasks via Celery, and a fully Dockerized deployment setup.

---

## 🚀 Features

- 👤 User registration, login & JWT authentication
- 🛡️ Role-based **dynamic permissions**
- 📮 Job creation, listing, application, and management
- 🔐 Password reset via **email OTP**
- ⚙️ Background tasks with **Celery** & **Redis**
- ⏰ Scheduled tasks using **Celery Beat**
- 🐳 Dockerized for easy setup & deployment
- 🗃️ PostgreSQL database
- 📤 API testing with **Postman**
- 🧪 Throttling & rate-limiting
- 📲 Twilio (or SMTP) integration for OTP/email
- 🧩 Clean code structure, reusable apps, and modular design

---

## 📁 Project Structure

```bash
job_portal/
├── docker/
├── users/
├── jobs/
├── core/
├── media/
├── static/
├── manage.py
├── Dockerfile
├── docker-compose.yml
├── requirements.txt
├── .env
└── .gitignore
