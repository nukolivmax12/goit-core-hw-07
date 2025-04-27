from collections import UserDict
from datetime import datetime, timedelta


class Field:
    def __init__(self, value):
        self.value = value

    def __str__(self):
        return str(self.value)


class Name(Field):
    pass


class Phone(Field):
    def __init__(self, value):
        if len(value) == 10 and value.isdigit():
            super().__init__(value)
        else:
            raise ValueError("Номер телефону має містити 10 цифр.")


class Birthday(Field):
    def __init__(self, value):
        try:
            datetime.strptime(value, "%d.%m.%Y")
            super().__init__(value)
        except ValueError:
            raise ValueError("Невірний формат дати. Використовуйте DD.MM.YYYY")


class Record:
    def __init__(self, name):
        self.name = Name(name)
        self.phones = []
        self.birthday = None

    def add_phone(self, phone):
        self.phones.append(Phone(phone))

    def edit_phone(self, old_phone, new_phone):
        for phone in self.phones:
            if phone.value == old_phone:
                phone.value = Phone(new_phone).value
                return
        raise ValueError("Номер не знайдено.")

    def remove_phone(self, phone):
        for p in self.phones:
            if p.value == phone:
                self.phones.remove(p)
                return
        raise ValueError("Номер не знайдено.")

    def find_phone(self, phone):
        for p in self.phones:
            if p.value == phone:
                return p
        return None

    def set_birthday(self, birthday):
        self.birthday = Birthday(birthday)

    def __str__(self):
        phones = '; '.join(p.value for p in self.phones)
        result = f"Ім'я: {self.name.value}, Телефони: {phones}"
        if self.birthday:
            result += f", День народження: {self.birthday.value}"
        return result


class AddressBook(UserDict):
    def add_record(self, record):
        self.data[record.name.value] = record

    def find(self, name):
        return self.data.get(name)

    def delete(self, name):
        if name in self.data:
            del self.data[name]

    def get_upcoming_birthdays(self):
        today = datetime.today()
        upcoming = []
        for record in self.data.values():
            if record.birthday:
                bd = datetime.strptime(record.birthday.value, "%d.%m.%Y").replace(year=today.year)
                days_diff = (bd - today).days
                if 0 <= days_diff <= 7:
                    if bd.weekday() >= 5:
                        bd += timedelta(days=7 - bd.weekday())
                    upcoming.append(f"{record.name.value} - {bd.strftime('%d.%m.%Y')}")
        return upcoming

def input_error(func):
    def inner(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except ValueError as e:
            return str(e)
        except KeyError:
            return "Контакт не знайдено."
        except IndexError:
            return "Недостатньо аргументів."
    return inner

@input_error
def parse_input(user_input):
    cmd, *args = user_input.strip().split()
    return cmd.lower(), args


@input_error
def add_contact(args, book):
    name, phone = args
    record = book.find(name)
    if not record:
        record = Record(name)
        book.add_record(record)
    record.add_phone(phone)
    return "Контакт додано/оновлено."


@input_error
def change_contact(args, book):
    name, phone = args
    record = book.find(name)
    if record:
        if record.phones:
            record.phones[0].value = Phone(phone).value
        else:
            record.add_phone(phone)
        return "Контакт оновлено."
    return "Контакт не знайдено."


@input_error
def get_phone(args, book):
    name = args[0]
    record = book.find(name)
    if record:
        return ', '.join(p.value for p in record.phones)
    return "Контакт не знайдено."


def show_all(book):
    if not book.data:
        return "Немає контактів."
    return '\n'.join(str(record) for record in book.data.values())


@input_error
def add_birthday(args, book):
    name, birthday = args
    record = book.find(name)
    if record:
        record.set_birthday(birthday)
        return "День народження додано."
    return "Контакт не знайдено."


@input_error
def show_birthday(args, book):
    name = args[0]
    record = book.find(name)
    if record and record.birthday:
        return f"{name} має день народження {record.birthday.value}"
    return "День народження не встановлено."


def birthdays(book):
    upcoming = book.get_upcoming_birthdays()
    return "\n".join(upcoming) if upcoming else "Немає днів народження в межах тижня."


def main():
    book = AddressBook()
    print("Welcome to the assistant bot!")
    while True:
        try:
            user_input = input("Enter a command: ")
            command, args = parse_input(user_input)

            if command in ["exit", "close"]:
                print("Good bye!")
                break
            elif command == "hello":
                print("How can I help you?")
            elif command == "add":
                print(add_contact(args, book))
            elif command == "change":
                print(change_contact(args, book))
            elif command == "phone":
                print(get_phone(args, book))
            elif command == "all":
                print(show_all(book))
            elif command == "add-birthday":
                print(add_birthday(args, book))
            elif command == "show-birthday":
                print(show_birthday(args, book))
            elif command == "birthdays":
                print(birthdays(book))
            else:
                print("Invalid command.")
        except ValueError:
            print("Enter valid command.")

if __name__ == "__main__":
    main()
