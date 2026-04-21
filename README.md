# Student Result Management System (SRMS)
### Developed during internship at Swizosoft (OPC) Private Limited
**Student:** Appaji Reddy V | **USN:** 1DB22CI017 | **Branch:** CSE (AI&ML)

---

## 🚀 Quick Start (5 steps)

### Prerequisites
- Python 3.10 or higher installed
- pip (comes with Python)

---

### Step 1 – Extract the zip
```
unzip student_result_system.zip
cd student_result_system
```

### Step 2 – Create & activate a virtual environment
**Windows:**
```cmd
python -m venv venv
venv\Scripts\activate
```
**macOS / Linux:**
```bash
python3 -m venv venv
source venv/bin/activate
```

### Step 3 – Install dependencies
```bash
pip install -r requirements.txt
```

### Step 4 – Set up the database & seed sample data
```bash
python manage.py migrate
python manage.py seed_data
```

### Step 5 – Run the development server
```bash
python manage.py runserver
```

Open your browser and go to: **http://127.0.0.1:8000**

---

## 🔑 Login Credentials

| Role      | Username   | Password     |
|-----------|------------|-------------|
| Admin     | `admin`    | `admin123`  |
| Student   | `appaji`   | `student123`|
| Student   | `student2` | `student123`|
| Student   | `student3` | `student123`|

---

## 📋 Features

### Admin Portal
- **Dashboard** – Overview stats (students, subjects, results, departments)
- **Student Management** – Add / edit / delete students with role-based access
- **Subject Management** – Create subjects with semester, credits, max marks
- **Marks Entry** – Enter marks per student per subject; grades & GPA auto-calculated
- **Department Management** – Manage departments
- **Django Admin** – Full admin at `/admin/`

### Student Portal
- **Dashboard** – Personal info, semester-wise GPA cards, quick result summary
- **Marksheet** – Full marksheet with subject-wise grades, pass/fail, GPA
- **Performance Chart** – Interactive bar chart (Chart.js) filterable by semester

### Grading Scale
| Grade | Range  | Grade Points |
|-------|--------|-------------|
| O     | ≥ 90%  | 10          |
| A+    | ≥ 80%  | 9           |
| A     | ≥ 70%  | 8           |
| B+    | ≥ 60%  | 7           |
| B     | ≥ 50%  | 6           |
| C     | ≥ 40%  | 5           |
| F     | < 40%  | 0           |

---

## 🛠 Tech Stack
| Layer       | Technology                        |
|-------------|-----------------------------------|
| Backend     | Python 3.x, Django 4.2            |
| Frontend    | HTML5, Bootstrap 5, Chart.js      |
| Database    | SQLite3 (dev) / PostgreSQL (prod) |
| Auth        | Django built-in + Role Groups     |

---

## 📁 Project Structure
```
student_result_system/
├── manage.py
├── requirements.txt
├── README.md
├── db.sqlite3                  ← created after migrate
├── student_result_system/
│   ├── settings.py
│   └── urls.py
└── results/
    ├── models.py               ← Department, StudentProfile, Subject, Result
    ├── views.py                ← All view logic
    ├── forms.py                ← Django forms
    ├── urls.py                 ← URL routing
    ├── admin.py                ← Admin registrations
    ├── migrations/
    └── templates/results/
        ├── base.html
        ├── login.html
        ├── admin_dashboard.html
        ├── student_dashboard.html
        ├── student_list/form/detail.html
        ├── subject_list/form.html
        ├── result_list/form.html
        ├── marksheet.html
        ├── department_list/form.html
        └── confirm_delete.html
```

---

## 🔒 Security Notes
- Change `SECRET_KEY` in `settings.py` before deploying
- Set `DEBUG = False` in production
- Use PostgreSQL and environment variables in production

---

## 📞 Support
**Appaji Reddy V** | appajireddyv7@gmail.com | +91 7483324384
