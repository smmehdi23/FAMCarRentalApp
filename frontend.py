import sys
from datetime import datetime
from pathlib import Path
from PySide6.QtWidgets import *
from PySide6.QtCore import Qt, QSize
from PySide6.QtGui import *
from Backend import * 
"""from backend base classes imported CarRentalSystem, Customer, Admin, InvalidCredentialsError"""

class StyleSheet:
    MAIN_STYLE = """
    * {
        font-family: 'Montserrat';
    }
    QMainWindow {
        background-color: #f0f0f0;
    }
    QLabel#title {
        color: #1a1a2e;
        font-size: 32px;
        font-weight: bold;
    }
    QPushButton {
        background-color: #7785AC;
        color: white;
        border: none;
        border-radius: 5px;
        padding: 10px 20px;
        font-size: 14px;
        min-width: 120px;
        font-weight: 500;
    }
    QPushButton:hover {
        background-color: #5D6B99;
    }
    QLineEdit {
        padding: 12px;
        border-radius: 5px;
        background-color: #e0e0e0;
        border: 1px solid #cccccc;
        margin: 5px;
        font-size: 14px;
    }
    QFrame#car-card {
        background-color: #1a1a2e;
        border-radius: 15px;
        padding: 20px;
        margin: 15px;
        min-height: 200px;
    }
    QFrame#car-card QLabel {
        color: white;
        font-size: 14px;
        margin: 5px 0;
    }
    QFrame#car-card QPushButton {
        background-color: #7785AC;
        color: white;
        font-weight: bold;
        padding: 10px 20px;
        margin: 10px;
        border-radius: 5px;
    }
    """
class RegisterDialog(QDialog):
    def __init__(self, system, parent=None):
        super().__init__(parent)
        self.system = system
        self.setup_ui()
        
    def setup_ui(self):
        self.setWindowTitle("Register New User")
        self.setModal(True)
        self.setStyleSheet(StyleSheet.MAIN_STYLE)
        layout = QFormLayout()
        
        # Create input fields
        self.fields = {
            'username': QLineEdit(),
            'password': QLineEdit(),
            'first_name': QLineEdit(),
            'last_name': QLineEdit(),
            'email': QLineEdit(),
            'phone': QLineEdit(),
            'address': QLineEdit()
        }
        
        # Set password field to password mode
        self.fields['password'].setEchoMode(QLineEdit.Password)
        
        # Add fields to layout
        for key, field in self.fields.items():
            label = QLabel(key.replace('_', ' ').title() + ':')
            label.setStyleSheet("font-weight: 500;")
            layout.addRow(label, field)
        
        # Add buttons
        button_layout = QHBoxLayout()
        register_btn = QPushButton("Register")
        cancel_btn = QPushButton("Cancel")
        
        register_btn.clicked.connect(self.handle_register)
        cancel_btn.clicked.connect(self.reject)
        
        button_layout.addWidget(register_btn)
        button_layout.addWidget(cancel_btn)
        layout.addRow(button_layout)
        
        self.setLayout(layout)
    
    def handle_register(self):
        try:
            user_data = {field: widget.text() for field, widget in self.fields.items()}
            
            if not all(user_data.values()):
                QMessageBox.warning(self, "Error", "All fields are required!")
                return
                
            self.system.register_user(user_data)
            QMessageBox.information(self, "Success", "Registration successful! You can now login.")
            self.accept()
            
        except Exception as e:
            QMessageBox.warning(self, "Error", str(e))
