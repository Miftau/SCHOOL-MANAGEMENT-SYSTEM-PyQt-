from PyQt5.QtWidgets import QWidget, QVBoxLayout, QLabel, QLineEdit, QPushButton, QListWidget, QMessageBox

class TeachersPage(QWidget):
    def __init__(self):
        super().__init__()
        self.teachers = []

        self.layout = QVBoxLayout()
        self.name_input = QLineEdit()
        self.name_input.setPlaceholderText("Enter teacher name")

        self.add_btn = QPushButton("Add Teacher")
        self.add_btn.clicked.connect(self.add_teacher)

        self.list_widget = QListWidget()

        self.layout.addWidget(QLabel("Add / View Teachers"))
        self.layout.addWidget(self.name_input)
        self.layout.addWidget(self.add_btn)
        self.layout.addWidget(self.list_widget)
        self.setLayout(self.layout)

    def add_teacher(self):
        name = self.name_input.text().strip()
        if name:
            self.teachers.append(name)
            self.list_widget.addItem(name)
            self.name_input.clear()
        else:
            QMessageBox.warning(self, "Input Error", "Teacher name cannot be empty.")
