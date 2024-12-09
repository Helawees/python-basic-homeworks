import view
from model import PhoneContact, PhoneBook
import sys

filepath = 'phonebook.json'

def process_action_menu(phonebook_object):
    flag_menu = True
    while flag_menu:
        input_choice = view.print_action_menu()
        if input_choice == "e":
            flag_menu = False
            sys.exit()
        elif input_choice == "m":
            flag_menu = False
            process_menu(phonebook_object)
        else:
            view.print_incorrect_input()

def process_menu(phonebook_object):
    flag_menu = True
    while flag_menu:
        choice = view.print_menu()
        if choice == "1": #вывод меню
            flag_menu = False
            view.print_data(phonebook_object.data)
            process_action_menu(phonebook_object)
        elif choice == "2": #поиск контакта
            flag_menu = False
            result = phonebook_object.find_contact(view.get_search_criteria())
            view.print_data(result)
            process_action_menu(phonebook_object)
        elif choice == "3": #добавить контакт
            flag_menu = False
            try:
                new_contact = PhoneContact(view.get_new_contact_data())
            except ValueError:
                view.print_no_contact_data()
                process_action_menu(phonebook_object)
            else:
                new_id = phonebook_object.get_new_id()
                try:
                    phonebook_object.add_contact(new_id, new_contact)
                    phonebook_object.upload_changes()
                except:
                    view.print_smth_went_wrong()
                else:
                    view.print_added_success(phonebook_object.data[new_id]['name'])
            process_action_menu(phonebook_object)
        elif choice == "4": #редактировать контакт
            flag_menu = False
            result = phonebook_object.find_contact(view.get_search_criteria())
            view.print_data(result)
            if result:
                edit_choice = view.edit_choice()
                if edit_choice in result.keys():
                    new_data = view.get_new_contact_data()
                    phonebook_object.edit_contact(edit_choice, new_data)
                    phonebook_object.upload_changes()
                    view.print_edited_success(phonebook_object.data[edit_choice]['name'])
                else:
                    view.print_incorrect_input()
                    process_action_menu(phonebook_object)
            process_action_menu(phonebook_object)
        elif choice == "5": #удалить контакт
            flag_menu = False
            contact_to_delete = phonebook_object.find_contact(view.get_search_criteria())
            if contact_to_delete:
                view.print_data(contact_to_delete)
                delete_choice = view.delete_choice()
                if delete_choice in contact_to_delete.keys():
                    view.print_data([phonebook_object.data[delete_choice]])
                    confirmation = view.delete_confirmation()
                    if confirmation == 'y':
                        phonebook_object.delete_contact(delete_choice)
                        phonebook_object.upload_changes()
                        view.print_deleted_success()
                        process_action_menu(phonebook_object)
                    elif confirmation == 'n':
                        process_action_menu(phonebook_object)
                    else:
                        view.print_incorrect_input()
                        process_action_menu(phonebook_object)
                else:
                    view.print_incorrect_input()
                    process_action_menu(phonebook_object)
            else:
                view.print_incorrect_input()
                process_action_menu(phonebook_object)

        elif choice == "6": #выход
            sys.exit()
        else:
            view.print_incorrect_input()

def run_app():
    phonebook_object = PhoneBook(filepath)
    process_menu(phonebook_object)