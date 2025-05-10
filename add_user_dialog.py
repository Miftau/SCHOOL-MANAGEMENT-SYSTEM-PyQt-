from PyQt5.QtWidgets import QDialog, QVBoxLayout, QLabel, QLineEdit, QPushButton, QComboBox, QMessageBox
import requests

class AddUserDialog(QDialog):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Add New User")
        self.setMinimumWidth(300)

        layout = QVBoxLayout()

        self.username_input = QLineEdit()
        self.username_input.setPlaceholderText("Username")

        self.email_input = QLineEdit()
        self.email_input.setPlaceholderText("Email")

        self.password_input = QLineEdit()
        self.password_input.setPlaceholderText("Password")
        self.password_input.setEchoMode(QLineEdit.Password)

        self.role_combo = QComboBox()
        self.role_combo.addItems(["Admin", "Teacher", "Student", "Parent"])

        self.add_button = QPushButton("Add User")
        self.add_button.clicked.connect(self.add_user)

        layout.addWidget(QLabel("Username"))
        layout.addWidget(self.username_input)
        layout.addWidget(QLabel("Email"))
        layout.addWidget(self.email_input)
        layout.addWidget(QLabel("Password"))
        layout.addWidget(self.password_input)
        layout.addWidget(QLabel("Role"))
        layout.addWidget(self.role_combo)
        layout.addWidget(self.add_button)

        self.setLayout(layout)

    def add_user(self):
        user_data = {
            "username": self.username_input.text(),
            "email": self.email_input.text(),
            "password": self.password_input.text(),
            "role": self.role_combo.currentText()
        }

        if not all(user_data.values()):
            QMessageBox.warning(self, "Error", "All fields are required.")
            return

        try:
            response = requests.post("http://127.0.0.1:5000/signup", json=user_data)
            if response.status_code == 201:
                QMessageBox.information(self, "Success", "User added successfully.")
                self.accept()
            else:
                QMessageBox.critical(self, "Error", response.json().get("message", "Unknown error"))
        except Exception as e:
            QMessageBox.critical(self, "Error", f"Failed to connect to backend.\n{str(e)}")
