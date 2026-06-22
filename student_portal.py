"""
╔═══════════════════════════════════════════════════════════════════════════════════╗
║                                                                                   ║
║                    STUDENT ACADEMIC PORTAL - SIERRA LEONE                          ║
║                                    GROUP B                                         ║
║                                                                                   ║
║         COMPLETE REGISTRATION & APPROVAL SYSTEM                                    ║
║                    SDG 4: QUALITY EDUCATION FOR ALL                               ║
║                                                                                   ║
║  FEATURES INCLUDED:                                                               ║
║  ✅ Fullscreen/Maximized Windows                                                  ║
║  ✅ CSV IMPORT - Bulk upload students from CSV file                               ║
║  ✅ BACK BUTTON on Teacher/Principal Dashboard                                    ║
║  ✅ Unified Admin Panel Colors (Elegant Purple Theme)                             ║
║  ✅ Student Signup with Full Details                                              ║
║  ✅ Teacher Signup with School, Subject, PIN Code                                 ║
║  ✅ Principal Signup with Full Details                                            ║
║  ✅ Admin Approval Panel - Approve/Reject Users                                   ║
║  ✅ Student Login with Student ID + Password                                      ║
║  ✅ Teacher Dashboard - Add/Edit/Delete Students                                  ║
║  ✅ Principal Dashboard - View All Students                                       ║
║  ✅ Custom Subjects & Grades                                                      ║
║  ✅ Automatic Student ID Generation                                                ║
║  ✅ Statistics Dashboard & SDG 4 Tracking                                         ║
║  ✅ Save/Load JSON & Export CSV                                                   ║
║  ✅ Admin User Management (Add/Edit/Delete Users)                                 ║
║  ✅ EDIT USERS in all sections                                                    ║
║  ✅ PRINT RESULTS in all sections                                                 ║
║  ✅ System Backup & Restore                                                       ║
║  ✅ Audit Logs for All Actions                                                    ║
║                                                                                   ║
╚═══════════════════════════════════════════════════════════════════════════════════╝
"""

import tkinter as tk
from tkinter import ttk, messagebox, filedialog
import json
import os
import hashlib
from datetime import datetime
import shutil
import csv

# ============================================================================
# CONSTANTS
# ============================================================================

APP_NAME = "Student Academic Portal - Sierra Leone"
SDG_TAG = "🌍 SDG 4: Quality Education for All 🇸🇱"
VERSION = "8.0 - CSV Import Added"

PASS_MARK = 50
DISTINCTION_MARK = 70

# Admin Panel Unified Colors (Elegant Purple Theme)
ADMIN_BG = "#6a1b9a"  # Deep Purple
ADMIN_BTN_BG = "#8e24aa"  # Medium Purple
ADMIN_BTN_HOVER = "#ab47bc"  # Light Purple
ADMIN_HEADER_BG = "#4a0072"  # Dark Purple

# Teacher Panel Colors
TEACHER_HEADER_BG = "#e63946"
TEACHER_BTN_BG = "#4CAF50"

# Principal Panel Colors
PRINCIPAL_HEADER_BG = "#FF9800"

# Education Levels
EDUCATION_LEVELS = [
    "Early Childhood (Nursery)",
    "Primary School",
    "Junior Secondary School (JSS)",
    "Senior Secondary School (SSS)",
    "Technical/Vocational",
    "Adult Education",
    "University/College"
]

# Sierra Leone Districts
SIERRA_LEONE_DISTRICTS = [
    "Western Area Urban (Freetown)", "Western Area Rural", "Kailahun", "Kenema",
    "Kono", "Bombali", "Falaba", "Koinadugu", "Tonkolili", "Kambia",
    "Karene", "Port Loko", "Bo", "Bonthe", "Moyamba", "Pujehun"
]

# District
DISTRICT_CODES = {
    "Kailahun": "KL", "Kenema": "KE", "Kono": "KO", "Bombali": "BD",
    "Bo": "BO", "Port Loko": "PL", "Western Area Urban (Freetown)": "WAU",
    "Western Area Rural": "WAR", "Pujehun": "PJ", "Moyamba": "MY",
    "Bonthe": "BT", "Tonkolili": "TO", "Kambia": "KB", "Karene": "KR",
    "Falaba": "FA", "Koinadugu": "KD"
}


# ============================================================================
# HELPER FUNCTIONS
# ============================================================================

def hash_password(password):
    return hashlib.sha256(password.encode()).hexdigest()


def generate_user_id(role, district, count):
    code = DISTRICT_CODES.get(district, "XX")
    role_codes = {"Student": "STD", "Teacher": "TCH", "Principal": "PRN", "Admin": "ADM"}
    role_code = role_codes.get(role, "USR")
    return f"{role_code}-{code}-{count + 1:04d}"


def calculate_average(grades):
    if not grades:
        return 0
    return round(sum(grades.values()) / len(grades), 2)


def determine_status(avg):
    if avg >= DISTINCTION_MARK:
        return "🏆 Distinction"
    elif avg >= PASS_MARK:
        return "✅ Pass"
    else:
        return "📚 Needs Improvement"


def log_action(action, user, details):
    os.makedirs("data", exist_ok=True)
    log_file = "data/audit.log"
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    log_entry = f"[{timestamp}] USER: {user} | ACTION: {action} | DETAILS: {details}\n"
    try:
        with open(log_file, 'a', encoding='utf-8') as f:
            f.write(log_entry)
    except:
        pass


def maximize_window(window):
    """Maximize the window"""
    window.state('zoomed')


def print_report(content, title="Academic Report"):
    print_window = tk.Toplevel()
    print_window.title(f"Print - {title}")
    print_window.geometry("800x700")
    print_window.configure(bg='#f0f4f8')

    header = tk.Frame(print_window, bg='#e63946', height=60)
    header.pack(fill='x')
    tk.Label(header, text=SDG_TAG, bg='#e63946', fg='white',
             font=('Arial', 12, 'bold')).pack(pady=15)

    text_frame = tk.Frame(print_window, bg='white')
    text_frame.pack(fill='both', expand=True, padx=20, pady=20)

    text_widget = tk.Text(text_frame, font=('Courier', 10), wrap=tk.WORD)
    text_widget.pack(fill='both', expand=True)

    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    full_content = f"""
{'=' * 70}
STUDENT ACADEMIC PORTAL - SIERRA LEONE
{SDG_TAG}
Printed: {timestamp}
{'=' * 70}

{content}
{'=' * 70}
This report supports SDG 4: Quality Education in Sierra Leone
    """

    text_widget.insert(1.0, full_content)
    text_widget.config(state='disabled')

    btn_frame = tk.Frame(print_window, bg='#f0f4f8')
    btn_frame.pack(fill='x', pady=10)

    def do_print():
        try:
            text_widget.config(state='normal')
            text_widget.tag_add("sel", "1.0", "end")
            text_widget.event_generate("<<Copy>>")
            text_widget.tag_remove("sel", "1.0", "end")
            text_widget.config(state='disabled')
            messagebox.showinfo("Print", "Report copied to clipboard.")
        except:
            messagebox.showinfo("Print", "You can save this report as a text file.")

    def save_to_file():
        filename = filedialog.asksaveasfilename(
            defaultextension=".txt",
            filetypes=[("Text files", "*.txt")],
            initialfile=f"report_{datetime.now().strftime('%Y%m%d_%H%M%S')}.txt"
        )
        if filename:
            try:
                with open(filename, 'w', encoding='utf-8') as f:
                    f.write(full_content)
                messagebox.showinfo("Success", f"Report saved to {filename}")
            except Exception as e:
                messagebox.showerror("Error", str(e))

    tk.Button(btn_frame, text="🖨️ Copy to Clipboard", command=do_print,
              bg='#2196F3', fg='white', font=('Arial', 10, 'bold'), padx=15).pack(side='left', padx=10)
    tk.Button(btn_frame, text="💾 Save to File", command=save_to_file,
              bg='#4CAF50', fg='white', font=('Arial', 10, 'bold'), padx=15).pack(side='left', padx=10)
    tk.Button(btn_frame, text="Close", command=print_window.destroy,
              bg='#9E9E9E', fg='white', font=('Arial', 10, 'bold'), padx=15).pack(side='left', padx=10)


# ============================================================================
# DATA MANAGEMENT
# ============================================================================

USERS_FILE = "data/users.json"
PENDING_FILE = "data/pending.json"


def load_users():
    os.makedirs("data", exist_ok=True)

    if os.path.exists(USERS_FILE):
        try:
            with open(USERS_FILE, 'r') as f:
                return json.load(f)
        except:
            pass

    default_users = {
        "admin": {
            "password": hash_password("admin123"),
            "full_name": "System Administrator",
            "role": "Admin",
            "status": "approved",
            "date_registered": datetime.now().strftime("%Y-%m-%d"),
            "students": []
        },
        "teacher1": {
            "password": hash_password("teacher123"),
            "full_name": "Fatmata Kamara",
            "role": "Teacher",
            "status": "approved",
            "district": "Kailahun",
            "school": "St. Mary's Primary School",
            "class_name": "Class 6A",
            "subjects_taught": "English, Mathematics, Science",
            "date_registered": datetime.now().strftime("%Y-%m-%d"),
            "students": []
        },
        "principal1": {
            "password": hash_password("principal123"),
            "full_name": "Mohamed Sesay",
            "role": "Principal",
            "status": "approved",
            "district": "Kailahun",
            "school": "St. Mary's Primary School",
            "date_registered": datetime.now().strftime("%Y-%m-%d"),
            "students": []
        }
    }

    with open(USERS_FILE, 'w') as f:
        json.dump(default_users, f, indent=4)
    return default_users


def save_users(users):
    try:
        with open(USERS_FILE, 'w') as f:
            json.dump(users, f, indent=4)
        return True
    except:
        return False


def load_pending():
    os.makedirs("data", exist_ok=True)

    if os.path.exists(PENDING_FILE):
        try:
            with open(PENDING_FILE, 'r') as f:
                return json.load(f)
        except:
            return {}
    return {}


def save_pending(pending):
    try:
        with open(PENDING_FILE, 'w') as f:
            json.dump(pending, f, indent=4)
        return True
    except:
        return False


def add_pending_user(user_data):
    pending = load_pending()
    pending[user_data["username"]] = user_data
    return save_pending(pending)


def create_backup():
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    backup_dir = f"data/backup_{timestamp}"
    os.makedirs(backup_dir, exist_ok=True)

    files_to_backup = [USERS_FILE, PENDING_FILE]
    for file in files_to_backup:
        if os.path.exists(file):
            shutil.copy(file, backup_dir)

    return backup_dir


# ============================================================================
# STUDENT GRADE VIEWER
# ============================================================================

