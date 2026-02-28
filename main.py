from collections import UserDict
from typing import Optional, List


class AddressBookError(Exception):
    """Base exception class for Address Book application."""
    pass


class PhoneValidationError(AddressBookError):
    """Raised when the phone number validation fails."""
    pass


class Field:
    """Base class for record fields."""
    def __init__(self, value: str):
        self._value = None
        self.value = value

    @property
    def value(self) -> str:
        return self._value

    @value.setter
    def value(self, new_value: str):
        self._value = new_value

    def __str__(self) -> str:
        return str(self.value)


class Name(Field):
    """Field for storing a contact name. Mandatory field."""
    pass


class Phone(Field):
    """Field for storing a phone number with 10-digit validation."""
    @Field.value.setter
    def value(self, new_value: str):
        clean_phone = new_value.strip()
        if not (len(clean_phone) == 10 and clean_phone.isdigit()):
            raise PhoneValidationError("Phone number must contain exactly 10 digits.")
        self._value = clean_phone


class Record:
    """Class for managing contact information and phone numbers."""
    def __init__(self, name: str):
        self.name: Name = Name(name)
        self.phones: List[Phone] = []

    def add_phone(self, phone_number: str) -> None:
        """Adds a new phone number if it doesn't already exist."""
        if not self.find_phone(phone_number):
            self.phones.append(Phone(phone_number))

    def remove_phone(self, phone_number: str) -> None:
        """Removes a phone number. Silent if not found for safety."""
        phone_obj = self.find_phone(phone_number)
        if phone_obj:
            self.phones.remove(phone_obj)

    def edit_phone(self, old_phone: str, new_phone: str) -> None:
        """Updates an existing phone number. Validates new phone before changing."""
        old_phone_obj = self.find_phone(old_phone)
        if old_phone_obj:
            new_phone_obj = Phone(new_phone)
            index = self.phones.index(old_phone_obj)
            self.phones[index] = new_phone_obj

    def find_phone(self, phone_number: str) -> Optional[Phone]:
        """Searches for a phone number and returns the Phone object."""
        for phone in self.phones:
            if phone.value == phone_number.strip():
                return phone
        return None

    def __str__(self) -> str:
        phones_str = "; ".join(p.value for p in self.phones)
        return f"Contact name: {self.name.value}, phones: {phones_str}"


class AddressBook(UserDict):
    """Storage for contact records, inheriting from UserDict."""
    def add_record(self, record: Record) -> None:
        """Adds a record to the address book."""
        self.data[record.name.value] = record

    def find(self, name: str) -> Optional[Record]:
        """Finds a record by name."""
        return self.data.get(name)

    def delete(self, name: str) -> None:
        """Deletes a record by name. Silent if not found."""
        if name in self.data:
            del self.data[name]


if __name__ == "__main__":
    try:
        book = AddressBook()

        john = Record("John")
        john.add_phone("1234567890")
        john.add_phone("5555555555")
        book.add_record(john)

        jane = Record("Jane")
        jane.add_phone("9876543210")
        book.add_record(jane)

        print("--- Address Book ---")
        for name, record in book.data.items():
            print(record)

        john.edit_phone("1234567890", "1112223333")
        print(f"\nUpdated John: {john}")

        found_phone = john.find_phone("5555555555")
        print(f"Found phone: {found_phone}")

        book.delete("Jane")
        print(f"\nBook after deleting Jane:\n{book}")

    except AddressBookError as e:
        print(f"Application Error: {e}")