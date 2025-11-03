import os

from SixteenNumbersGenerator.generator import generate_sum
from X256.X256 import X256
from key.keyGenerator import generate_headers, create_numeric_form, key_generator


class Key:
    def __init__(self, key, folder_path):
        self.folder_path = folder_path
        self.key_string = key
        self.last_index = 0

    def run(self):
        self.generate_key()

    def passwords_file_cleaner(self):
        password_path = r"C:\Program Files\SCAT\passwords.txt"
        target_dir = os.path.dirname(password_path)
        os.makedirs(target_dir, exist_ok=True)

        with open(password_path, "w") as password_file:
            password_file.write('')

    def generate_key(self):
        flash_path = self.folder_path

        v1 = generate_sum(self.key_string)
        h1 = generate_headers()

        with open(f'{flash_path}\key.txt', 'w', encoding='utf-8') as f:
            f.write(' '.join(v1) + '\n')
            f.write(' '.join(h1) + '\n')

        self.save_key = create_numeric_form(self.key_string)
        self.key_string = None

    def add_password(self, username, password, service):
        password_path = r"C:\Program Files\SCAT\passwords.txt"
        target_dir = os.path.dirname(password_path)
        os.makedirs(target_dir, exist_ok=True)

        k = key_generator(self.save_key)
        with open(password_path, 'a', encoding='utf-8') as f:
            B = X256()
            encoded_value = B.generate(password, k)
            f.write(f'{str(encoded_value)} -- {self.last_index} -- {username} -- {self.last_index} -- {service}\n')

        with open(f'{self.folder_path}\key.txt', 'a', encoding='utf-8') as f:
            f.write(str(hex(self.last_index)[2:].zfill(2)) + ' ' + ' '.join(k) + '\n')

        self.last_index += 1

    # def clear_password(self, number):