class LoginWindow(QWidget):
    def __init__(self, system, stacked_widget):
        super().__init__()
        self.system = system
        self.stacked_widget = stacked_widget
        self.setup_ui()

    def setup_ui(self):
        layout = QHBoxLayout()
        
        # Left side - Welcome and Car Image
        left_widget = QWidget()
        left_widget.setStyleSheet("background-color: #f0f0f0; padding-right: 50px; padding-left: 50px;padding-top: 100px;")
        left_layout = QVBoxLayout()
        
        welcome_label = QLabel("WELCOME TO\nFAM CAR RENTAL SYSTEM")
        welcome_label.setObjectName("title")
        welcome_label.setStyleSheet("font-size: 40px; font-weight: bold; color: #1a1a2e;")
        welcome_label.setAlignment(Qt.AlignCenter)
        
        car_image = QLabel()
        car_image_path = "C:/UNI DATA/CP/OOP CEP/FAM CAR RENTAL/assets/main_car.png"
        if Path(car_image_path).exists():
            pixmap = QPixmap(car_image_path)
            car_image.setPixmap(pixmap.scaled(600, 500, Qt.KeepAspectRatio))
        
        left_layout.addWidget(welcome_label)
        left_layout.addWidget(car_image)
        left_layout.addStretch()
        left_widget.setLayout(left_layout)
        
        # Right side - Login Form
        right_widget = QWidget()
        right_widget.setStyleSheet("""
    QWidget {
        background-color: #1a1a2e;
        border-radius: 10px;  
    }
    QLabel {
        color: #f0f0f0;
    }
    QLineEdit {
        color: white;
        background-color: rgba(255, 255, 255, 0.1);
        border: 1px solid rgba(255, 255, 255, 0.2);
    }
    QLineEdit::placeholder {
        color: rgba(255, 255, 255, 0.7);
    }
""")
        right_layout = QVBoxLayout()
        
        auth_label = QLabel("USER AUTHENTICATION")
        auth_label.setStyleSheet("font-size: 24px; font-weight: bold;")
        auth_label.setAlignment(Qt.AlignCenter)
        
        self.username_input = QLineEdit()
        self.username_input.setPlaceholderText("Username")
        self.username_input.setFixedSize(300, 50)
        
        self.password_input = QLineEdit()
        self.password_input.setPlaceholderText("Password")
        self.password_input.setEchoMode(QLineEdit.Password)
        self.password_input.setFixedSize(300, 50)
        
        button_layout = QHBoxLayout()
        login_button = QPushButton("LOGIN")
        register_button = QPushButton("REGISTER")
        
        login_button.clicked.connect(self.handle_login)
        register_button.clicked.connect(self.show_register)
        
        button_layout.addWidget(login_button)
        button_layout.addWidget(register_button)
        
        right_layout.addWidget(auth_label)
        right_layout.addWidget(self.username_input)
        right_layout.addWidget(self.password_input)
        right_layout.addLayout(button_layout)
        right_layout.setAlignment(Qt.AlignCenter)
        right_widget.setLayout(right_layout)
        
        layout.addWidget(left_widget)
        layout.addWidget(right_widget)
        self.setLayout(layout)

    def handle_login(self):
        try:
            user = self.system.authenticate(
                self.username_input.text(),
                self.password_input.text()
            )
            dashboard = DashboardWindow(self.system, user, self.stacked_widget)
            self.stacked_widget.addWidget(dashboard)
            self.stacked_widget.setCurrentWidget(dashboard)
        except InvalidCredentialsError:
            QMessageBox.warning(self, "Error", "Invalid username or password")

    def show_register(self):
        dialog = RegisterDialog(self.system, self)
        dialog.exec()

