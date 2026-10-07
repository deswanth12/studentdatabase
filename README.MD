# Student Database Management System

A desktop student record administration and academic analytics suite built in Python with modern UI components (`ttkbootstrap`), SQLite storage, and visual analytics (`matplotlib`, `pandas`).

---

## Overview

The **Student Database Management System** provides educational administrators and faculty with a centralized console to manage student enrollments, track 6-semester examination marks (Mid-1 & Mid-2), record attendance rates, perform batch queries, and export reports to CSV. It includes built-in role-based access control (Admin & User roles) with SHA-256 hashed credentials.

---

## Features

* **Student Enrollment & CRUD Management**:
  * Add, update, view, and delete student records with Roll Number, Name, Department, Year, Phone, and Attendance percentage.
  * Search and filter student records by Name, Roll Number, or Department.
* **Academic Performance Tracking**:
  * Multi-semester examination tracking across 6 semesters (Sem 1 through Sem 6, Mid-1 and Mid-2 marks).
* **Analytics & Visual Charts**:
  * Department-wise student distribution and performance analytics powered by Matplotlib.
* **Data Export & Reporting**:
  * One-click CSV export of student datasets powered by Pandas.
* **Authentication & Security**:
  * Role-based login system separating Administrator access from standard User accounts.
  * SHA-256 password hashing.
  * Default accounts initialized automatically (`admin` and `user1`).

---

## Project Structure

```text
studentdatabase/
├── .gitignore               # Ignored build, cache, and database artifacts
├── requirements.txt         # Pinned third-party dependencies
├── README.MD                # Documentation and setup guide
└── index.py                 # Main entry point and GUI application
```

---

## Dependencies

* **Python 3.10+**
* `ttkbootstrap` – Modern Bootstrap UI styling for Tkinter
* `pandas` – Data manipulation and CSV export
* `matplotlib` – Academic analytics and charts

All other packages (`tkinter`, `sqlite3`, `hashlib`) are included in the Python Standard Library.

---

## Installation & Setup

1. **Clone the repository:**
   ```bash
   git clone https://github.com/deswanth12/studentdatabase.git
   cd studentdatabase
   ```

2. **Create and activate a virtual environment (recommended):**
   ```bash
   # Windows (PowerShell)
   python -m venv venv
   .\venv\Scripts\Activate.ps1

   # Linux / macOS
   python3 -m venv venv
   source venv/bin/activate
   ```

3. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

4. **Run the application:**
   ```bash
   python index.py
   ```

*Note: On initial launch, the system automatically initializes the SQLite schema (`students.db`) and seeds default user roles if not already present.*

---

## Default Login Credentials

| Role | Username | Default Password |
| :--- | :--- | :--- |
| **Administrator** | `admin` | `admin` |
| **Standard User** | `user1` | `pass1` |

*(It is recommended to update default passwords upon first deployment).*

---

## Author

Developed by **k Deswanth** ([@deswanth12](https://github.com/deswanth12)).
