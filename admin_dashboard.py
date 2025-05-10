from PyQt5.QtWidgets import QWidget, QVBoxLayout, QLabel, QPushButton, QTableWidget, QTableWidgetItem, QHBoxLayout
from PyQt5.QtCore import Qt
import sqlite3
from add_user_dialog import AddUserDialog

class AdminDashboard(QWidget):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Admin Dashboard")
        self.setGeometry(100, 100, 600, 400)

        self.layout = QVBoxLayout()

        # Title Label
        self.title_label = QLabel("Admin Dashboard")
        self.layout.addWidget(self.title_label)

        # Create a Table to list users
        self.table = QTableWidget(self)
        self.table.setColumnCount(4)  # Columns: Username, Email, Role, Action
        self.table.setHorizontalHeaderLabels(["Username", "Email", "Role", "Action"])
        self.layout.addWidget(self.table)

        # Load Users Button
        self.load_users_button = QPushButton("Load Users", self)
        self.load_users_button.clicked.connect(self.load_users)
        self.layout.addWidget(self.load_users_button)

        # Logout Button
        self.logout_button = QPushButton("Logout", self)
        self.logout_button.clicked.connect(self.logout)
        self.layout.addWidget(self.logout_button)

        self.setLayout(self.layout)

    def open_add_user_dialog(self):
        self.add_user_btn = QPushButton("Add New User")
        self.add_user_btn.clicked.connect(self.open_add_user_dialog)
        dialog = AddUserDialog()
        dialog.exec_()


    def load_users(self):
        # Connect to the database
        conn = sqlite3.connect('school_management.db')
        cursor = conn.cursor()

        # Fetch all users from the database
        cursor.execute("SELECT * FROM users")
        users = cursor.fetchall()

        # Fill the table with data
        self.table.setRowCount(len(users))
        for i, user in enumerate(users):
            self.table.setItem(i, 0, QTableWidgetItem(user[1]))  # Username
            self.table.setItem(i, 1, QTableWidgetItem(user[2]))  # Email
            self.table.setItem(i, 2, QTableWidgetItem(user[4]))  # Role
            self.table.setItem(i, 3, QTableWidgetItem("Manage"))  # Action

        conn.close()

    def logout(self):
        self.close()

