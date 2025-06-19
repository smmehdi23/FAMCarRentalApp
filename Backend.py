from abc import abstractmethod
from dataclasses import dataclass, field
from datetime import datetime
from typing import Optional, List, Dict, Any
from pathlib import Path
import json
from decimal import Decimal
from uuid import uuid4

class CarRentalError(Exception):
    def __init__(self, message: str):
        self.message = f"{message}"

    def __str__(self):
        return self.message


class AuthenticationError(CarRentalError):
    def __init__(self, message: str):
        super().__init__(message)


class InvalidCredentialsError(AuthenticationError):
    def __init__(self):
        super().__init__("Invalid username or password")


class RegistrationError(CarRentalError):
    def __init__(self, message: str):
        super().__init__(message)

class InvalidSecretCodeError(CarRentalError):
    def __init__(self):
        super().__init__("Please enter the correct secret code!")


class UsernameExistsError(RegistrationError):
    def __init__(self, username: str):
        super().__init__(f"Username '{username}' already exists")


class PaymentError(CarRentalError):
    def __init__(self, message: str):
        super().__init__(message)


class InsufficientBalanceError(PaymentError):
    def __init__(self, current: float, required: float):
        super().__init__(f"Insufficient balance: Current Pkr{current:.2f}, Required PKr{required:.2f}")


class InventoryError(CarRentalError):
    def __init__(self, message: str):
        super().__init__(message)


class InvalidVehicleYearError(InventoryError):
    def __init__(self, year: int):
        super().__init__(f"Year {year} is invalid. Must be between 2000 and 2025.")


class DuplicateVehicleError(CarRentalError):
    def __init__(self, License_Plate: str):
        super().__init__(f"Vehicle {License_Plate} already exists")


class VehicleNotFoundError(CarRentalError):
    def __init__(self, License_Plate: str):
        super().__init__(f"Vehicle {License_Plate} not found")


class VehicleNotAvailableError(InventoryError):
    def __init__(self, License_Plate: str):
        super().__init__(f"Vehicle {License_Plate} is not available")


class RentalError(CarRentalError):
    def __init__(self, message: str):
        super().__init__(message)


class InvalidUserError(CarRentalError):
    def __init__(self):
        super().__init__("Invalid user type")


class ActiveRentalExistsError(CarRentalError):
    def __init__(self, username: str):
        super().__init__(f"User {username} has active rental")


class NoActiveRentalError(CarRentalError):
    def __init__(self, username: str):
        super().__init__(f"No active rental for {username}")


class InvalidRentalDurationError(RentalError):
    def __init__(self, message: str):
        super().__init__(message)


class DatabaseError(CarRentalError):
    def __init__(self, message: str):
        super().__init__(message)


@dataclass
class AbstractUser:
    username: str
    password: str
    first_name: str
    last_name: str
    email: str
    phone: str
    address: str

    @property
    @abstractmethod
    def balance(self) -> float:
        pass

    @abstractmethod
    def deduct_balance(self, amount: float):
        pass

    def get_role(self) -> str:
        raise NotImplementedError


@dataclass
class Customer(AbstractUser):
    _balance: float = 0.0
    current_rental: Optional['Rental'] = None
    rental_history: List['Rental'] = field(default_factory=list)

    def get_role(self) -> str:
        return "customer"

    @property
    def balance(self) -> float:
        return self._balance

    def add_balance(self, amount: float):
        if amount <= 0:
            raise ValueError("Amount must be positive")
        self._balance = round(self._balance + amount, 2)

    def deduct_balance(self, amount: float):
        if amount > self._balance:
            raise InsufficientBalanceError(self._balance, amount)
        self._balance = round(self._balance - amount, 2)


@dataclass
class Admin(AbstractUser):
    is_administrator: bool = field(default=True, init=False)
    
    def get_role(self) -> str:
        return "admin"


@dataclass
class Vehicle:
    License_Plate: str
    make: str
    model: str
    year: int
    daily_rate: float 
    seating: int
    transmission: str
    fuel_type: str
    is_available: bool = True

    def __post_init__(self):
        if not (2000 <= self.year <= 2025):
            raise InvalidVehicleYearError(self.year)


@dataclass
class Rental:
    user: Customer
    vehicle: Vehicle
    start_date: datetime
    end_date: datetime
    id: str = field(default_factory=lambda: str(uuid4()))

    def __post_init__(self):
        if self.start_date >= self.end_date:
            raise InvalidRentalDurationError("End date must be after start date")

    @property
    def duration_days(self) -> int:
        return (self.end_date - self.start_date).days

    @property
    def total_cost(self) -> Decimal:
        return Decimal(str(self.vehicle.daily_rate)) * Decimal(str(self.duration_days))