class StudentGradeViewer:
    def __init__(self, student):
        self.student = student
        self.root = tk.Toplevel()
        self.root.title(f"Student Portal - {student['name']}")
        self.root.geometry("900x750")
        self.root.configure(bg='#f0f4f8')
        maximize_window(self.root)

        self.setup_ui()

    def setup_ui(self):
        header = tk.Frame(self.root, bg='#4CAF50', height=100)
        header.pack(fill='x')

        tk.Label(header, text="📚 YOUR ACADEMIC REPORT", bg='#4CAF50', fg='white',
                 font=('Arial', 20, 'bold')).pack(pady=(25, 5))
        tk.Label(header, text=SDG_TAG, bg='#4CAF50', fg='#FFD700',
                 font=('Arial', 12)).pack()

        info_frame = tk.Frame(self.root, bg='white', relief=tk.RAISED, bd=2)
        info_frame.pack(fill='x', padx=30, pady=20)

        tk.Label(info_frame, text=f"👨‍🎓 Student: {self.student['name']}",
                 font=('Arial', 16, 'bold'), bg='white', fg='#2c3e50').pack(anchor='w', padx=25, pady=10)
        tk.Label(info_frame, text=f"🆔 Student ID: {self.student['student_id']}",
                 font=('Arial', 12), bg='white').pack(anchor='w', padx=25)
        tk.Label(info_frame, text=f"📍 District: {self.student.get('district', 'N/A')}",
                 font=('Arial', 12), bg='white').pack(anchor='w', padx=25, pady=(0, 10))

        grades_frame = tk.LabelFrame(self.root, text="📊 SUBJECT GRADES",
                                     bg='white', font=('Arial', 14, 'bold'), fg='#2c3e50')
        grades_frame.pack(fill='both', expand=True, padx=30, pady=10)

        columns = ("Subject", "Grade", "Performance", "Teacher Comment")
        tree = ttk.Treeview(grades_frame, columns=columns, show="headings", height=10)

        tree.heading("Subject", text="Subject")
        tree.heading("Grade", text="Grade")
        tree.heading("Performance", text="Performance")
        tree.heading("Teacher Comment", text="Teacher Comment")

        tree.column("Subject", width=200)
        tree.column("Grade", width=100)
        tree.column("Performance", width=180)
        tree.column("Teacher Comment", width=300)

        for subject, grade in self.student.get('subjects', {}).items():
            if grade >= 80:
                perf = "Excellent 🌟"
                comment = "Outstanding work!"
            elif grade >= 70:
                perf = "Very Good 👍"
                comment = "Well done!"
            elif grade >= 60:
                perf = "Good 📚"
                comment = "Good effort!"
            elif grade >= 50:
                perf = "Satisfactory ✅"
                comment = "Satisfactory, keep improving"
            else:
                perf = "Needs Improvement ⚠️"
                comment = "Please focus more on this subject"

            tree.insert("", "end", values=(subject, f"{grade}%", perf, comment))

        tree.pack(fill='both', expand=True, padx=15, pady=15)

        summary_frame = tk.Frame(self.root, bg='#e8f5e9', relief=tk.GROOVE, bd=2)
        summary_frame.pack(fill='x', padx=30, pady=10)

        avg = self.student.get('average', 0)
        status = self.student.get('status', 'N/A')

        tk.Label(summary_frame, text=f"📈 Overall Average: {avg:.1f}%",
                 bg='#e8f5e9', font=('Arial', 14, 'bold'), fg='#2c3e50').pack(anchor='w', padx=25, pady=10)
        tk.Label(summary_frame, text=f"🏆 Overall Status: {status}",
                 bg='#e8f5e9', font=('Arial', 14, 'bold')).pack(anchor='w', padx=25, pady=(0, 10))

        if avg >= 70:
            comment = "🌟 Excellent work! Keep up the great performance!"
            comment_color = '#2e7d32'
        elif avg >= 50:
            comment = "✅ Good effort! Keep working hard to improve."
            comment_color = '#f57c00'
        else:
            comment = "📚 Keep trying! Focus on areas that need improvement."
            comment_color = '#c62828'

        tk.Label(summary_frame, text=f"💬 Teacher's Comment: {comment}",
                 bg='#e8f5e9', font=('Arial', 12, 'italic'), fg=comment_color).pack(anchor='w', padx=25, pady=(0, 15))

        footer = tk.Frame(self.root, bg='#f0f4f8')
        footer.pack(fill='x', pady=20)

        tk.Button(footer, text="🖨️ Print Report Card", command=self.print_report,
                  bg='#2196F3', fg='white', font=('Arial', 12, 'bold'), padx=25, pady=10).pack(side='left', padx=30)
        tk.Button(footer, text="🔙 BACK TO LOGIN", command=self.go_back,
                  bg='#9E9E9E', fg='white', font=('Arial', 12, 'bold'), padx=25, pady=10).pack(side='right', padx=30)

        sdg_footer = tk.Label(self.root, text=SDG_TAG, bg='#e63946', fg='white',
                              font=('Arial', 10), pady=10)
        sdg_footer.pack(side='bottom', fill='x')

    def print_report(self):
        report_content = f"""
STUDENT ACADEMIC REPORT
{'=' * 60}

Student Name: {self.student['name']}
Student ID: {self.student['student_id']}
District: {self.student.get('district', 'N/A')}
Date: {datetime.now().strftime('%B %d, %Y')}

{'=' * 60}
SUBJECT GRADES
{'=' * 60}

"""
        for subject, grade in self.student.get('subjects', {}).items():
            report_content += f"{subject:25} {grade:>3}%\n"

        report_content += f"""
{'=' * 60}
SUMMARY
{'=' * 60}
Overall Average: {self.student.get('average', 0):.1f}%
Overall Status: {self.student.get('status', 'N/A')}

{'=' * 60}
This report supports SDG 4: Quality Education in Sierra Leone
        """
        print_report(report_content, f"Report_{self.student['name']}")

    def go_back(self):
        if messagebox.askyesno("Back", "Go back to login screen?"):
            self.root.destroy()
            login = LoginWindow()
            login.root.mainloop()


# ============================================================================
# STUDENT LOGIN WINDOW
# ============================================================================

