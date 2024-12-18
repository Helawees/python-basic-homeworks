#модуль обработки ввода-вывода
import pandas as pd
from termcolor import cprint

table_width = 50

menu_txt = (f"Справочник OTUS 2024\n"
            f"Введите номер действия:\n"
            f"1. Вывести существующие контакты на экран\n"
            f"2. Поиск контакта\n"
            f"3. Добавить контакт\n"
            f"4. Редактировать контакт\n"
            f"5. Удалить контакт\n"
            f"6. Выход\n\n")

action_menu_txt = (f"Для выхода из программы введите 'e'\n"
                   f"Для вывода меню введите 'm'\n")


def print_incorrect_input():
    cprint("Некорректный ввод!\n", 'red')


def print_added_success(contact_name):
    cprint(f"Контакт {contact_name} успешно добавлен!", 'green')


def print_deleted_success():
    cprint(f"Контакт успешно удалён!", 'green')


def print_edited_success(contact_name):
    cprint(f"Контакт {contact_name} успешно обновлён!", 'green')


def print_smth_went_wrong():
    cprint("Что-то пошло не так, попробуйте еще раз!", 'red')


def print_no_contact_data():
    cprint("Не предоставлены данные: имя или телефон контакта!", 'red')


def get_new_contact_data():
    contact_name = input("Введите имя контакта: ")
    contact_phone = input("Введите номер контакта: ")
    contact_comment = input("Введите комментарий: ")
    contact_item = {'name': contact_name,
                    'phone': contact_phone,
                    'comment': contact_comment}
    return contact_item


def get_search_criteria():
    input_choice = input("Введите критерий поиска: ")
    return input_choice.lower()


def print_menu():
    input_choice: str = input(menu_txt + "Ваш выбор: ")
    return input_choice.lower()


def print_action_menu():
    input_choice: str = input(action_menu_txt)
    return input_choice.lower()


def print_data(data):
    if data:
        table_pandas = pd.DataFrame(data).transpose()
        print("=" * table_width)
        print(table_pandas.to_string(header=True, justify='center'))
        print("=" * table_width)
    else:
        cprint("Нет данных!\n", 'red')


def edit_choice():
    choice = input("Введите id контакта, который желаете изменить: ")
    return choice.lower()


def delete_choice():
    choice = input("Введите id контакта, который желаете удалить: ")
    return choice.lower()

def delete_confirmation():
    answer = input("Удалить данный контакт (y/n) ?")
    return answer.lower()

