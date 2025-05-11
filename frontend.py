import sys
from datetime import datetime, timedelta
from PySide6.QtWidgets import (QApplication, QMainWindow, QWidget, QVBoxLayout, 
                              QHBoxLayout, QLabel, QLineEdit, QPushButton, 
                              QStackedWidget, QTableWidget, QTableWidgetItem,
                              QMessageBox, QSpinBox, QDateEdit, QGroupBox,
                              QScrollArea, QComboBox)
from PySide6.QtCore import Qt, QDate
from PySide6.QtGui import QFont, QColor
from Backend import (CarRentalSystem, Customer, Admin, Vehicle, Car,
                    InvalidCredentialsError, UsernameExistsError, 
                    InsufficientBalanceError, VehicleNotAvailableError)


class ModernLineEdit(QLineEdit):
    def __init__(self, placeholder="", password=False):
        super().__init__()
        self.setPlaceholderText(placeholder)
        if password:
            self.setEchoMode(QLineEdit.Password)
        self.setStyleSheet("""
            QLineEdit {
                color: #757575;
                padding: 12px;
                border: 2px solid #e0e0e0;
                border-radius: 6px;
                background-color: white;
                font-size: 14px;
            }
            QLineEdit:focus {
                border: 2px solid #2962ff;
            }
        """)

class ModernButton(QPushButton):
    def __init__(self, text, primary=True):
        super().__init__(text)
        color = "#2962ff" if primary else "#757575"
        hover_color = "#1e88e5" if primary else "#616161"
        self.setStyleSheet(f"""
            QPushButton {{
                background-color: {color};
                color: white;
                border: none;
                border-radius: 6px;
                padding: 12px 24px;
                font-size: 14px;
                font-weight: bold;
            }}
            QPushButton:hover {{
                background-color: {hover_color};
            }}
        """)

