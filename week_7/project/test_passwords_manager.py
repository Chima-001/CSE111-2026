# Running this test program removes/deletes the master.txt and the secret.key files initially created
# in the passwords_manager.py program. User will have to create a new master password in the 
# passwords_manager.py program after running this program.

from passwords_manager import Password, PasswordVault
from unittest.mock import patch
import pytest
import os

@pytest.fixture
def vault():
    '''Create a vault for testing'''
    v = PasswordVault('test_master')
    yield v

    # Cleanup
    if os.path.exists('test_passwords.txt'):
        os.remove('test_passwords.txt')
    
    if os.path.exists('secret.key'):
        os.remove('secret.key')

@pytest.fixture
def cleanup_master():
    if os.path.exists('master.txt'):
        os.remove('master.txt')

    yield
    if os.path.exists('master.txt'):
        os.remove('master.txt')
    
# Test Password class
def test_password_init():
    pwd = Password('Facebook', 'Chima', 'BYU-CSE111')
    pwd2 = Password('Outlook', 'Miles', '$HEX[66617368696f6e310d]')
    pwd3 = Password('Red+=|t', 'Valen$3/', ')#hfmdfhv443') # Testing edge cases (services, usernames, passwords) with special characters

    assert pwd.service == 'Facebook'
    assert pwd.username == 'Chima'
    assert pwd.password == 'BYU-CSE111'

    assert pwd2.service == 'Outlook'
    assert pwd2.username == 'Miles'
    assert pwd2.password == '$HEX[66617368696f6e310d]'

    assert pwd3.service == 'Red+=|t'
    assert pwd3.username == 'Valen$3/'
    assert pwd3.password == ')#hfmdfhv443'

def test_password_str():
    pwd = Password('Facebook', 'Chima', 'BYU-CSE111')
    pwd2 = Password('Outlook', 'Miles', '$HEX[66617368696f6e310d]')
    pwd3 = Password('Red+=|t', 'Valen$3/', ')#hfmdfhv443')

    assert str(pwd) == 'Service: Facebook | Username: Chima | Password: BYU-CSE111'
    assert str(pwd2) == 'Service: Outlook | Username: Miles | Password: $HEX[66617368696f6e310d]'
    assert str(pwd3) == 'Service: Red+=|t | Username: Valen$3/ | Password: )#hfmdfhv443'

# Test PasswordVault methods
def test_setup_encryption(vault):
    assert vault.cipher is not None


def test_add_password(vault):

    result = vault.add_password('Facebook', 'Chima', 'BYU-CSE111')
    assert result == True
    assert len(vault.password_list) == 1

    result2 = vault.add_password('facEbOok', 'Nnaji', 'pwd-mngr!7t4')  # Testing duplicate check with case insentivity
    assert result2 == False  # Returns False, a service with the same name already exists
    assert len(vault.password_list) == 1

    result3 = vault.add_password('Gmail', 'Track', 'blake1999')
    assert result3 == True
    assert len(vault.password_list) == 2

    result4 = vault.add_password('Twitter', 'Valen$3/', ')#hfmdfhv443')
    assert result4 == True
    assert len(vault.password_list) == 3

    result5 = vault.add_password('Twitter', 'Adams23', 'doncarlo')  # Testing without case insensivity
    assert result5 == False  # Returns False
    assert len(vault.password_list) == 3

def test_edit_password(vault):
    vault.password_list = []
    password4 = vault.edit_password('Compute', '@Dev5674') 
    assert password4 == False

    vault.password_list.append(Password('Facebook', 'Chima', 'BYU-CSE111'))
    assert vault.edit_password('Facebook', '@Dev5674') == True
    password = vault.get_password('Facebook')
    assert password == '@Dev5674'

    vault.password_list.append(Password('Amazon', 'Adams23', 'doncarlo'))
    assert vault.edit_password('AmAZon', '1blaine') == True  # Tests case sensitivity
    password2 = vault.get_password('Amazon')
    assert password2 == '1blaine'

    vault.password_list.append(Password('whatsapp', 'Nnaji', 'pwd-mngr!7t4'))
    assert vault.edit_password('snapchat', 'pwd-mngr!7t4') is False # Test inexistent services

def test_get_password(vault):
    vault.password_list = []
    assert vault.get_password('Facebook') is None  # Test to get password from empty vault returns None

    vault.password_list.append(Password('Facebook', 'Chima', 'BYU-CSE111'))
    assert vault.get_password('Facebook') == 'BYU-CSE111'

    vault.password_list.append(Password('Whatsapp', 'Nnaji', 'pwd-mngr!7t4'))
    assert vault.get_password('Whatsapp') == 'pwd-mngr!7t4'
    assert vault.get_password('WHATSAPP') == 'pwd-mngr!7t4'  # Test for case insensitivity
    assert vault.get_password('WHatSApp') == 'pwd-mngr!7t4'

