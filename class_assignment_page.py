from PyQt5.QtWidgets import QWidget, QVBoxLayout, QLabel, QLineEdit, QPushButton, QComboBox, QListWidget, QMessageBox

class ClassAssignmentPage(QWidget):
    def __init__(self, teachers_page):
        super().__init__()
        self.teachers_page = teachers_page
        self.class_assignments = []

        self.layout = QVBoxLayout()

        self.class_input = QLineEdit()
        self.class_input.setPlaceholderText("Enter class name")

        self.teacher_dropdown = QComboBox()
        self.refresh_teachers()

        self.assign_btn = QPushButton("Assign Teacher to Class")
        self.assign_btn.clicked.connect(self.assign_class)

        self.list_widget = QListWidget()

        self.layout.addWidget(QLabel("Class & Teacher Assignment"))
        self.layout.addWidget(self.class_input)
        self.layout.addWidget(self.teacher_dropdown)
        self.layout.addWidget(self.assign_btn)
        self.layout.addWidget(QLabel("Assignments:"))
        self.layout.addWidget(self.list_widget)
        self.setLayout(self.layout)

    def refresh_teachers(self):
        self.teacher_dropdown.clear()
        for teacher in self.teachers_page.teachers:
            self.teacher_dropdown.addItem(teacher)

    def assign_class(self):
        class_name = self.class_input.text().strip()
        teacher = self.teacher_dropdown.currentText()

        if class_name and teacher:
            assignment = f"{class_name} - {teacher}"
            self.class_assignments.append(assignment)
            self.list_widget.addItem(assignment)
            self.class_input.clear()
        else:
            QMessageBox.warning(self, "Input Error", "Please enter a class name and select a teacher.")