class CarCard(QFrame):
    def __init__(self, car, user, system, parent=None):
        super().__init__(parent)
        self.car = car
        self.user = user
        self.system = system
        self.setObjectName("car-card")
        self.setStyleSheet("""
            QFrame#car-card {
                background-color: #ffffff;
                border-radius: 10px;
                min-width: 400px;
                max-width: 400px;
            }
            QLabel {
                color: #1a1a2e;
            }
            QLabel#title {
                font-size: 20px;
                font-weight: bold;
                color: #1a1a2e;
            }
            QLabel#price {
                font-size: 16px;
                color: #7785AC;
            }
            QPushButton {
                background-color: #7785AC;
                color: white;
                border: none;
                padding: 10px;
                border-radius: 5px;
                font-size: 14px;
                min-width: 120px;
            }
            QPushButton:hover {
                background-color: #5D6B99;
            }
        """)
        self.setup_ui()

    def setup_ui(self):
        main_layout = QVBoxLayout(self)
        main_layout.setSpacing(10)
        main_layout.setContentsMargins(15, 15, 15, 15)

        # Car title
        title = QLabel(self.car.make + " " + self.car.model)
        title.setObjectName("title")
        title.setAlignment(Qt.AlignCenter)

        # Car image
        image_label = QLabel()
        image_path = f"C:/UNI DATA/CP/OOP CEP/FAM CAR RENTAL/assets/cars/{self.car.make.lower()}_{self.car.model.lower()}.png"
        if Path(image_path).exists():
            pixmap = QPixmap(image_path)
            scaled_pixmap = pixmap.scaled(300, 200, Qt.KeepAspectRatio, Qt.SmoothTransformation)
            image_label.setPixmap(scaled_pixmap)
        image_label.setAlignment(Qt.AlignCenter)

        # Price
        price = QLabel(f"PKR {self.car.daily_rate}/-")
        price.setObjectName("price")
        price.setAlignment(Qt.AlignCenter)

        # Car details
        details = QLabel(f"Year: {self.car.year}\nTransmission: {self.car.transmission}\nFuel Type: {self.car.fuel_type}")
        details.setAlignment(Qt.AlignCenter)

        # Rent button
        rent_button = QPushButton("RENT ME!")
        rent_button.setCursor(Qt.PointingHandCursor)
        rent_button.clicked.connect(self.handle_rent)

        # Add widgets to layout
        main_layout.addWidget(title)
        main_layout.addWidget(image_label)
        main_layout.addWidget(price)
        main_layout.addWidget(details)
        main_layout.addWidget(rent_button)
        main_layout.setAlignment(Qt.AlignCenter)

    

    def handle_rent(self):
        if not isinstance(self.user, Customer):
            QMessageBox.warning(self, "Error", "Only customers can rent cars!")
            return
            
        if self.user.current_rental:
            QMessageBox.warning(self, "Error", "You already have an active rental!")
            return

        try:
            dialog = QDialog(self)
            dialog.setWindowTitle("Rent Car")
            dialog.setStyleSheet(StyleSheet.MAIN_STYLE)
            layout = QFormLayout()

            start_date = QCalendarWidget()
            end_date = QCalendarWidget()
            
            start_date.setMinimumDate(datetime.now().date())
            end_date.setMinimumDate(datetime.now().date())

            layout.addRow("Start Date:", start_date)
            layout.addRow("End Date:", end_date)

            buttons = QHBoxLayout()
            confirm = QPushButton("Confirm Rental")
            cancel = QPushButton("Cancel")

            buttons.addWidget(confirm)
            buttons.addWidget(cancel)

            layout.addRow(buttons)
            dialog.setLayout(layout)

            def handle_confirm():
                start = datetime.combine(start_date.selectedDate().toPython(), datetime.min.time())
                end = datetime.combine(end_date.selectedDate().toPython(), datetime.min.time())
                
                try:
                    rental = self.system.rent_vehicle(self.user.username, self.car.vin, start, end)
                    QMessageBox.information(self, "Success", 
                        f"Car rented successfully!\nTotal Cost: PKR {rental.total_cost}/-")
                    dialog.accept()
                except Exception as e:
                    QMessageBox.warning(self, "Error", str(e))

            confirm.clicked.connect(handle_confirm)
            cancel.clicked.connect(dialog.reject)

            dialog.exec()

        except Exception as e:
            QMessageBox.warning(self, "Error", str(e))

