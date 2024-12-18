import pytest

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
