import sqlite3
import tkinter as tk
from tkinter import ttk, messagebox, filedialog
import pandas as pd
import matplotlib.pyplot as plt
import hashlib
import ttkbootstrap as tb

DB_NAME = "students.db"

# ---------------- Utility Functions ----------------
def hash_password(password: str) -> str:
    """Return SHA256 hashed password."""
    return hashlib.sha256(password.encode()).hexdigest()

def db_execute(query, params=(), fetch=False):
    """Execute an SQL query with optional fetch."""
    try:
        with sqlite3.connect(DB_NAME) as conn:
            cursor = conn.cursor()
            cursor.execute(query, params)
            if fetch:
                return cursor.fetchall()
            conn.commit()
    except sqlite3.Error as e:
        # In a real application, you might want to log this error.
        print(f"Database error: {e}")
        # For a GUI app, showing a message box is often appropriate.
        messagebox.showerror("Database Error", f"An unexpected database error occurred: {e}")
        return None if fetch else False
def init_db():
    """Initialize database tables and default users."""
    db_execute("""
        CREATE TABLE IF NOT EXISTS users (
            username TEXT PRIMARY KEY,
            password TEXT NOT NULL,
            role TEXT DEFAULT 'user'
        )
    """)
    db_execute("""
        CREATE TABLE IF NOT EXISTS students (
            roll_no TEXT PRIMARY KEY,
            name TEXT NOT NULL,
            department TEXT NOT NULL,
            year INTEGER,
            sem1_mid1 INTEGER, sem1_mid2 INTEGER,
            sem2_mid1 INTEGER, sem2_mid2 INTEGER,
            sem3_mid1 INTEGER, sem3_mid2 INTEGER,
            sem4_mid1 INTEGER, sem4_mid2 INTEGER,
            sem5_mid1 INTEGER, sem5_mid2 INTEGER,
            sem6_mid1 INTEGER, sem6_mid2 INTEGER,
            phone TEXT,
            attendance TEXT
        )
    """)
    # Default accounts
    db_execute("INSERT OR IGNORE INTO users VALUES (?, ?, ?)", 
               ("admin", hash_password("admin"), "admin"))
    db_execute("INSERT OR IGNORE INTO users VALUES (?, ?, ?)", 
               ("user1", hash_password("pass1"), "user"))