class DashboardWindow(QWidget):
    def __init__(self, system, user, stacked_widget):
        super().__init__()
        self.system = system
        self.user = user
        self.stacked_widget = stacked_widget
        self.setup_ui()

    def setup_ui(self):
        layout = QHBoxLayout()
        
        # Left Menu
        menu_widget = QWidget()
        menu_widget.setStyleSheet("""
            QWidget {
                background-color: #1a1a2e;
                min-width: 200px;
                max-width: 200px;
            }
            QLabel {
                color: white;
                font-size: 20px;
                padding: 10px;
                font-family: 'Montserrat';
            }
            QPushButton {
                text-align: left;
                padding: 15px;
                margin: 5px;
                border-radius: 5px;
                font-family: 'Montserrat';
            }
        """)
        menu_layout = QVBoxLayout()
        
        menu_label = QLabel("MENU")
        menu_label.setStyleSheet("font-weight: bold; font-family: 'Montserrat';")
        
        # Initialize buttons list based on user type
        if isinstance(self.user, Admin):
            buttons = [
                ("AVAILABLE CARS", self.show_available_cars),
                ("CAR MANAGEMENT", self.show_car_management),
                ("ADD NEW CARS", self.show_add_car)
            ]
        else:
            buttons = [
                ("AVAILABLE CARS", self.show_available_cars),
                ("MY RENTALS", self.show_my_rentals),
                ("MY FUNDS", self.show_funds)
            ]
        
        # Add logout button for all users
        buttons.append(("LOGOUT", self.logout))
        
        menu_layout.addWidget(menu_label)
        for text, handler in buttons:
            button = QPushButton(text)
            button.clicked.connect(handler)
            menu_layout.addWidget(button)
        
        menu_layout.addStretch()
        menu_widget.setLayout(menu_layout)
        
            
        # Main Content Area
        content_widget = QWidget()
        content_widget.setStyleSheet("""
            QWidget {
                background-color: #f0f0f0;
            }
            QFrame {
                background-color: #ffffff;
                border-radius: 10px;
            }
        """)
        
        self.content_layout = QVBoxLayout(content_widget)
        self.content_layout.setContentsMargins(20, 20, 20, 20)
        self.content_layout.setSpacing(20)
        # Welcome header
        header_frame = QFrame()
        header_frame.setStyleSheet("""
            QFrame {
                background-color: #1a1a2e;
                border-radius: 10px;
                margin: 10px;
                padding: 10px;
            }
            QLabel {
                color: white;
                font-size: 24px;
                font-family: 'Montserrat';
            }
        """)
        header_layout = QVBoxLayout()
        welcome_label = QLabel(f"WELCOME BACK {self.user.username.upper()}")
        if isinstance(self.user, Admin):
            welcome_label.setText(welcome_label.text() + " (ADMIN)")
        header_layout.addWidget(welcome_label)
        
        # Add balance for customers
        if isinstance(self.user, Customer):
            balance_label = QLabel(f"YOUR BALANCE: {self.user.balance} PKR")
            balance_label.setStyleSheet("font-size: 18px; font-family: 'Montserrat';")
            header_layout.addWidget(balance_label)
        
        header_frame.setLayout(header_layout)
        self.content_layout.addWidget(header_frame)
        
        content_widget.setLayout(self.content_layout)
        
        # Add scroll area for car listings
        scroll_area = QScrollArea()
        scroll_area.setWidget(content_widget)
        scroll_area.setWidgetResizable(True)
        scroll_area.setStyleSheet("""
            QScrollArea {
                border: none;
                background-color: #f0f0f0;
            }
        """)
        
        layout.addWidget(menu_widget)
        layout.addWidget(scroll_area, stretch=1)
        self.setLayout(layout)
        
        # Show available cars by default
        self.show_available_cars()

    def clear_content(self):
        """Clear all widgets from the content area except the header"""
        # Keep track of the header (first widget)
        header = None
        if self.content_layout.count() > 0:
            header = self.content_layout.itemAt(0).widget()
        
        # Clear all widgets
        for i in reversed(range(self.content_layout.count())):
            widget = self.content_layout.itemAt(i).widget()
            if widget:
                widget.deleteLater()
        
        # Add back the header if it existed
        if header:
            self.content_layout.addWidget(header)

    def show_available_cars(self):
        self.clear_content()
        cars = self.system.get_available_vehicles()
        
        if not cars:
            no_cars_label = QLabel("No cars available at the moment.")
            no_cars_label.setAlignment(Qt.AlignCenter)
            self.content_layout.addWidget(no_cars_label)
            return
            
        cars_grid = QWidget()
        grid_layout = QGridLayout()
        row = 0
        col = 0
        max_cols = 2  # Show 2 cars per row
        
        for car in cars:
            car_card = CarCard(car, self.user, self.system)
            grid_layout.addWidget(car_card, row, col)
            col += 1
            if col >= max_cols:
                col = 0
                row += 1
        
        cars_grid.setLayout(grid_layout)
        self.content_layout.addWidget(cars_grid)

    def show_my_rentals(self):
        self.clear_content()
        
        if isinstance(self.user, Customer):
            # Show current rental if exists
            if self.user.current_rental:
                current_rental_frame = QFrame()
                current_rental_frame.setObjectName("car-card")
                current_rental_frame.setStyleSheet("""
                    QFrame#car-card {
                        background-color: #ffffff;
                        border-radius: 10px;
                        padding: 20px;
                        margin: 10px;
                        min-width: 400px;
                    }
                    QLabel {
                        color: #1a1a2e;
                        font-size: 14px;
                        margin: 5px 0;
                    }
                    QPushButton {
                        background-color: #7785AC;
                        color: white;
                        border: none;
                        padding: 10px;
                        border-radius: 5px;
                        font-size: 14px;
                        min-width: 120px;
                        margin-top: 10px;
                    }
                """)
                layout = QVBoxLayout(current_rental_frame)
                
                # Current rental title
                title = QLabel("Current Rental")
                title.setStyleSheet("font-size: 18px; font-weight: bold; color: #1a1a2e;")
                layout.addWidget(title)
                
                # Car details
                car_details = QLabel(f"Car: {self.user.current_rental.vehicle.make} {self.user.current_rental.vehicle.model}")
                layout.addWidget(car_details)
                
                # Dates
                dates = QLabel(
                    f"Start Date: {self.user.current_rental.start_date.strftime('%Y-%m-%d')}\n"
                    f"End Date: {self.user.current_rental.end_date.strftime('%Y-%m-%d')}"
                )
                layout.addWidget(dates)
                
                # Cost
                cost = QLabel(f"Total Cost: PKR {self.user.current_rental.total_cost}/-")
                cost.setStyleSheet("color: #7785AC; font-weight: bold;")
                layout.addWidget(cost)
                
                # Return button
                return_button = QPushButton("Return Vehicle")
                return_button.clicked.connect(self.handle_return_vehicle)
                layout.addWidget(return_button)
                
                self.content_layout.addWidget(current_rental_frame)
            
            # Show rental history
            history = self.system.get_user_rental_history(self.user.username)
            if history:
                history_label = QLabel("Rental History")
                history_label.setStyleSheet("""
                    font-size: 18px;
                    font-weight: bold;
                    color: #1a1a2e;
                    margin: 20px 10px;
                """)
                self.content_layout.addWidget(history_label)
                
                # Create scroll area for history
                scroll_area = QScrollArea()
                scroll_area.setWidgetResizable(True)
                scroll_area.setHorizontalScrollBarPolicy(Qt.ScrollBarAsNeeded)
                scroll_area.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
                scroll_area.setStyleSheet("""
                    QScrollArea {
                        border: none;
                        background-color: transparent;
                    }
                    QScrollBar:horizontal {
                        height: 10px;
                        background: #f0f0f0;
                    }
                    QScrollBar::handle:horizontal {
                        background: #7785AC;
                        min-width: 20px;
                        border-radius: 5px;
                    }
                """)
                
                # Container for history cards
                container = QWidget()
                horizontal_layout = QHBoxLayout(container)
                horizontal_layout.setSpacing(20)
                horizontal_layout.setContentsMargins(20, 20, 20, 20)
                
                for rental in history:
                    history_frame = QFrame()
                    history_frame.setObjectName("car-card")
                    history_frame.setStyleSheet("""
                        QFrame#car-card {
                            background-color: #ffffff;
                            border-radius: 10px;
                            padding: 20px;
                            margin: 5px;
                            min-width: 300px;
                        }
                        QLabel {
                            color: #1a1a2e;
                            margin: 5px 0;
                        }
                    """)
                    layout = QVBoxLayout(history_frame)
                    
                    car_label = QLabel(f"Car: {rental.vehicle.make} {rental.vehicle.model}")
                    date_label = QLabel(f"Date: {rental.start_date.strftime('%Y-%m-%d')} to {rental.end_date.strftime('%Y-%m-%d')}")
                    cost_label = QLabel(f"Total Cost: PKR {rental.total_cost}/-")
                    cost_label.setStyleSheet("color: #7785AC; font-weight: bold;")
                    
                    layout.addWidget(car_label)
                    layout.addWidget(date_label)
                    layout.addWidget(cost_label)
                    
                    horizontal_layout.addWidget(history_frame)
                
                horizontal_layout.addStretch()
                scroll_area.setWidget(container)
                self.content_layout.addWidget(scroll_area)
            else:
                no_history_label = QLabel("No rental history available.")
                no_history_label.setStyleSheet("""
                    color: #1a1a2e;
                    font-size: 14px;
                    margin: 20px;
                """)
                no_history_label.setAlignment(Qt.AlignCenter)
                self.content_layout.addWidget(no_history_label)
    
    def show_funds(self):
        self.clear_content()
        
        if isinstance(self.user, Customer):
            funds_frame = QFrame()
            funds_frame.setObjectName("car-card")
            layout = QVBoxLayout()
            
            # Balance display
            balance_label = QLabel(f"Current Balance: PKR {self.user.balance}/-")
            balance_label.setStyleSheet("""
                font-size: 28px;
                font-weight: bold;
                color: #1a1a2e;
                margin-bottom: 30px;
            """)
            balance_label.setAlignment(Qt.AlignCenter)
            layout.addWidget(balance_label)
            
            # Quick top-up options
            amounts_widget = QWidget()
            amounts_layout = QGridLayout()
            amounts = [1000, 2000, 5000, 10000]
            row = 0
            col = 0
            for amount in amounts:
                btn = QPushButton(f"Add {amount} PKR")
                btn.setStyleSheet("""
                    QPushButton {
                        padding: 15px;
                        font-size: 16px;
                        background-color: #1a1a2e;
                    }
                    QPushButton:hover {
                        background-color: #1a1a2e;
                    }
                """)
                # Use handle_add_funds_direct instead of handle_add_funds
                btn.clicked.connect(lambda checked, a=amount: self.handle_add_funds_direct(a))
                amounts_layout.addWidget(btn, row, col)
                col += 1
                if col > 1:
                    col = 0
                    row += 1
            
            amounts_widget.setLayout(amounts_layout)
            layout.addWidget(amounts_widget)
            
            # Custom amount button
            custom_amount_btn = QPushButton("Add Custom Amount")
            custom_amount_btn.setStyleSheet("""
                QPushButton {
                    padding: 15px;
                    font-size: 16px;
                    background-color: #1a1a2e;
                    margin-top: 20px;
                }
            """)
            custom_amount_btn.clicked.connect(self.handle_add_funds_custom)
            layout.addWidget(custom_amount_btn)
            
            funds_frame.setLayout(layout)
            self.content_layout.addWidget(funds_frame)
        else:
            self.content_layout.addWidget(QLabel("Fund management not available for admin users."))

    def handle_add_funds_direct(self, amount):
        """Handle direct amount top-up"""
        try:
            new_balance = self.system.add_funds(self.user.username, amount)
            QMessageBox.information(self, "Success", 
                f"Funds added successfully!\nNew Balance: PKR {new_balance}/-")
            self.show_funds()  # Refresh the view
        except Exception as e:
            QMessageBox.warning(self, "Error", str(e))

    def handle_add_funds_custom(self):
        """Handle custom amount top-up"""
        amount, ok = QInputDialog.getDouble(
            self, 
            "Add Funds", 
            "Enter amount to add (PKR):", 
        )
        if ok:
            try:
                new_balance = self.system.add_funds(self.user.username, amount)
                QMessageBox.information(self, "Success", 
                    f"Funds added successfully!\nNew Balance: PKR {new_balance}/-")
                self.show_funds()  # Refresh the view
            except Exception as e:
                QMessageBox.warning(self, "Error", str(e))
    
    def show_available_cars(self):
        self.clear_content()
        cars = self.system.get_available_vehicles()
        
        if not cars:
            no_cars_label = QLabel("No cars available at the moment.")
            no_cars_label.setAlignment(Qt.AlignCenter)
            self.content_layout.addWidget(no_cars_label)
            return
        
        # Create scroll area
        scroll_area = QScrollArea()
        scroll_area.setWidgetResizable(True)
        scroll_area.setHorizontalScrollBarPolicy(Qt.ScrollBarAsNeeded)
        scroll_area.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        scroll_area.setStyleSheet("""
            QScrollArea {
                border: none;
                background-color: #f0f0f0;
            }
            QScrollBar:horizontal {
                height: 10px;
                background: #f0f0f0;
            }
            QScrollBar::handle:horizontal {
                background: #7785AC;
                min-width: 20px;
                border-radius: 5px;
            }
        """)

        # Create container for cards
        container = QWidget()
        horizontal_layout = QHBoxLayout(container)
        horizontal_layout.setSpacing(20)
        horizontal_layout.setContentsMargins(20, 20, 20, 20)
        
        # Add car cards
        for car in cars:
            car_card = CarCard(car, self.user, self.system)
            horizontal_layout.addWidget(car_card)
        
        horizontal_layout.addStretch()
        scroll_area.setWidget(container)
        self.content_layout.addWidget(scroll_area)

    def show_car_management(self):
        if not isinstance(self.user, Admin):
            QMessageBox.warning(self, "Error", "Only admin users can access car management!")
            return
            
        self.clear_content()
        
        # Create scroll area
        scroll_area = QScrollArea()
        scroll_area.setWidgetResizable(True)
        scroll_area.setHorizontalScrollBarPolicy(Qt.ScrollBarAsNeeded)
        scroll_area.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        scroll_area.setStyleSheet("""
            QScrollArea {
                border: none;
                background-color: #f0f0f0;
            }
            QScrollBar:horizontal {
                height: 10px;
                background: #f0f0f0;
            }
            QScrollBar::handle:horizontal {
                background: #7785AC;
                min-width: 20px;
                border-radius: 5px;
            }
        """)

        # Create container for cards
        container = QWidget()
        horizontal_layout = QHBoxLayout(container)
        horizontal_layout.setSpacing(20)
        horizontal_layout.setContentsMargins(20, 20, 20, 20)
        
        # Add car cards
        for vehicle in self.system.vehicles:
            car_frame = QFrame()
            car_frame.setObjectName("car-card")
            layout = QVBoxLayout(car_frame)  # Added parent widget to layout
            
            # Car Image Container
            image_container = QFrame()
            image_container.setObjectName("image-container")
            image_layout = QVBoxLayout(image_container)
            
            # Car Image
            image_label = QLabel()
            image_path = f"C:/UNI DATA/CP/OOP CEP/FAM CAR RENTAL/assets/cars/{vehicle.make.lower()}_{vehicle.model.lower()}.png"
            if Path(image_path).exists():
                pixmap = QPixmap(image_path)
                scaled_pixmap = pixmap.scaled(220, 150, Qt.KeepAspectRatio, Qt.SmoothTransformation)
                image_label.setPixmap(scaled_pixmap)
            image_label.setAlignment(Qt.AlignCenter)
            image_layout.addWidget(image_label)
            
            # Car details
            title = QLabel(f"{vehicle.make} {vehicle.model} ({vehicle.year})")
            title.setStyleSheet("color: #1a1a2e; font-size: 18px; font-weight: bold;")
            title.setAlignment(Qt.AlignCenter)
            
            vin = QLabel(f"VIN: {vehicle.vin}")
            vin.setStyleSheet("color: #1a1a2e;")
            vin.setAlignment(Qt.AlignCenter)
            
            status = QLabel(f"Status: {'Available' if vehicle.is_available else 'Rented'}")
            status.setStyleSheet("color: #7785AC;")
            status.setAlignment(Qt.AlignCenter)
            
            # Remove button
            remove_btn = QPushButton("Remove Vehicle")
            remove_btn.setStyleSheet("background-color: #ff4d4d; color: white; font-weight: bold;")
            remove_btn.clicked.connect(lambda checked, v=vehicle: self.handle_remove_vehicle(v))
            
            # Add widgets to layout
            layout.addWidget(title)
            layout.addWidget(image_container)
            layout.addWidget(vin)
            layout.addWidget(status)
            layout.addWidget(remove_btn)
            
            horizontal_layout.addWidget(car_frame)
        
        horizontal_layout.addStretch()
        scroll_area.setWidget(container)
        self.content_layout.addWidget(scroll_area)
    def handle_remove_vehicle(self, vehicle):
        try:
            if QMessageBox.question(self, "Confirm Removal", 
                f"Are you sure you want to remove {vehicle.make} {vehicle.model}?",
                QMessageBox.Yes | QMessageBox.No) == QMessageBox.Yes:
                self.system.remove_vehicle(vehicle.vin)
                QMessageBox.information(self, "Success", "Vehicle removed successfully!")
                self.show_car_management()  # Refresh the view
        except Exception as e:
            QMessageBox.warning(self, "Error", str(e))

    def show_add_car(self):
        if not isinstance(self.user, Admin):
            QMessageBox.warning(self, "Error", "Only admin users can add cars!")
            return
            
        dialog = QDialog(self)
        dialog.setWindowTitle("Add New Car")
        dialog.setStyleSheet(StyleSheet.MAIN_STYLE)
        layout = QFormLayout()
        
        # Create input fields
        fields = {}
        fields['vin'] = QLineEdit()
        fields['make'] = QLineEdit()
        fields['model'] = QLineEdit()
        fields['year'] = QSpinBox()
        fields['year'].setRange(2000, 2025)
        fields['daily_rate'] = QDoubleSpinBox()
        fields['daily_rate'].setRange(1000, 100000)
        fields['seating'] = QSpinBox()
        fields['seating'].setRange(2, 8)
        fields['transmission'] = QLineEdit()
        fields['fuel_type'] = QLineEdit()
        
        # Add fields to layout
        for key, field in fields.items():
            label = QLabel(key.replace('_', ' ').title() + ':')
            label.setStyleSheet("font-family: 'Montserrat';")
            layout.addRow(label, field)
        
        # Add buttons
        buttons = QHBoxLayout()
        save_btn = QPushButton("Save")
        cancel_btn = QPushButton("Cancel")
        buttons.addWidget(save_btn)
        buttons.addWidget(cancel_btn)
        layout.addRow(buttons)
        
        dialog.setLayout(layout)
        
        def handle_save():
            try:
                car_data = {
                    'vin': fields['vin'].text(),
                    'make': fields['make'].text(),
                    'model': fields['model'].text(),
                    'year': fields['year'].value(),
                    'daily_rate': fields['daily_rate'].value(),
                    'seating': fields['seating'].value(),
                    'transmission': fields['transmission'].text(),
                    'fuel_type': fields['fuel_type'].text(),
                    'is_available': True
                }
                
                # Continuing from where it was cut off in show_add_car method:
                self.system.add_vehicle(car_data)
                QMessageBox.information(dialog, "Success", "Car added successfully!")
                dialog.accept()
                self.show_available_cars()  # Refresh the view
            except Exception as e:
                QMessageBox.warning(dialog, "Error", str(e))
        
        save_btn.clicked.connect(handle_save)
        cancel_btn.clicked.connect(dialog.reject)
        
        dialog.exec()

    def handle_return_vehicle(self):
        try:
            self.system.return_vehicle(self.user.username)
            QMessageBox.information(self, "Success", "Vehicle returned successfully!")
            self.show_my_rentals()  # Refresh the view
        except Exception as e:
            QMessageBox.warning(self, "Error", str(e))

    def logout(self):
        reply = QMessageBox.question(
            self, 
            'Confirm Logout',
            'Are you sure you want to logout?',
            QMessageBox.Yes | QMessageBox.No,
            QMessageBox.No
        )
        
        if reply == QMessageBox.Yes:
            # Save system state
            self.system.shutdown()
            # Switch back to login window
            self.stacked_widget.setCurrentIndex(0)
            # Clear login fields
            login_window = self.stacked_widget.widget(0)
            login_window.username_input.clear()
            login_window.password_input.clear()
