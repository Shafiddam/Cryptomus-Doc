import os

import pytest
from selenium import webdriver
from selenium.webdriver.chrome.options import Options  # для запуска браузера в безоконном режиме; на английском
from selenium.webdriver.chrome.service import Service


@pytest.fixture
def driver():
    """
    Функция для настройки браузера
    """
    chrome_options = Options()
    chrome_options.add_argument("--lang=en-US")  # Установите желаемый язык, например, en-US для английского
    # chrome_options.add_argument("--headless")
    driver_path = "c:\\Chromedriver\\chromedriver.exe"
    service = Service(driver_path)  # Создание объекта Service с указанием пути к драйверу
    # Создание экземпляра браузерного драйвера с использованием объекта Service
    driver = webdriver.Chrome(service=service, options=chrome_options)
    driver.maximize_window()  # Максимизация окна браузера
    yield driver
    driver.quit()