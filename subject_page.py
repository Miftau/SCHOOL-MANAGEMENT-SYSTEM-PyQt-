from PyQt5.QtWidgets import QWidget, QVBoxLayout, QLabel, QLineEdit, QPushButton, QListWidget, QMessageBox

class SubjectPage(QWidget):
    def __init__(self):
        super().__init__()
        self.subjects = []

        self.layout = QVBoxLayout()
        self.subject_input = QLineEdit()
        self.subject_input.setPlaceholderText("Enter subject name")

        self.add_btn = QPushButton("Add Subject")
        self.add_btn.clicked.connect(self.add_subject)

        self.list_widget = QListWidget()

        self.layout.addWidget(QLabel("Add / View Subjects"))
        self.layout.addWidget(self.subject_input)
        self.layout.addWidget(self.add_btn)
        self.layout.addWidget(self.list_widget)
        self.setLayout(self.layout)

    def add_subject(self):
        subject = self.subject_input.text().strip()
        if subject and subject not in self.subjects:
            self.subjects.append(subject)
            self.list_widget.addItem(subject)
            self.subject_input.clear()
        else:
            QMessageBox.warning(self, "Input Error", "Subject name is invalid or already exists.")