class CarRentalApp(QMainWindow):
    def __init__(self):
        super().__init__()
        self.system = CarRentalSystem()
        self.current_user = None
        self.init_ui()

    def init_ui(self):
        self.setWindowTitle('FAM Car Rental System')
        self.setMinimumSize(1000, 700)
        self.setStyleSheet("""
            QMainWindow {
                background-color: #f5f5f5;
            }
            QLabel {
                font-size: 14px;
            }
            QGroupBox {
                font-size: 14px;
                font-weight: bold;
                border: 2px solid #e0e0e0;
                border-radius: 6px;
                margin-top: 12px;
            }
            QGroupBox::title {
                color: #2962ff;
            }
        """)

        # Create central widget and main layout
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        self.main_layout = QVBoxLayout(central_widget)

        # Create stacked widget for different pages
        self.stacked_widget = QStackedWidget()
        self.main_layout.addWidget(self.stacked_widget)

        # Create pages
        self.create_login_page()
        self.create_register_page()
        self.create_customer_page()
        self.create_admin_page()

        # Set initial page
        self.stacked_widget.setCurrentIndex(0)

    def create_login_page(self):
        page = QWidget()
        layout = QVBoxLayout(page)
        layout.setAlignment(Qt.AlignCenter)

        # Create a container for login form
        form_container = QWidget()
        form_container.setMaximumWidth(400)
        form_container.setStyleSheet("""
            QWidget {
                background-color: white;
                border-radius: 10px;
            }
        """)
        form_layout = QVBoxLayout(form_container)
        form_layout.setSpacing(20)
        form_layout.setContentsMargins(30, 30, 30, 30)

        # Title
        title = QLabel("Welcome to FAM Car Rental")
        title.setStyleSheet("""
            QLabel {
                color: #2962ff;
                font-size: 24px;
                font-weight: bold;
            }
        """)
        title.setAlignment(Qt.AlignCenter)

        # Login inputs
        self.username_input = ModernLineEdit(placeholder="Username")
        self.password_input = ModernLineEdit(placeholder="Password", password=True)
        
        # Login button
        login_button = ModernButton("Login")
        login_button.clicked.connect(self.handle_login)

        # Register link
        register_button = ModernButton("Create Account", primary=False)
        register_button.clicked.connect(lambda: self.stacked_widget.setCurrentIndex(1))

        # Add widgets to form layout
        form_layout.addWidget(title)
        form_layout.addWidget(self.username_input)
        form_layout.addWidget(self.password_input)
        form_layout.addWidget(login_button)
        form_layout.addWidget(register_button)

        # Add form container to page layout
        layout.addWidget(form_container)
        self.stacked_widget.addWidget(page)

    def create_register_page(self):
        page = QWidget()
        layout = QVBoxLayout(page)
        layout.setAlignment(Qt.AlignCenter)

        # Create a container for registration form
        form_container = QWidget()
        form_container.setMaximumWidth(500)
        form_container.setStyleSheet("""
            QWidget {
                background-color: white;
                border-radius: 10px;
            }
        """)
        form_layout = QVBoxLayout(form_container)
        form_layout.setSpacing(15)
        form_layout.setContentsMargins(30, 30, 30, 30)

        # Title
        title = QLabel("Create New Account")
        title.setStyleSheet("""
            QLabel {
                color: #2962ff;
                font-size: 24px;
                font-weight: bold;
            }
        """)
        title.setAlignment(Qt.AlignCenter)

        # Registration inputs
        self.reg_fields = {
            'username': ModernLineEdit(placeholder="Username"),
            'password': ModernLineEdit(placeholder="Password", password=True),
            'first_name': ModernLineEdit(placeholder="First Name"),
            'last_name': ModernLineEdit(placeholder="Last Name"),
            'email': ModernLineEdit(placeholder="Email"),
            'phone': ModernLineEdit(placeholder="Phone"),
            'address': ModernLineEdit(placeholder="Address")
        }

        # Register button
        register_button = ModernButton("Register")
        register_button.clicked.connect(self.handle_register)

        # Back button
        back_button = ModernButton("Back to Login", primary=False)
        back_button.clicked.connect(lambda: self.stacked_widget.setCurrentIndex(0))

        # Add widgets to form layout
        form_layout.addWidget(title)
        for field in self.reg_fields.values():
            form_layout.addWidget(field)
        form_layout.addWidget(register_button)
        form_layout.addWidget(back_button)

        # Add form container to page layout
        layout.addWidget(form_container)
        self.stacked_widget.addWidget(page)

    def create_customer_page(self):
        page = QWidget()
        layout = QVBoxLayout(page)

        # Header
        header = QWidget()
        header_layout = QHBoxLayout(header)
        
        welcome_label = QLabel()
        welcome_label.setStyleSheet("font-size: 20px; font-weight: bold; color: #2962ff;")
        self.customer_welcome = welcome_label

        balance_label = QLabel()
        balance_label.setStyleSheet("font-size: 16px; color: #4CAF50;")
        self.customer_balance = balance_label

        logout_button = ModernButton("Logout", primary=False)
        logout_button.clicked.connect(self.handle_logout)
        
        header_layout.addWidget(welcome_label)
        header_layout.addWidget(balance_label)
        header_layout.addWidget(logout_button)

        # Available Cars Section
        cars_group = QGroupBox("Available Vehicles")
        cars_layout = QVBoxLayout()
        
        self.cars_table = QTableWidget()
        self.cars_table.setStyleSheet("""
            QTableWidget {
                border: none;
                background-color: white;
            }
            QHeaderView::section {
                background-color: #2962ff;
                color: white;
                padding: 8px;
                border: none;
            }
        """)
        
        cars_layout.addWidget(self.cars_table)
        cars_group.setLayout(cars_layout)

        # Add Funds Section
        funds_group = QGroupBox("Add Funds")
        funds_layout = QHBoxLayout()
        
        self.fund_amount = QSpinBox()
        self.fund_amount.setRange(1, 1000)
        self.fund_amount.setPrefix("$ ")
        self.fund_amount.setStyleSheet("""
            QSpinBox {
                padding: 8px;
                border: 2px solid #e0e0e0;
                border-radius: 6px;
            }
        """)
        
        add_funds_button = ModernButton("Add Funds")
        add_funds_button.clicked.connect(self.handle_add_funds)
        
        funds_layout.addWidget(self.fund_amount)
        funds_layout.addWidget(add_funds_button)
        funds_group.setLayout(funds_layout)

        # Add all sections to main layout
        layout.addWidget(header)
        layout.addWidget(cars_group)
        layout.addWidget(funds_group)
        
        self.stacked_widget.addWidget(page)

    def create_admin_page(self):
        page = QWidget()
        layout = QVBoxLayout(page)

        # Header
        header = QWidget()
        header_layout = QHBoxLayout(header)
        
        title = QLabel("Admin Dashboard")
        title.setStyleSheet("font-size: 24px; font-weight: bold; color: #2962ff;")
        
        logout_button = ModernButton("Logout", primary=False)
        logout_button.clicked.connect(self.handle_logout)
        
        header_layout.addWidget(title)
        header_layout.addWidget(logout_button)
        
        # Add Vehicle Section
        add_vehicle_group = QGroupBox("Add New Vehicle")
        add_vehicle_layout = QVBoxLayout()
        
        self.vehicle_fields = {
            'vin': ModernLineEdit(placeholder="VIN"),
            'make': ModernLineEdit(placeholder="Make"),
            'model': ModernLineEdit(placeholder="Model"),
            'year': QSpinBox(),
            'daily_rate': QSpinBox(),
            'seating': QSpinBox(),
            'transmission': QComboBox(),
            'fuel_type': QComboBox()
        }
        
        self.vehicle_fields['year'].setRange(2000, 2025)
        self.vehicle_fields['daily_rate'].setRange(1, 1000)
        self.vehicle_fields['daily_rate'].setPrefix("Pkr ")
        self.vehicle_fields['seating'].setRange(2, 8)
        self.vehicle_fields['transmission'].addItems(['Automatic', 'Manual'])
        self.vehicle_fields['fuel_type'].addItems(['Gasoline', 'Diesel', 'Electric', 'Hybrid'])
        
        add_vehicle_button = ModernButton("Add Vehicle")
        add_vehicle_button.clicked.connect(self.handle_add_vehicle)
        
        for field in self.vehicle_fields.values():
            add_vehicle_layout.addWidget(field)
        add_vehicle_layout.addWidget(add_vehicle_button)
        add_vehicle_group.setLayout(add_vehicle_layout)

        # Vehicle Management Section
        vehicles_group = QGroupBox("Vehicle Management")
        vehicles_layout = QVBoxLayout()
        
        self.admin_vehicles_table = QTableWidget()
        self.admin_vehicles_table.setStyleSheet("""
            QTableWidget {
                border: none;
                background-color: white;
            }
            QHeaderView::section {
                background-color: #2962ff;
                color: white;
                padding: 8px;
                border: none;
            }
        """)
        
        vehicles_layout.addWidget(self.admin_vehicles_table)
        vehicles_group.setLayout(vehicles_layout)

        # Add all sections to main layout
        layout.addWidget(header)
        layout.addWidget(add_vehicle_group)
        layout.addWidget(vehicles_group)
        
        self.stacked_widget.addWidget(page)

    def handle_login(self):
        try:
            username = self.username_input.text()
            password = self.password_input.text()
            
            self.current_user = self.system.authenticate(username, password)
            
            if isinstance(self.current_user, Admin):
                self.update_admin_view()
                self.stacked_widget.setCurrentIndex(3)
            else:
                self.update_customer_view()
                self.stacked_widget.setCurrentIndex(2)
                
        except InvalidCredentialsError as e:
            QMessageBox.warning(self, "Login Failed", str(e))

    def handle_register(self):
        try:
            user_data = {
                field: widget.text() 
                for field, widget in self.reg_fields.items()
            }
            
            self.current_user = self.system.register_user(user_data)
            QMessageBox.information(self, "Success", "Registration successful!")
            self.stacked_widget.setCurrentIndex(0)
            
        except UsernameExistsError as e:
            QMessageBox.warning(self, "Registration Failed", str(e))

    def handle_logout(self):
        self.current_user = None
        self.stacked_widget.setCurrentIndex(0)
        self.username_input.clear()
        self.password_input.clear()
        self.system.shutdown()

    def handle_add_funds(self):
        amount = self.fund_amount.value()
        try:
            new_balance = self.system.add_funds(self.current_user.username, amount)
            self.update_customer_balance()
            QMessageBox.information(self, "Success", f"Added ${amount}. New balance: ${new_balance:.2f}")
        except Exception as e:
            QMessageBox.warning(self, "Error", str(e))

    def handle_add_vehicle(self):
        try:
            vehicle_data = {
                'vin': self.vehicle_fields['vin'].text(),
                'make': self.vehicle_fields['make'].text(),
                'model': self.vehicle_fields['model'].text(),
                'year': self.vehicle_fields['year'].value(),
                'daily_rate': self.vehicle_fields['daily_rate'].value(),
                'seating': self.vehicle_fields['seating'].value(),
                'transmission': self.vehicle_fields['transmission'].currentText(),
                'fuel_type': self.vehicle_fields['fuel_type'].currentText(),
                'is_available': True
            }
            
            self.system.add_vehicle(vehicle_data)
            self.update_admin_view()
            QMessageBox.information(self, "Success", "Vehicle added successfully!")
            
            # Clear the input fields
            for field in self.vehicle_fields.values():
                if isinstance(field, QLineEdit):
                    field.clear()
                elif isinstance(field, QSpinBox):
                    field.setValue(field.minimum())
                elif isinstance(field, QComboBox):
                    field.setCurrentIndex(0)
                    
        except Exception as e:
            QMessageBox.warning(self, "Error", str(e))

    def update_customer_view(self):
        # Update welcome message
        self.customer_welcome.setText(f"Welcome, {self.current_user.first_name} {self.current_user.last_name}")
        
        # Update balance
        self.update_customer_balance()
        
        # Update available cars table
        self.update_cars_table()

    def update_customer_balance(self):
        self.customer_balance.setText(f"Balance: ${self.current_user.balance:.2f}")

    def update_cars_table(self):
        available_cars = self.system.get_available_vehicles()
        self.cars_table.clear()
        self.cars_table.setRowCount(len(available_cars))
        self.cars_table.setColumnCount(9)
        
        headers = ["VIN", "Make", "Model", "Year", "Daily Rate", "Seats", 
                  "Transmission", "Fuel Type", "Actions"]
        self.cars_table.setHorizontalHeaderLabels(headers)
        
        for row, car in enumerate(available_cars):
            self.cars_table.setItem(row, 0, QTableWidgetItem(car.vin))
            self.cars_table.setItem(row, 1, QTableWidgetItem(car.make))
            self.cars_table.setItem(row, 2, QTableWidgetItem(car.model))
            self.cars_table.setItem(row, 3, QTableWidgetItem(str(car.year)))
            self.cars_table.setItem(row, 4, QTableWidgetItem(f"${car.daily_rate:.2f}"))
            self.cars_table.setItem(row, 5, QTableWidgetItem(str(car.seating)))
            self.cars_table.setItem(row, 6, QTableWidgetItem(car.transmission))
            self.cars_table.setItem(row, 7, QTableWidgetItem(car.fuel_type))
            
            rent_button = ModernButton("Rent", primary=True)
            rent_button.clicked.connect(lambda checked, c=car: self.show_rental_dialog(c))
            
            button_widget = QWidget()
            button_layout = QHBoxLayout(button_widget)
            button_layout.addWidget(rent_button)
            button_layout.setContentsMargins(4, 4, 4, 4)
            
            self.cars_table.setCellWidget(row, 8, button_widget)
            
        self.cars_table.resizeColumnsToContents()

    def show_rental_dialog(self, car):
        from PySide6.QtWidgets import QDialog, QCalendarWidget, QVBoxLayout
        
        dialog = QDialog(self)
        dialog.setWindowTitle("Rent Vehicle")
        dialog.setMinimumWidth(400)
        layout = QVBoxLayout(dialog)
        
        # Car details
        details = QLabel(f"""
            Vehicle: {car.make} {car.model} ({car.year})
            Daily Rate: ${car.daily_rate:.2f}
            Transmission: {car.transmission}
            Fuel Type: {car.fuel_type}
        """)
        details.setStyleSheet("font-size: 14px; margin: 10px;")
        
        # Date selection
        start_date = QDateEdit(QDate.currentDate())
        start_date.setMinimumDate(QDate.currentDate())
        start_date.setCalendarPopup(True)
        
        end_date = QDateEdit(QDate.currentDate().addDays(1))
        end_date.setMinimumDate(QDate.currentDate().addDays(1))
        end_date.setCalendarPopup(True)
        
        # Duration and cost calculation
        duration_label = QLabel()
        cost_label = QLabel()
        
        def update_duration_cost():
            days = start_date.date().daysTo(end_date.date())
            total_cost = days * car.daily_rate
            duration_label.setText(f"Duration: {days} days")
            cost_label.setText(f"Total Cost: ${total_cost:.2f}")
        
        start_date.dateChanged.connect(update_duration_cost)
        end_date.dateChanged.connect(update_duration_cost)
        update_duration_cost()
        
        # Rent button
        rent_button = ModernButton("Confirm Rental")
        rent_button.clicked.connect(lambda: self.handle_rental_confirmation(
            dialog, car, start_date.date().toPython(), end_date.date().toPython()
        ))
        
        # Cancel button
        cancel_button = ModernButton("Cancel", primary=False)
        cancel_button.clicked.connect(dialog.reject)
        
        # Add widgets to layout
        layout.addWidget(details)
        layout.addWidget(QLabel("Start Date:"))
        layout.addWidget(start_date)
        layout.addWidget(QLabel("End Date:"))
        layout.addWidget(end_date)
        layout.addWidget(duration_label)
        layout.addWidget(cost_label)
        layout.addWidget(rent_button)
        layout.addWidget(cancel_button)
        
        dialog.exec_()

    def handle_rental_confirmation(self, dialog, car, start_date, end_date):
        try:
            rental = self.system.rent_vehicle(
                self.current_user.username,
                car.vin,
                start_date,
                end_date
            )
            
            QMessageBox.information(self, "Success", 
                f"Vehicle rented successfully!\n\n"
                f"Total Cost: ${rental.total_cost:.2f}\n"
                f"Duration: {rental.duration_days} days"
            )
            
            dialog.accept()
            self.update_customer_view()
            
        except InsufficientBalanceError as e:
            QMessageBox.warning(self, "Error", str(e))
        except VehicleNotAvailableError as e:
            QMessageBox.warning(self, "Error", str(e))
        except Exception as e:
            QMessageBox.warning(self, "Error", f"Failed to rent vehicle: {str(e)}")

    def update_admin_view(self):
        self.update_admin_vehicles_table()

    def update_admin_vehicles_table(self):
        vehicles = self.system.vehicles
        self.admin_vehicles_table.clear()
        self.admin_vehicles_table.setRowCount(len(vehicles))
        self.admin_vehicles_table.setColumnCount(10)
        
        headers = ["VIN", "Make", "Model", "Year", "Daily Rate", "Seats", 
                  "Transmission", "Fuel Type", "Status", "Actions"]
        self.admin_vehicles_table.setHorizontalHeaderLabels(headers)
        
        for row, vehicle in enumerate(vehicles):
            self.admin_vehicles_table.setItem(row, 0, QTableWidgetItem(vehicle.vin))
            self.admin_vehicles_table.setItem(row, 1, QTableWidgetItem(vehicle.make))
            self.admin_vehicles_table.setItem(row, 2, QTableWidgetItem(vehicle.model))
            self.admin_vehicles_table.setItem(row, 3, QTableWidgetItem(str(vehicle.year)))
            self.admin_vehicles_table.setItem(row, 4, QTableWidgetItem(f"${vehicle.daily_rate:.2f}"))
            self.admin_vehicles_table.setItem(row, 5, QTableWidgetItem(str(vehicle.seating)))
            self.admin_vehicles_table.setItem(row, 6, QTableWidgetItem(vehicle.transmission))
            self.admin_vehicles_table.setItem(row, 7, QTableWidgetItem(vehicle.fuel_type))
            
            status = "Available" if vehicle.is_available else "Rented"
            status_item = QTableWidgetItem(status)
            status_item.setForeground(
                QColor("#4CAF50") if vehicle.is_available else QColor("#F44336")
            )
            self.admin_vehicles_table.setItem(row, 8, status_item)
            
            if vehicle.is_available:
                remove_button = ModernButton("Remove", primary=False)
                remove_button.clicked.connect(lambda checked, v=vehicle: self.handle_remove_vehicle(v))
                
                button_widget = QWidget()
                button_layout = QHBoxLayout(button_widget)
                button_layout.addWidget(remove_button)
                button_layout.setContentsMargins(4, 4, 4, 4)
                
                self.admin_vehicles_table.setCellWidget(row, 9, button_widget)
            
        self.admin_vehicles_table.resizeColumnsToContents()

    def handle_remove_vehicle(self, vehicle):
        try:
            self.system.remove_vehicle(vehicle.vin)
            self.update_admin_view()
            QMessageBox.information(self, "Success", "Vehicle removed successfully!")
        except Exception as e:
            QMessageBox.warning(self, "Error", str(e))

    def closeEvent(self, event):
        self.system.shutdown()
        event.accept()

if __name__ == '__main__':
    app = QApplication(sys.argv)
    
    # Set application style
    app.setStyle("Fusion")
    
    # Set default font
    font = QFont("Segoe UI", 10)
    app.setFont(font)
    
    # Create and show the main window
    window = CarRentalApp()
    window.show()
    
    sys.exit(app.exec())
