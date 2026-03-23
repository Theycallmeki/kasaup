# Kasaup Marketplace 

Kasaup is a **service marketplace platform** where customers can discover local service providers, browse services, and book appointments.

This repository contains the **backend API** built using **FastAPI**, **SQLAlchemy**, and **PostgreSQL**.

The system supports provider listings, service management, appointment scheduling, and location-based provider discovery.

---

# Tech Stack

Backend Framework

* FastAPI

Database

* PostgreSQL

ORM

* SQLAlchemy

Authentication

* JWT Access Tokens
* Refresh Tokens
* Cookie-based Authentication

Security

* bcrypt password hashing

Planned Frontend

* Vue
* PrimeVue

Future Infrastructure

* Docker
* Nginx
* DigitalOcean

---

# Architecture Overview

The backend follows a **layered architecture**.

Router Layer
Handles API endpoints.

Service Layer
Contains business logic and reusable services.

Schema Layer
Pydantic models for request and response validation.

Model Layer
SQLAlchemy ORM models representing database tables.

Core Layer
Application configuration, dependencies, and security utilities.

---

# Core Features

Authentication System

* JWT Access Tokens
* Refresh Tokens
* Cookie-based authentication
* bcrypt password hashing
* Protected routes

Authentication Endpoints

```text
POST /auth/login
POST /auth/refresh
POST /auth/logout
GET /auth/me
```

---

# Running the Backend

Follow these steps to start the backend locally.

## 1 Clone the repository

```bash
git clone <repository-url>
cd kasaup-backend
```

---

## 2 Create a virtual environment

```bash
python -m venv venv
```

Activate the virtual environment.

Windows

```bash
venv\Scripts\activate
```

macOS / Linux

```bash
source venv/bin/activate
```

---

## 3 Install dependencies

```bash
pip install -r requirements.txt
```

---

## 4 Configure environment variables

Create a `.env` file in the project root.

Example configuration

```env
DATABASE_URL=postgresql://postgres:password@localhost/your-db-name
SECRET_KEY=your-secret-key
ACCESS_TOKEN_EXPIRE_MINUTES=30
REFRESH_TOKEN_EXPIRE_DAYS=7
```

Make sure PostgreSQL is running and the database exists.

Example

```sql
CREATE DATABASE kasaup;
```

---

## 5 Start the FastAPI server

Run the development server using Uvicorn.

```bash
uvicorn app.main:app --reload
```

After the server starts, open the following page in your browser to view and test the API documentation:

```
http://127.0.0.1:8000/docs#/
```

This interactive documentation allows you to explore and test all available API endpoints directly from the browser.

---

# Development Status

Current progress

Authentication ✔
Users ✔
Providers ✔
Services ✔
Categories ✔
Appointments ✔
Provider availability ✔
Booking system ✔
Nearby search ✔
Provider dashboard ✔




---

# Frontend (Planned)

Frontend will be built with

* Vue
* PrimeVue



---

# License

This project is currently under development.
