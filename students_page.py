from PyQt5.QtWidgets import QWidget, QVBoxLayout, QLabel, QLineEdit, QPushButton, QListWidget, QMessageBox

class StudentsPage(QWidget):
    def __init__(self):
        super().__init__()
        self.students = []

        self.layout = QVBoxLayout()
        self.name_input = QLineEdit()
        self.name_input.setPlaceholderText("Enter student name")

        self.add_btn = QPushButton("Add Student")
        self.add_btn.clicked.connect(self.add_student)

        self.list_widget = QListWidget()

        self.layout.addWidget(QLabel("Add / View Students"))
        self.layout.addWidget(self.name_input)
        self.layout.addWidget(self.add_btn)
        self.layout.addWidget(self.list_widget)
        self.setLayout(self.layout)

    def add_student(self):
        name = self.name_input.text().strip()
        if name:
            self.students.append(name)
            self.list_widget.addItem(name)
            self.name_input.clear()
        else:
            QMessageBox.warning(self, "Input Error", "Student name cannot be empty.")