class Database:
    def __init__(self, system: 'CarRentalSystem', data_dir: str = 'data'):
        self.data_dir = Path(data_dir)
        self.data_dir.mkdir(exist_ok=True)
        self.system = system
        self.users_file = self.data_dir / 'users.json'
        self.vehicles_file = self.data_dir / 'vehicles.json'
        self.rentals_file = self.data_dir / 'rentals.json'

    def load_users(self) -> List[AbstractUser]:
        return self._load_entities(self.users_file, self._decode_user)

    def load_vehicles(self) -> List[Vehicle]:
        return self._load_entities(self.vehicles_file, self._decode_vehicle)

    def load_rentals(self) -> List[Rental]:
        return self._load_entities(self.rentals_file, self._decode_rental)

    @staticmethod
    def _load_entities(path: Path, decoder):
        if not path.exists():
            return []
        with open(path) as f:
            return [decoder(data) for data in json.load(f)]

    def save_all(self, users: List[AbstractUser], vehicles: List[Vehicle], rentals: List[Rental]):
        self._save_entities(self.users_file, users, self._encode_user)
        self._save_entities(self.vehicles_file, vehicles, self._encode_vehicle)
        self._save_entities(self.rentals_file, rentals, self._encode_rental)

    def _save_entities(self, path: Path, entities: List[Any], encoder):
        try:
            with open(path, 'w') as f:
                json.dump([encoder(e) for e in entities], f, default=self._json_default, indent=2)
        except Exception as e:
            raise DatabaseError(f"Failed to save {path.name}: {str(e)}")

    @staticmethod
    def _json_default(obj):
        if isinstance(obj, datetime):
            return obj.isoformat()
        if isinstance(obj, Decimal):
            return str(obj)
        raise TypeError(f"Object of type {obj.__class__.__name__} is not JSON serializable")

    @staticmethod
    def _encode_user(user: AbstractUser) -> Dict:
        data = {
            "type": "Admin" if isinstance(user, Admin) else "Customer",
            "username": user.username,
            "password": user.password,
            "first_name": user.first_name,
            "last_name": user.last_name,
            "email": user.email,
            "phone": user.phone,
            "address": user.address
        }
        if isinstance(user, Customer):
            data.update({
                "balance": user.balance,
                "current_rental": user.current_rental.id if user.current_rental else None,
                "rental_history": [r.id for r in user.rental_history]
            })
        return data

    @staticmethod
    def _decode_user(data: Dict) -> AbstractUser:
        user_type = data.pop("type")
        if user_type == "Admin":
            return Admin(
                username=data['username'],
                password=data['password'],
                first_name=data['first_name'],
                last_name=data['last_name'],
                email=data['email'],
                phone=data['phone'],
                address=data['address'])
        if user_type == "Customer":
            return Customer(
                username=data['username'],
                password=data['password'],
                first_name=data['first_name'],
                last_name=data['last_name'],
                email=data['email'],
                phone=data['phone'],
                address=data['address'],
                _balance=data.get('balance', 0.0)
            )
        return Admin(**data)

    @staticmethod
    def _encode_vehicle(vehicle: Vehicle) -> Dict:
        data = {
            "type": "Vehicle",
            "License_Plate": vehicle.License_Plate,
            "make": vehicle.make,
            "model": vehicle.model,
            "year": vehicle.year,
            "daily_rate": vehicle.daily_rate,
            "seating": vehicle.seating,
            "transmission": vehicle.transmission,
            "fuel_type": vehicle.fuel_type,
            "is_available": vehicle.is_available
        }

    @staticmethod
    def _decode_vehicle(data: Dict) -> Vehicle:
        
        return Vehicle(
            License_Plate=data['License_Plate'],
            make=data['make'],
            model=data['model'],
            year=data['year'],
            daily_rate=data['daily_rate'],
            seating=data['seating'],
            transmission=data['transmission'],
            fuel_type=data['fuel_type'],
            is_available=data['is_available']
        )

    @staticmethod
    def _encode_rental(rental: Rental) -> Dict:
        return {
            "id": rental.id,
            "user": rental.user.username,
            "vehicle": rental.vehicle.License_Plate,
            "start_date": rental.start_date,
            "end_date": rental.end_date
        }

    def _decode_rental(self, data: Dict) -> Rental:
        try:
            user = next(u for u in self.system.users if u.username == data['user'] and isinstance(u, Customer))
            vehicle = next(v for v in self.system.vehicles if v.License_Plate == data['vehicle'])
        except StopIteration:
            raise DatabaseError("Invalid rental reference")

        return Rental(
            user=user,
            vehicle=vehicle,
            start_date=datetime.fromisoformat(data['start_date']),
            end_date=datetime.fromisoformat(data['end_date']),
            id=data['id']
        )


