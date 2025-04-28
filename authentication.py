from PyQt5.QtWidgets import QWidget, QVBoxLayout, QFormLayout, QLabel, QLineEdit, QPushButton, QMessageBox, QDialog
from PyQt5.QtCore import Qt
from admin_dashboard import AdminDashboard
from sign_up import SignUpWindow
from teacher_dashboard import TeacherDashboard
from student_dashboard import StudentDashboard
import sqlite3

class LoginWindow(QDialog):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Login")
        self.resize(600, 800)

        self.layout = QVBoxLayout()

        # Form Layout
        self.form_layout = QFormLayout()

        # Add fields
        self.username_field = QLineEdit(self)
        self.password_field = QLineEdit(self)
        self.password_field.setEchoMode(QLineEdit.Password)

        self.form_layout.addRow("Username:", self.username_field)
        self.form_layout.addRow("Password:", self.password_field)

        self.layout.addLayout(self.form_layout)

        # Login Button
        self.login_button = QPushButton("Login", self)
        self.login_button.clicked.connect(self.login_user)
        self.layout.addWidget(self.login_button)

        # SignUp Button
        self.signup_button = QPushButton("Don't have an account? Sign Up", self)
        self.signup_button.clicked.connect(self.open_signup_window)
        self.layout.addWidget(self.signup_button)

        self.setLayout(self.layout)

    def login_user(self):
        # Get values from form
        username = self.username_field.text()
        password = self.password_field.text()

        # Validate and check if the username exists in DB
        if not username or not password:
            self.show_message("Error", "Both fields are required.")
            return

        # Check credentials in the database
        user_id, role = self.check_credentials(username, password)
        if user_id:
            self.show_message("Success", "Login successful!")
            # Navigate to the appropriate dashboard based on the role
            self.close()
            if role == "Admin":
                self.admin_dashboard = AdminDashboard()
                self.admin_dashboard.show()
            elif role == "Teacher":
                self.teacher_dashboard = TeacherDashboard()
                self.teacher_dashboard.show()
            elif role == "Student":
                self.student_dashboard = StudentDashboard()
                self.student_dashboard.show()
        else:
            self.show_message("Error", "Invalid credentials.")

    def check_credentials(self, username, password):
        # Connect to SQLite DB (you can replace with actual DB logic)
        conn = sqlite3.connect('school_management.db')
        cursor = conn.cursor()

        cursor.execute("SELECT * FROM users WHERE username = ? AND password = ?", (username, password))
        user = cursor.fetchone()

        conn.close()
        if user:
            return user[0], user[4]  # Return user_id and role
        return None, None

    def open_signup_window(self):
        self.signup_window = SignUpWindow()  # Open SignUp Window for new user
        self.signup_window.show()

    def show_message(self, title, message):
        msg = QMessageBox()
        msg.setWindowTitle(title)
        msg.setText(message)
        msg.exec_()