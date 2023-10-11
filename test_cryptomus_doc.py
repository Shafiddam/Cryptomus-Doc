import os
from time import sleep

import pytest
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait

from pages.doc_page import DocPage
from data.data import *


def test_input_search_is_displayed(driver):
    """ Проверка наличия поля поиска в документации. Ожид.результат: поле поиска есть """
    doc_page = DocPage(driver)

    try:
        driver.get(link)
        element = doc_page.find_input_search()
        assert element, 'ОШИБКА: нет поля поиска по документации!'
    except Exception as e:
        pytest.fail(f"ERROR: {str(e)}")
    finally:
        driver.quit()


def test_search_area_is_displayed(driver):
    """ ПРОВЕРКА ПОЯВЛЕНИЯ ОБЛАСТИ ПОИСКА В ДОКУМЕНТАЦИИ. Ожид.результат: поле поиска ищет и выводит информацию """
    doc_page = DocPage(driver)
    word = 'payment'
    try:
        driver.get(link)
        element = doc_page.search_area(word)
        # Проверка, что область вывода поиска появилась на странице
        assert element, 'ОШИБКА: нет вывода в поиске!'
    except Exception as e:
        pytest.fail(f"ERROR: {str(e)}")
    finally:
        driver.quit()