# ---------------- Application Class ----------------
class StudentDBApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Student DB")
        self.root.geometry("400x380")
        self.root.resizable(False, False)
        init_db()
        self.main_frame = None  # To hold the main app view
        self.login_screen()

    def login_screen(self):
        """Display login window."""
        if self.main_frame:
            self.main_frame.destroy()
            self.root.geometry("400x380") # Resize for login

        # Main frame to center content
        frame = ttk.Frame(self.root, padding="20")
        frame.pack(expand=True, fill="both")

        ttk.Label(frame, text="Student DB Login", font=("Helvetica", 16, "bold")).pack(pady=(0, 20))

        ttk.Label(frame, text="Username").pack(anchor="w", padx=5)
        username_entry = ttk.Entry(frame, width=30)
        username_entry.pack(pady=(0, 10))
        username_entry.focus_set() # Set focus here

        ttk.Label(frame, text="Password").pack(anchor="w", padx=5)
        password_entry = ttk.Entry(frame, width=30, show="*")
        password_entry.pack(pady=(0, 10))

        show_var = tb.BooleanVar()
        show_check = tb.Checkbutton(frame, text="Show Password", variable=show_var, bootstyle="secondary",
                                    command=lambda: password_entry.config(show="" if show_var.get() else "*"))
        show_check.pack(anchor="w", padx=5, pady=(0, 15))

        def login():
            uname, pwd = username_entry.get().strip(), password_entry.get().strip()
            if not uname or not pwd:
                messagebox.showwarning("Input Error", "Please fill both fields", parent=self.root)
                return
            hashed_pwd = hash_password(pwd)
            result = db_execute("SELECT role FROM users WHERE username=? AND password=?", 
                                (uname, hashed_pwd), fetch=True)
            if result:
                frame.destroy() # Destroy the login frame, not the window
                self.main_app(uname, result[0][0])
            else:
                messagebox.showerror("Login Failed", "Invalid credentials", parent=self.root)

        def open_register():
            self.register_screen(self.root)

        tb.Button(frame, text="Login", bootstyle="success", width=28, command=login).pack(pady=5)
        tb.Button(frame, text="Register New Account", bootstyle="info-outline", width=28, command=open_register).pack(pady=5)
        self.root.bind("<Return>", lambda event: login()) # Bind Enter key

    def register_screen(self, parent):
        """Display user registration."""
        reg = tb.Toplevel(parent)
        reg.title("Register")
        reg.geometry("350x280")
        reg.resizable(False, False)

        frame = ttk.Frame(reg, padding="20")
        frame.pack(expand=True)

        ttk.Label(frame, text="Create an Account", font=("Helvetica", 14, "bold")).pack(pady=(0, 15))

        ttk.Label(frame, text="Username").pack(anchor="w", padx=5)
        user_entry = ttk.Entry(frame, width=30)
        user_entry.pack(pady=(0, 10))
        user_entry.focus_set()

        ttk.Label(frame, text="Password").pack(anchor="w", padx=5)
        pass_entry = ttk.Entry(frame, width=30, show="*")
        pass_entry.pack(pady=(0, 15))

        def register():
            user, pwd = user_entry.get().strip(), pass_entry.get().strip()
            if not user or not pwd:
                messagebox.showerror("Error", "All fields required", parent=reg)
                return
            try:
                db_execute("INSERT INTO users (username, password) VALUES (?, ?)", 
                           (user, hash_password(pwd)))
                messagebox.showinfo("Success", "User registered successfully", parent=reg)
                reg.destroy()
            except sqlite3.IntegrityError:
                messagebox.showerror("Error", "Username already exists", parent=reg)

        tb.Button(frame, text="Register", bootstyle="primary", width=28, command=register).pack(pady=10)
        reg.bind("<Return>", lambda event: register())

    def _validate_digit(self, P, max_len):
        """Validation function to allow only digits up to a max length."""
        if P == "":
            return True
        if P.isdigit() and len(P) <= max_len:
            return True
        return False

    def main_app(self, username, role):
        """Main student database UI."""
        self.root.unbind("<Return>") # Unbind login's Enter key
        self.root.title(f"Student DB - Logged in as {username} ({role})")
        self.root.geometry("950x600")
        self.root.resizable(True, True)

        self.main_frame = ttk.Frame(self.root, padding=10)
        self.main_frame.pack(fill="both", expand=True)

        # Top bar with theme switcher and logout
        top_bar = ttk.Frame(self.main_frame)
        top_bar.pack(fill="x", pady=(0, 10))

        def toggle_theme():
            current_theme = self.root.style.theme_use()
            if "dark" in current_theme or "superhero" in current_theme:
                self.root.style.theme_use("flatly")
            else:
                self.root.style.theme_use("superhero")
        
        theme_button = tb.Checkbutton(top_bar, text="Dark Mode", bootstyle="round-toggle", command=toggle_theme)
        theme_button.pack(side="right")

        logout_button = tb.Button(top_bar, text="Logout", bootstyle="danger-outline", command=self.logout_screen)
        logout_button.pack(side="right", padx=10)
        
        # Search bar
        search_frame = ttk.Frame(self.main_frame)
        search_frame.pack(fill="x", pady=5)
        ttk.Label(search_frame, text="Search:").pack(side="left", padx=5)
        search_entry = ttk.Entry(search_frame)
        search_entry.pack(side="left", fill="x", expand=True, padx=5)
        ttk.Button(search_frame, text="Go", command=lambda: load_data(search_entry.get())).pack(side="left")
        ttk.Button(search_frame, text="Show All", command=lambda: load_data(), bootstyle="secondary").pack(side="left", padx=5)
        
        # Treeview
        tree_cols = ("Roll No", "Name", "Department", "Year", "Phone", "Attendance")
        cols = tree_cols
        tree = ttk.Treeview(self.main_frame, columns=tree_cols, show="headings")
        for col in cols:
            tree.heading(col, text=col)
            tree.column(col, width=100)
        tree.pack(fill=tk.BOTH, expand=True)

        def load_data(search_term=""):
            tree.delete(*tree.get_children())
            # Only show the first few columns in the main view for clarity
            rows_query = "SELECT roll_no, name, department, year, phone, attendance FROM students"
            if search_term:
                rows = db_execute(f"{rows_query} WHERE name LIKE ? OR roll_no LIKE ? OR department LIKE ?", (f"%{search_term}%", f"%{search_term}%", f"%{search_term}%"), fetch=True)
            else:
                rows = db_execute(rows_query, fetch=True)
            if rows: [tree.insert("", tk.END, values=row) for row in rows]

        def add_student():
            def save():
                try:
                    roll = basic_entries["Roll No"].get().strip()
                    name = basic_entries["Name"].get().strip()
                    dept = basic_entries["Department"].get().strip()
                    year = int(basic_entries["Year"].get() or 0)
                    if not (1 <= year <= 4):
                        raise ValueError("Year must be between 1 and 4.")
                    phone = basic_entries["Phone"].get().strip()
                    att = basic_entries["Attendance"].get().strip()

                    if not (roll and name and dept):
                        raise ValueError("Roll No, Name, and Department cannot be empty")

                    marks_values = []
                    for sem in range(1, 7):
                        for mid in range(1, 3):
                            mark = sem_entries[sem][mid].get().strip()
                            mark_val = int(mark) if mark else 0
                            if not (0 <= mark_val <= 99):
                                raise ValueError(f"Mid-term marks must be between 0 and 99.")
                            marks_values.append(mark_val)

                    db_execute("INSERT INTO students VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)", 
                               (roll, name, dept, year, *marks_values, phone, att))
                    top.destroy()
                    load_data()
                except Exception as err:
                    messagebox.showerror("Error", str(err))

            top = tb.Toplevel(self.root)
            top.title("Add New Student")
            top.geometry("600x700")

            nb = ttk.Notebook(top)
            nb.pack(fill="both", expand=True, padx=10, pady=10)

            # Basic Info Tab
            basic_frame = ttk.Frame(nb)
            nb.add(basic_frame, text="Basic Info")
            basic_labels = ["Roll No", "Name", "Department", "Year", "Phone", "Attendance"]
            basic_entries = {}
            
            vcmd_2digit = (self.root.register(self._validate_digit), '%P', 2)
            vcmd_year = (self.root.register(self._validate_digit), '%P', 1)

            for i, lbl in enumerate(basic_labels):
                ttk.Label(basic_frame, text=lbl).grid(row=i, column=0, padx=10, pady=10, sticky="w")
                ent = ttk.Entry(basic_frame, width=40)
                ent.grid(row=i, column=1, padx=10, pady=10)
                if lbl == "Year":
                    ent.config(validate='key', validatecommand=vcmd_year)
                basic_entries[lbl] = ent

            # Semester Marks Tabs
            sem_entries = {}
            for sem in range(1, 7):
                sem_frame = ttk.Frame(nb)
                nb.add(sem_frame, text=f"Sem {sem}")
                sem_entries[sem] = {}
                for mid in range(1, 3):
                    ttk.Label(sem_frame, text=f"Mid {mid} Marks").grid(row=mid-1, column=0, padx=10, pady=10, sticky="w")
                    ent = ttk.Entry(sem_frame, width=20)
                    ent.config(validate='key', validatecommand=vcmd_2digit)
                    ent.grid(row=mid-1, column=1, padx=10, pady=10)
                    sem_entries[sem][mid] = ent

            ttk.Button(top, text="Save", bootstyle="success", command=save).pack(pady=10)

        def edit_student():
            selected = tree.selection()
            if not selected:
                messagebox.showwarning("Select a record", "Please select a student to edit.")
                return
            
            student_data = tree.item(selected[0])['values']

            def save_changes():
                try:
                    # The roll number (PK) is not editable.
                    roll = student_data[0]
                    name = basic_entries["Name"].get().strip()
                    dept = basic_entries["Department"].get().strip()
                    year = int(basic_entries["Year"].get() or 0)
                    if not (1 <= year <= 4):
                        raise ValueError("Year must be between 1 and 4.")
                    phone = basic_entries["Phone"].get().strip()
                    att = basic_entries["Attendance"].get().strip()
                    if not (name and dept):
                        raise ValueError("Name and Department cannot be empty")
                    marks_values = []
                    for sem in range(1, 7):
                        mid1_val = int(sem_entries[sem][1].get() or 0)
                        mid2_val = int(sem_entries[sem][2].get() or 0)
                        if not (0 <= mid1_val <= 99 and 0 <= mid2_val <= 99):
                            raise ValueError("Mid-term marks must be between 0 and 99.")
                        marks_values.extend([mid1_val, mid2_val])
                    db_execute("UPDATE students SET name=?, department=?, year=?, sem1_mid1=?, sem1_mid2=?, sem2_mid1=?, sem2_mid2=?, sem3_mid1=?, sem3_mid2=?, sem4_mid1=?, sem4_mid2=?, sem5_mid1=?, sem5_mid2=?, sem6_mid1=?, sem6_mid2=?, phone=?, attendance=? WHERE roll_no=?",
                               (name, dept, year, *marks_values, phone, att, roll))
                    top.destroy()
                    load_data()
                except Exception as err:
                    messagebox.showerror("Error", str(err))

            top = tb.Toplevel(self.root)
            top.title("Edit Student")
            top.geometry("600x700")

            nb = ttk.Notebook(top)
            nb.pack(fill="both", expand=True, padx=10, pady=10)

            # Basic Info
            basic_frame = ttk.Frame(nb)
            nb.add(basic_frame, text="Basic Info")
            basic_labels = ["Roll No", "Name", "Department", "Year", "Phone", "Attendance"]
            basic_entries = {}
            
            vcmd_2digit = (self.root.register(self._validate_digit), '%P', 2)
            vcmd_year = (self.root.register(self._validate_digit), '%P', 1)

            basic_data_map = { "Roll No": 0, "Name": 1, "Department": 2, "Year": 3, "Phone": 16, "Attendance": 17 }
            for i, lbl in enumerate(basic_labels):
                ttk.Label(basic_frame, text=lbl).grid(row=i, column=0, padx=10, pady=10, sticky="w")
                ent = ttk.Entry(basic_frame, width=40)
                ent.insert(0, student_data[basic_data_map[lbl]])
                if lbl == "Year":
                    ent.config(validate='key', validatecommand=vcmd_year)
                ent.grid(row=i, column=1, padx=10, pady=10)
                basic_entries[lbl] = ent
            basic_entries["Roll No"].config(state='readonly')

            # Semester Marks
            sem_entries = {}
            mark_idx = 4
            for sem in range(1, 7):
                sem_frame = ttk.Frame(nb)
                nb.add(sem_frame, text=f"Sem {sem}")
                sem_entries[sem] = {}
                for mid in range(1, 3):
                    ttk.Label(sem_frame, text=f"Mid {mid} Marks").grid(row=mid-1, column=0, padx=10, pady=10, sticky="w")
                    ent = ttk.Entry(sem_frame, width=20)
                    ent.config(validate='key', validatecommand=vcmd_2digit)
                    ent.insert(0, student_data[mark_idx])
                    ent.grid(row=mid-1, column=1, padx=10, pady=10)
                    sem_entries[sem][mid] = ent
                    mark_idx += 1

            ttk.Button(top, text="Save Changes", bootstyle="success", command=save_changes).pack(pady=10)

        def delete_student():
            selected = tree.selection()
            if not selected:
                messagebox.showwarning("Select a record", "Select a student first")
                return
            roll = tree.item(selected[0])['values'][0]
            if messagebox.askyesno("Confirm", "Delete this student?"):
                db_execute("DELETE FROM students WHERE roll_no=?", (roll,))
                load_data()

        def export_data():
            file = filedialog.asksaveasfilename(defaultextension=".xlsx")
            if file:
                rows = db_execute("SELECT * FROM students", fetch=True)
                pd.DataFrame(rows, columns=get_all_db_columns()).to_excel(file, index=False)
                messagebox.showinfo("Exported", "Data exported successfully")

        def show_graph():
            # Calculate average score across all semesters for each student
            query = """
                SELECT name, 
                    (sem1_mid1 + sem1_mid2 + sem2_mid1 + sem2_mid2 + sem3_mid1 + sem3_mid2 + 
                     sem4_mid1 + sem4_mid2 + sem5_mid1 + sem5_mid2 + sem6_mid1 + sem6_mid2) / 12.0 as avg_score
                FROM students
                ORDER BY avg_score DESC
                LIMIT 5
            """
            data = db_execute(query, fetch=True)
            if data:
                names, scores = zip(*data)
                plt.figure(figsize=(8, 5))
                plt.bar(names, scores, color=tb.Style().colors.primary)
                plt.title("Top 5 Scorers")
                plt.ylabel("Average Score")
                plt.xticks(rotation=15)
                plt.tight_layout()
                plt.show()
            else:
                messagebox.showinfo("No Data", "No student data available to generate a graph.")
        def get_all_db_columns():
            base = ["Roll No", "Name", "Department", "Year"]
            marks = []
            for sem in range(1, 7):
                marks.extend([f"Sem{sem} Mid1", f"Sem{sem} Mid2"])
            extra = ["Phone", "Attendance"]
            return base + marks + extra


        # Buttons
        btn_frame = ttk.Frame(self.main_frame)
        btn_frame.pack(pady=5)
        if role == "admin":
            ttk.Button(btn_frame, text="Add", width=12, command=add_student, bootstyle="success").grid(row=0, column=0, padx=5)
            ttk.Button(btn_frame, text="Edit", width=12, command=edit_student, bootstyle="info").grid(row=0, column=1, padx=5)
            ttk.Button(btn_frame, text="Delete", width=12, command=delete_student, bootstyle="danger").grid(row=0, column=2, padx=5)
        ttk.Button(btn_frame, text="Export", width=12, command=export_data, bootstyle="secondary").grid(row=0, column=3, padx=5)
        ttk.Button(btn_frame, text="Top Graph", width=12, command=show_graph, bootstyle="secondary").grid(row=0, column=4, padx=5)

        load_data()

    def logout_screen(self):
        """Logs out and returns to the login screen."""
        if messagebox.askyesno("Logout", "Are you sure you want to log out?"):
            self.root.unbind("<Return>")
            self.login_screen()

# Run the app
if __name__ == "__main__":
    root = tb.Window(themename="superhero")
    app = StudentDBApp(root)
    root.mainloop()
