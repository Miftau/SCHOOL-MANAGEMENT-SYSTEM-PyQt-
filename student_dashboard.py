from PyQt5.QtWidgets import *

class StudentDashboard(QWidget):
    def __init__(self, student_name, enrolled_classes, student_grades):
        super().__init__()
        self.student_name = student_name
        self.enrolled_classes = enrolled_classes  # List of classes student is enrolled in
        self.student_grades = student_grades  # Dict of grades (student, subject, grade)

        self.layout = QVBoxLayout()
        self.setLayout(self.layout)

        self.layout.addWidget(QLabel(f"Welcome, {self.student_name}"))

        self.class_dropdown = QComboBox()
        self.class_dropdown.addItems(self.enrolled_classes)
        self.layout.addWidget(self.class_dropdown)

        self.subject_dropdown = QComboBox()
        self.layout.addWidget(self.subject_dropdown)

        self.view_grades_btn = QPushButton("View Grades")
        self.view_grades_btn.clicked.connect(self.view_grades)
        self.layout.addWidget(self.view_grades_btn)

        self.attendance_list = QListWidget()
        self.layout.addWidget(QLabel("Attendance:"))
        self.layout.addWidget(self.attendance_list)

        self.grades_list = QListWidget()
        self.layout.addWidget(QLabel("Grades:"))
        self.layout.addWidget(self.grades_list)

        self.view_attendance_btn = QPushButton("View Attendance")
        self.view_attendance_btn.clicked.connect(self.view_attendance)
        self.layout.addWidget(self.view_attendance_btn)

        self.load_subjects()

    def load_subjects(self):
        # Load the subjects based on the class selected
        selected_class = self.class_dropdown.currentText()
        if selected_class:
            self.subject_dropdown.clear()
            subjects = [f"Subject {i+1}" for i in range(5)]  # Replace with actual subject list from data
            self.subject_dropdown.addItems(subjects)

    def view_grades(self):
        self.grades_list.clear()
        selected_class = self.class_dropdown.currentText()
        selected_subject = self.subject_dropdown.currentText()

        if selected_class and selected_subject:
            for student, subject, grade in self.student_grades:
                if student == self.student_name and subject == selected_subject:
                    self.grades_list.addItem(f"Grade: {grade}")

    def view_attendance(self):
        self.attendance_list.clear()
        selected_class = self.class_dropdown.currentText()

        if selected_class:
            # For simplicity, showing just a dummy attendance status for the class
            self.attendance_list.addItem("Present")
            self.attendance_list.addItem("Absent")
            self.attendance_list.addItem("Present")
