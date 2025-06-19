**READMEFILE.txt**

---

# FAM Car Rental System  
A Python-based car rental management system with GUI (PySide6) and JSON database.  

---

---

## Features  
- User Roles:  
  - Admin: Add/remove vehicles, view active rentals, manage inventory.  
  - Customer: Rent vehicles, view rental history, add funds.  
- GUI:  
  - Login/registration system.  
  - Interactive dashboards for admins and customers.  
  - Car cards with images, rental calendars, and payment handling.  
- Error Handling: Custom exceptions for invalid inputs, rentals, and authentication.  
- Persistent Storage: Data saved in JSON files (`users.json`, `vehicles.json`, `rentals.json`).  

---

##  Technologies Used  
- Python 3.10  
- PySide6: For GUI components.  
- Dataclasses: For structured data (User, Vehicle, Rental).  
- JSON: Database storage.  

---

##  Setup & Installation  
1. Clone the repository or download the files (`backend.py`, `frontend.py`).  
2. Install dependencies:  
   ```bash  
   pip install PySide6  
   ```   
3. **Run the application**:  
   ```bash  
   python frontend.py  
   ```  

---

##  Configuration  
- Default Admin Credentials:  
  - Username: `admin`  
  - Password: `admin123`  
- Admin Secret Code: `CCLG2024` (required during admin registration).  
- Asset Paths:  
  - Car images: `assets/cars/<make>_<model>.png` (e.g., `toyota_corolla.png`).  
  - Fonts: Place Montserrat `.ttf` files in `assets/fonts/`.  

---

##  Usage Guide  
### Login/Registration  
- Register: Customers can sign up directly. Admins must provide the secret code (`CCLG2024`).  
- Login: Use credentials to access the dashboard.  

### Customer Dashboard  
- Rent a Car:  
  1. Select a car from "Available Cars".  
  2. Choose start/end dates.  
  3. Confirm payment (balance deducted automatically).  
- Add Funds: Via "My Funds" (quick top-up or custom amount).  
- Return Vehicle: Navigate to "My Rentals" and click "Return Vehicle".  

### Admin Dashboard  
- Add/Remove Vehicles**:  
  - Use "Car Management" to remove existing vehicles.  
  - Use "Add New Cars" to add vehicles (ensure valid year: 2000–2025).  
- View Active Rentals**: Table with rental IDs, customers, and costs.  

---

##  File Structure  
```  
├── backend.py           # Core logic (users, vehicles, rentals, database)  
├── frontend.py          # GUI implementation (PySide6)  
├── data/                # Auto-generated JSON database  
│   ├── users.json  
│   ├── vehicles.json  
│   └── rentals.json  
└── assets/              # Images and fonts (optional)  
    ├── cars/  
    ├── fonts/  
    └── icon.png  
```  

---

##  Database Details  
- Users: Stored as `Customer` or `Admin` with encrypted passwords (plaintext for simplicity; **not secure for production**).  
- Vehicles: Includes make, model, year, availability, and daily rate.  
- Rentals: Tracks user-vehicle associations, dates, and total costs.  

---