class StudentLoginWindow:
    def __init__(self, parent_app=None):
        self.parent_app = parent_app
        self.root = tk.Toplevel()
        self.root.title("Student Portal - View Your Grades")
        self.root.geometry("550x600")
        self.root.configure(bg='#f0f4f8')
        self.root.resizable(False, False)

        self.setup_ui()
        self.center_window()

    def center_window(self):
        self.root.update_idletasks()
        x = (self.root.winfo_screenwidth() // 2) - 275
        y = (self.root.winfo_screenheight() // 2) - 300
        self.root.geometry(f'550x600+{x}+{y}')

    def setup_ui(self):
        header = tk.Frame(self.root, bg='#4CAF50', height=100)
        header.pack(fill='x')

        tk.Label(header, text="👨‍🎓 STUDENT PORTAL", bg='#4CAF50', fg='white',
                 font=('Arial', 20, 'bold')).pack(pady=(25, 5))
        tk.Label(header, text="View Your Academic Performance", bg='#4CAF50', fg='white',
                 font=('Arial', 12)).pack()

        main = tk.Frame(self.root, bg='#f0f4f8')
        main.pack(fill='both', expand=True, padx=50, pady=40)

        tk.Label(main, text="Enter your credentials to view your grades:",
                 bg='#f0f4f8', font=('Arial', 12)).pack(anchor='w', pady=(0, 25))

        id_frame = tk.Frame(main, bg='white', relief=tk.GROOVE, bd=2)
        id_frame.pack(fill='x', pady=10)
        tk.Label(id_frame, text="Student ID", bg='#e0e0e0', font=('Arial', 11, 'bold')).pack(anchor='w', padx=15,
                                                                                             pady=8)
        self.id_entry = tk.Entry(id_frame, font=('Arial', 13), width=35)
        self.id_entry.pack(fill='x', padx=15, pady=(0, 12))

        pwd_frame = tk.Frame(main, bg='white', relief=tk.GROOVE, bd=2)
        pwd_frame.pack(fill='x', pady=10)
        tk.Label(pwd_frame, text="Password", bg='#e0e0e0', font=('Arial', 11, 'bold')).pack(anchor='w', padx=15,
                                                                                             pady=8)
        self.pwd_entry = tk.Entry(pwd_frame, font=('Arial', 13), width=35, show="•")
        self.pwd_entry.pack(fill='x', padx=15, pady=(0, 12))

        self.show_var = tk.BooleanVar()
        tk.Checkbutton(main, text="Show Password", variable=self.show_var,
                       command=self.toggle_password, bg='#f0f4f8', font=('Arial', 11)).pack(anchor='w', pady=10)

        tk.Button(main, text="🔓 VIEW MY GRADES", command=self.student_login,
                  bg='#4CAF50', fg='white', font=('Arial', 13, 'bold'),
                  height=1, width=28, pady=10).pack(pady=25)

        tk.Button(main, text="🔙 BACK TO MAIN LOGIN", command=self.go_back,
                  bg='#9E9E9E', fg='white', font=('Arial', 12, 'bold'), height=1, width=28, pady=8).pack(pady=10)

        info = tk.Label(main,
                        text="💡 Ask your teacher for your Student ID and Password.\nDefault password is 'pass123' unless changed.",
                        bg='#e8f0fe', font=('Arial', 10), relief=tk.GROOVE, padx=15, pady=10)
        info.pack(fill='x', pady=15)

        self.root.bind('<Return>', lambda e: self.student_login())

    def go_back(self):
        self.root.destroy()

    def toggle_password(self):
        if self.show_var.get():
            self.pwd_entry.config(show="")
        else:
            self.pwd_entry.config(show="•")

    def student_login(self):
        student_id = self.id_entry.get().strip()
        password = self.pwd_entry.get().strip()

        if not student_id or not password:
            messagebox.showerror("Error", "Please enter Student ID and Password")
            return

        users = load_users()
        student = None

        for username, user_data in users.items():
            if user_data.get("role") in ["Teacher", "Principal", "Admin"]:
                for stud in user_data.get("students", []):
                    if stud.get("student_id") == student_id:
                        if stud.get("password") == hash_password(password):
                            student = stud
                            break
            if student:
                break

        if student:
            log_action("STUDENT_LOGIN", student_id, "Successful login")
            self.root.destroy()
            StudentGradeViewer(student)
        else:
            messagebox.showerror("Login Failed", "Invalid Student ID or Password.\n\nPlease check with your teacher.")


# ============================================================================
# REGISTRATION WINDOWS
# ============================================================================

class StudentSignupWindow:
    def __init__(self, parent=None):
        self.parent = parent
        self.root = tk.Toplevel()
        self.root.title("Student Signup - Create Account")
        self.root.geometry("700x800")
        self.root.configure(bg='#f0f4f8')
        self.root.resizable(False, False)
        maximize_window(self.root)

        self.setup_ui()

    def setup_ui(self):
        header = tk.Frame(self.root, bg='#4CAF50', height=80)
        header.pack(fill='x')
        tk.Label(header, text="👨‍🎓 STUDENT SIGNUP", bg='#4CAF50', fg='white',
                 font=('Arial', 20, 'bold')).pack(pady=(20, 5))
        tk.Label(header, text="Create your student account", bg='#4CAF50', fg='white',
                 font=('Arial', 12)).pack()

        canvas = tk.Canvas(self.root, bg='#f0f4f8')
        scrollbar = tk.Scrollbar(self.root, orient="vertical", command=canvas.yview)
        scrollable_frame = tk.Frame(canvas, bg='#f0f4f8')

        scrollable_frame.bind("<Configure>", lambda e: canvas.configure(scrollregion=canvas.bbox("all")))
        canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
        canvas.configure(yscrollcommand=scrollbar.set)

        canvas.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")

        main = scrollable_frame

        row = 0
        # Personal Information
        tk.Label(main, text="📝 PERSONAL INFORMATION", bg='#f0f4f8',
                 font=('Arial', 14, 'bold'), fg='#2c3e50').grid(row=row, column=0, columnspan=2, sticky='w',
                                                                pady=(15, 10))
        row += 1

        self.name_entry = self.create_entry(main, "Full Name:", row)
        row += 1
        self.dob_entry = self.create_entry(main, "Date of Birth (YYYY-MM-DD):", row)
        self.dob_entry.insert(0, "2005-01-01")
        row += 1

        tk.Label(main, text="Gender:", bg='#f0f4f8', font=('Arial', 11)).grid(row=row, column=0, sticky='w', pady=8)
        self.gender_var = tk.StringVar(value="Female")
        gender_frame = tk.Frame(main, bg='#f0f4f8')
        gender_frame.grid(row=row, column=1, sticky='w', padx=10)
        tk.Radiobutton(gender_frame, text="Male", variable=self.gender_var, value="Male", bg='#f0f4f8',
                       font=('Arial', 11)).pack(side='left')
        tk.Radiobutton(gender_frame, text="Female", variable=self.gender_var, value="Female", bg='#f0f4f8',
                       font=('Arial', 11)).pack(side='left', padx=15)
        row += 1

        tk.Label(main, text="District:", bg='#f0f4f8', font=('Arial', 11)).grid(row=row, column=0, sticky='w', pady=8)
        self.district_var = tk.StringVar(value="Kailahun")
        ttk.Combobox(main, textvariable=self.district_var, values=SIERRA_LEONE_DISTRICTS, width=28,
                     font=('Arial', 11)).grid(row=row, column=1, pady=8, padx=10)
        row += 1

        tk.Label(main, text="🎓 EDUCATION INFORMATION", bg='#f0f4f8',
                 font=('Arial', 14, 'bold'), fg='#2c3e50').grid(row=row, column=0, columnspan=2, sticky='w',
                                                                pady=(20, 10))
        row += 1

        tk.Label(main, text="Education Level:", bg='#f0f4f8', font=('Arial', 11)).grid(row=row, column=0, sticky='w',
                                                                                       pady=8)
        self.level_var = tk.StringVar(value="Senior Secondary School (SSS)")
        ttk.Combobox(main, textvariable=self.level_var, values=EDUCATION_LEVELS, width=28, font=('Arial', 11)).grid(
            row=row, column=1, pady=8, padx=10)
        row += 1

        self.school_entry = self.create_entry(main, "School Name:", row)
        row += 1

        tk.Label(main, text="👨‍👩‍👧 PARENT/GUARDIAN INFORMATION", bg='#f0f4f8',
                 font=('Arial', 14, 'bold'), fg='#2c3e50').grid(row=row, column=0, columnspan=2, sticky='w',
                                                                pady=(20, 10))
        row += 1

        self.parent_name_entry = self.create_entry(main, "Parent Name:", row)
        row += 1
        self.parent_phone_entry = self.create_entry(main, "Parent Phone:", row)
        row += 1

        tk.Label(main, text="🔐 ACCOUNT SECURITY", bg='#f0f4f8',
                 font=('Arial', 14, 'bold'), fg='#2c3e50').grid(row=row, column=0, columnspan=2, sticky='w',
                                                                pady=(20, 10))
        row += 1

        self.username_entry = self.create_entry(main, "Create Username:", row)
        row += 1
        self.password_entry = self.create_entry(main, "Create Password:", row, show="•")
        row += 1
        self.confirm_entry = self.create_entry(main, "Confirm Password:", row, show="•")
        row += 1

        btn_frame = tk.Frame(main, bg='#f0f4f8')
        btn_frame.grid(row=row, column=0, columnspan=2, pady=30)

        tk.Button(btn_frame, text="📝 SIGNUP", command=self.signup,
                  bg='#4CAF50', fg='white', font=('Arial', 12, 'bold'), padx=30, pady=10).pack(side='left', padx=15)
        tk.Button(btn_frame, text="🔙 BACK", command=self.root.destroy,
                  bg='#9E9E9E', fg='white', font=('Arial', 12, 'bold'), padx=30, pady=10).pack(side='left', padx=15)

    def create_entry(self, parent, label, row, show=None):
        tk.Label(parent, text=label, bg='#f0f4f8', font=('Arial', 11)).grid(row=row, column=0, sticky='w', pady=8)
        entry = tk.Entry(parent, width=30, font=('Arial', 11), show=show if show else "")
        entry.grid(row=row, column=1, pady=8, padx=10)
        return entry

    def signup(self):
        username = self.username_entry.get().strip()
        password = self.password_entry.get().strip()
        confirm = self.confirm_entry.get().strip()
        name = self.name_entry.get().strip()

        if not username or not password or not name:
            messagebox.showerror("Error", "Please fill all required fields")
            return

        if password != confirm:
            messagebox.showerror("Error", "Passwords do not match")
            return

        if len(password) < 4:
            messagebox.showerror("Error", "Password must be at least 4 characters")
            return

        user_data = {
            "username": username,
            "password": hash_password(password),
            "full_name": name,
            "date_of_birth": self.dob_entry.get().strip(),
            "gender": self.gender_var.get(),
            "district": self.district_var.get(),
            "education_level": self.level_var.get(),
            "school": self.school_entry.get().strip(),
            "parent_name": self.parent_name_entry.get().strip(),
            "parent_phone": self.parent_phone_entry.get().strip(),
            "role": "Student",
            "status": "pending",
            "date_registered": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "students": []
        }

        users = load_users()
        pending = load_pending()

        if username in users or username in pending:
            messagebox.showerror("Error", "Username already exists!")
            return

        add_pending_user(user_data)
        log_action("STUDENT_SIGNUP", username, "Account registered, pending approval")
        messagebox.showinfo("Success",
                            f"Student account submitted for approval!\n\nUsername: {username}\n\nPlease wait for Admin approval.")
        self.root.destroy()


# ============================================================================
# TEACHER SIGNUP
# ============================================================================

class TeacherSignupWindow:
    def __init__(self, parent=None):
        self.parent = parent
        self.root = tk.Toplevel()
        self.root.title("Teacher Signup - Create Account")
        self.root.geometry("700x850")
        self.root.configure(bg='#f0f4f8')
        self.root.resizable(False, False)
        maximize_window(self.root)

        self.setup_ui()

    def setup_ui(self):
        header = tk.Frame(self.root, bg='#2196F3', height=80)
        header.pack(fill='x')
        tk.Label(header, text="👩‍🏫 TEACHER SIGNUP", bg='#2196F3', fg='white',
                 font=('Arial', 20, 'bold')).pack(pady=(20, 5))
        tk.Label(header, text="Create your teacher account", bg='#2196F3', fg='white',
                 font=('Arial', 12)).pack()

        canvas = tk.Canvas(self.root, bg='#f0f4f8')
        scrollbar = tk.Scrollbar(self.root, orient="vertical", command=canvas.yview)
        scrollable_frame = tk.Frame(canvas, bg='#f0f4f8')

        scrollable_frame.bind("<Configure>", lambda e: canvas.configure(scrollregion=canvas.bbox("all")))
        canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
        canvas.configure(yscrollcommand=scrollbar.set)

        canvas.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")

        main = scrollable_frame

        row = 0
        tk.Label(main, text="📝 PERSONAL INFORMATION", bg='#f0f4f8',
                 font=('Arial', 14, 'bold'), fg='#2c3e50').grid(row=row, column=0, columnspan=2, sticky='w',
                                                                pady=(15, 10))
        row += 1

        self.name_entry = self.create_entry(main, "Full Name:", row)
        row += 1
        self.email_entry = self.create_entry(main, "Email:", row)
        row += 1
        self.phone_entry = self.create_entry(main, "Phone:", row)
        row += 1

        tk.Label(main, text="Gender:", bg='#f0f4f8', font=('Arial', 11)).grid(row=row, column=0, sticky='w', pady=8)
        self.gender_var = tk.StringVar(value="Female")
        gender_frame = tk.Frame(main, bg='#f0f4f8')
        gender_frame.grid(row=row, column=1, sticky='w', padx=10)
        tk.Radiobutton(gender_frame, text="Male", variable=self.gender_var, value="Male", bg='#f0f4f8',
                       font=('Arial', 11)).pack(side='left')
        tk.Radiobutton(gender_frame, text="Female", variable=self.gender_var, value="Female", bg='#f0f4f8',
                       font=('Arial', 11)).pack(side='left', padx=15)
        row += 1

        tk.Label(main, text="District:", bg='#f0f4f8', font=('Arial', 11)).grid(row=row, column=0, sticky='w', pady=8)
        self.district_var = tk.StringVar(value="Kailahun")
        ttk.Combobox(main, textvariable=self.district_var, values=SIERRA_LEONE_DISTRICTS, width=28,
                     font=('Arial', 11)).grid(row=row, column=1, pady=8, padx=10)
        row += 1

        tk.Label(main, text="🏫 SCHOOL INFORMATION", bg='#f0f4f8',
                 font=('Arial', 14, 'bold'), fg='#2c3e50').grid(row=row, column=0, columnspan=2, sticky='w',
                                                                pady=(20, 10))
        row += 1

        self.school_entry = self.create_entry(main, "School Name:", row)
        row += 1

        tk.Label(main, text="Education Level You Teach:", bg='#f0f4f8', font=('Arial', 11)).grid(row=row, column=0,
                                                                                                 sticky='w', pady=8)
        self.level_var = tk.StringVar(value="Senior Secondary School (SSS)")
        ttk.Combobox(main, textvariable=self.level_var, values=EDUCATION_LEVELS, width=28, font=('Arial', 11)).grid(
            row=row, column=1, pady=8, padx=10)
        row += 1

        self.subjects_entry = self.create_entry(main, "Subjects You Teach:", row)
        self.subjects_entry.insert(0, "English, Mathematics, Science")
        row += 1
        self.class_entry = self.create_entry(main, "Class/Form:", row)
        row += 1

        tk.Label(main, text="🔐 PIN CODE (4-digit staff PIN)", bg='#f0f4f8',
                 font=('Arial', 14, 'bold'), fg='#2c3e50').grid(row=row, column=0, columnspan=2, sticky='w',
                                                                pady=(20, 10))
        row += 1

        self.pin_entry = self.create_entry(main, "Staff PIN Code:", row, show="•")
        row += 1

        tk.Label(main, text="🔐 ACCOUNT SECURITY", bg='#f0f4f8',
                 font=('Arial', 14, 'bold'), fg='#2c3e50').grid(row=row, column=0, columnspan=2, sticky='w',
                                                                pady=(20, 10))
        row += 1

        self.username_entry = self.create_entry(main, "Create Username:", row)
        row += 1
        self.password_entry = self.create_entry(main, "Create Password:", row, show="•")
        row += 1
        self.confirm_entry = self.create_entry(main, "Confirm Password:", row, show="•")
        row += 1

        btn_frame = tk.Frame(main, bg='#f0f4f8')
        btn_frame.grid(row=row, column=0, columnspan=2, pady=30)

        tk.Button(btn_frame, text="📝 SIGNUP", command=self.signup,
                  bg='#2196F3', fg='white', font=('Arial', 12, 'bold'), padx=30, pady=10).pack(side='left', padx=15)
        tk.Button(btn_frame, text="🔙 BACK", command=self.root.destroy,
                  bg='#9E9E9E', fg='white', font=('Arial', 12, 'bold'), padx=30, pady=10).pack(side='left', padx=15)

    def create_entry(self, parent, label, row, show=None):
        tk.Label(parent, text=label, bg='#f0f4f8', font=('Arial', 11)).grid(row=row, column=0, sticky='w', pady=8)
        entry = tk.Entry(parent, width=30, font=('Arial', 11), show=show if show else "")
        entry.grid(row=row, column=1, pady=8, padx=10)
        return entry

    def signup(self):
        username = self.username_entry.get().strip()
        password = self.password_entry.get().strip()
        confirm = self.confirm_entry.get().strip()
        pin = self.pin_entry.get().strip()

        if not username or not password:
            messagebox.showerror("Error", "Please enter username and password")
            return

        if password != confirm:
            messagebox.showerror("Error", "Passwords do not match")
            return

        if len(password) < 4:
            messagebox.showerror("Error", "Password must be at least 4 characters")
            return

        if len(pin) != 4 or not pin.isdigit():
            messagebox.showerror("Error", "PIN code must be exactly 4 digits")
            return

        user_data = {
            "username": username,
            "password": hash_password(password),
            "pin_code": pin,
            "full_name": self.name_entry.get().strip(),
            "email": self.email_entry.get().strip(),
            "phone": self.phone_entry.get().strip(),
            "gender": self.gender_var.get(),
            "district": self.district_var.get(),
            "school": self.school_entry.get().strip(),
            "education_level": self.level_var.get(),
            "subjects_taught": self.subjects_entry.get().strip(),
            "class_name": self.class_entry.get().strip(),
            "role": "Teacher",
            "status": "pending",
            "date_registered": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "students": []
        }

        users = load_users()
        pending = load_pending()

        if username in users or username in pending:
            messagebox.showerror("Error", "Username already exists!")
            return

        add_pending_user(user_data)
        log_action("TEACHER_SIGNUP", username, "Teacher account registered, pending approval")
        messagebox.showinfo("Success",
                            f"Teacher account submitted for approval!\n\nUsername: {username}\n\nWait for Admin approval.")
        self.root.destroy()


# ============================================================================
# PRINCIPAL SIGNUP
# ============================================================================

class PrincipalSignupWindow:
    def __init__(self, parent=None):
        self.parent = parent
        self.root = tk.Toplevel()
        self.root.title("Principal Signup - Create Account")
        self.root.geometry("700x750")
        self.root.configure(bg='#f0f4f8')
        self.root.resizable(False, False)
        maximize_window(self.root)

        self.setup_ui()

    def setup_ui(self):
        header = tk.Frame(self.root, bg='#FF9800', height=80)
        header.pack(fill='x')
        tk.Label(header, text="👔 PRINCIPAL SIGNUP", bg='#FF9800', fg='white',
                 font=('Arial', 20, 'bold')).pack(pady=(20, 5))
        tk.Label(header, text="Create your principal account", bg='#FF9800', fg='white',
                 font=('Arial', 12)).pack()

        canvas = tk.Canvas(self.root, bg='#f0f4f8')
        scrollbar = tk.Scrollbar(self.root, orient="vertical", command=canvas.yview)
        scrollable_frame = tk.Frame(canvas, bg='#f0f4f8')

        scrollable_frame.bind("<Configure>", lambda e: canvas.configure(scrollregion=canvas.bbox("all")))
        canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
        canvas.configure(yscrollcommand=scrollbar.set)

        canvas.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")

        main = scrollable_frame

        row = 0
        tk.Label(main, text="📝 PERSONAL INFORMATION", bg='#f0f4f8',
                 font=('Arial', 14, 'bold'), fg='#2c3e50').grid(row=row, column=0, columnspan=2, sticky='w',
                                                                pady=(15, 10))
        row += 1

        self.name_entry = self.create_entry(main, "Full Name:", row)
        row += 1
        self.email_entry = self.create_entry(main, "Email:", row)
        row += 1
        self.phone_entry = self.create_entry(main, "Phone:", row)
        row += 1

        tk.Label(main, text="District:", bg='#f0f4f8', font=('Arial', 11)).grid(row=row, column=0, sticky='w', pady=8)
        self.district_var = tk.StringVar(value="Kailahun")
        ttk.Combobox(main, textvariable=self.district_var, values=SIERRA_LEONE_DISTRICTS, width=28,
                     font=('Arial', 11)).grid(row=row, column=1, pady=8, padx=10)
        row += 1

        tk.Label(main, text="🏫 SCHOOL INFORMATION", bg='#f0f4f8',
                 font=('Arial', 14, 'bold'), fg='#2c3e50').grid(row=row, column=0, columnspan=2, sticky='w',
                                                                pady=(20, 10))
        row += 1

        self.school_entry = self.create_entry(main, "School Name:", row)
        row += 1

        tk.Label(main, text="School Type:", bg='#f0f4f8', font=('Arial', 11)).grid(row=row, column=0, sticky='w',
                                                                                   pady=8)
        self.school_type_var = tk.StringVar(value="Primary School")
        ttk.Combobox(main, textvariable=self.school_type_var, values=EDUCATION_LEVELS, width=28,
                     font=('Arial', 11)).grid(row=row, column=1, pady=8, padx=10)
        row += 1

        self.experience_entry = self.create_entry(main, "Years of Experience:", row)
        row += 1

        tk.Label(main, text="🔐 ACCOUNT SECURITY", bg='#f0f4f8',
                 font=('Arial', 14, 'bold'), fg='#2c3e50').grid(row=row, column=0, columnspan=2, sticky='w',
                                                                pady=(20, 10))
        row += 1

        self.username_entry = self.create_entry(main, "Create Username:", row)
        row += 1
        self.password_entry = self.create_entry(main, "Create Password:", row, show="•")
        row += 1
        self.confirm_entry = self.create_entry(main, "Confirm Password:", row, show="•")
        row += 1

        btn_frame = tk.Frame(main, bg='#f0f4f8')
        btn_frame.grid(row=row, column=0, columnspan=2, pady=30)

        tk.Button(btn_frame, text="📝 SIGNUP", command=self.signup,
                  bg='#FF9800', fg='white', font=('Arial', 12, 'bold'), padx=30, pady=10).pack(side='left', padx=15)
        tk.Button(btn_frame, text="🔙 BACK", command=self.root.destroy,
                  bg='#9E9E9E', fg='white', font=('Arial', 12, 'bold'), padx=30, pady=10).pack(side='left', padx=15)

    def create_entry(self, parent, label, row, show=None):
        tk.Label(parent, text=label, bg='#f0f4f8', font=('Arial', 11)).grid(row=row, column=0, sticky='w', pady=8)
        entry = tk.Entry(parent, width=30, font=('Arial', 11), show=show if show else "")
        entry.grid(row=row, column=1, pady=8, padx=10)
        return entry

    def signup(self):
        username = self.username_entry.get().strip()
        password = self.password_entry.get().strip()
        confirm = self.confirm_entry.get().strip()

        if not username or not password:
            messagebox.showerror("Error", "Please enter username and password")
            return

        if password != confirm:
            messagebox.showerror("Error", "Passwords do not match")
            return

        if len(password) < 4:
            messagebox.showerror("Error", "Password must be at least 4 characters")
            return

        user_data = {
            "username": username,
            "password": hash_password(password),
            "full_name": self.name_entry.get().strip(),
            "email": self.email_entry.get().strip(),
            "phone": self.phone_entry.get().strip(),
            "district": self.district_var.get(),
            "school": self.school_entry.get().strip(),
            "school_type": self.school_type_var.get(),
            "experience": self.experience_entry.get().strip(),
            "role": "Principal",
            "status": "pending",
            "date_registered": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "students": []
        }

        users = load_users()
        pending = load_pending()

        if username in users or username in pending:
            messagebox.showerror("Error", "Username already exists!")
            return

        add_pending_user(user_data)
        log_action("PRINCIPAL_SIGNUP", username, "Principal account registered, pending approval")
        messagebox.showinfo("Success",
                            f"Principal account submitted for approval!\n\nUsername: {username}\n\nWait for Admin approval.")
        self.root.destroy()


# ============================================================================
# ADMIN DASHBOARD
# ============================================================================

class AdminDashboard:
    def __init__(self, admin_user):
        self.admin_user = admin_user
        self.root = tk.Toplevel()
        self.root.title("Admin Dashboard")
        self.root.configure(bg=ADMIN_BG)
        maximize_window(self.root)

        self.setup_ui()

    def setup_ui(self):
        header = tk.Frame(self.root, bg=ADMIN_HEADER_BG, height=100)
        header.pack(fill='x')

        tk.Label(header, text="👑 ADMIN DASHBOARD", bg=ADMIN_HEADER_BG, fg='white',
                 font=('Arial', 24, 'bold')).pack(pady=(25, 5))
        tk.Label(header, text=f"Welcome, {self.admin_user.get('full_name', 'Admin')} | SDG 4: Quality Education",
                 bg=ADMIN_HEADER_BG, fg='#FFD700', font=('Arial', 12)).pack()

        main_container = tk.Frame(self.root, bg=ADMIN_BG)
        main_container.pack(fill='both', expand=True)

        center_frame = tk.Frame(main_container, bg=ADMIN_BG)
        center_frame.pack(expand=True)

        tk.Label(center_frame, text="SYSTEM MANAGEMENT", bg=ADMIN_BG, fg='white',
                 font=('Arial', 20, 'bold')).pack(pady=(0, 40))

        buttons = [
            ("📋 Pending Approvals", self.open_approval_panel, "Approve new user registrations"),
            ("👥 User Management", self.open_user_management, "Manage all system users"),
            ("📊 View Audit Log", self.view_audit_log, "View system activity logs"),
            ("💾 System Backup", self.backup_system, "Create data backup"),
            ("🖨️ Print System Report", self.print_system_report, "Generate system report"),
            ("🚪 Logout", self.logout, "Exit admin panel"),
        ]

        for text, command, tooltip in buttons:
            btn = tk.Button(center_frame, text=text, command=command,
                            bg=ADMIN_BTN_BG, fg='white',
                            font=('Arial', 13, 'bold'),
                            width=28, height=2,
                            relief=tk.RAISED, bd=2,
                            activebackground=ADMIN_BTN_HOVER,
                            activeforeground='white')
            btn.pack(pady=10)
            self.add_tooltip(btn, tooltip)

        footer = tk.Frame(self.root, bg=ADMIN_HEADER_BG, height=50)
        footer.pack(side='bottom', fill='x')
        tk.Label(footer, text=SDG_TAG, bg=ADMIN_HEADER_BG, fg='white',
                 font=('Arial', 10)).pack(pady=15)

    def add_tooltip(self, widget, text):
        def show_tooltip(event):
            tooltip = tk.Toplevel(widget)
            tooltip.wm_overrideredirect(True)
            tooltip.wm_geometry(f"+{event.x_root + 10}+{event.y_root + 10}")
            label = tk.Label(tooltip, text=text, background="#ffffe0", relief="solid", borderwidth=1)
            label.pack()
            widget.tooltip = tooltip

        def hide_tooltip(event):
            if hasattr(widget, 'tooltip'):
                widget.tooltip.destroy()

        widget.bind('<Enter>', show_tooltip)
        widget.bind('<Leave>', hide_tooltip)

    def open_approval_panel(self):
        self.root.destroy()
        AdminApprovalPanel(self.admin_user, self)

    def open_user_management(self):
        self.root.destroy()
        AdminUserManagement(self.admin_user, self)

    def view_audit_log(self):
        log_window = tk.Toplevel(self.root)
        log_window.title("System Audit Log")
        log_window.geometry("900x600")
        log_window.configure(bg=ADMIN_BG)
        maximize_window(log_window)

        text_widget = tk.Text(log_window, font=('Courier', 10), wrap=tk.WORD)
        text_widget.pack(fill='both', expand=True, padx=20, pady=20)

        log_file = "data/audit.log"
        content = ""
        if os.path.exists(log_file):
            try:
                with open(log_file, 'r', encoding='utf-8') as f:
                    content = f.read()
                    text_widget.insert(1.0, content)
            except:
                text_widget.insert(1.0, "No audit logs found.")
        else:
            text_widget.insert(1.0, "No audit logs found.")

        text_widget.config(state='disabled')

        btn_frame = tk.Frame(log_window, bg=ADMIN_BG)
        btn_frame.pack(pady=15)

        tk.Button(btn_frame, text="🖨️ Print Log",
                  command=lambda: print_report(content if content else "No logs", "Audit_Log"),
                  bg=ADMIN_BTN_BG, fg='white', font=('Arial', 11, 'bold'), padx=20, pady=8).pack(side='left', padx=15)
        tk.Button(btn_frame, text="🔙 BACK", command=log_window.destroy,
                  bg=ADMIN_BTN_BG, fg='white', font=('Arial', 11, 'bold'), padx=20, pady=8).pack(side='left', padx=15)

    def backup_system(self):
        backup_dir = create_backup()
        messagebox.showinfo("Backup Created", f"System backup created at:\n\n{backup_dir}")

    def print_system_report(self):
        users = load_users()
        pending = load_pending()

        report = f"""
SYSTEM ADMINISTRATION REPORT
{'=' * 60}

SYSTEM OVERVIEW
{'=' * 60}
Total Approved Users: {len(users)}
Total Pending Users: {len(pending)}
Report Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}

USER BREAKDOWN
{'=' * 60}
"""
        for username, data in users.items():
            report += f"\nUsername: {username}\n   Role: {data.get('role', 'N/A')}\n   Status: {data.get('status', 'N/A')}\n"

        print_report(report, "System_Administration_Report")

    def logout(self):
        if messagebox.askyesno("Logout", "Are you sure you want to logout?"):
            self.root.destroy()
            login = LoginWindow()
            login.root.mainloop()


# ============================================================================
# ADMIN USER MANAGEMENT
# ============================================================================

class AdminUserManagement:
    def __init__(self, admin_user, parent_dashboard=None):
        self.admin_user = admin_user
        self.parent_dashboard = parent_dashboard
        self.root = tk.Toplevel()
        self.root.title("Admin User Management - Manage All Users")
        self.root.configure(bg=ADMIN_BG)
        maximize_window(self.root)

        self.setup_ui()
        self.load_all_users()

    def setup_ui(self):
        header = tk.Frame(self.root, bg=ADMIN_HEADER_BG, height=70)
        header.pack(fill='x')
        tk.Label(header, text="👑 ADMIN USER MANAGEMENT", bg=ADMIN_HEADER_BG, fg='white',
                 font=('Arial', 20, 'bold')).pack(pady=18)

        main = tk.Frame(self.root, bg=ADMIN_BG)
        main.pack(fill='both', expand=True, padx=20, pady=15)

        list_frame = tk.LabelFrame(main, text="All System Users", bg='white', font=('Arial', 14, 'bold'), fg=ADMIN_BG)
        list_frame.pack(fill='both', expand=True)

        columns = ("Username", "Full Name", "Role", "District/School", "Status", "Registered")
        self.tree = ttk.Treeview(list_frame, columns=columns, show="headings", height=18)

        col_widths = {"Username": 140, "Full Name": 180, "Role": 120, "District/School": 200, "Status": 100,
                      "Registered": 140}
        for col in columns:
            self.tree.heading(col, text=col)
            self.tree.column(col, width=col_widths.get(col, 120))

        self.tree.pack(side='left', fill='both', expand=True)

        scrollbar = ttk.Scrollbar(list_frame, orient='vertical', command=self.tree.yview)
        self.tree.configure(yscrollcommand=scrollbar.set)
        scrollbar.pack(side='right', fill='y')

        self.tree.bind('<Double-1>', self.edit_user)

        btn_frame = tk.Frame(main, bg=ADMIN_BG)
        btn_frame.pack(fill='x', pady=15)

        buttons = [
            ("✏️ Edit User", self.edit_user),
            ("🗑️ Delete User", self.delete_user),
            ("🔐 Reset Password", self.reset_password),
            ("🖨️ Print User List", self.print_users),
            ("🔄 Refresh", self.load_all_users),
            ("🔙 BACK TO ADMIN", self.go_back),
        ]

        for text, command in buttons:
            tk.Button(btn_frame, text=text, command=command,
                      bg=ADMIN_BTN_BG, fg='white', font=('Arial', 11, 'bold'),
                      padx=18, pady=8).pack(side='left', padx=8)

    def go_back(self):
        self.root.destroy()
        if self.parent_dashboard:
            self.parent_dashboard.root.destroy()
        AdminDashboard(self.admin_user)

    def load_all_users(self):
        for item in self.tree.get_children():
            self.tree.delete(item)

        users = load_users()

        for username, data in users.items():
            status = "✅ Approved" if data.get("status") == "approved" else "⏳ Pending"
            self.tree.insert("", "end", values=(
                username,
                data.get("full_name", "N/A"),
                data.get("role", "N/A"),
                data.get("school", data.get("district", "N/A")),
                status,
                data.get("date_registered", "N/A")[:10]
            ), tags=(username,))

    def edit_user(self, event=None):
        selected = self.tree.selection()
        if not selected:
            messagebox.showwarning("No Selection", "Please select a user to edit")
            return

        username = self.tree.item(selected[0])['tags'][0]
        users = load_users()

        if username not in users:
            messagebox.showerror("Error", "User not found")
            return

        user = users[username]

        edit_window = tk.Toplevel(self.root)
        edit_window.title(f"Edit User - {username}")
        edit_window.geometry("550x550")
        edit_window.configure(bg=ADMIN_BG)

        tk.Label(edit_window, text=f"EDIT USER: {username}", bg=ADMIN_BG, fg='white',
                 font=('Arial', 16, 'bold')).pack(pady=15)

        main = tk.Frame(edit_window, bg='white')
        main.pack(fill='both', expand=True, padx=30, pady=20)

        fields = [
            ("Full Name:", user.get("full_name", "")),
            ("Role:", user.get("role", "")),
            ("District:", user.get("district", "")),
            ("School:", user.get("school", "")),
        ]

        entries = {}
        row = 0
        for label, value in fields:
            tk.Label(main, text=label, bg='white', font=('Arial', 11)).grid(row=row, column=0, sticky='w', pady=8)
            entry = tk.Entry(main, width=35, font=('Arial', 11))
            entry.grid(row=row, column=1, pady=8, padx=15)
            entry.insert(0, value)
            entries[label] = entry
            row += 1

        if user.get("role") == "Teacher":
            tk.Label(main, text="Class:", bg='white', font=('Arial', 11)).grid(row=row, column=0, sticky='w', pady=8)
            class_entry = tk.Entry(main, width=35, font=('Arial', 11))
            class_entry.grid(row=row, column=1, pady=8, padx=15)
            class_entry.insert(0, user.get("class_name", ""))
            entries["Class:"] = class_entry
            row += 1

            tk.Label(main, text="Subjects:", bg='white', font=('Arial', 11)).grid(row=row, column=0, sticky='w', pady=8)
            subj_entry = tk.Entry(main, width=35, font=('Arial', 11))
            subj_entry.grid(row=row, column=1, pady=8, padx=15)
            subj_entry.insert(0, user.get("subjects_taught", ""))
            entries["Subjects:"] = subj_entry

        def save_changes():
            users[username]["full_name"] = entries["Full Name:"].get().strip()
            users[username]["district"] = entries["District:"].get().strip()
            users[username]["school"] = entries["School:"].get().strip()

            if user.get("role") == "Teacher":
                users[username]["class_name"] = entries.get("Class:", tk.Entry()).get().strip()
                users[username]["subjects_taught"] = entries.get("Subjects:", tk.Entry()).get().strip()

            save_users(users)
            log_action("EDIT_USER", self.admin_user.get("username", "Admin"), f"Edited user: {username}")
            messagebox.showinfo("Success", f"User '{username}' has been updated!")
            edit_window.destroy()
            self.load_all_users()

        btn_frame = tk.Frame(edit_window, bg=ADMIN_BG)
        btn_frame.pack(pady=20)

        tk.Button(btn_frame, text="💾 Save Changes", command=save_changes,
                  bg=ADMIN_BTN_BG, fg='white', font=('Arial', 11, 'bold'), padx=25, pady=8).pack(side='left', padx=15)
        tk.Button(btn_frame, text="Cancel", command=edit_window.destroy,
                  bg=ADMIN_BTN_BG, fg='white', font=('Arial', 11, 'bold'), padx=25, pady=8).pack(side='left', padx=15)

    def delete_user(self):
        selected = self.tree.selection()
        if not selected:
            messagebox.showwarning("No Selection", "Please select a user to delete")
            return

        username = self.tree.item(selected[0])['tags'][0]

        if username == "admin":
            messagebox.showerror("Error", "Cannot delete the main Admin account!")
            return

        if messagebox.askyesno("Confirm Delete", f"Delete user '{username}'?\nThis cannot be undone."):
            users = load_users()
            if username in users:
                del users[username]
                save_users(users)
                log_action("DELETE_USER", self.admin_user.get("username", "Admin"), f"Deleted user: {username}")
                messagebox.showinfo("Success", f"User '{username}' deleted.")
                self.load_all_users()

    def reset_password(self):
        selected = self.tree.selection()
        if not selected:
            messagebox.showwarning("No Selection", "Select a user")
            return

        username = self.tree.item(selected[0])['tags'][0]
        users = load_users()

        if username not in users:
            messagebox.showerror("Error", "User not found")
            return

        new_password = "reset123"
        users[username]["password"] = hash_password(new_password)
        save_users(users)

        log_action("RESET_PASSWORD", self.admin_user.get("username", "Admin"), f"Reset password for: {username}")
        messagebox.showinfo("Success", f"Password for '{username}' reset to: {new_password}")

    def print_users(self):
        users = load_users()
        report = f"""
USER MANAGEMENT REPORT
{'=' * 60}
Total Users: {len(users)}
Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}

USER LIST
{'=' * 60}
"""
        for username, data in users.items():
            report += f"\nUsername: {username}\n   Name: {data.get('full_name', 'N/A')}\n   Role: {data.get('role', 'N/A')}\n   Status: {data.get('status', 'N/A')}\n"

        print_report(report, "User_Management_Report")


# ============================================================================
# ADMIN APPROVAL PANEL
# ============================================================================

class AdminApprovalPanel:
    def __init__(self, admin_user, parent_dashboard=None):
        self.admin_user = admin_user
        self.parent_dashboard = parent_dashboard
        self.root = tk.Toplevel()
        self.root.title("Admin Approval Panel - Pending Users")
        self.root.configure(bg=ADMIN_BG)
        maximize_window(self.root)

        self.setup_ui()
        self.load_pending_users()

    def setup_ui(self):
        header = tk.Frame(self.root, bg=ADMIN_HEADER_BG, height=70)
        header.pack(fill='x')
        tk.Label(header, text="👑 ADMIN APPROVAL PANEL", bg=ADMIN_HEADER_BG, fg='white',
                 font=('Arial', 20, 'bold')).pack(pady=18)

        stats_frame = tk.Frame(self.root, bg=ADMIN_BG)
        stats_frame.pack(fill='x', padx=20, pady=10)

        self.pending_count_label = tk.Label(stats_frame, text="Pending: 0", bg=ADMIN_BG, fg='#FFD700',
                                            font=('Arial', 14, 'bold'))
        self.pending_count_label.pack(side='left', padx=10)

        main = tk.Frame(self.root, bg=ADMIN_BG)
        main.pack(fill='both', expand=True, padx=20, pady=10)

        list_frame = tk.LabelFrame(main, text="Pending User Requests", bg='white', font=('Arial', 14, 'bold'),
                                   fg=ADMIN_BG)
        list_frame.pack(fill='both', expand=True)

        columns = ("Username", "Full Name", "Role", "School/District", "Date Registered", "Status")
        self.tree = ttk.Treeview(list_frame, columns=columns, show="headings", height=18)

        col_widths = {"Username": 140, "Full Name": 180, "Role": 120, "School/District": 200, "Date Registered": 140,
                      "Status": 100}
        for col in columns:
            self.tree.heading(col, text=col)
            self.tree.column(col, width=col_widths.get(col, 120))

        self.tree.pack(side='left', fill='both', expand=True)

        scrollbar = ttk.Scrollbar(list_frame, orient='vertical', command=self.tree.yview)
        self.tree.configure(yscrollcommand=scrollbar.set)
        scrollbar.pack(side='right', fill='y')

        self.tree.bind('<Double-1>', self.view_details)

        btn_frame = tk.Frame(main, bg=ADMIN_BG)
        btn_frame.pack(fill='x', pady=15)

        buttons = [
            ("✅ Approve Selected", self.approve_user),
            ("❌ Reject Selected", self.reject_user),
            ("🔄 Refresh", self.load_pending_users),
            ("👁️ View Details", self.view_details),
            ("🖨️ Print Pending List", self.print_pending),
            ("🔙 BACK TO ADMIN", self.go_back),
        ]

        for text, command in buttons:
            tk.Button(btn_frame, text=text, command=command,
                      bg=ADMIN_BTN_BG, fg='white', font=('Arial', 11, 'bold'),
                      padx=18, pady=8).pack(side='left', padx=8)

    def go_back(self):
        self.root.destroy()
        if self.parent_dashboard:
            self.parent_dashboard.root.destroy()
        AdminDashboard(self.admin_user)

    def load_pending_users(self):
        for item in self.tree.get_children():
            self.tree.delete(item)

        pending = load_pending()
        count = 0

        for username, data in pending.items():
            self.tree.insert("", "end", values=(
                username,
                data.get("full_name", "N/A"),
                data.get("role", "N/A"),
                data.get("school", data.get("district", "N/A")),
                data.get("date_registered", "N/A")[:10],
                "⏳ Pending"
            ), tags=(username,))
            count += 1

        self.pending_count_label.config(text=f"📊 Pending Users: {count}")

    def view_details(self, event=None):
        selected = self.tree.selection()
        if not selected:
            messagebox.showwarning("No Selection", "Please select a user")
            return

        username = self.tree.item(selected[0])['tags'][0]
        pending = load_pending()

        if username not in pending:
            messagebox.showerror("Error", "User not found")
            return

        user = pending[username]

        detail_window = tk.Toplevel(self.root)
        detail_window.title(f"User Details - {username}")
        detail_window.geometry("600x700")
        detail_window.configure(bg=ADMIN_BG)

        text_widget = tk.Text(detail_window, font=('Courier', 11), wrap=tk.WORD)
        text_widget.pack(fill='both', expand=True, padx=20, pady=20)

        details = f"""
╔══════════════════════════════════════════════════════════════════════════════╗
║                              USER DETAILS                                     ║
╚══════════════════════════════════════════════════════════════════════════════╝

📋 BASIC INFORMATION
────────────────────────────────────────────────────────────────────────────────
   Username:     {username}
   Full Name:    {user.get('full_name', 'N/A')}
   Role:         {user.get('role', 'N/A')}
   Status:       {user.get('status', 'pending')}
   Registered:   {user.get('date_registered', 'N/A')}

"""

        if user.get('role') == 'Student':
            details += f"""
🎓 STUDENT DETAILS
────────────────────────────────────────────────────────────────────────────────
   Date of Birth:    {user.get('date_of_birth', 'N/A')}
   Gender:           {user.get('gender', 'N/A')}
   District:         {user.get('district', 'N/A')}
   Education Level:  {user.get('education_level', 'N/A')}
   School:           {user.get('school', 'N/A')}

👨‍👩‍👧 PARENT INFORMATION
────────────────────────────────────────────────────────────────────────────────
   Parent Name:      {user.get('parent_name', 'N/A')}
   Parent Phone:     {user.get('parent_phone', 'N/A')}
"""
        elif user.get('role') == 'Teacher':
            details += f"""
👩‍🏫 TEACHER DETAILS
────────────────────────────────────────────────────────────────────────────────
   Email:            {user.get('email', 'N/A')}
   Phone:            {user.get('phone', 'N/A')}
   Gender:           {user.get('gender', 'N/A')}
   District:         {user.get('district', 'N/A')}
   School:           {user.get('school', 'N/A')}
   Education Level:  {user.get('education_level', 'N/A')}
   Subjects Taught:  {user.get('subjects_taught', 'N/A')}
   Class:            {user.get('class_name', 'N/A')}
   PIN Code:         {user.get('pin_code', 'N/A')}
"""
        elif user.get('role') == 'Principal':
            details += f"""
👔 PRINCIPAL DETAILS
────────────────────────────────────────────────────────────────────────────────
   Email:            {user.get('email', 'N/A')}
   Phone:            {user.get('phone', 'N/A')}
   District:         {user.get('district', 'N/A')}
   School:           {user.get('school', 'N/A')}
   School Type:      {user.get('school_type', 'N/A')}
   Years Experience: {user.get('experience', 'N/A')}
"""

        text_widget.insert(1.0, details)
        text_widget.config(state='disabled')

        btn_frame = tk.Frame(detail_window, bg=ADMIN_BG)
        btn_frame.pack(pady=15)

        tk.Button(btn_frame, text="✅ Approve", command=lambda: self.approve_from_details(username, detail_window),
                  bg=ADMIN_BTN_BG, fg='white', font=('Arial', 11, 'bold'), padx=20, pady=8).pack(side='left', padx=10)
        tk.Button(btn_frame, text="❌ Reject", command=lambda: self.reject_from_details(username, detail_window),
                  bg=ADMIN_BTN_BG, fg='white', font=('Arial', 11, 'bold'), padx=20, pady=8).pack(side='left', padx=10)
        tk.Button(btn_frame, text="🖨️ Print", command=lambda: print_report(details, f"User_{username}"),
                  bg=ADMIN_BTN_BG, fg='white', font=('Arial', 11, 'bold'), padx=20, pady=8).pack(side='left', padx=10)
        tk.Button(btn_frame, text="Close", command=detail_window.destroy,
                  bg=ADMIN_BTN_BG, fg='white', font=('Arial', 11, 'bold'), padx=20, pady=8).pack(side='left', padx=10)

    def approve_from_details(self, username, window):
        self.approve_user_by_username(username)
        window.destroy()

    def reject_from_details(self, username, window):
        self.reject_user_by_username(username)
        window.destroy()

    def approve_user_by_username(self, username):
        pending = load_pending()
        if username not in pending:
            return

        user_data = pending[username]
        user_data["status"] = "approved"
        user_data["date_approved"] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

        del pending[username]
        save_pending(pending)

        users = load_users()
        users[username] = user_data
        save_users(users)

        log_action("APPROVE_USER", self.admin_user.get("username", "Admin"), f"Approved user: {username}")
        messagebox.showinfo("Success", f"User '{username}' has been APPROVED!")
        self.load_pending_users()

    def reject_user_by_username(self, username):
        if messagebox.askyesno("Confirm Reject", f"Reject '{username}'?"):
            pending = load_pending()
            if username in pending:
                del pending[username]
                save_pending(pending)
                log_action("REJECT_USER", self.admin_user.get("username", "Admin"), f"Rejected user: {username}")
                messagebox.showinfo("Success", f"User '{username}' has been REJECTED.")
                self.load_pending_users()

    def approve_user(self):
        selected = self.tree.selection()
        if not selected:
            messagebox.showwarning("No Selection", "Please select a user")
            return

        username = self.tree.item(selected[0])['tags'][0]
        self.approve_user_by_username(username)

    def reject_user(self):
        selected = self.tree.selection()
        if not selected:
            messagebox.showwarning("No Selection", "Please select a user")
            return

        username = self.tree.item(selected[0])['tags'][0]
        self.reject_user_by_username(username)

    def print_pending(self):
        pending = load_pending()
        report = f"""
PENDING USER REQUESTS
{'=' * 60}
Total Pending: {len(pending)}
Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}

PENDING LIST
{'=' * 60}
"""
        for username, data in pending.items():
            report += f"\nUsername: {username}\n   Name: {data.get('full_name', 'N/A')}\n   Role: {data.get('role', 'N/A')}\n   Date: {data.get('date_registered', 'N/A')}\n"

        print_report(report, "Pending_Approvals_Report")


# ============================================================================
# MAIN APPLICATION (Teacher/Principal Dashboard) WITH CSV IMPORT & BACK BUTTON
# ============================================================================

class MainApplication:
    def __init__(self, root, user):
        self.root = root
        self.user = user
        self.records = user.get("students", [])
        self.subject_entries = {}

        self.root.title(f"{APP_NAME} - {user['full_name']} ({user['role']})")
        self.root.configure(bg='#f0f4f8')
        maximize_window(self.root)

        self.setup_ui()
        self.load_sample_data()
        self.refresh_table()
        self.update_stats()

    def setup_ui(self):
        header_color = TEACHER_HEADER_BG if self.user['role'] == "Teacher" else PRINCIPAL_HEADER_BG
        header = tk.Frame(self.root, bg=header_color, height=70)
        header.pack(fill='x')

        tk.Label(header, text=SDG_TAG, bg=header_color, fg='white',
                 font=('Arial', 14, 'bold')).pack(side='left', padx=30, pady=20)

        user_frame = tk.Frame(header, bg=header_color)
        user_frame.pack(side='right', padx=30)
        tk.Label(user_frame, text=f"👤 {self.user['full_name']}",
                 bg=header_color, fg='white', font=('Arial', 13, 'bold')).pack()
        tk.Label(user_frame, text=f"Role: {self.user['role']} | School: {self.user.get('school', 'N/A')}",
                 bg=header_color, fg='#FFD700', font=('Arial', 10)).pack()

        main = tk.Frame(self.root, bg='#f0f4f8')
        main.pack(fill='both', expand=True, padx=20, pady=15)

        # LEFT PANEL
        left = tk.LabelFrame(main, text="📝 Student Information", bg='white', font=('Arial', 13, 'bold'), padx=15,
                             pady=15)
        left.pack(side='left', fill='both', expand=True, padx=(0, 10))

        tk.Label(left, text="Student Name:", bg='white', font=('Arial', 11)).grid(row=0, column=0, sticky='w', pady=8)
        self.name_entry = tk.Entry(left, width=30, font=('Arial', 11))
        self.name_entry.grid(row=0, column=1, pady=8, padx=10)

        tk.Label(left, text="District:", bg='white', font=('Arial', 11)).grid(row=1, column=0, sticky='w', pady=8)
        self.district_var = tk.StringVar(value="Kailahun")
        ttk.Combobox(left, textvariable=self.district_var, values=SIERRA_LEONE_DISTRICTS, width=27,
                     font=('Arial', 11)).grid(row=1, column=1, pady=8, padx=10)

        tk.Label(left, text="Gender:", bg='white', font=('Arial', 11)).grid(row=2, column=0, sticky='w', pady=8)
        self.gender_var = tk.StringVar(value="Female")
        g_frame = tk.Frame(left, bg='white')
        g_frame.grid(row=2, column=1, sticky='w')
        tk.Radiobutton(g_frame, text="Male", variable=self.gender_var, value="Male", bg='white',
                       font=('Arial', 11)).pack(side='left')
        tk.Radiobutton(g_frame, text="Female", variable=self.gender_var, value="Female", bg='white',
                       font=('Arial', 11)).pack(side='left', padx=15)

        tk.Label(left, text="Student Password:", bg='white', font=('Arial', 11)).grid(row=3, column=0, sticky='w',
                                                                                      pady=8)
        self.student_pwd_entry = tk.Entry(left, width=30, font=('Arial', 11), show="•")
        self.student_pwd_entry.grid(row=3, column=1, pady=8, padx=10)
        self.student_pwd_entry.insert(0, "pass123")

        subj_frame = tk.LabelFrame(left, text="📚 Subjects & Grades", bg='white', font=('Arial', 11, 'bold'), padx=10,
                                   pady=5)
        subj_frame.grid(row=4, column=0, columnspan=2, sticky='nsew', pady=15)
        left.grid_rowconfigure(4, weight=1)

        self.subj_container = tk.Frame(subj_frame, bg='white')
        self.subj_container.pack(fill='both', expand=True)

        tk.Button(subj_frame, text="➕ Add New Subject", command=self.add_subject,
                  bg='#2196F3', fg='white', font=('Arial', 10, 'bold')).pack(pady=8)

        btn_frame = tk.Frame(left, bg='white')
        btn_frame.grid(row=5, column=0, columnspan=2, pady=15)

        buttons = [
            ("➕ Add Student", self.add_student, '#4CAF50'),
            ("📝 Update", self.update_student, '#2196F3'),
            ("🗑️ Delete", self.delete_student, '#f44336'),
            ("🗑️ Clear", self.clear_form, '#9E9E9E'),
            ("🖨️ Print Class", self.print_class_list, '#FF9800'),
        ]

        for text, command, color in buttons:
            tk.Button(btn_frame, text=text, command=command,
                      bg=color, fg='white', font=('Arial', 10, 'bold'), padx=12).pack(side='left', padx=6)

        # RIGHT PANEL
        right = tk.Frame(main, bg='#f0f4f8')
        right.pack(side='right', fill='both', expand=True)

        s_frame = tk.Frame(right, bg='#f0f4f8')
        s_frame.pack(fill='x', pady=(0, 10))
        tk.Label(s_frame, text="🔍 Search:", bg='#f0f4f8', font=('Arial', 11)).pack(side='left')
        self.search_entry = tk.Entry(s_frame, width=30, font=('Arial', 11))
        self.search_entry.pack(side='left', padx=15)
        self.search_entry.bind('<KeyRelease>', lambda e: self.refresh_table())

        table_frame = tk.LabelFrame(right, text="📋 Student Records", bg='white', font=('Arial', 13, 'bold'))
        table_frame.pack(fill='both', expand=True)

        cols = ("ID", "Name", "District", "Gender", "Subjects", "Average", "Status")
        self.tree = ttk.Treeview(table_frame, columns=cols, show="headings", height=18)

        widths = {"ID": 140, "Name": 160, "District": 140, "Gender": 90, "Subjects": 110, "Average": 100, "Status": 150}
        for col in cols:
            self.tree.heading(col, text=col)
            self.tree.column(col, width=widths.get(col, 120))

        scroll_y = ttk.Scrollbar(table_frame, orient='vertical', command=self.tree.yview)
        scroll_x = ttk.Scrollbar(table_frame, orient='horizontal', command=self.tree.xview)
        self.tree.configure(yscrollcommand=scroll_y.set, xscrollcommand=scroll_x.set)

        self.tree.pack(side='left', fill='both', expand=True)
        scroll_y.pack(side='right', fill='y')
        scroll_x.pack(side='bottom', fill='x')

        self.tree.bind('<<TreeviewSelect>>', self.on_select)

        stats_frame = tk.LabelFrame(right, text="📊 Statistics Dashboard - SDG 4 Progress", bg='white',
                                    font=('Arial', 13, 'bold'))
        stats_frame.pack(fill='x', pady=(10, 0))

        self.stats_text = tk.Text(stats_frame, height=7, font=('Courier', 10), bg='#e8f5e9')
        self.stats_text.pack(fill='x', padx=10, pady=10)

        footer = tk.Frame(right, bg='#f0f4f8')
        footer.pack(fill='x', pady=10)

        footer_buttons = [
            ("💾 Save Data", self.save_data, '#4CAF50'),
            ("📂 Load Data", self.load_data, '#2196F3'),
            ("📊 Export CSV", self.export_csv, '#FF9800'),
            ("👨‍🎓 Student Portal", self.open_student_portal, '#9C27B0'),
            ("🖨️ Print Selected", self.print_selected_student, '#4CAF50'),
            ("📥 Import CSV", self.import_csv, '#4CAF50'),
            ("🔙 BACK TO LOGIN", self.back_to_login, '#9E9E9E'),  # BACK BUTTON
            ("🚪 Logout", self.logout, '#9E9E9E'),
        ]

        for text, command, color in footer_buttons:
            tk.Button(footer, text=text, command=command,
                      bg=color, fg='white', font=('Arial', 10, 'bold'), padx=12).pack(side='left', padx=6)

        self.status_bar = tk.Label(self.root, text="✅ Ready", bd=1, relief=tk.SUNKEN, anchor='w', bg='#e0e0e0',
                                   font=('Arial', 10))
        self.status_bar.pack(side='bottom', fill='x')

        for _ in range(3):
            self.add_subject()

    # ========================================================================
    # BACK TO LOGIN FUNCTION
    # ========================================================================

    def back_to_login(self):
        """Go back to login screen"""
        if messagebox.askyesno("Back to Login", "Are you sure you want to go back to the login screen?\n\nAny unsaved data will be lost."):
            log_action("BACK_TO_LOGIN", self.user.get("username", "User"), "Returned to login screen")
            self.root.destroy()
            login = LoginWindow()
            login.root.mainloop()

    # ========================================================================
    # CSV IMPORT FUNCTION
    # ========================================================================

    def import_csv(self):
        """Import students from CSV file - Bulk upload feature"""
        filename = filedialog.askopenfilename(
            filetypes=[("CSV files", "*.csv"), ("All files", "*.*")]
        )

        if not filename:
            return

        if not messagebox.askyesno("Confirm Import",
                                   "This will import students from the CSV file.\n\n"
                                   "Duplicate names will be skipped.\n\n"
                                   "Continue?"):
            return

        try:
            imported_count = 0
            skipped_count = 0

            with open(filename, 'r', encoding='utf-8-sig') as file:
                reader = csv.DictReader(file)

                if not reader.fieldnames:
                    messagebox.showerror("Error", "CSV file must have headers")
                    return

                for row_num, row in enumerate(reader, start=2):
                    try:
                        name = row.get('Name', row.get('name', '')).strip()
                        district = row.get('District', row.get('district', 'Kailahun')).strip()
                        gender = row.get('Gender', row.get('gender', 'Female')).strip()
                        student_password = row.get('Password', row.get('password', 'pass123')).strip()

                        if not name:
                            skipped_count += 1
                            continue

                        duplicate = False
                        for s in self.records:
                            if s["name"].lower() == name.lower():
                                duplicate = True
                                break

                        if duplicate:
                            skipped_count += 1
                            continue

                        subjects = {}
                        for key, value in row.items():
                            if key.startswith('Subject_') and value:
                                subject_name = key.replace('Subject_', '').replace('_', ' ')
                                try:
                                    grade = float(value)
                                    if 0 <= grade <= 100:
                                        subjects[subject_name] = grade
                                except:
                                    pass

                        if not subjects:
                            subjects = {"English": 70, "Mathematics": 70, "Science": 70}

                        if district not in SIERRA_LEONE_DISTRICTS:
                            district = "Kailahun"
                        if gender not in ["Male", "Female"]:
                            gender = "Female"

                        avg = calculate_average(subjects)
                        status = determine_status(avg)
                        student_id = generate_user_id("Student", district, len(self.records) + imported_count)

                        self.records.append({
                            "student_id": student_id,
                            "name": name,
                            "district": district,
                            "gender": gender,
                            "subjects": subjects,
                            "average": avg,
                            "status": status,
                            "password": hash_password(student_password),
                            "date_added": datetime.now().strftime("%Y-%m-%d")
                        })

                        imported_count += 1

                    except Exception as e:
                        skipped_count += 1
                        print(f"Error at row {row_num}: {e}")

            users = load_users()
            if self.user.get("username"):
                users[self.user["username"]]["students"] = self.records
                save_users(users)

            log_action("IMPORT_STUDENTS", self.user.get("username", "Teacher"), f"Imported {imported_count} students")

            self.refresh_table()
            self.update_stats()

            messagebox.showinfo("Import Complete",
                               f"✅ Successfully imported: {imported_count} students\n"
                               f"⚠️ Skipped (duplicates/errors): {skipped_count}")
            self.status(f"📥 Imported {imported_count} students from CSV")

        except Exception as e:
            messagebox.showerror("Import Error", f"Failed to import CSV: {str(e)}")

    # ========================================================================
    # REST OF THE METHODS
    # ========================================================================

    def open_student_portal(self):
        StudentLoginWindow(self)

    def print_selected_student(self):
        selected = self.tree.selection()
        if not selected:
            messagebox.showwarning("No Selection", "Please select a student to print")
            return

        name = self.tree.item(selected[0])['values'][1]
        for s in self.records:
            if s["name"] == name:
                report = f"""
STUDENT REPORT CARD
{'=' * 60}
Student Name: {s['name']}
Student ID: {s['student_id']}
District: {s['district']}
Gender: {s['gender']}
Date: {datetime.now().strftime('%B %d, %Y')}

{'=' * 60}
SUBJECT GRADES
{'=' * 60}
"""
                for subject, grade in s.get('subjects', {}).items():
                    report += f"{subject:25} {grade:>3}%\n"

                report += f"""
{'=' * 60}
SUMMARY
{'=' * 60}
Overall Average: {s['average']:.1f}%
Overall Status: {s['status']}

This report supports SDG 4: Quality Education in Sierra Leone
"""
                print_report(report, f"Report_{s['name']}")
                break

    def print_class_list(self):
        if not self.records:
            messagebox.showwarning("No Data", "No students to print")
            return

        report = f"""
CLASS LIST REPORT
{'=' * 60}
Teacher: {self.user.get('full_name', 'N/A')}
School: {self.user.get('school', 'N/A')}
Class: {self.user.get('class_name', 'N/A')}
Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}

STUDENT LIST
{'=' * 60}
"""
        for s in self.records:
            report += f"\n{s['student_id']} | {s['name']} | {s['district']} | Avg: {s['average']:.1f}% | {s['status']}\n"

        report += f"\n{'=' * 60}\nTotal Students: {len(self.records)}"
        print_report(report, "Class_List_Report")

    def add_subject(self):
        num = len(self.subject_entries) + 1
        frame = tk.Frame(self.subj_container, bg='white')
        frame.pack(fill='x', pady=3)

        tk.Label(frame, text=f"Subject {num}:", bg='white', width=12, anchor='w', font=('Arial', 10)).pack(side='left')

        subj_entry = tk.Entry(frame, width=20, font=('Arial', 10))
        subj_entry.pack(side='left', padx=8)
        subj_entry.insert(0, f"Subject {num}")

        tk.Label(frame, text="Grade:", bg='white', font=('Arial', 10)).pack(side='left', padx=(10, 0))

        grade_entry = tk.Entry(frame, width=8, font=('Arial', 10))
        grade_entry.pack(side='left', padx=8)

        def validate(e, e2=grade_entry):
            val = e2.get()
            if val:
                try:
                    g = float(val)
                    e2.config(bg='#e8f5e9' if 0 <= g <= 100 else '#ffebee')
                except:
                    e2.config(bg='#fff3e0')
            else:
                e2.config(bg='white')

        grade_entry.bind('<KeyRelease>', validate)

        tk.Button(frame, text="✖", command=lambda: self.remove_subject(frame),
                  bg='#ffebee', fg='red', font=('Arial', 9), width=2).pack(side='left', padx=5)

        self.subject_entries[subj_entry] = grade_entry

    def remove_subject(self, frame):
        for s in list(self.subject_entries.keys()):
            if s.master == frame:
                del self.subject_entries[s]
                break
        frame.destroy()

    def get_grades(self):
        grades = {}
        for subj, grade in self.subject_entries.items():
            s = subj.get().strip()
            g = grade.get().strip()
            if s and g:
                try:
                    val = float(g)
                    if 0 <= val <= 100:
                        grades[s] = val
                except:
                    pass
        return grades

    def load_sample_data(self):
        if not self.records:
            self.records = [
                {"student_id": "STD-KL-0001", "name": "Mariatu Kamara", "district": "Kailahun", "gender": "Female",
                 "subjects": {"English": 85, "Mathematics": 90, "Science": 78}, "average": 84.33,
                 "status": "🏆 Distinction",
                 "password": hash_password("pass123")},
                {"student_id": "STD-KL-0002", "name": "John Sesay", "district": "Kailahun", "gender": "Male",
                 "subjects": {"English": 65, "Mathematics": 70, "Science": 68}, "average": 67.67, "status": "✅ Pass",
                 "password": hash_password("pass123")},
            ]
            self.status("📚 Sample data loaded")

    def add_student(self):
        name = self.name_entry.get().strip()
        district = self.district_var.get()
        gender = self.gender_var.get()
        grades = self.get_grades()
        student_password = self.student_pwd_entry.get().strip()

        if not name:
            messagebox.showerror("Error", "Enter student name")
            return
        if not grades:
            messagebox.showerror("Error", "Add at least one subject")
            return
        if not student_password:
            messagebox.showerror("Error", "Enter student password")
            return

        for s in self.records:
            if s["name"].lower() == name.lower():
                messagebox.showerror("Error", f"Student '{name}' already exists!")
                return

        avg = calculate_average(grades)
        status = determine_status(avg)
        student_id = generate_user_id("Student", district, len(self.records))

        self.records.append({
            "student_id": student_id,
            "name": name,
            "district": district,
            "gender": gender,
            "subjects": grades,
            "average": avg,
            "status": status,
            "password": hash_password(student_password),
            "date_added": datetime.now().strftime("%Y-%m-%d")
        })

        users = load_users()
        if self.user.get("username"):
            users[self.user["username"]]["students"] = self.records
            save_users(users)

        log_action("ADD_STUDENT", self.user.get("username", "Teacher"), f"Added student: {name}")

        self.refresh_table()
        self.update_stats()
        self.clear_form()
        self.status(f"✅ Added {name} - Avg: {avg:.1f}%")
        messagebox.showinfo("Success",
                            f"Student Added!\n\nName: {name}\nID: {student_id}\nPassword: {student_password}\nAverage: {avg:.1f}%\nStatus: {status}")

    def update_student(self):
        selected = self.tree.selection()
        if not selected:
            messagebox.showerror("Error", "Select a student first")
            return

        old_name = self.tree.item(selected[0])['values'][1]
        name = self.name_entry.get().strip()
        grades = self.get_grades()

        if not name or not grades:
            messagebox.showerror("Error", "Fill all fields")
            return

        avg = calculate_average(grades)
        status = determine_status(avg)

        for s in self.records:
            if s["name"] == old_name:
                s.update({"name": name, "district": self.district_var.get(), "gender": self.gender_var.get(),
                          "subjects": grades, "average": avg, "status": status})
                break

        users = load_users()
        if self.user.get("username"):
            users[self.user["username"]]["students"] = self.records
            save_users(users)

        log_action("UPDATE_STUDENT", self.user.get("username", "Teacher"), f"Updated student: {name}")

        self.refresh_table()
        self.update_stats()
        self.clear_form()
        self.status(f"✅ Updated {name}")
        messagebox.showinfo("Success", f"Updated {name}\nNew Average: {avg:.1f}%")

    def delete_student(self):
        selected = self.tree.selection()
        if not selected:
            messagebox.showerror("Error", "Select a student")
            return

        name = self.tree.item(selected[0])['values'][1]
        if messagebox.askyesno("Confirm", f"Delete {name}?"):
            self.records = [s for s in self.records if s["name"] != name]

            users = load_users()
            if self.user.get("username"):
                users[self.user["username"]]["students"] = self.records
                save_users(users)

            log_action("DELETE_STUDENT", self.user.get("username", "Teacher"), f"Deleted student: {name}")

            self.refresh_table()
            self.update_stats()
            self.clear_form()
            self.status(f"🗑️ Deleted {name}")

    def refresh_table(self):
        for item in self.tree.get_children():
            self.tree.delete(item)

        search = self.search_entry.get().lower()
        for s in self.records:
            if search and search not in s["name"].lower():
                continue

            tag = "dist" if "Distinction" in s["status"] else ("pass" if "Pass" in s["status"] else "fail")
            item = self.tree.insert("", "end", values=(
                s["student_id"], s["name"], s["district"], s["gender"],
                f"{len(s['subjects'])} subj", f"{s['average']:.1f}%", s["status"]
            ))
            self.tree.tag_configure("dist", background="#c8e6c9")
            self.tree.tag_configure("pass", background="#e8f5e9")
            self.tree.tag_configure("fail", background="#ffebee")
            self.tree.item(item, tags=(tag,))

        visible = len([s for s in self.records if not search or search in s["name"].lower()])
        self.status(f"📋 {visible} of {len(self.records)} students")

    def update_stats(self):
        self.stats_text.delete(1.0, tk.END)
        if not self.records:
            self.stats_text.insert(1.0, "No data available. Add students to see statistics!")
            return

        total = len(self.records)
        avg = sum(s["average"] for s in self.records) / total
        passing = len([s for s in self.records if "Pass" in s["status"] or "Distinction" in s["status"]])
        distinct = len([s for s in self.records if "Distinction" in s["status"]])
        girls = len([s for s in self.records if s["gender"] == "Female"])

        stats_text = f"""
╔══════════════════════════════════════════════════════════════════════════╗
║                         📊 CLASS DASHBOARD                               ║
╠══════════════════════════════════════════════════════════════════════════╣
║                                                                          ║
║  📈 TOTAL STUDENTS:      {total:>3}                                                  ║
║  📊 CLASS AVERAGE:       {avg:>6.1f}%                                                    ║
║  ✅ PASS RATE:           {(passing / total) * 100:>6.1f}%  ({passing}/{total} students)                ║
║  🏆 DISTINCTIONS:        {distinct:>3}                                                  ║
║                                                                          ║
║  👥 GENDER BREAKDOWN (SDG 4.5):                                          ║
║     • Girls: {girls}                                                    ║
║     • Boys:  {total - girls}                                                  ║
║                                                                          ║
║  🎯 SDG 4 PROGRESS:                                                      ║
║     Quality Education Target: {avg:.1f}% achieved                                   ║
║     Gender Equity: {'✅ On Track' if abs(girls - (total - girls)) <= 5 else '⚠️ Monitor'}                          ║
║                                                                          ║
╚══════════════════════════════════════════════════════════════════════════╝
        """
        self.stats_text.insert(1.0, stats_text)

    def on_select(self, event):
        selected = self.tree.selection()
        if not selected:
            return

        name = self.tree.item(selected[0])['values'][1]
        for s in self.records:
            if s["name"] == name:
                self.name_entry.delete(0, tk.END)
                self.name_entry.insert(0, s["name"])
                self.district_var.set(s["district"])
                self.gender_var.set(s["gender"])

                for f in self.subj_container.winfo_children():
                    f.destroy()
                self.subject_entries.clear()

                for subj, grade in s["subjects"].items():
                    self.add_subject()
                    for se, ge in self.subject_entries.items():
                        if se.get() == f"Subject {len(self.subject_entries)}":
                            se.delete(0, tk.END)
                            se.insert(0, subj)
                            ge.delete(0, tk.END)
                            ge.insert(0, str(int(grade) if grade == int(grade) else grade))
                            break
                break

    def clear_form(self):
        self.name_entry.delete(0, tk.END)
        self.district_var.set("Kailahun")
        self.gender_var.set("Female")
        self.student_pwd_entry.delete(0, tk.END)
        self.student_pwd_entry.insert(0, "pass123")

        for f in self.subj_container.winfo_children():
            f.destroy()
        self.subject_entries.clear()

        for _ in range(3):
            self.add_subject()

        self.status("🗑️ Form cleared")

    def save_data(self):
        if not self.records:
            messagebox.showwarning("No Data", "Nothing to save")
            return
        f = filedialog.asksaveasfilename(defaultextension=".json", filetypes=[("JSON", "*.json")])
        if f:
            with open(f, 'w') as file:
                json.dump(self.records, file, indent=4)
            self.status(f"💾 Saved to {os.path.basename(f)}")
            messagebox.showinfo("Success", f"Saved {len(self.records)} records")

    def load_data(self):
        f = filedialog.askopenfilename(filetypes=[("JSON", "*.json")])
        if f:
            with open(f, 'r') as file:
                self.records = json.load(file)
            self.refresh_table()
            self.update_stats()
            self.status(f"📂 Loaded {len(self.records)} records")
            messagebox.showinfo("Success", f"Loaded {len(self.records)} records")

    def export_csv(self):
        if not self.records:
            messagebox.showwarning("No Data", "Nothing to export")
            return
        f = filedialog.asksaveasfilename(defaultextension=".csv", filetypes=[("CSV", "*.csv")])
        if f:
            import csv
            with open(f, 'w', newline='', encoding='utf-8-sig') as file:
                w = csv.writer(file)
                w.writerow(["Student ID", "Name", "District", "Gender", "Subjects", "Average", "Status", "Date Added"])
                for s in self.records:
                    subs = ", ".join([f"{k}:{v}" for k, v in s["subjects"].items()])
                    w.writerow([s["student_id"], s["name"], s["district"], s["gender"], subs, f"{s['average']:.1f}%",
                                s["status"], s.get("date_added", "")])
            self.status(f"📊 Exported to CSV")
            messagebox.showinfo("Success", f"Exported {len(self.records)} records")

    def logout(self):
        if messagebox.askyesno("Logout", "Are you sure you want to logout?"):
            log_action("LOGOUT", self.user.get("username", "User"), "User logged out")
            self.root.destroy()
            login = LoginWindow()
            login.root.mainloop()

    def status(self, msg):
        self.status_bar.config(text=f" {datetime.now().strftime('%H:%M:%S')} | {msg}")


# ============================================================================
# LOGIN WINDOW
# ============================================================================

class LoginWindow:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title(f"Login - {APP_NAME}")
        self.root.geometry("650x750")
        self.root.configure(bg='#f0f4f8')
        self.root.resizable(False, False)

        self.role_var = tk.StringVar(value="Admin")

        self.setup_ui()
        self.center_window()

    def center_window(self):
        self.root.update_idletasks()
        x = (self.root.winfo_screenwidth() // 2) - 325
        y = (self.root.winfo_screenheight() // 2) - 375
        self.root.geometry(f'650x750+{x}+{y}')

    def setup_ui(self):
        header = tk.Frame(self.root, bg='#e63946', height=120)
        header.pack(fill='x')

        tk.Label(header, text=SDG_TAG, bg='#e63946', fg='white',
                 font=('Arial', 16, 'bold')).pack(pady=(25, 5))
        tk.Label(header, text="Student Academic Portal", bg='#e63946', fg='white',
                 font=('Arial', 13)).pack()

        main = tk.Frame(self.root, bg='#f0f4f8')
        main.pack(fill='both', expand=True, padx=50, pady=30)

        tk.Label(main, text="Select Role:", bg='#f0f4f8',
                 font=('Arial', 13, 'bold')).pack(anchor='w')

        role_frame = tk.Frame(main, bg='#f0f4f8')
        role_frame.pack(fill='x', pady=10)

        roles = [("👩‍🏫 Teacher", "Teacher"), ("👔 Principal", "Principal"),
                 ("👑 Admin", "Admin"), ("👨‍🎓 Student", "Student")]

        for text, value in roles:
            tk.Radiobutton(role_frame, text=text, variable=self.role_var,
                           value=value, bg='#f0f4f8', font=('Arial', 12)).pack(side='left', padx=20)

        tk.Label(main, text="Username:", bg='#f0f4f8', font=('Arial', 12)).pack(anchor='w', pady=(25, 8))
        self.username_entry = tk.Entry(main, font=('Arial', 13), width=35, relief=tk.GROOVE, bd=2)
        self.username_entry.pack(fill='x', pady=5, ipady=8)
        self.username_entry.insert(0, "admin")

        tk.Label(main, text="Password:", bg='#f0f4f8', font=('Arial', 12)).pack(anchor='w', pady=(15, 8))
        self.password_entry = tk.Entry(main, font=('Arial', 13), width=35, show="•", relief=tk.GROOVE, bd=2)
        self.password_entry.pack(fill='x', pady=5, ipady=8)
        self.password_entry.insert(0, "admin123")

        self.show_var = tk.BooleanVar()
        tk.Checkbutton(main, text="Show Password", variable=self.show_var,
                       command=self.toggle_password, bg='#f0f4f8', font=('Arial', 11)).pack(anchor='w', pady=10)

        tk.Button(main, text="🔓 LOGIN", command=self.login,
                  bg='#4CAF50', fg='white', font=('Arial', 14, 'bold'),
                  height=1, width=25, pady=12).pack(pady=20)

        sep = tk.Frame(main, height=2, bg='#cccccc')
        sep.pack(fill='x', pady=20)

        tk.Label(main, text="📝 DON'T HAVE AN ACCOUNT?", bg='#f0f4f8',
                 font=('Arial', 12, 'bold')).pack()

        signup_frame = tk.Frame(main, bg='#f0f4f8')
        signup_frame.pack(pady=15)

        tk.Button(signup_frame, text="👨‍🎓 Student Signup", command=lambda: StudentSignupWindow(self),
                  bg='#4CAF50', fg='white', font=('Arial', 11, 'bold'), width=18, pady=8).pack(side='left', padx=8)
        tk.Button(signup_frame, text="👩‍🏫 Teacher Signup", command=lambda: TeacherSignupWindow(self),
                  bg='#2196F3', fg='white', font=('Arial', 11, 'bold'), width=18, pady=8).pack(side='left', padx=8)
        tk.Button(signup_frame, text="👔 Principal Signup", command=lambda: PrincipalSignupWindow(self),
                  bg='#FF9800', fg='white', font=('Arial', 11, 'bold'), width=18, pady=8).pack(side='left', padx=8)

        info = tk.Frame(main, bg='#e8f0fe', relief=tk.GROOVE, bd=1)
        info.pack(fill='x', pady=20)

        tk.Label(info, text="📋 Default Login Credentials:",
                 bg='#e8f0fe', font=('Arial', 12, 'bold')).pack(anchor='w', padx=15, pady=(12, 5))
        tk.Label(info, text="👑 Admin:      admin / admin123",
                 bg='#e8f0fe', font=('Arial', 11)).pack(anchor='w', padx=15)
        tk.Label(info, text="👩‍🏫 Teacher:    teacher1 / teacher123",
                 bg='#e8f0fe', font=('Arial', 11)).pack(anchor='w', padx=15)
        tk.Label(info, text="👔 Principal:  principal1 / principal123",
                 bg='#e8f0fe', font=('Arial', 11)).pack(anchor='w', padx=15, pady=(0, 12))

        self.root.bind('<Return>', lambda e: self.login())

    def toggle_password(self):
        if self.show_var.get():
            self.password_entry.config(show="")
        else:
            self.password_entry.config(show="•")

    def login(self):
        username = self.username_entry.get().strip()
        password = self.password_entry.get().strip()
        role = self.role_var.get()

        if not username or not password:
            messagebox.showerror("Error", "Please enter username and password")
            return

        users = load_users()
        pending = load_pending()

        if username not in users:
            if username in pending:
                messagebox.showerror("Error",
                                     f"Your account is pending approval.\n\nPlease wait for Admin to approve your account.")
            else:
                messagebox.showerror("Error", f"Username '{username}' not found!\n\nPlease sign up first.")
            return

        user = users[username]
                               
        if user["password"] != hash_password(password):
            messagebox.showerror("Error", "Incorrect password!")
            return

        if user.get("status") != "approved":
            messagebox.showerror("Error",
                                 f"Your account is {user.get('status', 'pending')}.\n\nPlease wait for Admin approval.")
            return

        if user["role"] != role:
            messagebox.showerror("Error", f"This account                                                                                  is a {user['role']}, not a {role}.")
            return

        log_action("LOGIN", username, f"Successful login as {role}")
        self.root.destroy()

        if role == "Admin":
            AdminDashboard(user)
        elif role == "Student":
            student = None
            for username, user_data in users.items():
                if user_data.get("role") in ["Teacher", "Principal"]:
                    for stud in user_data.get("students", []):
                        if stud.get("student_id") == username or stud.get("name") == user.get("full_name"):
                            student = stud
                            break
                if student:
                    break

            if student:
                StudentGradeViewer(student)
            else:
                messagebox.showinfo("Info",
                                    "No grade records found. Please contact your teacher.\n\nUse Student ID and password 'pass123' to login.")
        else:
            main_root = tk.Tk()
            app = MainApplication(main_root, user)
            main_root.mainloop()


# ============================================================================
# RUN THE PROGRAM
# ============================================================================

if __name__ == "__main__":
    print("=" * 65)
    print("   STUDENT ACADEMIC PORTAL - SIERRA LEONE")
    print("   SDG 4: Quality Education for All")
    print("=" * 65)
    print("\n📋 DEFAULT LOGIN CREDENTIALS:")
    print("   👑 Admin:      admin / admin123")
    print("   👩‍🏫 Teacher:    teacher1 / teacher123")
    print("   👔 Principal:  principal1 / principal123")
    print("\n💡 STUDENT LOGIN:")
    print("   Use Student ID (e.g., STD-KL-0001) and password 'pass123'")
    print("\n📥 CSV IMPORT FORMAT:")
    print("   Columns: Name, District, Gender, Password, Subject_English, Subject_Mathematics, etc.")
    print("\n" + "=" * 65)
    print("   Starting Application...")
    print("=" * 65 + "\n")

    os.makedirs("data", exist_ok=True)

    login = LoginWindow()
    login.root.mainloop()