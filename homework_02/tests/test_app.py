#модуль тестирования
import pytest
from conftest import sample_phonebook_path, sample_contact_item

import os
import sys

parent_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
sys.path.append(parent_dir)
from model import PhoneContact, PhoneBook


def test_create_contact_with_valid_data(sample_contact_item):
    """Проверка создания объекта Контакт с корректными данными."""
    test_contact = PhoneContact(sample_contact_item)
    assert test_contact.name == 'test_name'
    assert test_contact.phone == '123456789'
    assert test_contact.comment == 'test_comment'


def test_create_contact_without_comment():
    """Проверка создания объекта Контакт при отсутствии текста комментария (допустимо нулевое значение)."""
    test_contact = PhoneContact({'name': "test_name",
                                 'phone': '123456789',
                                 'comment': ''})
    assert test_contact.name == 'test_name'


def test_create_contact_without_name():
    """Проверка создания объекта Контакт при отсутствии ввода имени (обязательный атрибут)."""
    with pytest.raises(ValueError):
        test_contact = PhoneContact({'name': '',
                                     'phone': '123456789',
                                     'comment': "test_comment"})


def test_create_contact_without_phone():
    """Проверка создания объекта Контакт при отсутствии ввода номера телефона (обязательный атрибут)."""
    with pytest.raises(ValueError):
        test_contact = PhoneContact({'name': 'test_name',
                                     'phone': '',
                                     'comment': "test_comment"})


def test_create_phonebook_manager_without_file(sample_phonebook_path):
    """Проверка создания объекта Менеджер Телефонной Книги при отсутствии файла телефонного справочника."""
    if os.path.exists(sample_phonebook_path): os.remove(sample_phonebook_path)
    book_manager = PhoneBook(sample_phonebook_path)
    assert os.path.exists(sample_phonebook_path)
    os.remove(sample_phonebook_path)


def test_add_contact(sample_phonebook_path, sample_contact_item):
    """Проверка добавления контакта в объект телефонной книги."""
    book_manager = PhoneBook(sample_phonebook_path)
    contact = PhoneContact(sample_contact_item)
    test_new_id = book_manager.get_new_id()
    book_manager.add_contact(test_new_id, contact)
    book_manager.upload_changes()
    assert max(book_manager.data.keys()) == test_new_id


def test_remove_contact(sample_phonebook_path):
    """Проверка удаления контакта из объекта телефонной книги."""
    book_manager = PhoneBook(sample_phonebook_path)
    book_manager.delete_contact("1")
    test_new_id = book_manager.get_new_id()
    assert test_new_id == '1'
    os.remove(sample_phonebook_path)
