import bcrypt
from PyQt5.QtWidgets import (
    QVBoxLayout, QLineEdit, QPushButton, QFormLayout,
    QMessageBox, QDialog, QComboBox
)
import requests
import json
import sqlite3
import os
from config import DB_PATH


def get_connection():
    return sqlite3.connect(DB_PATH)

class SignUpWindow(QDialog):
    def __init__(self, user_id=None):
        super().__init__()
        self.setWindowTitle("Sign Up / Update")
        self.resize(800, 700)
        self.user_id = user_id

        self.layout = QVBoxLayout()
        self.form_layout = QFormLayout()

        self.username_field = QLineEdit()
        self.email_field = QLineEdit()
        self.password_field = QLineEdit()
        self.password_field.setEchoMode(QLineEdit.Password)
        self.confirm_password_field = QLineEdit()
        self.confirm_password_field.setEchoMode(QLineEdit.Password)
        self.role_field = QComboBox()

        self.role_field.addItems(["Admin", "Teacher", "Student", "Parent"])

        self.form_layout.addRow("Username:", self.username_field)
        self.form_layout.addRow("Email:", self.email_field)
        self.form_layout.addRow("Password:", self.password_field)
        self.form_layout.addRow("Confirm Password:", self.confirm_password_field)
        self.form_layout.addRow("Role:", self.role_field)

        self.layout.addLayout(self.form_layout)

        self.signup_button = QPushButton("Sign Up")
        self.signup_button.clicked.connect(self.signup_or_update_user)
        self.layout.addWidget(self.signup_button)

        self.setLayout(self.layout)

        if self.user_id:
            self.load_user_data()

    def load_user_data(self):
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM users WHERE id = ?", (self.user_id,))
        user = cursor.fetchone()
        conn.close()

        if user:
            self.username_field.setText(user[1])
            self.email_field.setText(user[2])
            self.password_field.setText("")
            self.confirm_password_field.setText("")
            self.role_field.setCurrentText(user[4].capitalize())
            self.signup_button.setText("Update")

    def signup_or_update_user(self):
        username = self.username_field.text().strip()
        email = self.email_field.text().strip()
        password = self.password_field.text()
        confirm_password = self.confirm_password_field.text()
        role = self.role_field.currentText().strip().lower()

        if not all([username, email, password, confirm_password, role]):
            self.show_message("Error", "All fields are required.")
            return

        if password != confirm_password:
            self.show_message("Error", "Passwords do not match.")
            return

        if not self.is_valid_email(email):
            self.show_message("Error", "Invalid email format.")
            return

        hashed_password = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')

        use_remote = False

        if self.user_id:
            if use_remote:
                self.update_user_remote(username, email, hashed_password, role)
            else:
                self.update_user_in_db(username, email, hashed_password, role)
        else:
            if self.user_exists(username, email):
                self.show_message("Error", "Username or Email already exists.")
                return

            if use_remote:
                self.signup_user_remote(username, email, hashed_password, role)
            else:
                self.save_user_to_db(username, email, hashed_password, role)
                self.show_message("Success", "User created successfully.")
                self.close()

    def save_user_to_db(self, username, email, hashed_password, role):
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute("INSERT INTO users (username, email, password, role) VALUES (?, ?, ?, ?)",
                       (username, email, hashed_password, role))
        conn.commit()
        conn.close()

    def update_user_in_db(self, username, email, hashed_password, role):
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute("UPDATE users SET username=?, email=?, password=?, role=? WHERE id=?",
                       (username, email, hashed_password, role, self.user_id))
        conn.commit()
        conn.close()
        self.show_message("Success", "User updated successfully.")
        self.close()

    def user_exists(self, username, email):
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT id FROM users WHERE username=? OR email=?", (username, email))
        exists = cursor.fetchone() is not None
        conn.close()
        return exists

    def is_valid_email(self, email):
        return "@" in email and "." in email

    def signup_user_remote(self, username, email, password, role):
        try:
            response = requests.post("http://127.0.0.1:5000/signup",
                                     headers={"Content-Type": "application/json"},
                                     data=json.dumps({
                                         "username": username,
                                         "email": email,
                                         "password": password,
                                         "role": role
                                     }))
            if response.status_code == 201:
                self.show_message("Success", "User created successfully.")
                self.close()
            else:
                self.show_message("Error", response.json().get("message", "Failed to register user."))
        except requests.exceptions.RequestException as e:
            self.show_message("Network Error", str(e))

    def update_user_remote(self, username, email, password, role):
        try:
            response = requests.put(f"http://127.0.0.1:5000/update_user/{self.user_id}",
                                    headers={"Content-Type": "application/json"},
                                    data=json.dumps({
                                        "username": username,
                                        "email": email,
                                        "password": password,
                                        "role": role
                                    }))
            if response.status_code == 200:
                self.show_message("Success", "User updated successfully.")
                self.close()
            else:
                self.show_message("Error", response.json().get("message", "Failed to update user."))
        except requests.exceptions.RequestException as e:
            self.show_message("Network Error", str(e))

    def show_message(self, title, message):
        msg = QMessageBox()
        msg.setWindowTitle(title)
        msg.setText(message)
        msg.exec_()
