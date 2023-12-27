from collections import UserDict
from datetime import datetime, date
import pickle

class Field:
    
    def __init__(self, value):
        self._value = None
        self.value = value

    @property
    def value(self):
        return self._value
    
    @value.setter
    def value(self, value):
        self._value = value

    

class Name(Field):
    
    def __init__(self, value):
        super().__init__(value)

class Phone(Field):
    
    def __init__(self, value):
        super().__init__(value)
        

    def phone_valid(self):
        if self.value is not None:
            if len(self.value) != 10 or not self.value.isdigit():
                raise ValueError("Your phone must contain 10 digit")
            

    @property
    def value(self):
        return self._value
    
    @value.setter
    def value(self, value):
        self._value = value
        self.phone_valid()


class Birthday(Field):
    def __init__(self, value):
        super().__init__(value)
        

    def birthday_valid(self):
        try:
            birthday_day = datetime.strptime(self._value, "%Y-%m-%d")
        except ValueError:
            print('Invalid date. Enter date in format: Year-Month-Day')

    @property
    def value(self):
        return self._value
    
    @value.setter
    def value(self, value):
        self._value = value  
        self.birthday_valid()      



class Record:
    def __init__(self, name, birthday):
        self.name = Name(name)
        self.birthday = birthday
        self.phones = []


    def add_phone(self, phone):
        phone_number = Phone(phone)
        phone_number.phone_valid()                   
        self.phones.append(phone_number)

    def remove_phone(self, phone):
        for element in self.phones:
            if element.value == phone:
                self.phones.remove(element)

    def edit_phone(self, phone, new_phone):
        for element in self.phones:
            if element.value == phone:
                element.value = new_phone
                return
        raise ValueError(f'Phone {phone} not found')
        
    def find_phone(self, phone):
        for element in self.phones:
            if element.value == phone:
                return element
            
    def days_to_birthday(self):
        if not self.birthday:
            return None
        today = date.today()
        birthday_day = datetime.strptime(self.birthday.value, "%Y-%m-%d")
        user_birthday_in_this_year = date(today.year, birthday_day.month, birthday_day.day)
        different = user_birthday_in_this_year - today
        if different.days > 0:
            return f'left until birthday {different.days} days'
        else:
            user_birthday_in_next_year = date(today.year + 1, birthday_day.month, birthday_day.day)
            different_new = user_birthday_in_next_year - today
            return f'left until birthday {different_new.days} days'

        
         


    def __str__(self):
        return f"Contact name: {self.name.value}, phones: {'; '.join(p.value for p in self.phones)}"

class AddressBook(UserDict):
    
    def add_record(self, record):
        self.data[record.name.value] = record

    def find(self, search):           
        #return self.data.get(name)
        value_records = []
        for key, value in self.data.items():
            if search.lower() in key.lower() or search in value.phone.value:
                value_records.append((key, value))
        return value_records
        


    
    def delete(self, name):
        if name in self.data:
            del self.data[name]

    def iterator(self, number):
        counter = 0
        result = ''
        for key, value in self.data.items():
            result += f'{key}:{value}\n'
            counter += 1
            if counter >= number:
                yield result
                counter = 0
                result = ""
        if result:
            yield result

    def save_to_file(self):
        with open('contacts.pickle', "wb") as file:
            pickle.dump(self.data, file)

    def read_from_file(self):
        try:
            with open('contacts.pickle', "rb") as file:
                self.data = pickle.load(file)
        except FileNotFoundError:
            print("File not found. Creating a new AddressBook.")
        

    



if __name__ == "__main__":
    book = AddressBook()