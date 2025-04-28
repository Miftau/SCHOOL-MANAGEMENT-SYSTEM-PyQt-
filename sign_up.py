from PyQt5.QtWidgets import QWidget, QVBoxLayout, QLabel, QLineEdit, QPushButton, QFormLayout, QMessageBox, QDialog
from PyQt5.QtCore import Qt
import sqlite3


class SignUpWindow(QDialog):
    def __init__(self, user_id=None):
        super().__init__()

        self.setWindowTitle("Sign Up / Update")
        self.resize(800, 700)

        self.layout = QVBoxLayout()

        # Form Layout
        self.form_layout = QFormLayout()

        # Add fields
        self.username_field = QLineEdit(self)
        self.email_field = QLineEdit(self)
        self.password_field = QLineEdit(self)
        self.password_field.setEchoMode(QLineEdit.Password)
        self.confirm_password_field = QLineEdit(self)
        self.confirm_password_field.setEchoMode(QLineEdit.Password)
        self.role_field = QLineEdit(self)

        self.form_layout.addRow("Username:", self.username_field)
        self.form_layout.addRow("Email:", self.email_field)
        self.form_layout.addRow("Password:", self.password_field)
        self.form_layout.addRow("Confirm Password:", self.confirm_password_field)
        self.form_layout.addRow("Role (Admin/Teacher/Student):", self.role_field)

        self.layout.addLayout(self.form_layout)

        # SignUp/Update Button
        self.signup_button = QPushButton("Sign Up", self)
        self.signup_button.clicked.connect(self.signup_or_update_user)
        self.layout.addWidget(self.signup_button)

        self.setLayout(self.layout)

        # If user_id is provided, it's for updating existing user
        self.user_id = user_id
        if self.user_id:
            self.load_user_data()

    def load_user_data(self):
        # Load existing user data for update
        conn = sqlite3.connect('school_management.db')
        cursor = conn.cursor()

        cursor.execute("SELECT * FROM users WHERE id = ?", (self.user_id,))
        user = cursor.fetchone()

        if user:
            self.username_field.setText(user[1])  # username
            self.email_field.setText(user[2])  # email
            self.password_field.setText(user[3])  # password
            self.confirm_password_field.setText(user[3])  # confirm password
            self.role_field.setText(user[4])  # role

        conn.close()

        # Change button text to 'Update'
        self.signup_button.setText("Update")

    def signup_or_update_user(self):
        # Get values from form
        username = self.username_field.text()
        email = self.email_field.text()
        password = self.password_field.text()
        confirm_password = self.confirm_password_field.text()
        role = self.role_field.text()

        # Validation
        if not username or not email or not password or not confirm_password or not role:
            self.show_message("Error", "All fields are required.")
            return

        if password != confirm_password:
            self.show_message("Error", "Passwords do not match.")
            return

        if not self.is_valid_email(email):
            self.show_message("Error", "Invalid email format.")
            return

        if self.user_id:  # If user exists, update their data
            self.update_user_in_db(username, email, password, role)
        else:  # If no user_id, sign up new user
            self.save_user_to_db(username, email, password, role)

        # After successful operation, show success message
        self.show_message("Success", "Operation successful!")

        # Close SignUp window
        self.close()

    def is_valid_email(self, email):
        return "@" in email and "." in email  # Simple email validation

    def save_user_to_db(self, username, email, password, role):
        # Connect to SQLite DB (you can replace with actual DB logic)
        conn = sqlite3.connect('school_management.db')
        cursor = conn.cursor()

        # Create the user table if not exists
        cursor.execute('''CREATE TABLE IF NOT EXISTS users
                          (
                              id
                              INTEGER
                              PRIMARY
                              KEY
                              AUTOINCREMENT,
                              username
                              TEXT
                              NOT
                              NULL,
                              email
                              TEXT
                              NOT
                              NULL,
                              password
                              TEXT
                              NOT
                              NULL,
                              role
                              TEXT
                              NOT
                              NULL
                          )''')

        # Insert new user into the users table
        cursor.execute("INSERT INTO users (username, email, password, role) VALUES (?, ?, ?, ?)",
                       (username, email, password, role))

        # Commit and close connection
        conn.commit()
        conn.close()

    def update_user_in_db(self, username, email, password, role):
        # Update existing user in the database
        conn = sqlite3.connect('school_management.db')
        cursor = conn.cursor()

        cursor.execute("UPDATE users SET username = ?, email = ?, password = ?, role = ? WHERE id = ?",
                       (username, email, password, role, self.user_id))

        # Commit and close connection
        conn.commit()
        conn.close()

    def show_message(self, title, message):
        msg = QMessageBox()
        msg.setWindowTitle(title)
        msg.setText(message)
        msg.exec_()
