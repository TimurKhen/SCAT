import os

from X256.X256 import X256
from key.keyGenerator import generate_headers, key_generator


class Key:
    def __init__(self, folder_path, last_password_index=0):
        self.folder_path = folder_path
        if last_password_index == 0:
            self.last_index = 1
        else:
            self.last_index = last_password_index

    def run(self):
        self.generate_key()

    def generate_key(self):
        flash_path = self.folder_path

        h1 = generate_headers()
        with open(f'{flash_path}/key.txt', 'w', encoding='utf-8') as f:
            f.write(' '.join(h1) + '\n')


    def add_password(self, username, password, service):
        password_path = "C://SCAT/passwords.txt"

        if not os.path.exists(password_path):
            try:
                with open(password_path, 'w') as f:
                    f.write('')
            except FileExistsError:
                print(f'No file exists {password_path}')

        k = key_generator()
        with open(password_path, 'a', encoding='utf-8') as f:
            B = X256()
            encoded_value = B.generate(password, k)
            f.write(f'{str(encoded_value)} {self.last_index} {username} {service}\n')
            f.close()

        with open(f'{self.folder_path}/key.txt', 'a', encoding='utf-8') as f:
            f.write(str(hex(self.last_index)[2:].zfill(2)) + ' ' + ' '.join(k) + '\n')

        self.last_index += 1