def test_list_services(vault):
    assert vault.list_services() == []  # Test for empty services

    vault.password_list.append(Password('Amazon', 'Adams23', 'doncarlo'))
    vault.password_list.append(Password('Facebook', 'Chima', 'BYU-CSE111'))
    vault.password_list.append(Password('Whatsapp', 'Nnaji', 'pwd-mngr!7t4'))

    assert vault.list_services() == ['Amazon', 'Facebook', 'Whatsapp']  # Asides checking if all services is in list,  
                                                                        # this also checks services are in alphabetical order

def test_gen_password(vault):
    password = vault.gen_password()
    assert password != ''  

    password = vault.gen_password()
    assert len(password) == 16 

def test_save_to_file(vault):
    vault.password_list.append(Password('whatsapp', 'Nnaji', 'pwd-mngr!7t4'))
    vault.password_list.append(Password('Outlook', 'Miles', '$HEX[66617368696f6e310d]'))
    vault.password_list.append(Password('Facebook', 'Chima', 'BYU-CSE111'))
    assert vault.save_to_file('test_passwords.txt') == True

def test_load_from_file(vault):
    vault.password_list.append(Password('Facebook', 'Chima', 'BYU-CSE111'))
    assert vault.save_to_file('test_passwords.txt') == True

    vault.save_to_file('test_passwords.txt')

    new_vault = PasswordVault('test_master')
    new_vault.load_from_file('test_passwords.txt')

    entry = new_vault.password_list[0]

    assert entry.service == 'Facebook'
    assert entry.username == 'Chima'
    assert entry.password == 'BYU-CSE111'
    
    new_vault = PasswordVault('test_master')
    assert new_vault.load_from_file('test_passwords.txt') == True
    assert len(new_vault.password_list) == 1

def test_delete_password(vault):
    vault.password_list.append(Password('Facebook', 'Chima', 'BYU-CSE111'))
    vault.password_list.append(Password('Whatsapp', 'Nnaji', 'pwd-mngr!7t4'))
    vault.password_list.append(Password('Pinterest', 'Track', 'blake1999'))
    
    assert vault.delete_password('Facebook') == True
    assert vault.delete_password('WHAtsApp') == True  # Test case insensitivity
    assert vault.delete_password('Pinterest') == True

    # Verify deleted password no longer in list
    assert vault.get_password('Facebook') is None
    assert vault.get_password('Whatsapp') is None
    assert vault.get_password('Pinterest') is None

def test_encrypt(vault):
    encrypted = vault._encrypt('test')
    assert encrypted is not None
    assert encrypted != 'test'

    encrypted = vault._encrypt('benqfp71g0941')
    assert encrypted is not None
    assert encrypted != 'benqfp71g0941'
    
    encrypted = vault._encrypt('$HEX[3168653a]')
    assert encrypted is not None
    assert encrypted != '$HEX[3168653a]'

def test_decrypt(vault): 
    encrypted = vault._encrypt('test')
    assert vault._decrypt(encrypted) == 'test'

    encrypted = vault._encrypt('benqfp71g0941')
    assert vault._decrypt(encrypted) == 'benqfp71g0941'

    encrypted = vault._encrypt('$HEX[3168653a]')
    assert vault._decrypt(encrypted) == '$HEX[3168653a]'

def test_get_master_password(cleanup_master):
    result = PasswordVault.get_master_password()
    assert result is None

    temp_vault = PasswordVault('')
    encrypted = temp_vault._encrypt('test_password')
    with open('master.txt', 'w') as file:
        file.write(encrypted)
    result = PasswordVault.get_master_password()
    assert result == 'test_password'

    encrypted = temp_vault._encrypt('password123')
    with open('master.txt', 'w') as file:
        file.write(encrypted)
    result = PasswordVault.get_master_password()
    assert result == 'password123'

def test_create_master_password(cleanup_master):
    with patch('builtins.input', side_effect= ['mypassword', 'mypassword']):
        result = PasswordVault.create_master_password()
    assert result == 'mypassword'
    assert os.path.exists('master.txt')

    os.remove('master.txt')
    with patch('builtins.input', side_effect= ['a', 'b']):
        result = PasswordVault.create_master_password()
    assert result is None

    os.remove('secret.key')


pytest.main(["-v", "--tb=line", "-rN", __file__])
