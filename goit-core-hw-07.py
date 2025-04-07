from datetime import datetime, timedelta

class Field:
    def __init__(self, value):
        self.value = value

    def __str__(self):
        return str(self.value)

class Birthday(Field):
    def __init__(self, value):
        super().__init__(value)
        try:
            self.value = datetime.strptime(value, "%d.%m.%Y")
        except ValueError:
            raise ValueError("Invalid date format. Use DD.MM.YYYY")

class Name(Field):
    pass

class Record:
    def __init__(self, name):
        self.name = Name(name)
        self.phones = []
        self.birthday = None

    def add_phone(self, phone):
        self.phones.append(phone)

    def set_birthday(self, birthday):
        self.birthday = Birthday(birthday)

class AddressBook:
    def __init__(self):
        self.contacts = []

    def find(self, name):
        for contact in self.contacts:
            if contact.name.value == name:
                return contact
        return None

    def add_record(self, record):
        self.contacts.append(record)

    def get_upcoming_birthdays(self):
        today = datetime.today()
        upcoming_birthdays = []
        for contact in self.contacts:
            if contact.birthday:
                delta = contact.birthday.value - today
                if timedelta(days=0) <= delta <= timedelta(days=7):
                    birthday_date = contact.birthday.value
                    if birthday_date.weekday() >= 5:
                        birthday_date += timedelta(days=(7 - birthday_date.weekday()))
                    upcoming_birthdays.append({
                        "name": contact.name,
                        "birthday": birthday_date.strftime("%d.%m.%Y")
                    })

        return upcoming_birthdays

def input_error(func):
    def inner(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except ValueError:
            return "Введіть ім'я та номер телефону."
        except KeyError:
            return "Контакт не знайдеон."
        except IndexError:
            return "Невідомий аргумент"
    return inner

@input_error
def add_birthday(args, book):
    name, birthday = args
    record = book.find(name)
    if record:
        record.set_birthday(birthday)
        return f"День народження для {name} додано."
    else:
        return "Контакт не знайдено."

@input_error
def show_birthday(args, book):
    name = args[0]
    record = book.find(name)
    if record and record.birthday:
        return f"Ім'я: {name}, день народження: {record.birthday.value.strftime('%d.%m.%Y')}"
    return f"Не встановлено день народження для {name}."

@input_error
def birthdays(args, book):
    upcoming_birthdays = book.get_upcoming_birthdays()
    if upcoming_birthdays:
        return "\n".join([f"{entry['name']} - {entry['birthday']}" for entry in upcoming_birthdays])
    return "Немає найближчих днів народження."

@input_error
def add_contact(args, book: AddressBook):
    name, phone, *_ = args
    record = book.find(name)
    message = "Контакт оновлено."
    if record is None:
        record = Record(name)
        book.add_record(record)
        message = "Контакт додано."
    if phone:
        record.add_phone(phone)
    return message

def parse_input(user_input):
    return user_input.split()

def main():
    book = AddressBook()
    print("Welcome to the assistant bot!")
    while True:
        user_input = input("Enter a command: ")
        command, *args = parse_input(user_input)

        if command in ["close", "exit"]:
            print("Good bye!")
            break

        elif command == "hello":
            print("How can I help you?")

        elif command == "add":
            if args:
                name = args[0]
                phone = args[1] if len(args) > 1 else ""
                print(add_contact([name, phone], book))
            else:
                print("Введіть ім'я та номер телефону.")

        elif command == "change":
            if len(args) >= 2:
                name, new_phone = args[0], args[1]
                record = book.find(name)
                if record:
                    record.phones = [new_phone]
                    print(f"Телефон для {name} оновлено.")
                else:
                    print("Контакт не знайдено.")
            else:
                print("Введіть ім'я та номер телефону.")

        elif command == "phone":
            name = args[0] if args else ""
            record = book.find(name)
            if record:
                print(f"Номер телефону для {name}: {', '.join(record.phones)}")
            else:
                print("Контакт не знайдено.")

        elif command == "all":
            if book.contacts:
                for contact in book.contacts:
                    print(f"{contact.name.value} - Phones: {', '.join(contact.phones)}")
                    if contact.birthday:
                        print(f"Birthday: {contact.birthday.value.strftime('%d.%m.%Y')}")
            else:
                print("Немає контактів.")

        elif command == "add-birthday":
            if len(args) >= 2:
                print(add_birthday(args, book))
            else:
                print("Будь ласка введіть ім'я та день народження.")

        elif command == "show-birthday":
                print(show_birthday(args, book))

        elif command == "birthdays":
            print(birthdays(args, book))

        else:
            print("Invalid command.")

if __name__ == "__main__":
    main()
