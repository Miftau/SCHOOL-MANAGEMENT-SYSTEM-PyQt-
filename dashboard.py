from PyQt5.QtWidgets import QMainWindow, QLabel

class AdminDashboard(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Admin Dashboard")
        self.setCentralWidget(QLabel("Welcome, Admin!"))

class TeacherDashboard(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Teacher Dashboard")
        self.setCentralWidget(QLabel("Welcome, Teacher!"))

class StudentDashboard(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Student Dashboard")
        self.setCentralWidget(QLabel("Welcome, Student!"))

class ParentDashboard(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Parent Dashboard")
        self.setCentralWidget(QLabel("Welcome, Parent!"))
