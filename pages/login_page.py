import json
import os
import secrets
import string
from time import sleep
import re

from PIL import Image
from pyzbar.pyzbar import decode
from selenium.common import TimeoutException
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from datetime import datetime, date

from .base_page import BasePage
from .dashboard_page import DashboardPage
from ..data.data import *

current_directory = os.path.dirname(os.path.abspath(__file__))
counter_file_path = os.path.join(current_directory, '..', 'data', 'counter.txt')


class LoginPage(BasePage):
    base_email = "enot_2022_001"
    domain = "@mail.ru"

    class Locators:
        LOGIN_URL = 'https://app.cryptomus.com/login'
        FORGOT_PASSWORD_LINK = (By.XPATH, selector_password_link)
        FORGOT_PASSWORD_INPUT_LOGIN = (By.CSS_SELECTOR, selector_input_login)
        FORGOT_PASSWORD_INPUT_CODE = (By.CSS_SELECTOR, selector_input_code)
        SELECTOR_RESET_CONTINUE = (By.XPATH, selector_reset_continue)
        SELECTOR_RESET_CONFIRM = (By.XPATH, selector_reset_confirm)
        SELECTOR_LOGIN_CONFIRM = (By.XPATH, selector_login_confirm)
        SELECTOR_ENTER_PASSWORD = (By.CSS_SELECTOR, selector_enter_password)
        SELECTOR_RESET_CREATE = (By.XPATH, selector_reset_create)
        SELECTOR_BTN_LOGIN = (By.XPATH, selector_btn_login)
        SELECTOR_BTN_CREATE = (By.XPATH, selector_btn_create)
        SELECTOR_BTN_SIGNUP = (By.XPATH, selector_btn_signup)
        SELECTOR_BTN_TONKEEPER = (By.CSS_SELECTOR, selector_btn_tonkeeper)
        SELECTOR_BTN_TELEGRAM = (By.CSS_SELECTOR, selector_btn_telegram)
        BTN_GOOGLE_LOGIN = (By.CSS_SELECTOR, btn_google_login)
        SELECTOR_MODAL_TONKEEPER = (By.CSS_SELECTOR, selector_modal_tonkeeper)
        SELECTOR_QR_CODE_TONKEEPER = (By.CSS_SELECTOR, selector_qr_code_tonkeeper)
        SELECTOR_MESSAGE_TEXT = (By.XPATH, selector_message_text)
        SELECTOR_MESSAGE_TEXT2 = (By.XPATH, selector_message_text2)
        SELECTOR_QR_MESSAGE_TEXT = (By.XPATH, selector_qr_message_text)
        SELECTOR_QR_TONKEEPER_PICT = (By.CSS_SELECTOR, selector_qr_tonkeeper_pict)
        SELECTOR_BTN_QR_CODE = (By.CSS_SELECTOR, selector_btn_qr_code)
        SELECTOR_MODAL_QR_CODE = (By.CSS_SELECTOR, selector_modal_qr)
        SELECTOR_QR_CODE_PICT = (By.CSS_SELECTOR, selector_qr_code_pict)
        SELECTOR_AGREE_TERMS = (By.CLASS_NAME, agree_terms)
        ENTER_CODE = (By.CSS_SELECTOR, enter_code)
        # ... другие локаторы

    def prepare_before_settings(self, account_data):
        self.open()
        self.click_signup()
        new_email = self.get_new_email()  # создаем новый ящик
        self.send_keys(new_email)
        self.send_keys_password(password_for_new_email)
        self.click_agree_terms()
        self.click_create()
        # работа с окном mail_ru - код регистрации
        mail_page = MailPage(self.driver)
        mail_page.open_in_new_tab()
        mail_page.open_mail_ru()
        mail_page.login_mail_ru()
        mail_page.insert_user_name(account_data)
        mail_page.click_field_registration()
        code = mail_page.extract_code_from_mail()
        mail_page.switch_to_original_tab()
        self.enter_code(code)
        self.click_create()
        self.compare_url_dashboard()  # проверяем что вошли в дашборд
        # работа в дашборд
        dashboard_page = DashboardPage(self.driver)
        dashboard_page.click_out_new_feature()
        dashboard_page.confirm_cookies()
        return new_email

    def click_forgot_password(self):
        self.wait.until(EC.visibility_of_element_located(self.Locators.FORGOT_PASSWORD_LINK)).click()

    def open(self):
        self.driver.get(self.Locators.LOGIN_URL)

    def reset_continue(self):
        self.wait.until(EC.visibility_of_element_located(self.Locators.SELECTOR_RESET_CONTINUE)).click()

    def login_with_2fa(self, email, password_for_email):
        self.open()
        self.send_keys(email)
        self.send_keys_password(password_for_email)
        self.click_login()
        first_code2fa = self.code2fa(email)
        self.send_keys_2fa(first_code2fa)
        self.click_login_confirm()
        sleep(1)
        return first_code2fa

    def click_login(self):
        self.wait.until(EC.visibility_of_element_located(self.Locators.SELECTOR_BTN_LOGIN)).click()

    def click_create(self):
        self.wait.until(EC.visibility_of_element_located(self.Locators.SELECTOR_BTN_CREATE)).click()

    def click_signup(self):
        self.wait.until(EC.visibility_of_element_located(self.Locators.SELECTOR_BTN_SIGNUP)).click()

    def click_login_confirm(self):
        self.wait.until(EC.visibility_of_element_located(self.Locators.SELECTOR_LOGIN_CONFIRM)).click()

    def click_input_login(self):
        self.wait.until(EC.visibility_of_element_located(self.Locators.FORGOT_PASSWORD_INPUT_LOGIN)).click()

    def send_keys(self, data):
        self._send_keys_to_input(self.Locators.FORGOT_PASSWORD_INPUT_LOGIN, data)

    def send_keys_2fa(self, code2fa):
        self._send_keys_to_input(self.Locators.FORGOT_PASSWORD_INPUT_CODE, code2fa)

    def _send_keys_to_input(self, locator, data):
        input_element = self.wait.until(EC.visibility_of_element_located(locator))
        input_element.click()
        input_element.clear()
        input_element.send_keys(data)

    def click_agree_terms(self):
        self.wait.until(EC.visibility_of_element_located(self.Locators.SELECTOR_AGREE_TERMS)).click()

    def reset_confirm(self):
        self.wait.until(EC.visibility_of_element_located(self.Locators.SELECTOR_RESET_CONFIRM)).click()

    def enter_code(self, data):
        element = self.wait.until(EC.visibility_of_element_located(self.Locators.ENTER_CODE))
        element.click()
        element.send_keys(data)

    def send_keys_new_password(self, data):
        self._send_keys_to_input(self.Locators.SELECTOR_ENTER_PASSWORD, data)

    def send_keys_password(self, data):
        self.wait.until(EC.visibility_of_element_located(self.Locators.SELECTOR_ENTER_PASSWORD)).clear()
        self._send_keys_to_input(self.Locators.SELECTOR_ENTER_PASSWORD, data)

    def reset_create(self):
        self.wait.until(EC.visibility_of_element_located(self.Locators.SELECTOR_RESET_CREATE)).click()

    def click_login_tonkeeper(self):
        self.wait.until(EC.visibility_of_element_located(self.Locators.SELECTOR_BTN_TONKEEPER)).click()

    def click_signup_tonkeeper(self):
        self.wait.until(EC.visibility_of_element_located(self.Locators.SELECTOR_BTN_TONKEEPER)).click()

    def click_login_telegram(self):
        self.wait.until(EC.visibility_of_element_located(self.Locators.SELECTOR_BTN_TELEGRAM)).click()

    def click_login_google(self):
        self.wait.until(EC.visibility_of_element_located(self.Locators.BTN_GOOGLE_LOGIN)).click()

    def click_login_qr_code(self):
        self.wait.until(EC.visibility_of_element_located(self.Locators.SELECTOR_BTN_QR_CODE)).click()

    def modal_tonkeeper(self):
        # поиск модалки
        return self.wait.until(EC.visibility_of_element_located(self.Locators.SELECTOR_MODAL_TONKEEPER))

    def modal_qr_code(self):
        # поиск модалки
        return self.wait.until(EC.visibility_of_element_located(self.Locators.SELECTOR_MODAL_QR_CODE))

    def qr_code_tonkeeper(self):
        # поиск QR-кода
        return self.wait.until(EC.visibility_of_element_located(self.Locators.SELECTOR_QR_CODE_TONKEEPER))

    def qr_code_pict(self):
        # поиск QR-кода
        return self.wait.until(EC.visibility_of_element_located(self.Locators.SELECTOR_QR_CODE_PICT))

    def tonkeeper_message_text(self):
        # поиск названия модалки "Log in via TonKeeper"
        return self.wait.until(EC.visibility_of_element_located(self.Locators.SELECTOR_MESSAGE_TEXT))

    def tonkeeper_message_text2(self):
        # поиск названия модалки "Sign up via TonKeeper"
        return self.wait.until(EC.visibility_of_element_located(self.Locators.SELECTOR_MESSAGE_TEXT2))

    def qr_message_text(self):
        # поиск названия модалки "Log in with QR code"
        return self.wait.until(EC.visibility_of_element_located(self.Locators.SELECTOR_QR_MESSAGE_TEXT))

    def qr_code_tonkeeper_screenshot(self):
        """ Создание скриншота qr-кода (вход через тонкипер) и сохранение в папку screenshot """
        qr_code_modal = self.wait.until(EC.visibility_of_element_located(self.Locators.SELECTOR_QR_TONKEEPER_PICT))
        # путь к папке screenshot, которая находится на одном уровне с pages
        screenshot_folder = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), 'screenshot')
        # Если папка не существует, создаем ее
        if not os.path.exists(screenshot_folder):
            os.makedirs(screenshot_folder)
        sleep(1)  # надо явно задать паузу, иначе скриншот не распознается
        screenshot_path = os.path.join(screenshot_folder, 'qr_code_tonkeeper.png')
        qr_code_modal.screenshot(screenshot_path)
        return screenshot_path

    @staticmethod
    def qr_code_tonkeeper_screenshot_decode(screenshot_path):
        """ Загрузка изображения и распознование (вход через тонкипер) """
        try:
            image = Image.open(screenshot_path)
        except Exception as e:
            print(f"Не удалось загрузить изображение из {screenshot_path}!")
            print(f"Ошибка: {e}")
            return
        # Распознавание QR-кода
        decoded_objects = decode(image)
        # Печать распознанных данных
        for obj in decoded_objects:
            # получается ссылка вида https://app.tonkeeper.com/ton-connect?v=2&id=0e2ee91...и далее много символов
            data = obj.data.decode('utf-8')
            return data

    def qr_code_screenshot(self):
        """ Создание скриншота qr-кода и сохранение в папку screenshot (вход по QR-коду)"""
        qr_code_modal = self.wait.until(EC.visibility_of_element_located(self.Locators.SELECTOR_QR_CODE_PICT))
        # путь к папке screenshot, которая находится на одном уровне с pages
        screenshot_folder = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), 'screenshot')
        # Если папка не существует, создаем ее
        if not os.path.exists(screenshot_folder):
            os.makedirs(screenshot_folder)
        sleep(1)  # надо явно задать паузу, иначе скриншот не распознается
        screenshot_path = os.path.join(screenshot_folder, 'qr_code.png')
        qr_code_modal.screenshot(screenshot_path)
        return screenshot_path

    @staticmethod
    def qr_code_screenshot_decode(screenshot_path):
        """ Загрузка изображения и распознование (вход по QR-коду)"""
        try:
            image = Image.open(screenshot_path)
        except Exception as e:
            print(f"Не удалось загрузить изображение из {screenshot_path}!")
            print(f"Ошибка: {e}")
            return
        # Распознавание QR-кода
        decoded_objects = decode(image)
        # Печать распознанных данных
        for obj in decoded_objects:
            # получается ссылка вида https://app.tonkeeper.com/ton-connect?v=2&id=0e2ee91...и далее много символов
            data = obj.data.decode('utf-8')
            return data

    def compare_url_dashboard(self):
        """
        Сравнение url: проверяем, что вошли на дашборд
        """
        self.wait.until(EC.url_to_be('https://app.cryptomus.com/dashboard/'))

    def get_new_email(self):
        """ метод создания нового почтового ящика на основе добавления +1 к имени """
        # Попробуем прочитать счетчик из файла, и если его нет, создадим файл с начальным значением 0
        try:
            with open(counter_file_path, 'r') as f:
                counter = int(f.read().strip())
        except FileNotFoundError:
            # Убедимся, что папка data существует
            if not os.path.exists('data'):
                os.makedirs('data')
            counter = 0
            with open(counter_file_path, 'w') as f:
                f.write(str(counter))
        # Увеличиваем счетчик на 1
        counter += 1
        # Обновляем файл
        with open(counter_file_path, 'w') as f:
            f.write(str(counter))
        # Возвращаем новый email на основе счетчика
        return f"{self.base_email}+{counter}{self.domain}"


