# Student Management System

A web-based Student Management System built with Django, Django REST Framework, and PostgreSQL. It allows managing student profiles, filtering and searching records by department, and exposes REST API endpoints.

---

## 🚀 Features

- **Student Directory:** View, search, filter by department, and sort student lists.
- **Profile Management:** Add, view, update, and delete student details.
- **REST API:** Endpoints to fetch students in JSON format (`/api/students/`).
- **Pagination:** Clean, built-in paginated student list view.
- **Database:** Backed by PostgreSQL for production-ready data persistence.

---

## 📋 Prerequisites

Ensure you have the following installed on your system:

- **Python** (v3.10 or higher) - [Download Python](https://www.python.org/downloads/)
- **PostgreSQL** - [Download PostgreSQL](https://www.postgresql.org/download/)
- **Git** - [Download Git](https://git-scm.com/)

---

## 🛠️ Getting Started

Follow these steps to set up and run the project locally.

### 1. Clone the Repository

```bash
git clone https://github.com/JubairHossain-280/Student_Management_System.git
cd Student_Management_System
```

*(If `manage.py` is inside `myproject/`, navigate into it: `cd myproject`)*

---

### 2. Create and Activate a Virtual Environment

#### On Windows:
```bash
# Using PowerShell or Command Prompt
python -m venv venv

# Activate on PowerShell:
.\venv\Scripts\Activate.ps1

# Or activate on Command Prompt (CMD):
.\venv\Scripts\activate.bat
```

#### On macOS / Linux:
```bash
python3 -m venv venv
source venv/bin/activate
```

---

### 3. Install Dependencies

With the virtual environment activated, install all required packages:

```bash
pip install -r requirements.txt
```

---

### 4. Configure Environment Variables

1. Copy the sample environment file:
   ```bash
   cp .env.example .env
   ```
   *(On Windows Command Prompt: `copy .env.example .env`)*

2. Open `.env` and fill in your local PostgreSQL credentials and secret key:
   ```env
   SECRET_KEY=your-secret-key-here
   DEBUG=True
   ALLOWED_HOSTS=127.0.0.1,localhost

   DB_NAME=student_management_system
   DB_USER=postgres
   DB_PASSWORD=your_postgres_password
   DB_HOST=localhost
   DB_PORT=5432
   ```

3. Ensure you have created the database in PostgreSQL:
   ```sql
   CREATE DATABASE student_management_system;
   ```

---

### 5. Apply Migrations

Run database migrations to create all required tables:

```bash
python manage.py migrate
```

---

### 6. Create a Superuser (Optional)

To access the Django Admin panel:

```bash
python manage.py createsuperuser
```
Follow the prompts to set up a username, email, and password.

---

### 7. Run the Development Server

Start the local Django server:

```bash
python manage.py runserver
```

Once running, visit:
- **Application:** [http://127.0.0.1:8000/](http://127.0.0.1:8000/)
- **Student List:** [http://127.0.0.1:8000/students/](http://127.0.0.1:8000/students/)
- **Django Admin:** [http://127.0.0.1:8000/admin/](http://127.0.0.1:8000/admin/)
- **API Endpoints:** [http://127.0.0.1:8000/api/students/](http://127.0.0.1:8000/api/students/)

---

## 📂 Project Structure

```text
myproject/
│
├── myapp/                     # Core application
│   ├── migrations/            # Database schema migrations
│   ├── static/                # Static assets (CSS, JS, images)
│   ├── templates/             # HTML templates
│   ├── models.py              # Database models
│   ├── views.py               # View controllers / business logic
│   ├── serializers.py         # DRF serializers
│   └── urls.py                # App URL routing
│
├── myproject/                 # Project configuration
│   ├── settings.py            # Global settings
│   ├── urls.py                # Root URL configuration
│   └── wsgi.py / asgi.py      # Server entry points
│
├── .env.example               # Template for environment variables
├── .gitignore                 # Files ignored by Git
├── manage.py                  # Django CLI runner
└── requirements.txt           # Python dependencies
```

---

## 📄 License

This project is open source and available under the [MIT License](LICENSE).
