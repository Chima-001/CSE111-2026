'''
Password Manager Application
A secure command-line password manager with Fernet encryption.

Features:
- Add, View, edit, and delete passwords
- Fernet encryption for secure storage
- Duplicate prevention
- Input validation

Author: Chimamkpam Nnaji
Date: February 2026
'''

from passwords import generate_password
from cryptography.fernet import Fernet
import os

class Password:
    def __init__(self, service, username, password):
        self.service = service
        self.username = username
        self.password = password

    def __str__(self):
        return f'Service: {self.service} | Username: {self.username} | Password: {self.password}'

class PasswordVault:
    def __init__(self, master_password):
        self.master_password = master_password
        self.password_list = []
        self.key = None
        self.cipher = None
        self._setup_encryption()

    def _setup_encryption(self, key_file= 'secret.key'):
        try:
            if os.path.exists(key_file):
                with open(key_file, 'rb') as file:
                    self.key = file.read()

            else:
                self.key = Fernet.generate_key()
                with open(key_file, 'wb') as file:
                    file.write(self.key)

            self.cipher = Fernet(self.key)
            return True
        
        except Exception:
            return False
           
    def add_password(self, service, username, password):
        for entry in self.password_list:
            if entry.service.lower() == service.lower():
                return False

        new_password = Password(service, username, password)
        self.password_list.append(new_password)
        self.save_to_file(filename= 'passwords.txt')
        return True

    def get_password(self, service):
        for entry in self.password_list:

            if entry.service.lower() == service.lower():
                return entry.password
        return None

    def list_services(self):
        sorted_services = sorted([entry.service for entry in self.password_list])
        return sorted_services

    def gen_password(self):
        generated_password = generate_password(16)
        return generated_password

    def save_to_file(self, filename = 'passwords.txt'):
        try:
            with open(filename, 'w') as file:
                for entry in self.password_list:
                    encrypted_password = self._encrypt(entry.password)
                    if encrypted_password is None:
                        return False
                    file.write(f'{entry.service},{entry.username},{encrypted_password}\n')
            return True
        
        except Exception:
            return False

    def load_from_file(self, filename = 'passwords.txt'):
        self.password_list = []

        try:
            with open(filename, 'r') as file:
                lines = file.readlines()

                for line in lines:
                    clean_line = line.strip()

                    if not clean_line:
                        continue

                    new_line = clean_line.split(',')

                    if len(new_line) != 3:
                        continue 

                    service = new_line[0]
                    username = new_line[1]
                    password = self._decrypt(new_line[2])
                    new_password = Password(service, username, password)
                    self.password_list.append(new_password)
            return True

        except FileNotFoundError:
                return False

        except Exception:
                return False

    def _encrypt(self, text):
        try:
            return self.cipher.encrypt(text.encode()).decode()

        except Exception:
            return None

    def _decrypt(self, encrypted_text):
        try:
            return self.cipher.decrypt(encrypted_text.encode()).decode()
        
        except Exception:
            return None

    def edit_password(self, service, new_password):
        for entry in self.password_list:
            if entry.service.lower() == service.lower():
                entry.password = new_password
                self.save_to_file(filename='passwords.txt')
                return True
        return False

    def delete_password(self, service):
        for entry in self.password_list:
            if entry.service.lower() == service.lower():
                self.password_list.remove(entry)
                self.save_to_file(filename='passwords.txt')
                return True
        return False

