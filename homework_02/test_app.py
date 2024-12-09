#модуль тестирования
import pytest

from model import PhoneContact, PhoneBook, FileManager
import os

@pytest.fixture
def sample_contact_item():
    contact_item = {'name': "test_name",
                    'phone': '123456789',
                    'comment': 'test_comment'}
    return contact_item

@pytest.fixture
def sample_phonebook_path():
    test_phonebook_path = 'test_path.json'
    return test_phonebook_path

def test_create_contact_with_valid_data(sample_contact_item):
    test_contact = PhoneContact(sample_contact_item)
    assert test_contact.name == 'test_name'
    assert test_contact.phone == '123456789'
    assert test_contact.comment == 'test_comment'

def test_create_contact_without_comment():
    test_contact = PhoneContact({'name': "test_name",
                                 'phone': '123456789',
                                 'comment': ''})
    assert test_contact.name == 'test_name'

def test_create_contact_without_name():
    with pytest.raises(ValueError):
        test_contact = PhoneContact({'name': '',
                                     'phone': '123456789',
                                     'comment': "test_comment"})

def test_create_contact_without_phone():
    with pytest.raises(ValueError):
        test_contact = PhoneContact({'name': 'test_name',
                                     'phone': '',
                                     'comment': "test_comment"})

def test_create_phonebook_manager_without_file(sample_phonebook_path):
    if os.path.exists(sample_phonebook_path): os.remove(sample_phonebook_path)
    book_manager = PhoneBook(sample_phonebook_path)
    assert os.path.exists(sample_phonebook_path)
    os.remove(sample_phonebook_path)

def test_add_contact(sample_phonebook_path, sample_contact_item):
    book_manager = PhoneBook(sample_phonebook_path)
    contact = PhoneContact(sample_contact_item)
    test_new_id = book_manager.get_new_id()
    book_manager.add_contact(test_new_id, contact)
    book_manager.upload_changes()
    assert max(book_manager.data.keys()) == test_new_id

def test_remove_contact(sample_phonebook_path):
    book_manager = PhoneBook(sample_phonebook_path)
    book_manager.delete_contact("1")
    test_new_id = book_manager.get_new_id()
    assert test_new_id == '1'
    os.remove(sample_phonebook_path)
