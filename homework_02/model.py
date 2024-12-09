#модуль для работы с БД
import os
import json

class FileManager:
    @staticmethod
    def load_data(phonebook_path):
        if os.path.exists(phonebook_path): # проверка наличия файла
            with open(phonebook_path, 'r', encoding='UTF-8') as phonebook:
                loaded_data = json.load(phonebook)
        else:
            loaded_data = {}
            with open(phonebook_path, 'w+', encoding="UTF-8") as phonebook: # создаем файл и записываем туда пустой словарь
                json.dump(loaded_data, phonebook, indent=4, ensure_ascii=False)
        return loaded_data

    @staticmethod
    def upload_changes(data, filepath):
        with open(filepath, 'w', encoding='UTF-8') as phonebook:
            json.dump(data, phonebook, indent=4, ensure_ascii=False)

class PhoneContact:
    def __init__(self, contact_dictionary: dict):
        if not contact_dictionary['name'] or not contact_dictionary['phone']:
            raise ValueError("Не указаны данные для имени или телефона контакта.")
        self.name = contact_dictionary['name']
        self.phone = contact_dictionary['phone']
        self.comment = contact_dictionary['comment']

    def __str__(self):
        return f"{self.name} {self.phone} {self.comment}"

    def form_contact_item(self):
        contact_item = {'name': self.name,
                        'phone': self.phone,
                        'comment': self.comment}
        return contact_item

class PhoneBook:
    def __init__(self, phonebook_path):
        self.data = FileManager.load_data(phonebook_path)
        self.filepath = phonebook_path

    def get_new_id(self): # генерация следующего id
        if self.data:
            all_keys = list(map(int, self.data.keys()))
            new_key = str(max(all_keys) + 1)
            return new_key
        else:
            return "1"

    def add_contact(self, new_id, contact: PhoneContact):
        self.data[new_id] = contact.form_contact_item()
        return self.data

    def find_contact(self, search_criteria):
        result = {}
        for id_key, contact in self.data.items():
            for field_key, field in contact.items():
                if field_key == 'phone':
                    field = ''.join([symbol for symbol in field if symbol.isdigit()])
                if search_criteria.lower() in field.lower():
                    result[id_key] = contact
        if result:
            return result
        else:
            return None

    def delete_contact(self, contact_id):
        del self.data[contact_id]
        return self.data

    def edit_contact(self, contact_id, new_contact_item):
        self.data[contact_id] = new_contact_item
        return self.data

    def upload_changes(self):
        FileManager.upload_changes(self.data, self.filepath)



