import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QDialog
from authentication import LoginWindow  # Assuming you've placed the LoginDialog in its own file or above
from admin_dashboard import AdminDashboard
from teacher_dashboard import TeacherDashboard
from student_dashboard import StudentDashboard
from parent_dashboard import ParentDashboard
import traceback
import sqlite3
import json  # For user data handling

from sign_up import SignUpWindow

class MainApp(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("School Management System")

        # Show the login dialog modally
        login_dialog = LoginWindow()
        result = login_dialog.exec()

        if result == QDialog.Accepted:
            self.user_data = login_dialog.user_data
            self.launch_dashboard(self.user_data['role'])
        else:
            sys.exit()

    def launch_dashboard(self, role):
        """Close login window and launch appropriate dashboard."""
        self.close()  # Close the login/main window
        if role == "admin":
            self.dashboard = AdminDashboard()  # Pass user data to AdminDashboard
        elif role == "teacher":
            self.dashboard = TeacherDashboard(self.user_data)  # Pass user data to TeacherDashboard
        elif role == "student":
            self.dashboard = StudentDashboard(self.user_data)  # Pass user data to StudentDashboard
        elif role == "parent":
            self.dashboard = ParentDashboard(self.user_data)  # Pass user data to ParentDashboard
        self.dashboard.show()


#if __name__ == '__main__':
    #app = QApplication(sys.argv)
    #main_window = MainApp()
    #sys.exit(app.exec_())


def main():
    try:
        app = QApplication(sys.argv)
        window = MainApp()
        window.show()
        sys.exit(app.exec_())
    except Exception as e:
        print("Fatal Error:", e)
        traceback.print_exc()

if __name__ == "__main__":
    main()
