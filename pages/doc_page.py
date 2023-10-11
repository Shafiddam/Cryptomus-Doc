import json
import os
import re
import secrets
import string
from datetime import datetime
from time import sleep

import cv2
import pytest
from PIL import Image

from pyzbar.pyzbar import decode
from selenium.common import TimeoutException, NoSuchElementException
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.wait import WebDriverWait

from .base_page import BasePage
from ..data.data import *


class DocPage(BasePage):
    class Locators:
        # region
        DASHBOARD_URL = 'https://app.cryptomus.com/dashboard/'
        INPUT_SEARCH = (By.XPATH, input_search)
        # endregion

    def __init__(self, driver, timeout=10):
        super().__init__(driver, timeout)
        self.driver = driver
        self.wait = WebDriverWait(driver, 10)

    def find_input_search(self):
        self.wait.until(EC.visibility_of_element_located(self.Locators.INPUT_SEARCH))

    def search_area(self, word):
        try:
            locator = (By.CSS_SELECTOR, 'div.header > div > div > div.content__search-area > ul')
            # ввод слова в поле инпута
            element = self.wait.until(EC.visibility_of_element_located(self.Locators.INPUT_SEARCH))
            element.click()
            element.send_keys(word)
            # находим область вывода (список) "div.content__search-area > ul"
            self.wait.until(EC.visibility_of_element_located(locator))
            return True
        except TimeoutException:
            return None

    def rm_merchant(self, merchant_name):
        """ remove merchant """
        try:
            delete_button_locator = (By.CSS_SELECTOR, ".active.merchant__item button.btn__delete")
            self.wait.until(EC.presence_of_element_located(delete_button_locator)).click()

            return True
        except TimeoutException:
            return None

    def find_currency_network_on_site(self, currency, network):
        network_lower = f'{network}'.lower()  # на сайте все в нижнем регистре
        locator = (By.XPATH, f"//span[@class='info__currency-code' and text()='{currency}']"
                             f"/following-sibling::span[@class='info__network-code' and text()='{network_lower}']")
        try:
            element = self.wait.until(EC.visibility_of_element_located(locator))
            return element
        except TimeoutException:
            return False

    def click_delete_in_add_address(self, currency, network):
        network_lower = f'{network}'.lower()  # на сайте все в нижнем регистре
        locator = (By.XPATH, f"//div[contains(@class, 'item__info') and .//span[@class='info__currency-code' and "
                             f"text()='{currency}'] and .//span[@class='info__network-code' and "
                             f"text()='{network_lower}']]//following-sibling::div[contains(@class, "
                             f"'item__actions')]//button//span[text()='Delete']")
        try:
            self.wait.until(EC.visibility_of_element_located(locator)).click()
            sleep(1)
        except TimeoutException:
            return False

    def find_address_on_site(self, address):
        locator = (By.XPATH, f"//span[@class='details__value' and text()='{address}']")
        try:
            element = self.wait.until(EC.visibility_of_element_located(locator))
            return element
        except TimeoutException:
            return False

    def find_error_description(self, error_description):
        locator = (By.XPATH, f"//span[@class='error__description' and text()='{error_description}']")
        try:
            element = self.wait.until(EC.visibility_of_element_located(locator))
            return element
        except TimeoutException:
            return False

    def find_merchant_name(self, merchant_name):
        try:
            merchant_locator = (By.XPATH, f"//*[contains(text(), '{merchant_name}')]")
            element = self.wait.until(EC.visibility_of_element_located(merchant_locator))
            return element
        except TimeoutException:
            return None

    def _send_keys_to_input(self, locator, data):
        input_element = self.wait.until(EC.visibility_of_element_located(locator))
        input_element.click()
        input_element.clear()
        input_element.send_keys(data)

    def compare_url_dashboard(self):
        """
        Сравнение url, проверяем что вошли на дашборд
        """
        self.wait.until(EC.url_to_be('https://app.cryptomus.com/dashboard/')),

    def select_and_click_on_ticket(self, subject):
        """ ищем тему и кликаем """
        locator = (By.XPATH,
                   f"//div[@class='Tickets_table_column__bbD8V' and contains(text(), '{subject}')]")

        try:
            self.wait.until(EC.visibility_of_element_located(locator)).click()
            return True
        except TimeoutException:
            raise Exception("Не удалось найти тему в течение ожидания!")

    def click_selected_network_in_add_address(self, network):
        """ клик на уже выбранную ранее сеть при добавлении адреса в автовыводе """
        network_locator_1 = (By.XPATH, "//div[@class='title__text']//span[text()='Select network']")
        network_locator_2 = (By.XPATH, f"//li//span[@class='text__name' and text()='{network}']")
        try:
            self.wait.until(EC.visibility_of_element_located(network_locator_1)).click()
            sleep(2)
            self.wait.until(EC.visibility_of_element_located(network_locator_2)).click()
            return True
        except TimeoutException:
            return None

    def click_frequency_of_withdrawals(self, value):
        button_locator = (By.XPATH, f"//button[@value='{value}']")
        self.wait.until(EC.visibility_of_element_located(button_locator)).click()

    def check_usdt_polygon_present(self):
        usdt_locator = "//div[contains(@class, 'payment-details-wallet__subheading')]//span[text()='USDT']"
        polygon_locator = \
            "//div[contains(@class, 'payment-details-wallet__subheading')]//span[text()='Network · POLYGON   ']"

        usdt_element = self.wait.until(EC.presence_of_element_located((By.XPATH, usdt_locator)))
        polygon_element = self.wait.until(EC.presence_of_element_located((By.XPATH, polygon_locator)))

        assert usdt_element is not None, "USDT not found on the page!"
        assert polygon_element is not None, "POLYGON not found on the page!"

    def check_amount_currency_name(self, amount, currency, name):
        """ Проверка наличия amount , currency, name на пейформе """
        amount_locator = f"//span[contains(@class, 'payment-details__amount') and text()='{amount}']"
        currency_locator = f"//span[contains(@class, 'payment-details__amount') and text()='{currency}']"
        name_locator = f"//div[contains(@class, 'payment-details__subheading')]//span[contains(text(), '{name}')]"

        amount_element = self.wait.until(EC.presence_of_element_located((By.XPATH, amount_locator)))
        currency_element = self.wait.until(EC.presence_of_element_located((By.XPATH, currency_locator)))
        name_element = self.wait.until(EC.presence_of_element_located((By.XPATH, name_locator)))

        assert amount_element, f"{amount} not found on the page!"
        assert currency_element, f"{currency} not found on the page!"
        assert name_element, f"{name} not found on the page!"

    def find_balance_value_rub(self):
        """ поиск  """
        locator = "//span[@class='balance__value']//div[contains(text(), '₽')]"
        try:
            self.wait.until(EC.visibility_of_element_located((By.XPATH, locator)))
            return True
        except TimeoutException:
            return False

    def find_balance_value_currency(self, currency):
        """Поиск символа валюты на странице."""
        symbol = currency_symbols.get(currency)  # Получаем символ валюты из словаря
        if not symbol:
            raise ValueError(f"Unsupported currency code: {currency}")
        # Создаем локатор с помощью полученного символа
        locator = f"//span[@class='balance__value']//div[contains(text(), '{symbol}')]"
        try:
            self.wait.until(EC.visibility_of_element_located((By.XPATH, locator)))
            return True
        except TimeoutException:
            return False

    def find_pay_recepient_address(self):
        """ поиск адреса """
        locator = "//span[@class='address__text']"
        try:
            element = self.wait.until(EC.visibility_of_element_located((By.XPATH, locator)))
            return element.text
        except TimeoutException:
            return False

    def find_commission_in_manual_convert(self):
        """ поиск Commission в мануал-конверте и значения (0 BTC) """
        div_element = '//div[contains(@class, "WalletManualConvertCrypto_data__WkV8p")]//p[text()="Commission"]'

        try:
            commission_text = self.wait.until(EC.visibility_of_element_located((By.XPATH, div_element)))
            value_element = commission_text.find_element(By.XPATH, "following-sibling::p")

            return commission_text, value_element.text
        except TimeoutException:
            return False

    def check_fiat_amount_crypto_amount_network_in_pay_present(self):
        """ поиск fiat amount, currency amount и network в пейформе """
        usdt_locator = "//div[contains(@class, 'payment-details__amount')]//span[text()='USDT']"
        usd_locator = "//div[contains(@class, 'subheading__currency')]//span[text()='USD']"
        polygon_locator = \
        "//div[contains(@class, 'subheading__currency')]/following-sibling::span[contains(text(), 'Network · POLYGON')]"

        usdt_element = self.wait.until(EC.presence_of_element_located((By.XPATH, usdt_locator)))
        usd_element = self.wait.until(EC.presence_of_element_located((By.XPATH, usd_locator)))
        polygon_element = self.wait.until(EC.presence_of_element_located((By.XPATH, polygon_locator)))

        assert usdt_element is not None, "USDT not found on the page!"
        assert usd_element is not None, "USD not found on the page!"
        assert polygon_element is not None, "POLYGON not found on the page!"

    def check_fiat_crypto_in_pay_present(self, crypta, fiat):
        """ поиск fiat amount, currency amount и network в пейформе """
        crypta_locator = f"//div[contains(@class, 'payment-details__amount')]//span[text()='{crypta}']"
        fiat_locator = f"//div[contains(@class, 'subheading__currency')]//span[text()='{fiat}']"

        crypta_element = self.wait.until(EC.presence_of_element_located((By.XPATH, crypta_locator)))
        fiat_element = self.wait.until(EC.presence_of_element_located((By.XPATH, fiat_locator)))

        assert crypta_element is not None, f"{crypta} not found on the page!"
        assert fiat_element is not None, f"{fiat} not found on the page!"

    def check_fiat_in_pay_present(self, amount, fiat):
        """ поиск fiat amount в пейформе """
        fiat_locator = f"//div[contains(@class, 'subheading__currency')]" \
                       f"//span[text()='{amount}']/following-sibling::span[text()='{fiat}']"

        fiat_element = self.wait.until(EC.presence_of_element_located((By.XPATH, fiat_locator)))
        assert fiat_element is not None, f"{amount} {fiat} not found on the page!"

    def check_fiat_crypto_network_in_pay_present(self, crypta, fiat, network):
        """ поиск fiat amount, currency amount и network в пейформе """
        crypta_locator = f"//div[contains(@class, 'payment-details__amount')]//span[text()='{crypta}']"
        fiat_locator = f"//div[contains(@class, 'subheading__currency')]//span[text()='{fiat}']"
        network_locator = f"//div[contains(@class, 'subheading__currency')]/following-sibling::span[contains(text()," \
                          f" 'Network · {network}')]"

        crypta_element = self.wait.until(EC.presence_of_element_located((By.XPATH, crypta_locator)))
        fiat_element = self.wait.until(EC.presence_of_element_located((By.XPATH, fiat_locator)))
        network_element = self.wait.until(EC.presence_of_element_located((By.XPATH, network_locator)))

        assert crypta_element is not None, f"{crypta} not found on the page!"
        assert fiat_element is not None, f"{fiat} not found on the page!"
        assert network_element is not None, f"{network} not found on the page!"

    def check_convert_fiat_usd_crypto_usdt_in_pay_from_binance(self, amount_to_send):
        """ проверка правильности выставления суммы в крипте. Открываем курс USDT/USD на БИНАНС в новой вкладке."""
        link = 'https://www.binance.com/en/price/tether'
        self.driver.execute_script("window.open('');")  # открываем новую вкладку
        self.driver.switch_to.window(self.driver.window_handles[-1])  # переключаемся на новую вкладку
        self.driver.get(link)

        # надо принять куки:
        btn_accept_cookies_binance = "//button[@id='onetrust-accept-btn-handler']"
        self.wait.until(EC.presence_of_element_located((By.XPATH, btn_accept_cookies_binance))).click()

        # ищем курс:
        sleep(3)
        locator = "//div[@data-bn-type='text' and contains(@class, 'css-') " \
                  "and contains(text(), 'USD') and contains(text(), '$')]"
        element = self.wait.until(EC.visibility_of_element_located((By.XPATH, locator)))
        text_value = element.text  # забираем число

        # сумма из текста
        match = re.search(r"\$ (\d+\.\d+) per", text_value)
        if match:
            amount = float(match.group(1))
        else:
            # обработка ошибки, если не найдено соответствие
            print("Не удалось найти число в строке.")
            return None

        # Возвращаемся на первую вкладку (на сайт):
        self.driver.switch_to.window(self.driver.window_handles[0])
        return float(amount_to_send) / amount

    def check_convert_fiat_usd_crypto_trx_in_pay_from_binance(self, amount_to_send):
        """ проверка правильности выставления суммы в крипте. Открываем курс на БИНАНС в новой вкладке."""
        link = 'https://www.binance.com/en/price/tron'
        self.driver.execute_script("window.open('');")  # открываем новую вкладку
        self.driver.switch_to.window(self.driver.window_handles[-1])  # переключаемся на новую вкладку
        self.driver.get(link)

        # надо принять куки:
        btn_accept_cookies_binance = "//button[@id='onetrust-accept-btn-handler']"
        self.wait.until(EC.presence_of_element_located((By.XPATH, btn_accept_cookies_binance))).click()

        # ищем курс:
        sleep(3)
        locator = "//div[@data-bn-type='text' and contains(@class, 'css-') " \
                  "and contains(text(), 'USD') and contains(text(), '$')]"
        element = self.wait.until(EC.visibility_of_element_located((By.XPATH, locator)))
        text_value = element.text  # забираем число
        print('\n',text_value)

        # сумма из текста
        match = re.search(r"\$ (\d+\.\d+) per", text_value)
        if match:
            amount = float(match.group(1))
        else:
            # обработка ошибки, если не найдено соответствие
            print("Не удалось найти число в строке.")
            return None

        # Возвращаемся на первую вкладку (на сайт):
        self.driver.switch_to.window(self.driver.window_handles[0])
        return float(amount_to_send) / amount

    def get_site_value(self):
        """ Получение суммы в крипте с сайта """
        site_value_locator = "//span[@class='payment-details__amount']"
        site_value_element = self.wait.until(EC.presence_of_element_located((By.XPATH, site_value_locator)))
        site_value = float(site_value_element.text)
        return site_value

    def get_site_value_recurring(self):
        """ Получение суммы в крипте с сайта В РЕКУРЕНТКАХ """
        site_value_locator = "//div[contains(@class, 'payment-details__subheading')]/span[1]"
        site_value_element = self.wait.until(EC.presence_of_element_located((By.XPATH, site_value_locator)))
        site_value = float(site_value_element.text)
        return site_value

    def check_amount_currency_in_pay(self, amount, currency):
        """ поиск amount и currency в пейформе """
        amount_locator = f"//span[@class='payment-details__amount'][text()='{amount}']"
        currency_locator = f"//span[@class='payment-details__amount'][text()='{currency}']"
        try:
            amount_element = self.wait.until(EC.visibility_of_element_located((By.XPATH, amount_locator)))
            currency_element = self.wait.until(EC.visibility_of_element_located((By.XPATH, currency_locator)))

            assert amount_element, f"{amount} not found on the page!"
            assert currency_element, f"{currency} not found on the page!"

            return True
        except TimeoutException:
            return False

    def check_link_and_button(self):
        # Локатор для ссылки, в которой содержится кнопка
        link_locator = "//a[contains(@href, 'https://app.cryptomus.com/dashboard/get')]"
        button_locator = ".btn.primary"

        # Проверка, что ссылка правильная
        link_element = self.wait.until(EC.presence_of_element_located((By.XPATH, link_locator)))
        assert link_element.get_attribute("href") == "https://app.cryptomus.com/dashboard/get", "Неверная ссылка!"

        # Проверка кликабельности кнопки
        try:
            button_element = self.wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, button_locator)))
            assert button_element, "Кнопка не кликабельна!"
        except TimeoutException:
            assert False, "Кнопка не найдена или не кликабельна!"
        return button_element

    def check_text_enough_funds_in_pay(self):
        heading_text_locator = ".status-hint__heading-text"
        status_hint_locator = "//p[@class='status-hint__description']" \
                              "[text()='Top up your Cryptomus balance to confirm a recurring payment.']"

        try:
            # self.wait.until(EC.presence_of_element_located((By.XPATH, heading_text_locator)))
            self.wait.until(EC.visibility_of_element_located((By.CSS_SELECTOR, heading_text_locator)))
            heading_text_visible = True
        except TimeoutException:
            heading_text_visible = False

        try:
            self.wait.until(EC.visibility_of_element_located((By.XPATH, status_hint_locator)))
            status_hint_visible = True
        except TimeoutException:
            status_hint_visible = False

        return heading_text_visible, status_hint_visible

    def pay_qr_code_screenshot_name(self, test_name):
        """ Создание скриншота qr-кода в ПЕЙФОРМЕ и сохранение в папку screenshot с именем теста """
        locator = ".info__qr-wrapper"
        qr_code_address = self.wait.until(EC.visibility_of_element_located((By.CSS_SELECTOR, locator)))
        # путь к папке screenshot, которая находится на одном уровне с pages
        screenshot_folder = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), 'screenshot')
        # Если папка не существует, создаем ее
        if not os.path.exists(screenshot_folder):
            os.makedirs(screenshot_folder)
        sleep(1)  # надо явно задать паузу, иначе скриншот не распознается
        screenshot_name = f"{test_name}_pay_qr_code.png"
        screenshot_path = os.path.join(screenshot_folder, screenshot_name)
        qr_code_address.screenshot(screenshot_path)
        return screenshot_path

    @staticmethod
    def qr_code_screenshot_decode(screenshot_path):
        """ Загрузка изображения и распознование (вход по QR-коду)"""
        try:
            image = Image.open(screenshot_path)
            # ниже строки по ДОРАБОТКЕ картинки, можно убрать
            # image = image.convert("L")  # преобразование в оттенки серого
            # image = ImageEnhance.Contrast(image).enhance(2)  # увеличение контраста
            # image = image.filter(ImageFilter.MedianFilter(size=3))  # уменьшение шума
            # image = image.resize((int(image.width * 1.5), int(image.height * 1.5)),
            #                      Image.ANTIALIAS)  # увеличение размера изображения
        except Exception as e:
            print(f"Не удалось загрузить изображение из {screenshot_path}!")
            print(f"Ошибка: {e}")
            return
        # Распознавание QR-кода
        decoded_objects = decode(image)
        # Печать распознанных данных
        for obj in decoded_objects:
            # получается текст: адрес кошелька, ссылка на инвойс, ссылка на тонкипер или телеграм ...
            data = obj.data.decode('utf-8')
            return data

    @staticmethod
    def qr_code_screenshot_decode2(screenshot_path):
        """ Второй метод по декоду картинки, на основе библиотеки CV2 """

        image = cv2.imread(screenshot_path)
        if image is None:
            print("Ошибка загрузки изображения.")
            return

        gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        _, thresholded = cv2.threshold(gray, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)

        detector = cv2.QRCodeDetector()
        val, pts, qr_code = detector.detectAndDecode(image)
        if val:
            return val

    def get_market_price_from_binance(self, crypta_from, crypta_to):
        self.driver.execute_script("window.open('');")  # открываем новую вкладку
        self.driver.switch_to.window(self.driver.window_handles[-1])  # переключаемся на новую вкладку
        url = f"https://www.binance.com/ru/trade/{crypta_from}_{crypta_to}?theme=dark&type=spot"
        price_locator = (By.XPATH, "//div[@class='showPrice']")
        self.driver.get(url)
        try:
            btn_accept_cookies_binance = "//button[@id='onetrust-accept-btn-handler']"
            self.wait.until(EC.element_to_be_clickable((By.XPATH, btn_accept_cookies_binance))).click()
        except TimeoutException:
            pass  # Если кнопка не найдена, просто продолжаем
        try:
            market_price = self.wait.until(EC.visibility_of_element_located(price_locator))
            price = market_price.text
        except TimeoutException:
            price = None  # или какое-то другое действие в случае ошибки
        self.driver.close()
        self.driver.switch_to.window(self.driver.window_handles[0])  # возвращаемся в первоначальное окно
        return price

    def scroll_page(self, amount):
        """ Прокрутка страницы на "amount" пикселей вниз (или вверх, если ввести -) """
        self.driver.execute_script(f"window.scrollBy(0, {amount});")

    def scroll_to_top(self):
        """ Прокрутка страницы на самый верх """
        self.driver.execute_script("window.scrollTo(0, 0);")

    def find_text_convert(self, find_text_convert):
        """ Поиск find_text_convert """
        locator = (By.XPATH,
                   f"//p[starts-with(@class, 'TransactionHeaderItem_titleText')]/span[text()='{find_text_convert}']")
        element = self.wait.until(EC.visibility_of_element_located(locator))
        return element

    def find_amount_convert_in_transaction(self, find_amount_convert_in_transaction):
        """ Поиск find_amount_convert_in_transaction """
        locator = (By.XPATH, f"//p[starts-with(@class, "
                        f"'TransactionHeaderItem_amountTitle')][text()='{find_amount_convert_in_transaction}']")
        element = self.wait.until(EC.visibility_of_element_located(locator))
        return element

    def find_method_amount_convert_status_in_order_history(self, metod, find_amount_convert_in_transaction, status):
        """ Поиск method_amount_convert_status_in_order_history """
        locator = (By.XPATH, f"//div[contains(@class, 'WalletManualConvertHistoryTableRow_row__header__') and "
                             f".//p[contains(@class, 'WalletManualConvertHistoryTableRow_row_value__VDwmw') and text()='{metod}'] and "
                             f".//p[contains(@class, 'from_cell') and text()='{find_amount_convert_in_transaction}'] and "
                             f".//span[contains(@class, 'WalletManualConvertHistoryTableRow_done__PbiHF') and text()='{status}']]")
        try:
            element = self.wait.until(EC.visibility_of_element_located(locator))
            return element
        except NoSuchElementException:
            pytest.fail("Ошибка: не найдено - не все условия выполнены (метод, сумма, статус)!")

    def click_expand_in_found_order(self, metod, find_amount_convert_in_transaction, status):
        locator = (By.XPATH,
                   f"//div[contains(@class, 'WalletManualConvertHistoryTableRow_row__header__') and "
                   f".//p[contains(@class, 'WalletManualConvertHistoryTableRow_row_value__VDwmw') and text()='{metod}'] and "
                   f".//p[contains(@class, 'from_cell') and text()='{find_amount_convert_in_transaction}'] and "
                   f".//span[contains(@class, 'WalletManualConvertHistoryTableRow_done__PbiHF') and text()='{status}']]"
                   f"//div[contains(@class, 'WalletManualConvertHistoryTableRow_title__icon__eYKZS')]")
        try:
            element = self.wait.until(EC.element_to_be_clickable(locator))
            element.click()
        except TimeoutException:
            pytest.fail("Ошибка: не найдено - не все условия выполнены (метод, сумма, статус)!")

    def click_expand_in_found_order_active(self, metod, find_amount_convert_in_transaction, status):
        locator = (By.XPATH,
                   f"//div[contains(@class, 'WalletManualConvertHistoryTableRow_row__header__') and "
                   f".//p[contains(@class, 'WalletManualConvertHistoryTableRow_row_value__VDwmw') and text()='{metod}'] and "
                   f".//p[contains(@class, 'from_cell') and text()='{find_amount_convert_in_transaction}'] and "
                   f".//span[contains(@class, 'WalletManualConvertHistoryTableRow_active') and text()='{status}']]"
                   f"//div[contains(@class, 'WalletManualConvertHistoryTableRow_title__icon__eYKZS')]")
        try:
            element = self.wait.until(EC.element_to_be_clickable(locator))
            element.click()
        except TimeoutException:
            pytest.fail("Ошибка: не найдено - не все условия выполнены (метод, сумма, статус)!")

    def find_settlement_date_in_order_history(self):
        """ Поиск settlement_date_in_order_history """
        current_date = datetime.now()  # получаем текущие дату-время, пример: 2023-09-26 18:52:10.427038
        formatted_date = current_date.strftime('%d.%m.%Y')  # 26.09.2023 (так в order_history выводится)
        locator = (By.XPATH, f"//p[contains(@class, 'WalletManualConvertHistoryTableRow_footer__item__value__') "
                             f" and text()='{formatted_date}']")
        try:
            element = self.wait.until(EC.visibility_of_element_located(locator))
            return element
        except TimeoutException:
            print("Не удалось найти текущую дату в Оrder_history в течение ожидания!")
            return False

    def transfer_to_p2p(self):
        # кликаем на "transfer_to"
        self.wait.until(EC.visibility_of_element_located((By.XPATH,
                        "//span[@class='css-1hugxjs'][text()='personal wallet']"))).click()
        self.wait.until(EC.visibility_of_element_located((By.XPATH,
                        "//span[@class='css-1hugxjs'][text()='P2P trade wallet']"))).click()
        sleep(1)

    def transfer_to_p2p_from_personal(self):
        # кликаем на "transfer_to"
        self.wait.until(EC.visibility_of_element_located((By.XPATH,
                        "//span[@class='css-1hugxjs'][text()='business wallet']"))).click()
        self.wait.until(EC.visibility_of_element_located((By.XPATH,
                        "//span[@class='css-1hugxjs'][text()='P2P trade wallet']"))).click()
        sleep(1)

    def transfer_to_business(self):
        # кликаем на "transfer_to"
        self.wait.until(EC.visibility_of_element_located((By.XPATH,
                        "//span[@class='css-1hugxjs'][text()='personal wallet']"))).click()
        self.wait.until(EC.visibility_of_element_located((By.XPATH,
                        "//span[@class='css-1hugxjs'][text()='business wallet']"))).click()
        sleep(1)

    def get_unique_subject_for_ticket(self):
        current_datetime = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        unique_message = f"Message from autotest - {current_datetime}"
        return unique_message

    def get_transaction_record(self):
        """ Получение текущей даты, ее преобразование в формат как на фронте в транзакциях, поиск на странице """
        current_date = datetime.now()
        start_time = datetime.now()
        transaction_time = datetime.now()
        formatted_date = transaction_time.strftime("%d %B").lstrip("0")  # убираем ведущий ноль
        formatted_time = transaction_time.strftime("%H:%M")
        date_obj = datetime.strftime(current_date, "%d %B")
        self.wait.until(EC.visibility_of_element_located((By.XPATH, f"//*[contains(text(), '{date_obj}')]")))
        self.wait.until(EC.visibility_of_element_located
                        ((By.CSS_SELECTOR, ".TransactionItemNew_transactionItem__EqRL8"))).click()
        sleep(5)  # подождем, чтобы появилась запись на сайте
        print(f'\n{formatted_date} {formatted_time}')
        try:
            transaction_record = self.wait.until(
                EC.visibility_of_element_located((By.XPATH, f"//p[contains(@class, 'TransactionExtraInfoItem') "
                        f"and contains(text(), '{formatted_date}') and contains(text(), '{formatted_time}')]")))
        except TimeoutException:
            print("Не удалось найти запись транзакции в течение ожидания!")
            transaction_record = None

        record_time_text = transaction_record.text if transaction_record else None
        record_time = self.extract_datetime_from_element\
            (record_time_text,'%Y %d %B %H:%M') if record_time_text else None

        return transaction_record, record_time, start_time

    def get_transaction_time(self):
        """ Получение текущей даты, ее преобразование в формат как на фронте в транзакциях, поиск на странице """
        current_date = datetime.now()
        start_time = datetime.now()
        transaction_time = datetime.now()
        print(current_date)
        formatted_date = transaction_time.strftime("%d %B").lstrip("0")  # убираем ведущий ноль
        formatted_time = transaction_time.strftime("%H:%M")
        date_obj = datetime.strftime(current_date, "%d %B")
        self.wait.until(EC.visibility_of_element_located((By.XPATH, f"//*[contains(text(), '{date_obj}')]")))

        print(f'\n{formatted_date} {formatted_time} - {date_obj}')

        try:
            transaction_record = self.wait.until(
                EC.visibility_of_element_located((By.XPATH, f"//p[contains(@class, 'TransactionExtraInfoItem') "
                        f"and contains(text(), '{formatted_date}')]")))
        except TimeoutException:
            print("Не удалось найти запись транзакции в течение ожидания!")
            transaction_record = None

        record_time_text = transaction_record.text if transaction_record else None
        record_time = self.extract_datetime_from_element\
            (record_time_text,'%Y %d %B %H:%M') if record_time_text else None

        return transaction_record, record_time, start_time

    @staticmethod
    def extract_datetime_from_element(element_text, date_format):
        current_year = datetime.now().year
        # разбиваем текст элемента на дату и время, учитывая запятую
        date_str, time_str = element_text.split(", ")
        # формируем строку даты и времени с учетом текущего года
        record_datetime_str = f"{current_year} {date_str} {time_str}"
        return datetime.strptime(record_datetime_str, date_format)

    def click_trx_address(self):
        # находим строку с TRX, раскрываем ее(клик) и там должен быть адрес TK1bWEiuFoeL9ZsJnWpj6vcxBfLHnDXYGg:
        self.wait.until(EC.visibility_of_element_located((By.XPATH,
                        "//span[@class='info__currency-code'][text()='TRX']"))).click()
        # self.driver.find_element(By.XPATH, "//span[@class='info__currency-code'][text()='TRX']").click()

    def find_trx_address(self):
        """ поиск адреса TK1bWEiuFoeL9ZsJnWpj6vcxBfLHnDXYGg """
        address = self.wait.until(EC.visibility_of_element_located((By.XPATH,
                        "//span[@class='details__value'][text()='TK1bWEiuFoeL9ZsJnWpj6vcxBfLHnDXYGg']")))
        return address

    def click_to_dashboard(self):
        # кликаем на "To dashboard"
        self.wait.until(EC.visibility_of_element_located((By.XPATH,
                        "//span[@class='link__text'][text()='To dashboard']"))).click()

    def click_to_logout(self):
        # кликаем на "Logout"
        self.wait.until(EC.visibility_of_element_located((By.CSS_SELECTOR,
                        'div > div.dropdown-profile > div > button'))).click()
        self.wait.until(EC.visibility_of_element_located((By.XPATH, "//button[text()='Logout']"))).click()

    def date_time(self):
        """ метод поиска даты-времени и записи о транзакции: """
        # Получаем текущую дату:
        current_date = datetime.now()
        # Сохраните текущее время после совершения транзакции
        transaction_time = datetime.now()
        formatted_date = transaction_time.strftime("%d %B")
        # Форматирование объекта datetime в желаемый формат строку вида "16 August"
        date_obj = datetime.strftime(current_date, "%d %B")
        self.wait.until(EC.visibility_of_element_located
                       ((By.XPATH, f"//*[contains(text(), '{date_obj}')]")))
        self.wait.until(EC.visibility_of_element_located
                        ((By.CSS_SELECTOR, ".TransactionItemNew_transactionItem__EqRL8"))).click()
        sleep(5)  # подождем, чтобы появилась запись на сайте
        transaction_record = self.wait.until(EC.visibility_of_element_located
                        ((By.XPATH, f"//*[contains(text(), '{formatted_date}')]")))

        return date_obj, transaction_record

    def find_element_1(self):
        # находим "TRX Received":
        element_1 = self.wait.until(EC.visibility_of_element_located((By.XPATH,
                        "//p[@class='TransactionHeaderItem_titleText__PI2MO'][text()='TRX Received']")))
        return element_1

    def find_element_2(self):
        # находим адрес получения TK1bWEiuFoeL9ZsJnWpj6vcxBfLHnDXYGg:
        element_2 = self.wait.until(EC.visibility_of_element_located((By.XPATH,
                    "//p[@class='TransactionExtraInfoItem_value__Wyq6r'][text()='TK1bWEiuFoeL9ZsJnWpj6vcxBfLHnDXYGg']")))
        return element_2

    def find_element_3(self):
        # находим сумму "1 TRX":
        element_3 = self.wait.until(EC.visibility_of_element_located((By.XPATH,
                     "//p[@class='TransactionHeaderItem_amountTitle__P8Y7D'][text()='1 TRX']")))
        return element_3

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
        """ Сохраняет словарь паролей в JSON-файл """
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
        """ Загружает словарь паролей из JSON-файла """
        try:
            with open(filename, 'r') as file:
                self.passwords_dict = json.load(file)
        except FileNotFoundError:
            # Файл не найден, можно обработать ошибку или просто пропустить
            pass
