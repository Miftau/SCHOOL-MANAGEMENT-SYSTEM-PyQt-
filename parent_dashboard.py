from PyQt5.QtWidgets import QWidget, QVBoxLayout, QLabel, QTableWidget, QTableWidgetItem, QPushButton
import sqlite3

class ParentDashboard(QWidget):
    def __init__(self, user_data):
        super().__init__()
        self.user_data = user_data
        self.parent_username = user_data.get("username")

        self.setWindowTitle("Parent Dashboard")
        self.setGeometry(100, 100, 700, 500)

        self.layout = QVBoxLayout()

        self.title = QLabel(f"Welcome, {self.parent_username}")
        self.layout.addWidget(self.title)

        self.children_label = QLabel("Your Children's Progress:")
        self.layout.addWidget(self.children_label)

        # Table to display child's progress
        self.table = QTableWidget()
        self.table.setColumnCount(4)
        self.table.setHorizontalHeaderLabels(["Student", "Subject", "Grade", "Attendance (%)"])
        self.layout.addWidget(self.table)

        # Button to load progress
        self.load_button = QPushButton("Load Progress")
        self.load_button.clicked.connect(self.load_progress)
        self.layout.addWidget(self.load_button)

        self.setLayout(self.layout)

    def load_progress(self):
        conn = sqlite3.connect("school_management.db")
        cursor = conn.cursor()

        # Get list of children for this parent
        cursor.execute("SELECT student_username FROM parent_student WHERE parent_username = ?", (self.parent_username,))
        children = cursor.fetchall()

        all_progress = []
        for child in children:
            child_username = child[0]
            cursor.execute("SELECT student_username, subject, grade, attendance_percentage FROM child_progress WHERE student_username = ?", (child_username,))
            progress = cursor.fetchall()
            all_progress.extend(progress)

        self.table.setRowCount(len(all_progress))

        for row_idx, row_data in enumerate(all_progress):
            for col_idx, value in enumerate(row_data):
                self.table.setItem(row_idx, col_idx, QTableWidgetItem(str(value)))

        conn.close()
