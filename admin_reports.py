import matplotlib.pyplot as plt
from PyQt5.QtWidgets import QWidget, QVBoxLayout, QLabel, QComboBox, QPushButton, QTextEdit
from PyQt5.QtGui import QImageReader, QPixmap
import numpy as np

class AdminReports(QWidget):
    def __init__(self, grades_data, attendance_data, classes):
        super().__init__()

        self.grades_data = grades_data
        self.attendance_data = attendance_data
        self.classes = classes

        self.layout = QVBoxLayout()
        self.setLayout(self.layout)

        self.layout.addWidget(QLabel("Admin Performance Reports"))

        self.class_dropdown = QComboBox()
        self.class_dropdown.addItems(self.classes)
        self.layout.addWidget(self.class_dropdown)

        self.subject_dropdown = QComboBox()
        self.layout.addWidget(self.subject_dropdown)

        self.generate_report_btn = QPushButton("Generate Report")
        self.generate_report_btn.clicked.connect(self.generate_report)
        self.layout.addWidget(self.generate_report_btn)

        self.report_output = QTextEdit()
        self.layout.addWidget(self.report_output)

        # Placeholder for displaying graphs
        self.grade_graph_label = QLabel()
        self.layout.addWidget(self.grade_graph_label)

        self.attendance_graph_label = QLabel()
        self.layout.addWidget(self.attendance_graph_label)

        self.load_subjects()

    def load_subjects(self):
        selected_class = self.class_dropdown.currentText()
        if selected_class:
            self.subject_dropdown.clear()
            subjects = [f"Subject {i+1}" for i in range(5)]  # Replace with actual subject list from data
            self.subject_dropdown.addItems(subjects)

    def generate_report(self):
        selected_class = self.class_dropdown.currentText()
        selected_subject = self.subject_dropdown.currentText()

        if selected_class and selected_subject:
            report = self.generate_class_report(selected_class, selected_subject)
            self.report_output.setText(report)
            self.generate_graph(selected_class, selected_subject)
            self.display_graphs()

    def generate_class_report(self, selected_class, selected_subject):
        report = f"Performance Report for {selected_class} - {selected_subject}\n\n"
        report += "Students' Grades:\n"

        for (student, subject), grade in self.grades_data.items():
            if student in selected_class and subject == selected_subject:
                report += f"{student}: {grade}\n"

        report += "\nAttendance:\n"
        for student, attendance in self.attendance_data.items():
            if student in selected_class:
                report += f"{student}: {attendance}\n"

        return report

    def generate_graph(self, selected_class, selected_subject):
        grades = []
        attendance = {"Present": 0, "Absent": 0}

        for (student, subject), grade in self.grades_data.items():
            if student in selected_class and subject == selected_subject:
                grades.append(grade)

        for student, status in self.attendance_data.items():
            if student in selected_class:
                attendance[status] += 1

        # Plotting Grade Distribution
        grade_count = {"A": 0, "B": 0, "C": 0, "D": 0, "F": 0}
        for grade in grades:
            grade_count[grade] += 1

        grade_labels = list(grade_count.keys())
        grade_values = list(grade_count.values())

        plt.figure(figsize=(6, 4))
        plt.bar(grade_labels, grade_values, color='skyblue')
        plt.title(f"Grade Distribution for {selected_subject}")
        plt.xlabel("Grades")
        plt.ylabel("Number of Students")
        plt.tight_layout()
        plt.savefig('grade_distribution.png')
        plt.close()

        # Plotting Attendance Distribution
        attendance_labels = list(attendance.keys())
        attendance_values = list(attendance.values())

        plt.figure(figsize=(6, 4))
        plt.pie(attendance_values, labels=attendance_labels, autopct='%1.1f%%', startangle=90)
        plt.title(f"Attendance Distribution for {selected_class}")
        plt.tight_layout()
        plt.savefig('attendance_distribution.png')
        plt.close()

    def display_graphs(self):
        # Load the images into QPixmap and display them
        self.grade_graph_label.setPixmap(QPixmap('grade_distribution.png'))
        self.attendance_graph_label.setPixmap(QPixmap('attendance_distribution.png'))
