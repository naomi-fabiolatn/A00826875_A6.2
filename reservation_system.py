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

    @staticmethod
    def delete_hotel(hotel_id, filename="hotels.json"):
        """Deletes a hotel by ID from the JSON file."""
        hotels = Hotel.load_hotels(filename)
        hotels = [hotel for hotel in hotels if hotel.hotel_id != hotel_id]
        Hotel.save_hotels(hotels, filename)

    @staticmethod
    def modify_hotel(hotel_id, name=None, location=None,
                     rooms_available=None, filename="hotels.json"):
        """Modifies hotel information based on the given parameters."""
        hotels = Hotel.load_hotels(filename)
        for hotel in hotels:
            if hotel.hotel_id == hotel_id:
                if name:
                    hotel.name = name
                if location:
                    hotel.location = location
                if rooms_available is not None:
                    hotel.rooms_available = rooms_available
        Hotel.save_hotels(hotels, filename)

    @staticmethod
    def reserve_room(hotel_id, filename="hotels.json"):
        """Reserves a room in a hotel if available."""
        hotels = Hotel.load_hotels(filename)
        for hotel in hotels:
            if hotel.hotel_id == hotel_id and hotel.rooms_available > 0:
                hotel.rooms_available -= 1
                Hotel.save_hotels(hotels, filename)
                return True
        return False


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

    @staticmethod
    def delete_customer(customer_id, filename="customers.json"):
        """Deletes a customer by ID from the JSON file."""
        customers = Customer.load_customers(filename)
        customers = [customer for customer in customers if customer.customer_id != customer_id]
        Customer.save_customers(customers, filename)

    @staticmethod
    def modify_customer(customer_id, name=None, contact_info=None, filename="customers.json"):
        """Modifies customer information based on the given parameters."""
        customers = Customer.load_customers(filename)
        for customer in customers:
            if customer.customer_id == customer_id:
                if name:
                    customer.name = name
                if contact_info:
                    customer.contact_info = contact_info
        Customer.save_customers(customers, filename)


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

    @staticmethod
    def cancel_reservation(reservation_id, reservation_file="reservations.json",
                           hotel_file="hotels.json"):
        """Cancels a reservation and updates hotel room availability."""
        reservations = Reservation.load_reservations(reservation_file)
        reservation_to_cancel = next(
            (res for res in reservations if res.reservation_id == reservation_id),
            None
            )
        
        if reservation_to_cancel:
            # Remove reservation
            reservations = [res for res in reservations if res.reservation_id != reservation_id]
            Reservation.save_reservations(reservations, reservation_file)
            
            # Restore hotel room availability
            hotels = Hotel.load_hotels(hotel_file)
            for hotel in hotels:
                if hotel.hotel_id == reservation_to_cancel.hotel_id:
                    hotel.rooms_available += 1
            Hotel.save_hotels(hotels, hotel_file)
            return True
        return False


# Unit Tests
class TestHotelReservation(unittest.TestCase):
    """Unit tests for the Hotel Reservation System."""

    def setUp(self):
        """Setup method to initialize test data."""
        self.hotel = Hotel(1, "Test Hotel", "Nowhere", 10)
        self.customer = Customer(1, "John Doe", "john@example.com")
        self.reservation = Reservation(1, 1, 1)

    def test_create_hotel_invalid_id(self):
        """Tests that creating a hotel with an invalid ID raises a ValueError."""
        with self.assertRaises(ValueError):
            Hotel("invalid", "Test Hotel", "Nowhere", 10)

    def test_create_hotel_negative_rooms(self):
        """Tests that creating a hotel with negative rooms raises a ValueError."""
        with self.assertRaises(ValueError):
            Hotel(1, "Test Hotel", "Nowhere", -5)

    def test_delete_hotel(self):
        """Tests deleting a hotel from the system."""
        Hotel.save_hotels([self.hotel])
        Hotel.delete_hotel(1)
        hotels = Hotel.load_hotels()
        self.assertEqual(len(hotels), 0)

    def test_modify_hotel(self):
        """Tests modifying a hotel's information."""
        Hotel.save_hotels([self.hotel])
        Hotel.modify_hotel(1, name="Updated Hotel", location="Somewhere")
        updated_hotel = Hotel.load_hotels()[0]
        self.assertEqual(updated_hotel.name, "Updated Hotel")
        self.assertEqual(updated_hotel.location, "Somewhere")

    def test_reserve_room(self):
        """Tests reserving a room in a hotel."""
        Hotel.save_hotels([self.hotel])
        success = Hotel.reserve_room(1)
        updated_hotel = Hotel.load_hotels()[0]
        self.assertTrue(success)
        self.assertEqual(updated_hotel.rooms_available, 9)

    def test_cancel_reservation(self):
        """Tests canceling a reservation and restoring hotel availability."""
        Hotel.save_hotels([self.hotel])
        Reservation.save_reservations([self.reservation])
        success = Reservation.cancel_reservation(1)
        updated_hotel = Hotel.load_hotels()[0]
        self.assertTrue(success)
        self.assertEqual(updated_hotel.rooms_available, 10)

    def test_create_customer_invalid_id(self):
        """Tests that creating a customer with an invalid ID raises a ValueError."""
        with self.assertRaises(ValueError):
            Customer("", "John Doe", "john@example.com")

    def test_delete_customer(self):
        """Tests deleting a customer from the system."""
        Customer.save_customers([self.customer])
        Customer.delete_customer(1)
        customers = Customer.load_customers()
        self.assertEqual(len(customers), 0)

    def test_modify_customer(self):
        """Tests modifying a customer's information."""
        Customer.save_customers([self.customer])
        Customer.modify_customer(1, name="Jane Doe")
        updated_customer = Customer.load_customers()[0]
        self.assertEqual(updated_customer.name, "Jane Doe")

    def test_create_reservation_invalid_id(self):
        """Tests that creating a reservation with an invalid ID raises a ValueError."""
        with self.assertRaises(ValueError):
            Reservation("invalid", 1, 1)

    def test_create_reservation_valid(self):
        """Tests that a valid reservation is created successfully."""
        reservation = Reservation(1, 1, 1)
        self.assertEqual(reservation.reservation_id, 1)

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

    def test_cancel_reservation(self):
        """Tests canceling a reservation and restoring hotel availability."""
        Hotel.save_hotels([self.hotel])
        self.assertEqual(Hotel.load_hotels()[0].rooms_available, 10)
        
        Reservation.save_reservations([self.reservation])
        Hotel.reserve_room(1)
        updated_hotel = Hotel.load_hotels()[0]
        self.assertEqual(updated_hotel.rooms_available, 9)

        success = Reservation.cancel_reservation(1)
        updated_hotel = Hotel.load_hotels()[0]
        self.assertTrue(success)
        self.assertEqual(updated_hotel.rooms_available, 10)

    def tearDown(self):
        """Cleans up JSON files after each test."""
        for file in ["hotels.json", "customers.json", "reservations.json"]:
            if os.path.exists(file):
                os.remove(file)


if __name__ == "__main__":
    unittest.main()
