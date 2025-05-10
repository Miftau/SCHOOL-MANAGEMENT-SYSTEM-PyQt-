from PyQt5.QtWidgets import QVBoxLayout, QFormLayout, QLineEdit, QPushButton, QMessageBox, QDialog
from admin_dashboard import AdminDashboard
from teacher_dashboard import TeacherDashboard
from student_dashboard import StudentDashboard
from sign_up import SignUpWindow
import requests
import json


class LoginWindow(QDialog):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Login")
        self.resize(600, 800)

        self.layout = QVBoxLayout()
        self.form_layout = QFormLayout()

        self.username_field = QLineEdit()
        self.password_field = QLineEdit()
        self.password_field.setEchoMode(QLineEdit.Password)

        self.form_layout.addRow("Username:", self.username_field)
        self.form_layout.addRow("Password:", self.password_field)

        self.layout.addLayout(self.form_layout)

        self.login_button = QPushButton("Login")
        self.login_button.clicked.connect(self.login_user)
        self.layout.addWidget(self.login_button)

        self.signup_button = QPushButton("Don't have an account? Sign Up")
        self.signup_button.clicked.connect(self.open_signup_window)
        self.layout.addWidget(self.signup_button)

        self.setLayout(self.layout)

    def login_user(self):
        username = self.username_field.text().strip()
        password = self.password_field.text()

        if not username or not password:
            self.show_message("Error", "Both fields are required.")
            return

        try:
            response = requests.post(
                "http://127.0.0.1:5000/login",
                headers={"Content-Type": "application/json"},
                data=json.dumps({"username": username, "password": password})
            )

            data = response.json()
            if response.status_code == 200:
                self.show_message("Success", "Login successful!")
                role = data.get("role")
                self.user_data = {"username": username, "role": role}
                self.accept()

                if role == "Admin":
                    self.admin_dashboard = AdminDashboard(self.user_data)
                    self.admin_dashboard.show()
                elif role == "Teacher":
                    self.teacher_dashboard = TeacherDashboard(self.user_data)
                    self.teacher_dashboard.show()
                elif role == "Student":
                    self.student_dashboard = StudentDashboard(self.user_data)
                    self.student_dashboard.show()
            else:
                self.show_message("Login Failed", data.get("message", "Invalid credentials."))
        except requests.exceptions.RequestException as e:
            self.show_message("Network Error", f"Could not connect to server.\n{e}")

    def open_signup_window(self):
        self.signup_window = SignUpWindow()
        self.signup_window.exec_()

    def show_message(self, title, message):
        msg = QMessageBox()
        msg.setWindowTitle(title)
        msg.setText(message)
        msg.exec_()
