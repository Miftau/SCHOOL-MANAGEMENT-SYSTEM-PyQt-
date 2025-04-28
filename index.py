import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QDialog
from authentication import LoginWindow  # Assuming you've placed the LoginDialog in its own file or above
from dashboard import AdminDashboard, TeacherDashboard, StudentDashboard, ParentDashboard
import json  # For user data handling

from sign_up import SignUpWindow


class MainApp(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("School Management System")

        # Step 1: Show the login window
        self.login_window = LoginWindow()
        self.signup_window = SignUpWindow()

        if self.login_window.exec() == QDialog.Accepted:
            # Step 2: Retrieve the role and user data after successful login
            self.user_data = self.login_window.get_user_data()  # Assuming login_window returns user data
            role = self.user_data['role']  # Extract user role (admin, teacher, student, parent)
            self.launch_dashboard(role)

        elif self.signup_window:
            self.signup_window.exec()
        else:
            sys.exit()

    def launch_dashboard(self, role):
        """Close login window and launch appropriate dashboard."""
        self.close()  # Close the login/main window
        if role == "admin":
            self.dashboard = AdminDashboard(self.user_data)  # Pass user data to AdminDashboard
        elif role == "teacher":
            self.dashboard = TeacherDashboard(self.user_data)  # Pass user data to TeacherDashboard
        elif role == "student":
            self.dashboard = StudentDashboard(self.user_data)  # Pass user data to StudentDashboard
        elif role == "parent":
            self.dashboard = ParentDashboard(self.user_data)  # Pass user data to ParentDashboard
        self.dashboard.show()


if __name__ == '__main__':
    app = QApplication(sys.argv)
    main_window = MainApp()
    sys.exit(app.exec_())
