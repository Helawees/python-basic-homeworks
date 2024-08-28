import json
import sys
import pandas as pd

path_phonebook = 'phonebook.json'
table_width = 50

def add_contact():
    contact_name = input("Введите имя контакта: ")
    contact_phone = input("Введите номер контакта: ")
    contact_comment = input("Введите комментарий: ")
    contact_item = {'name': contact_name,
                    'phone': contact_phone,
                    'comment': contact_comment}
    with open(path_phonebook, 'r', encoding = 'UTF-8') as phonebook:
        data = json.load(phonebook)
        all_keys = list(map(int, data.keys()))
        new_key = str(max(all_keys) + 1)
        data[new_key] = contact_item
    with open(path_phonebook,'w', encoding = 'UTF-8') as phonebook:
        json.dump(data, phonebook, indent = 4, ensure_ascii = False)
        print(f"Контакт {data[new_key]['name']} добавлен!")

def menu_choice_process(input_choice):
    if input_choice == "1": #вывод меню
        print_phonebook()
        action_menu()
    elif input_choice == "2": #поиск контакта
        find_contact()
        action_menu()
    elif input_choice == "3": #добавить контакт
        add_contact()
        action_menu()
    elif input_choice == "4": #редактировать контакт
        edit_contact()
        action_menu()
    elif input_choice == "5": #удалить контакт
        delete_contact()
        action_menu()
    elif input_choice == "6": #выход
        sys.exit()
    else:
        print("Некорректный ввод!\n")
        print_menu()

def print_menu():
    menu_txt = (f"Справочник OTUS 2024\n"
                f"Введите номер действия:\n"
                f"1. Вывести существующие контакты на экран\n"
                f"2. Поиск контакта\n"
                f"3. Добавить контакт\n"
                f"4. Редактировать контакт\n"
                f"5. Удалить контакт\n"
                f"6. Выход\n\n")
    input_choice = input(menu_txt + "Ваш выбор: ")
    menu_choice_process(input_choice)

def action_menu():
    flag_menu = True
    while flag_menu:
        input_choice = input("Для выхода из программы введите 'e'\n"
                             "Для вывода меню введите 'm'\n")
        if input_choice == "e":
            flag_menu = False
            sys.exit()
        elif input_choice == "m":
            flag_menu = False
            print_menu()
        else:
            print("Некорректный ввод!\n")
            action_menu()

def contact_menu():
    flag_menu = True
    while flag_menu:
        input_choice = input("Для продолжения работы с контактом, введите ID контакта\n"
                             "Для выхода из программы введите 'e'\n"
                             "Для вывода меню введите 'm'\n")
        if input_choice == "e":
            flag_menu = False
            sys.exit()
        elif input_choice == "m":
            flag_menu = False
            print_menu()
        elif input_choice.isdigit():
            return input_choice
        else:
            print("Некорректный ввод!\n")
            action_menu()

def print_search_results(results):
    results_pandas = pd.DataFrame(results).transpose()
    print("=" * table_width)
    print(results_pandas.to_string(header=True, justify='center'))
    print("=" * table_width)

def print_phonebook():
    try: #проверяем существует ли файл справочника
        with open(path_phonebook, 'r', encoding = 'UTF-8') as phonebook:
            data = json.load(phonebook)
    except FileNotFoundError or ValueError or OSError:
        print("Файл справочника не найден!\n")
        sys.exit("File not found!")
    else: #файл существует, выводим данные
        if data:
            table_pandas = pd.DataFrame(data).transpose()
            print("="*table_width)
            print(table_pandas.to_string(header=True, justify='center'))
            print("=" * table_width)
        else: #файл существует, но данных в нем нет
            print("Справочник пуст!\n")

def find_contact():
    result = {}
    search_criteria = input("Введите критерий поиска: ")
    with open(path_phonebook, 'r', encoding = "UTF-8") as phonebook:
        data = json.load(phonebook)
        for id_key, contact in data.items():
            for field_key, field in contact.items():
                if field_key == 'phone':
                    field = ''.join([symbol for symbol in field if symbol.isdigit()])
                if search_criteria.lower() in field.lower():
                    result[id_key] = contact
    if result:
        print_search_results(result)
        return True
    else:
        print("Контакты не найдены!")
        return False

def delete_contact():
    if find_contact():
        contact_id = contact_menu()
        with open(path_phonebook, 'r', encoding="UTF-8") as phonebook:
            data = json.load(phonebook)
            if contact_id in data.keys():
                copy_item = data[contact_id]["name"]
            else:
                print(f"Контакта с ID {contact_id} не существует!")
                action_menu()
        confirm_message = input(f"Вы уверены, что хотите удалить контакт {copy_item} (y/n)?")
        if confirm_message.lower() == 'y':
            del data[contact_id]
            with open(path_phonebook, 'w', encoding="UTF-8") as phonebook:
                json.dump(data, phonebook, indent=4, ensure_ascii=False)
            print(f"Контакт {copy_item} удалён!")
        elif confirm_message.lower() == 'n':
                action_menu()
        else:
            print("Некорректный ввод!")
            action_menu()

def edit_contact():
    if find_contact():
        contact_id = contact_menu()
        with open(path_phonebook, 'r', encoding="UTF-8") as phonebook:
            data = json.load(phonebook)
            if contact_id in data.keys():
                copy_item = data[contact_id]
            else:
                print(f"Контакта с ID {contact_id} не существует!")
                action_menu()

        new_name = input("Введите новое имя контакта: ")
        new_phone = input("Введите новый телефон контакта: ")
        new_comment = input("Введите новый комментарий контакта: ")
        edited_contact = {"name": new_name,
                          "phone": new_phone,
                          "comment": new_comment}

        print("Отредактированный контакт будет выглядеть следующим образом:\n")
        new_contact_pandas = pd.DataFrame([edited_contact])
        print("=" * table_width)
        print(new_contact_pandas.to_string(index=False, header=True, justify='center'))
        print("=" * table_width)

        confirm_message = input(f"Вы уверены, что хотите изменить контакт {copy_item['name']} (y/n)?")
        if confirm_message.lower() == 'y':
            data[contact_id] = edited_contact
            with open(path_phonebook, 'w', encoding="UTF-8") as phonebook:
                json.dump(data, phonebook, indent=4, ensure_ascii=False)
            print(f"Контакт {copy_item['name']} изменён!")
        elif confirm_message.lower() == 'n':
            action_menu()
        else:
            print("Некорректный ввод!")
            action_menu()

print_menu()