class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("FAM CAR RENTAL SYSTEM")
        self.setMinimumSize(1200, 700)
        
        icon_path = "C:/UNI DATA/CP/OOP CEP/FAM CAR RENTAL/assets/icon.png"
        if Path(icon_path).exists():
            self.setWindowIcon(QIcon(icon_path))
    
        # Load Montserrat font
        font_id = QFontDatabase.addApplicationFont("C:/UNI DATA/CP/OOP CEP/FAM CAR RENTAL/assets/fonts/Montserrat-Regular.ttf")
        font_id_bold = QFontDatabase.addApplicationFont("C:/UNI DATA/CP/OOP CEP/FAM CAR RENTAL/assets/fonts/Montserrat-Bold.ttf")
        font_id_medium = QFontDatabase.addApplicationFont("C:/UNI DATA/CP/OOP CEP/FAM CAR RENTAL/assets/fonts/Montserrat-Medium.ttf")
        
        # Initialize the car rental system
        self.system = CarRentalSystem()
        
        # Add default admin if none exists
        if not any(isinstance(user, Admin) for user in self.system.users):
            admin = Admin(
                username="admin",
                password="admin123",
                first_name="Admin",
                last_name="User",
                email="admin@famcar.com",
                phone="1234567890",
                address="Admin Office"
            )
            self.system.users.append(admin)
            self.system.db.save_all(self.system.users, self.system.vehicles, self.system.rentals)
        
        # Create stacked widget
        self.stacked_widget = QStackedWidget()
        self.setCentralWidget(self.stacked_widget)
        
        # Create and add login window
        login_window = LoginWindow(self.system, self.stacked_widget)
        self.stacked_widget.addWidget(login_window)
        
        # Apply stylesheet
        self.setStyleSheet(StyleSheet.MAIN_STYLE)

    def closeEvent(self, event):
        self.system.shutdown()
        event.accept()

if __name__ == "__main__":
    app = QApplication(sys.argv)
    
    # Set application icon
    icon_path = "C:/UNI DATA/CP/OOP CEP/FAM CAR RENTAL/assets/icon.png"
    if Path(icon_path).exists():
        app.setWindowIcon(QIcon(icon_path))
    
    window = MainWindow()
    window.show()
    sys.exit(app.exec())