class CarRentalSystem:
    def __init__(self):
        self.db = Database(self)
        self.users: List[AbstractUser] = []
        self.vehicles: List[Vehicle] = []
        self.rentals: List[Rental] = []
        self._load_data()

    def _load_data(self):
        self.users = self.db.load_users()
        self.vehicles = self.db.load_vehicles()
        self.rentals = self.db.load_rentals()

    def register_user(self, user_data: dict) -> Customer:
        if any(u.username == user_data['username'] for u in self.users):
            raise UsernameExistsError(user_data['username'])
        
        # check for secret code
        secret_code = user_data.pop('secret_code', None)
        
        if secret_code:
            if secret_code != "CCLG2024": 
                raise InvalidSecretCodeError()
            user = Admin(**user_data)
        else:
            user = Customer(**user_data)

        # save and return the user
        self.users.append(user)
        self.db.save_all(self.users, self.vehicles, self.rentals)
        return user

    def authenticate(self, username: str, password: str) -> AbstractUser:
        user = next((u for u in self.users if u.username == username and u.password == password), None)
        if not user:
            raise InvalidCredentialsError()
        return user

    def get_active_rentals(self) -> List[Rental]:
        active = [r for r in self.rentals if not r.vehicle.is_available]
        return active

    def rent_vehicle(self, username: str, License_Plate: str, start_date: datetime, end_date: datetime) -> Rental:
        user = next((u for u in self.users if u.username == username), None)
        vehicle = next((v for v in self.vehicles if v.License_Plate == License_Plate), None)

        if not user or not isinstance(user, Customer):
            raise InvalidUserError()
        if not vehicle or not vehicle.is_available:
            raise VehicleNotAvailableError(License_Plate)
        if user.current_rental:
            raise ActiveRentalExistsError(username)

        rental = Rental(user=user, vehicle=vehicle, start_date=start_date, end_date=end_date)

        if user.balance < rental.total_cost:
            raise InsufficientBalanceError(user.balance, float(rental.total_cost))

        user.deduct_balance(float(rental.total_cost))
        vehicle.is_available = False
        user.current_rental = rental
        self.rentals.append(rental)
        return rental

    def return_vehicle(self, username: str) -> None:
        user = next((u for u in self.users if u.username == username), None)
        if not user or not isinstance(user, Customer):
            raise InvalidUserError()
        if not user.current_rental:
            raise NoActiveRentalError(username)

        user.rental_history.append(user.current_rental)
        user.current_rental.vehicle.is_available = True
        user.current_rental = None

    def add_vehicle(self, vehicle_data: Dict) -> Vehicle:
        if any(v.License_Plate == vehicle_data['License_Plate'] for v in self.vehicles):
            raise DuplicateVehicleError(vehicle_data['License_Plate'])

        vehicle = Vehicle(**vehicle_data)
        self.vehicles.append(vehicle)
        return vehicle

    def remove_vehicle(self, License_Plate: str) -> None:
        vehicle = next((v for v in self.vehicles if v.License_Plate == License_Plate), None)
        if not vehicle:
            raise VehicleNotFoundError(License_Plate)
        if not vehicle.is_available:
            raise VehicleNotAvailableError(License_Plate)
        self.vehicles.remove(vehicle)

    def get_available_vehicles(self) -> List[Vehicle]:
        return [v for v in self.vehicles if v.is_available]

    def get_user_rental_history(self, username: str) -> List[Rental]:
        user = next((u for u in self.users if u.username == username), None)
        if not user or not isinstance(user, Customer):
            raise InvalidUserError()
        return user.rental_history

    def add_funds(self, username: str, amount: float) -> float:
        user = next((u for u in self.users if u.username == username), None)
        if not user or not isinstance(user, Customer):
            raise InvalidUserError()
        user.add_balance(amount)
        return user.balance

    def shutdown(self):
        self.db.save_all(self.users, self.vehicles, self.rentals)