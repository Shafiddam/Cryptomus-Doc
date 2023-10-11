import os
from time import sleep

import pyotp
from selenium.webdriver.support.wait import WebDriverWait

# from ..data.secret_keys import secret_keys


class BasePage:
    current_directory = os.path.dirname(os.path.abspath(__file__))
    counter2_file_path = os.path.join(current_directory, '..', 'data', 'counter2.txt')

    def __init__(self, driver, timeout=10):
        self.driver = driver
        self.wait = WebDriverWait(driver, 10)

    # @staticmethod
    # def take_screenshot(self, driver, screenshot_name, screenshots_folder="screenshots"):
    #     if not os.path.exists(screenshots_folder):
    #         os.makedirs(screenshots_folder)
    #     screenshot_path = os.path.join(screenshots_folder, screenshot_name)
    #     driver.save_screenshot(screenshot_path)
    #     print(f"Screenshot saved as {screenshot_path}")

    def open_new_tab_with_link(self, link):
        """ Открывает новую вкладку и переходит по данной ссылке """
        self.driver.execute_script("window.open('');")  # открываем новую вкладку
        self.driver.switch_to.window(self.driver.window_handles[-1])  # переключаемся на новую вкладку
        self.driver.get(link)  # переходим по ссылке

    def code2fa(self, email, previous_code=None):
        """
        Генерация кода 2ФА. Если передан previous_code, генерируем новый код, отличный от предыдущего.
        """
        totp = pyotp.TOTP(self.secret_keys[email])
        code2fa = totp.now()

        while previous_code and code2fa == previous_code:
            sleep(1)  # ждем 1 секунду, чтобы гарантированно получить новый код
            code2fa = totp.now()

        return code2fa

    def generate_unique_merchant_name(self):
        """
        Метод создания уникального имени мерчанта на основе добавления +1 к имени Merch_name_000000001
        """
        # Попробуем прочитать счетчик из файла, и если его нет, создадим файл с начальным значением 1
        try:
            with open(self.counter2_file_path, 'r') as f:
                counter = int(f.read().strip())
        except FileNotFoundError:
            # Убедимся, что папка data существует
            if not os.path.exists('data'):
                os.makedirs('data')

            counter = 1
            with open(self.counter2_file_path, 'w') as f:
                f.write(str(counter))

            # Увеличиваем счетчик на 1 и форматируем имя мерчанта
        counter += 1
        merchant_name = f"Merch_name_{counter:09}"

        # Обновляем файл
        with open(self.counter2_file_path, 'w') as f:
            f.write(str(counter))

        # Возвращаем уникальное имя мерчанта
        return merchant_name

