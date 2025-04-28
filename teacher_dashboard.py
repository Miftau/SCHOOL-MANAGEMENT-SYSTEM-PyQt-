from PyQt5.QtWidgets import *
import json
import re  # For grade validation

class TeacherDashboard(QWidget):
    def __init__(self, teacher_name, class_assignments, students, subjects):
        super().__init__()
        self.teacher_name = teacher_name
        self.class_assignments = class_assignments
        self.students = students  # Dict: {class: [students]}
        self.subjects = subjects  # List of subjects the teacher can grade
        self.student_grades = {}

        self.grades_file = "grades.json"  # File where grades will be saved

        self.layout = QVBoxLayout()
        self.setLayout(self.layout)

        self.layout.addWidget(QLabel(f"Welcome, {self.teacher_name}"))

        self.class_list = self.get_assigned_classes()
        self.class_dropdown = QComboBox()
        self.class_dropdown.addItems(self.class_list)

        self.subject_dropdown = QComboBox()
        self.subject_dropdown.addItems(self.subjects)

        self.load_students_btn = QPushButton("Load Students for Grading")
        self.load_students_btn.clicked.connect(self.load_students)

        self.attendance_list = QListWidget()

        self.grade_input = QLineEdit()
        self.grade_input.setPlaceholderText("Enter Grade")

        self.assign_grade_btn = QPushButton("Assign Grade to Student")
        self.assign_grade_btn.clicked.connect(self.assign_grade)

        self.view_grades_btn = QPushButton("View Grades")
        self.view_grades_btn.clicked.connect(self.view_grades)

        self.grades_list = QListWidget()  # To display assigned grades

        self.layout.addWidget(QLabel("Assigned Classes:"))
        self.layout.addWidget(self.class_dropdown)
        self.layout.addWidget(QLabel("Select Subject:"))
        self.layout.addWidget(self.subject_dropdown)
        self.layout.addWidget(self.load_students_btn)
        self.layout.addWidget(QLabel("Students:"))
        self.layout.addWidget(self.attendance_list)
        self.layout.addWidget(self.grade_input)
        self.layout.addWidget(self.assign_grade_btn)
        self.layout.addWidget(self.view_grades_btn)
        self.layout.addWidget(QLabel("Assigned Grades:"))
        self.layout.addWidget(self.grades_list)

        # Load grades from file when teacher logs in
        self.load_grades()

    def get_assigned_classes(self):
        return [entry.split(" - ")[0] for entry in self.class_assignments if self.teacher_name in entry]

    def load_students(self):
        self.attendance_list.clear()
        class_selected = self.class_dropdown.currentText()
        if class_selected in self.students:
            for student in self.students[class_selected]:
                self.attendance_list.addItem(student)
        else:
            QMessageBox.information(self, "No Students", "No students found for this class.")

    def assign_grade(self):
        selected = self.attendance_list.selectedItems()
        grade = self.grade_input.text().strip()

        if selected and grade:
            if not self.is_valid_grade(grade):
                QMessageBox.warning(self, "Invalid Grade", "Please enter a valid grade (e.g., A, B, 90).")
                return

            for item in selected:
                student_name = item.text()
                subject = self.subject_dropdown.currentText()
                self.student_grades[(student_name, subject)] = grade
                item.setText(f"{student_name} - Grade: {grade}")
            self.grade_input.clear()
            self.save_grades()
            QMessageBox.information(self, "Grade Assigned", "Grade assigned to selected students.")
        else:
            QMessageBox.warning(self, "Input Error", "Please select a student and enter a grade.")

    def view_grades(self):
        self.grades_list.clear()
        class_selected = self.class_dropdown.currentText()
        subject_selected = self.subject_dropdown.currentText()

        # Find all students in the selected class and display their grades for the selected subject
        for student, grade in self.student_grades.items():
            if student[0] in self.students[class_selected] and student[1] == subject_selected:
                self.grades_list.addItem(f"{student[0]} - Grade: {grade}")

        if self.grades_list.count() == 0:
            self.grades_list.addItem("No grades found.")

    def save_grades(self):
        """Save grades to a JSON file."""
        try:
            with open(self.grades_file, 'w') as file:
                json.dump(self.student_grades, file)
        except Exception as e:
            QMessageBox.warning(self, "Save Error", f"Failed to save grades: {str(e)}")

    def load_grades(self):
        """Load grades from the JSON file."""
        try:
            with open(self.grades_file, 'r') as file:
                self.student_grades = json.load(file)
        except (FileNotFoundError, json.JSONDecodeError):
            self.student_grades = {}  # If file not found or empty, initialize as empty

    def is_valid_grade(self, grade):
        """Check if the grade is valid (either a letter grade or a number)."""
        # Allow grades like 'A', 'B+', '90', etc.
        grade_pattern = r'^[A-Fa-f][+-]?$|^\d{1,3}$'
        return bool(re.match(grade_pattern, grade))
