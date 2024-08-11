from collections import UserDict
import re

class Field:
    def __init__(self, value):
        self.value = value

    def __str__(self):
        return str(self.value)

class Name(Field):
    def __init__(self, value):
        if not value:
            raise ValueError("Name cannot be empty")
        super().__init__(value)

class Phone(Field):
    def __init__(self, value):
        if not self.validate(value):
            raise ValueError("Invalid phone number")
        super().__init__(value)

    @staticmethod
    def validate(value):
        return bool(re.fullmatch(r'\d{10}', value))

class Record:
    def __init__(self, name):
        self.name = Name(name)
        self.phones = []

    def add_phone(self, phone):
        phone = Phone(phone)
        self.phones.append(phone)

    def remove_phone(self, phone):
        phone_to_remove = next((p for p in self.phones if p.value == phone), None)
        if phone_to_remove:
            self.phones.remove(phone_to_remove)
        else:
            raise ValueError("Phone number not found")

    def edit_phone(self, old_phone, new_phone):
        old_phone_obj = next((p for p in self.phones if p.value == old_phone), None)
        if old_phone_obj:
            if not Phone.validate(new_phone):
                raise ValueError("Invalid new phone number")
            old_phone_obj.value = new_phone
        else:
            raise ValueError("Old phone number not found")

    def find_phone(self, phone):
        return next((p for p in self.phones if p.value == phone), None)

    def __str__(self):
        return f"Contact name: {self.name.value}, phones: {'; '.join(p.value for p in self.phones)}"

class AddressBook(UserDict):
    def add_record(self, record):
        if not isinstance(record, Record):
            raise ValueError("Record must be an instance of Record")
        self.data[record.name.value] = record

    def find(self, name):
        return self.data.get(name, None)

    def delete(self, name):
        if name in self.data:
            del self.data[name]
        else:
            raise ValueError("Record not found")

    def __str__(self):
        return '\n'.join(str(record) for record in self.data.values())

# Example usage:
if __name__ == "__main__":
    book = AddressBook()

    john_record = Record("John")
    john_record.add_phone("1234567890")
    john_record.add_phone("5555555555")
    book.add_record(john_record)

    jane_record = Record("Jane")
    jane_record.add_phone("9876543210")
    book.add_record(jane_record)

    print(book)

    john = book.find("John")
    if john:
        john.edit_phone("1234567890", "1112223333")
        print(john)

        found_phone = john.find_phone("5555555555")
        print(f"{john.name}: {found_phone}")

    book.delete("Jane")
    print(book)
