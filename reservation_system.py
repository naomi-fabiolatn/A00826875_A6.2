"""
Reservation System Module
This module provides classes for handling Hotels, Customers, and Reservations,
including methods for saving and loading data persistently.
"""

import json
import os
import unittest


class Hotel:
    """Represents a hotel entity."""

    def __init__(self, hotel_id, name, location, rooms_available):
        """Initializes a Hotel instance with the given attributes."""
        if not hotel_id or not isinstance(hotel_id, int):
            raise ValueError("Invalid hotel ID")
        if rooms_available < 0:
            raise ValueError("Rooms available cannot be negative")
        self.hotel_id = hotel_id
        self.name = name
        self.location = location
        self.rooms_available = rooms_available

    def to_dict(self):
        """Converts the hotel instance into a dictionary."""
        return {
            "hotel_id": self.hotel_id,
            "name": self.name,
            "location": self.location,
            "rooms_available": self.rooms_available
        }

    @staticmethod
    def save_hotels(hotels, filename="hotels.json"):
        """Saves a list of hotels to a JSON file."""
        with open(filename, "w", encoding="utf-8") as file:
            json.dump([hotel.to_dict() for hotel in hotels], file, indent=4)

    @staticmethod
    def load_hotels(filename="hotels.json"):
        """Loads hotels from a JSON file."""
        if not os.path.exists(filename):
            return []
        with open(filename, "r", encoding="utf-8") as file:
            return [Hotel(**data) for data in json.load(file)]


class Customer:
    """Represents a customer entity."""

    def __init__(self, customer_id, name, contact_info):
        """Initializes a Customer instance with the given attributes."""
        if not customer_id or not isinstance(customer_id, int):
            raise ValueError("Invalid customer ID")
        self.customer_id = customer_id
        self.name = name
        self.contact_info = contact_info

    def to_dict(self):
        """Converts the customer instance into a dictionary."""
        return {
            "customer_id": self.customer_id,
            "name": self.name,
            "contact_info": self.contact_info
        }

    @staticmethod
    def save_customers(customers, filename="customers.json"):
        """Saves a list of customers to a JSON file."""
        with open(filename, "w", encoding="utf-8") as file:
            json.dump(
                [customer.to_dict() for customer in customers],
                file,
                indent=4
            )

    @staticmethod
    def load_customers(filename="customers.json"):
        """Loads customers from a JSON file."""
        if not os.path.exists(filename):
            return []
        with open(filename, "r", encoding="utf-8") as file:
            return [Customer(**data) for data in json.load(file)]


class Reservation:
    """Represents a reservation entity."""

    def __init__(self, reservation_id, customer_id, hotel_id):
        """Initializes a Reservation instance with the given attributes."""
        if not reservation_id or not isinstance(reservation_id, int):
            raise ValueError("Invalid reservation ID")
        self.reservation_id = reservation_id
        self.customer_id = customer_id
        self.hotel_id = hotel_id

    def to_dict(self):
        """Converts the reservation instance into a dictionary."""
        return {
            "reservation_id": self.reservation_id,
            "customer_id": self.customer_id,
            "hotel_id": self.hotel_id
        }

    @staticmethod
    def save_reservations(reservations, filename="reservations.json"):
        """Saves a list of reservations to a JSON file."""
        with open(filename, "w", encoding="utf-8") as file:
            json.dump([res.to_dict() for res in reservations], file, indent=4)

    @staticmethod
    def load_reservations(filename="reservations.json"):
        """Loads reservations from a JSON file."""
        if not os.path.exists(filename):
            return []
        with open(filename, "r", encoding="utf-8") as file:
            return [Reservation(**data) for data in json.load(file)]