class MailPage(BasePage):
    class Locators:
        # селекторы страницы MAIL_RU:
        LINK_MAIL_RU = 'https://mail.ru/'
        BTN_ENTER_MAIL_PRIMARY = (By.CSS_SELECTOR, btn_enter_mail_primary)
        IFRAME_IFRAME = (By.CLASS_NAME, iframe_iframe)
        INPUT_USER_NAME = (By.CSS_SELECTOR, input_user_name)
        BTN_NEXT_BUTTON = (By.CSS_SELECTOR, btn_next_button)
        INPUT_PASSWORD = (By.CSS_SELECTOR, input_password)
        BTN_SUBMIT_BUTTON = (By.CSS_SELECTOR, btn_submit_button)
        FIELD_REGISTRATION = (By.XPATH, field_registration)
        FIELD_BINDING_GOOGLE_2FA = (By.XPATH, field_binding_google_2fa)
        BTN_BACK_IN_MAIL = (By.CSS_SELECTOR, btn_back_in_mail)
        FIELD_PERSONAL_WALLET_TRANSACTIONS = (By.XPATH, field_personal_wallet_transactions)
        FIELD_BUSINESS_WALLET_TRANSACTIONS = (By.XPATH, field_business_wallet_transactions)
        FIELD_P2P_WALLET_TRANSACTIONS = (By.XPATH, field_p2p_wallet_transactions)
        ATTACH_DOWNLOAD = (By.CSS_SELECTOR, attach_download)
        ELEMENT_CODE = (By.XPATH, element_code)
        ELEMENT_TEXT = (By.XPATH, element_text)

    def open_in_new_tab(self):
        """ открытие и переключение на новую вкладку """
        self.driver.execute_script("window.open('', '_blank');")
        self.driver.switch_to.window(self.driver.window_handles[1])

    def open_mail_ru(self):
        """" открытие ссылки майл-ру """
        self.driver.get(self.Locators.LINK_MAIL_RU)

    def login_mail_ru(self):
        """ клик на кнопку Войти на главной майл-ру """
        self.wait.until(EC.visibility_of_element_located(self.Locators.BTN_ENTER_MAIL_PRIMARY)).click()

    def insert_user_name(self, email):
        """ ввод логина в айфрейме входа в аккаунт, затем ввод пароля """
        iframe = self.wait.until(EC.presence_of_element_located(self.Locators.IFRAME_IFRAME))
        self.driver.switch_to.frame(iframe)
        email_input = self.wait.until(EC.presence_of_element_located(self.Locators.INPUT_USER_NAME))
        email_input.click()
        # sleep(2)
        email_input.send_keys(email)
        # sleep(2)
        self.wait.until(EC.visibility_of_element_located(self.Locators.BTN_NEXT_BUTTON)).click()
        # sleep(2)
        password_input = self.wait.until(EC.visibility_of_element_located(self.Locators.INPUT_PASSWORD))
        password_input.click()
        # sleep(2)
        password_input.send_keys('enot!@2022')
        # sleep(2)
        self.wait.until(EC.visibility_of_element_located(self.Locators.BTN_SUBMIT_BUTTON)).click()
        # sleep(2)
        self.driver.switch_to.default_content()

    def click_field_registration(self):
        """ клик на письмо с темой REGISTRATION """
        self.wait.until(EC.visibility_of_element_located(self.Locators.FIELD_REGISTRATION)).click()

    def click_field_binding_google_2fa(self):
        """ клик на письмо с темой BINDING_GOOGLE_2FA """
        self.wait.until(EC.visibility_of_element_located(self.Locators.FIELD_BINDING_GOOGLE_2FA)).click()

    def click_field_in_mail(self, field_in_mail):
        """ клик на письмо с темой field """
        locator = (By.XPATH, f"//span[@class='ll-sj__normal'][text()='{field_in_mail}']")
        self.wait.until(EC.visibility_of_element_located(locator)).click()

    def click_btn_back_in_mail(self):
        """ клик назад в почте """
        self.wait.until(EC.visibility_of_element_located(self.Locators.BTN_BACK_IN_MAIL)).click()

    def click_field_personal_wallet_transactions(self):
        """ клик на письмо с темой Personal wallet transactions """
        try:
            self.wait.until(EC.visibility_of_element_located(self.Locators.FIELD_PERSONAL_WALLET_TRANSACTIONS)).click()
            return True
        except TimeoutException:
            raise Exception("Не удалось найти письмо с темой Personal wallet transactions.")

    def click_field_wallet_transactions(self, wallet_locator):
        """Клик на письмо с заданной темой транзакции."""
        try:
            self.wait.until(EC.visibility_of_element_located(wallet_locator)).click()
            return True
        except TimeoutException:
            raise Exception(f"Не удалось найти письмо с темой {wallet_locator}.")

    def find_attach(self):
        try:
            self.wait.until(EC.visibility_of_element_located(self.Locators.ATTACH_DOWNLOAD))
            return True
        except TimeoutException:
            raise Exception("Ошибка: не удалось найти ссылку для скачивания!")

    def extract_code_from_mail(self):
        """ Извлекаем код из текста """
        # Ищем элемент с помощью XPath, который содержит текст "Your code:"
        element = self.wait.until(EC.visibility_of_element_located(self.Locators.ELEMENT_CODE))
        text = element.text
        # Извлекаем код из текста
        code = re.search(r'\d+', text).group()
        return code

    def extract_code_from_second_mail(self):
        """ Извлекаем код из текста второго сообщения """
        # Ищем все элементы с помощью XPath, которые содержат текст "Your code:"
        elements = self.wait.until(EC.presence_of_all_elements_located(self.Locators.ELEMENT_CODE))
        if len(elements) > 1:
            text = elements[1].text  # Извлекаем текст из второго элемента
            # Извлекаем код из текста
            code = re.search(r'\d+', text).group()
            return code
        else:
            # Обработка ошибки или возвращение None, если элементов меньше двух
            return None

    def extract_text_from_mail(self):
        """ Извлекаем текст из письма и проверяем содержимое, игнорируя дату и время """
        element = self.wait.until(EC.visibility_of_element_located(self.Locators.ELEMENT_TEXT))
        text = element.text
        # Заменяем дату и время на строку "DATETIME"
        cleaned_text = re.sub(r'\d{4}-\d{2}-\d{2} \d{2}:\d{2}', 'DATETIME', text)
        # Проверяем содержимое текста
        expected_text = "Withdrawals are frozen until DATETIME because you changed email"
        if cleaned_text == expected_text:
            return True
        else:
            return False

    def extract_code_from_mail_refactor(self, account_data, field_in_mail):
        """ Извлекаем код из письма """
        # работа с окном mail_ru
        mail_page = MailPage(self.driver)
        mail_page.switch_to_mail_tab()
        mail_page.click_btn_back_in_mail()
        sleep(10)  # подождем немного чтобы письмо пришло
        mail_page.click_field_in_mail(field_in_mail)
        code_from_mail = mail_page.extract_code_from_mail()
        mail_page.switch_to_original_tab()
        return code_from_mail

    def switch_to_original_tab(self):
        """ переключение на предыдущую вкладку (обратно в Криптомус) """
        self.driver.switch_to.window(self.driver.window_handles[0])

    def switch_to_mail_tab(self):
        """Переключение на вкладку с mail.ru"""
        self.driver.switch_to.window(self.driver.window_handles[1])

    def check_date_in_letter(self):
        """ Поиск текущей дата-время в письме """
        locator = (By.XPATH, "//div[@class='letter__date' and contains(text(), 'Сегодня')]")
        try:
            element = self.wait.until(EC.visibility_of_element_located(locator))
            date_time_text = element.text  # это будет строка "Today, 11:50"
            date_part, time_part = date_time_text.split(", ")  # делим на "Today" и "11:50"

            if date_part == "Сегодня":
                # Преобразование строки времени в объект datetime.time
                received_time = datetime.strptime(time_part, "%H:%M").time()

                # Получаем текущее время
                current_time = datetime.now().time()

                # Вычисляем разницу в секундах
                time_difference = (datetime.combine(date.min, current_time) - datetime.combine(date.min,
                                                                                               received_time)).seconds

                # Проверка, что разница не превышает 600 секунд
                assert time_difference <= 600, "Ошибка: разница во времени больше 600 секунд!"
            return True
        except TimeoutException:
            raise Exception("Не удалось найти текущую дату в письме в течение ожидания!")


