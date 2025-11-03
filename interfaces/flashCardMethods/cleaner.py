class Cleaner:
    def __init__(self, folder_path):
        self.folder_path = folder_path

    def run(self):
        try:
            self.formatter()
        except Exception as e:
            return f'Unexpected error: {e}'

    def formatter(self):
        import subprocess

        flash_path = self.folder_path

        try:
            subprocess.run(f'format {flash_path} /fs:fat32 /q /y', check=True, shell=True)
            print(f'Флешка {flash_path} была успешно отформатирована.')
        except subprocess.CalledProcessError as e:
            print(f'Ошибка при форматировании флешки: {e}')