# Unit Tests
class TestHotelReservation(unittest.TestCase):
    """Unit tests for the Hotel Reservation System."""

    def test_create_hotel_invalid_id(self):
        """
        Tests that creating a hotel with an invalid ID raises a ValueError.
        """
        with self.assertRaises(ValueError):
            Hotel("invalid", "Test Hotel", "Nowhere", 10)

    def test_create_hotel_negative_rooms(self):
        """
        Tests that creating a hotel with negative rooms raises a ValueError.
        """
        with self.assertRaises(ValueError):
            Hotel(1, "Test Hotel", "Nowhere", -5)

    def test_load_hotels_no_file(self):
        """
        Tests that load_hotels() returns an empty list if the file is missing.
        """
        if os.path.exists("hotels.json"):
            os.remove("hotels.json")
        self.assertEqual(Hotel.load_hotels(), [])

    def test_create_customer_invalid_id(self):
        """
        Tests that creating a customer with an invalid ID raises a ValueError.
        """
        with self.assertRaises(ValueError):
            Customer("", "John Doe", "john@example.com")

    def test_load_customers_no_file(self):
        """
        Tests that load_customers() returns an empty
        list if the file is missing.
        """
        if os.path.exists("customers.json"):
            os.remove("customers.json")
        self.assertEqual(Customer.load_customers(), [])

    def test_create_reservation_invalid_id(self):
        """
        Tests that creating a reservation with an invalid ID
        raises a ValueError.
        """
        with self.assertRaises(ValueError):
            Reservation("invalid", 1, 1)

    def test_cancel_nonexistent_reservation(self):
        """
        Tests that canceling a nonexistent reservation returns None.
        """
        reservations = Reservation.load_reservations()
        non_existent_reservation = next(
            (r for r in reservations if r.reservation_id == 999),
            None
            )
        self.assertIsNone(non_existent_reservation,
                          "La reserva no debería existir"
                          )

    def test_load_reservations_no_file(self):
        """
        Tests that load_reservations() returns an empty list
        if the file is missing.
        """
        if os.path.exists("reservations.json"):
            os.remove("reservations.json")
        self.assertEqual(Reservation.load_reservations(), [])

    def test_create_hotel_valid(self):
        """Tests that a valid hotel is created successfully."""
        hotel = Hotel(1, "Valid Hotel", "City", 5)
        self.assertEqual(hotel.name, "Valid Hotel")

    def test_create_customer_valid(self):
        """Tests that a valid customer is created successfully."""
        customer = Customer(1, "Alice", "alice@example.com")
        self.assertEqual(customer.name, "Alice")

    def test_create_reservation_valid(self):
        """Tests that a valid reservation is created successfully."""
        reservation = Reservation(1, 1, 1)
        self.assertEqual(reservation.reservation_id, 1)

    def test_create_hotel_empty_name(self):
        """
        Tests that creating a hotel with an empty name is allowed.
        """
        hotel = Hotel(2, "", "Unknown", 5)
        self.assertEqual(hotel.name, "")

    def test_save_and_load_hotels(self):
        """
        Tests that saving and loading hotels from JSON works correctly.
        """
        hotels = [Hotel(3, "Test Hotel", "City", 10)]
        Hotel.save_hotels(hotels)
        loaded_hotels = Hotel.load_hotels()
        self.assertEqual(loaded_hotels[0].name, "Test Hotel")

    def test_customer_to_dict(self):
        """
        Tests that Customer.to_dict() returns the correct dictionary.
        """
        customer = Customer(1, "John Doe", "john@example.com")
        expected = {"customer_id": 1,
                    "name": "John Doe",
                    "contact_info": "john@example.com"
                    }
        self.assertEqual(customer.to_dict(), expected)

    def test_reservation_to_dict(self):
        """
        Tests that Reservation.to_dict() returns the correct dictionary.
        """
        reservation = Reservation(1, 1, 1)
        expected = {"reservation_id": 1, "customer_id": 1, "hotel_id": 1}
        self.assertEqual(reservation.to_dict(), expected)

    def test_save_customers(self):
        """
        Tests that customers are saved correctly to JSON.
        """
        customers = [Customer(1, "Alice", "alice@example.com")]
        Customer.save_customers(customers)
        with open("customers.json", "r", encoding="utf-8") as file:
            data = json.load(file)
        self.assertEqual(data[0]["name"], "Alice")

    def test_save_reservations(self):
        """
        Tests that reservations are saved correctly to JSON.
        """
        reservations = [Reservation(1, 1, 1)]
        Reservation.save_reservations(reservations)
        with open("reservations.json", "r", encoding="utf-8") as file:
            data = json.load(file)
        self.assertEqual(data[0]["reservation_id"], 1)

    def test_load_customers_existing_file(self):
        """
        Tests that load_customers() correctly loads data from an existing file.
        """
        customers = [Customer(2, "Bob", "bob@example.com")]
        Customer.save_customers(customers)
        loaded_customers = Customer.load_customers()
        self.assertEqual(loaded_customers[0].name, "Bob")

    def test_load_reservations_existing_file(self):
        """
        Tests that load_reservations() correctly loads
        data from an existing file.
        """
        reservations = [Reservation(2, 2, 2)]
        Reservation.save_reservations(reservations)
        loaded_reservations = Reservation.load_reservations()
        self.assertEqual(loaded_reservations[0].reservation_id, 2)


if __name__ == "__main__":
    unittest.main()