class PasswordManager:

    def __init__(self):
        self.passwords_dict = {}

    @staticmethod
    def generate_password(length=10):
        """
        генерация нового пароля из 10 символов (обязательно одна заглавная и одна цифра)
        """
        alphabet = string.ascii_letters + string.digits + string.punctuation
        password = ''.join(secrets.choice(alphabet) for _ in range(length))
        # Check if the password contains at least one uppercase letter and one digit
        while not any(char.isupper() for char in password) or not any(char.isdigit() for char in password):
            password = ''.join(secrets.choice(alphabet) for _ in range(length))
        print("Пароль:", password)
        return password

    @staticmethod
    def save_password_to_env(password):
        """ Сохраняем пароль в переменной окружения """
        os.environ["AUTOMATION_PASSWORD"] = password

    @staticmethod
    def get_saved_password():
        """ получить сохраненный пароль из переменной окружения """
        return os.environ.get("AUTOMATION_PASSWORD", "")

    def save_password(self, login, password):
        """ Сохраняет пароль в словаре """
        self.passwords_dict[login] = password

    def save_to_json(self, filename='passwords.json'):
        """
        Сохраняет словарь паролей в JSON-файл
        """
        # Получаем директорию, в которой находится данный скрипт
        current_script_dir = os.path.dirname(os.path.abspath(__file__))
        # Возвращаемся на уровень вверх (из pages в Work)
        parent_dir = os.path.dirname(current_script_dir)
        # Создайте путь к папке data
        data_dir = os.path.join(parent_dir, 'data')
        # Если папка data не существует, создайте её
        if not os.path.exists(data_dir):
            os.makedirs(data_dir)
        # Создайте полный путь к файлу внутри папки data
        full_path = os.path.join(data_dir, filename)
        with open(full_path, 'w') as file:
            json.dump(self.passwords_dict, file)

    def load_from_json(self, filename='passwords.json'):
        """
        Загружает словарь паролей из JSON-файла
        """
        try:
            with open(filename, 'r') as file:
                self.passwords_dict = json.load(file)
        except FileNotFoundError:
            # Файл не найден, можно обработать ошибку или просто пропустить
            pass