def main():
    print('\n===== PASSWORD MANAGER ======')
    attempts = 0

    while True:
        master = input('Enter master password or \'0\' to quit: ')
        vault = PasswordVault('master')

        if master == '0':
            break

        if vault.cipher is None:
            print('⚠ Error: Failed to initialize encryption.')
            continue

        elif master != vault.master_password:
            attempts += 1
            if attempts >= 3:
                print('❗ Too many failed attempts. Exiting for security.')
                break
            print(f'Wrong password. Try again. {3-attempts} attempts remaining.')
            continue

        else:
            vault.load_from_file(filename='passwords.txt')

            while True:
                print('\n-- MENU OPTIONS --\n')
                print(f'Passwords stored: {len(vault.password_list)}')
                print('1. Add Password\n2. Edit Password\n3. Get Password\n4. List Services\n5. View All Passwords\n6. Delete Password\n7. Exit')

                try:
                    user_choice = int(input('Enter an option (1-7): '))

                except ValueError:
                    print('Invalid input. Enter numbers (1-7)')
                    continue

                if user_choice == 1:
                    while True:
                        while True:
                            service = input('Enter password service: ')
                            if not service:
                                print('❗ Service name cannot be empty.')
                            else:
                                break

                        while True: 
                            username = input('Enter username: ')
                            if not username:
                                print('❗ Username cannot be empty.')
                            else:
                                break

                        while True:
                            password = input('Enter password or \'g\' to generate password: ')
                            if password.lower() == 'g'.lower():
                                password = vault.gen_password()
                                break

                            elif not password:
                                print('❗ Password cannot be empty.')

                            else:
                                break

                        if not vault.add_password(service, username, password):
                            print(f'Service \'{service}\' already exists, use another password service.')
                            continue

                        print(f'Password {password} has been successfully saved.')
                        break
                            
                    continue

                elif user_choice == 2:
                    if not vault.password_list:
                        print('No password stored')

                    else:
                        while True:
                            service  = input('Enter password service to edit: ')
                            if not service:
                                print('❗ Service name cannot be empty.')
                            
                            else:
                                current_password = vault.get_password(service)
                                break

                        if current_password:
                            print(f'Current password for {service.capitalize()}: {current_password}')

                            while True:
                                new_password = input('Enter new password or \'g\' to generate: ')
                                if not new_password:
                                    print('❗ Password cannot be empty.')
                                
                                else:
                                    break

                            if new_password.lower() == 'g':
                                new_password = vault.gen_password()
                                print(f'Generated password: {new_password}')

                            if vault.edit_password(service, new_password):
                                print(f'Password for {service} sucessfully updated to {new_password}')

                        else:
                            print(f'Password service \'{service}\' not found.')

                    continue

                elif user_choice == 3:
                    if not vault.password_list:
                        print('No password stored. Add a password first.')
                        continue

                    while True:
                        service = input('Enter password service: ')
                        if not service:
                            print('❗ Service name cannot be empty.')
                        
                        else:
                            break

                    print(vault.get_password(service))
                    continue

                elif user_choice == 4:
                    if not vault.password_list:
                        print('No password stored. Add a password first.')

                    else:
                        print('\nStored services:')
                        for service in vault.list_services():
                            print(service)

                    continue

                elif user_choice == 5:
                    if not vault.password_list:
                        print('No passwords available. Add a password first.')

                    for entry in vault.password_list:
                        print(entry)

                    continue

                    
                elif user_choice == 6:
                    if not vault.password_list:
                        print(f'No password stored.')

                    else:
                        while True:
                            service = input('Enter password service: ')
                            if not service:
                                print('❗ Service name cannot be empty.')
                            
                            else:
                                break

                        while True:
                            confirm = input(f'Are you sure you want to delete \'{service}\'? (y/n): ')
                            if confirm.lower() == 'y':
                                if vault.delete_password(service):
                                   print('Password successfully deleted.')
                                   break

                                else:
                                    print(f'Password service \'{service}\' not found.')
                                    break

                            elif confirm.lower() == 'n':
                                print('Delete cancelled')
                                break

                            else:
                                print('⚠ Invalid! Enter a valid input (y/n)')

                            continue

                elif user_choice == 7:
                    print('Exiting...')
                    return
                
                else:
                    print('⚠ Invalid input. Enter numbers (1-7): ')
                    continue

if __name__ == '__main__':
    main()