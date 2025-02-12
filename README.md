# A00826875_A6.2
Ejercicio de programación 3 y pruebas de unidad
# Hotel Reservation System

## Overview
This Python project is a **Hotel Reservation System** that allows users to manage:
- **Hotels** (create, save, load, and retrieve hotel data)
- **Customers** (manage customer information and persistence)
- **Reservations** (create, save, load, and manage reservations between customers and hotels)

All data is stored persistently using **JSON files**.

## Features
### Hotel Management
- Add new hotels with name, location, and available rooms.
- Save and retrieve hotel data from a JSON file.
- Handle invalid input cases (e.g., negative room counts).

### Customer Management
- Create new customers with contact information.
- Save and load customer data.
- Validate inputs to prevent incorrect data storage.

### Reservation Management
- Create reservations linking customers and hotels.
- Store and retrieve reservations.
- Ensure data integrity by handling invalid reservation attempts.

## File Structure
```
├── reservation_system.py  # Main module with classes and methods
├── hotels.json            # Storage for hotel data
├── customers.json         # Storage for customer data
├── reservations.json      # Storage for reservation data
└── README.md              # Project documentation
```

## Running the Tests
This project includes a **unit test suite** using Python’s `unittest` module.
To execute the tests, run the following command:
```bash
python -m unittest reservation_system.py
```
This will run a series of tests to validate the functionality of the system.

## Test Cases Overview
The test suite covers:
- **Creation of hotels, customers, and reservations** with valid and invalid data.
- **JSON file operations** to ensure data persistence works correctly.
- **Edge cases**, including missing files and incorrect inputs.

### Example Test Cases
#### ✅ Valid Test Case
```python
def test_create_hotel_valid(self):
    """Tests that a valid hotel is created successfully."""
    hotel = Hotel(1, "Valid Hotel", "City", 5)
    self.assertEqual(hotel.name, "Valid Hotel")
```
#### ❌ Negative Test Case
```python
def test_create_hotel_invalid_id(self):
    """Tests that creating a hotel with an invalid ID raises a ValueError."""
    with self.assertRaises(ValueError):
        Hotel("invalid", "Test Hotel", "Nowhere", 10)
```

## Code Coverage
To verify code coverage (must be at least **85%**), use `coverage.py`:

### Latest Coverage Report
```
Name                     Stmts   Miss  Cover   
------------------------------------------------
reservation_system.py      264      24     91%      
------------------------------------------------
TOTAL                      264      24     91%
```

```bash
pip install coverage
coverage run --source=reservation_system -m unittest reservation_system.py
coverage report -m
```
This will generate a report indicating which lines of code are covered by the tests.
