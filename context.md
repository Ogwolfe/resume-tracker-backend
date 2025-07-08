# 📌 Resume Tracker – Backend Context

This document provides essential context for the Flask backend of the Resume Tracker web application. It is designed for use with Cursor.ai, collaborators, and contributors.

---

## 🧠 Project Summary

Resume Tracker is a full-stack web app to help users keep track of job applications. This backend is built with **Flask** and will provide a RESTful API to support user registration, login, and job entry management.

---

## ⚙️ Tech Stack

- **Language**: Python 3
- **Framework**: Flask
- **Database (Dev)**: SQLite
- **Database (Prod)**: PostgreSQL (via Render)
- **Auth**: Flask-Login
- **ORM**: SQLAlchemy
- **CORS**: Flask-CORS
- **Secrets Config**: python-dotenv
- **Server (Prod)**: Gunicorn
- **Deployment**: Render.com

---

## 🏗 Directory Structure

- app/
  - __init__.py: App factory, extension initialization, blueprint registration
  - models.py: SQLAlchemy models (User, etc.)
  - routes.py: Blueprints for authentication and other endpoints
- config.py: Configuration for Flask, database, and secrets
- run.py: Entrypoint to run the Flask app
- requirements.txt: Python dependencies
- context.md: Project context and documentation

