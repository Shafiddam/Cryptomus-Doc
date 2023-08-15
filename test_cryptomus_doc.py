# from Tests.pages.locators import BasePageLocators
from time import sleep
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import os
import pytest
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.chrome.options import Options # для запуска браузера в безоконном режиме; на английском
from selenium.webdriver.chrome.service import Service

# ссылка на стенд лендинг:
link_dev = "http://doc.cryptomus.kotyata.space/"
# ссылка на прод лендинг:
link = "https://doc.cryptomus.com/"


# ФУНКЦИЯ ДЛЯ НАСТРОЙКИ БРАУЗЕРА, ЧТОБЫ НЕ ПОВТОРЯТЬ КОД
@pytest.fixture
def driver():
    """
    Функция для настройки браузера
    """
    chrome_options = Options()
    chrome_options.add_argument("--lang=en-US")  # Установите желаемый язык, например, en-US для английского
    # путь к драйверу браузера, например, для Chrome используйте ChromeDriver
    driver_path = "c:\\Chromedriver\\chromedriver.exe"
    # Создание объекта Service с указанием пути к драйверу
    service = Service(driver_path)
    # Создание экземпляра браузерного драйвера с использованием объекта Service
    driver = webdriver.Chrome(service=service, options=chrome_options)
    # Максимизация окна браузера
    driver.maximize_window()
    return driver


# ПРОВЕРКА НАЛИЧИЯ ПОЛЯ ПОИСКА В ДОКУМЕНТАЦИИ
# Ожид.результат: поле поиска есть
def test_input_search_is_displayed(driver):
    """
    Проверка наличия поля поиска в документации
    Ожид.результат: поле поиска есть
    """
    try:
        # открытие страницы
        driver.get(link)

        # поиск
        input_search = WebDriverWait(driver, 10).until(EC.presence_of_element_located(
            (By.XPATH, '//*[@id="root"]/div/div[1]/div/div[1]/div/div/div[1]/div/input')))
        # Проверка, что поиск есть на странице
        assert input_search.is_displayed(), 'ОШИБКА: нет поля поиска по документации !!!'

    except Exception as e:
        # обработка исключений
        pytest.fail(f"ERROR: {str(e)}")
    finally:
        # закрытие браузера в любом случае
        driver.quit()


# ПРОВЕРКА ПОЯВЛЕНИЯ ОБЛАСТИ ПОИСКА В ДОКУМЕНТАЦИИ
# Ожид.результат: поле поиска ищет и выводит информацию
# root > div > div.layout-wrapper > div > div.header > div > div > div.content__search-area > ul
def test_search_area_is_displayed(driver):
    """
    ПРОВЕРКА ПОЯВЛЕНИЯ ОБЛАСТИ ПОИСКА В ДОКУМЕНТАЦИИ
    Ожид.результат: поле поиска ищет и выводит информацию
    """
    try:
        # открытие страницы
        driver.get(link)
        # ввод слова в поле инпута, например "payment"
        driver.find_element(By.CSS_SELECTOR, 'div.content__search-area > div > input').send_keys('payment')
        # находим область вывода (список) "div.content__search-area > ul"
        search_area = WebDriverWait(driver, 10).until(EC.presence_of_element_located(
            (By.CSS_SELECTOR, 'div.header > div > div > div.content__search-area > ul')))
        # Проверка, что область вывода поиска появилась на странице
        assert search_area.is_displayed(), 'ОШИБКА: нет вывода в поиске !!!'
        sleep(2) # для наглядности
    except Exception as e:
        # обработка исключений
        pytest.fail(f"ERROR: {str(e)}")
    finally:
        # закрытие браузера в любом случае
        driver.quit()


# ПРОВЕРКА НАЛИЧИЯ КНОПКИ СМЕНЫ ТЕМЫ
# Ожид.результат: кнопка есть
def test_theme_button_is_displayed(driver):
    """
    ПРОВЕРКА НАЛИЧИЯ КНОПКИ СМЕНЫ ТЕМЫ
    """
    try:
        # открытие страницы
        driver.get(link)
        # поиск
        theme_button = WebDriverWait(driver, 10).until(EC.presence_of_element_located(
            (By.XPATH, '//*[@id="root"]/div/div[1]/div/div[1]/div/div/div[2]/div[1]/button')))
        # Проверка, что есть на странице
        assert theme_button.is_displayed(), 'ОШИБКА: нет кнопки смены темы !!!'
    except Exception as e:
        # обработка исключений
        pytest.fail(f"ERROR: {str(e)}")
    finally:
        # закрытие браузера в любом случае
        driver.quit()


# ПРОВЕРКА СМЕНЫ ТЕМЫ
# Ожид.результат: смена происходит добавлением class="dark-content" в <body class="dark-content">
def test_theme_is_changed(driver):
    """"
    Проверка смены темы
    Ожид.результат: смена происходит добавлением class="dark-content" в <body class="dark-content">
    """
    try:
        # открытие страницы
        driver.get(link)
        # Получение текущего состояния темы
        current_theme = driver.find_element(By.TAG_NAME, 'body').get_attribute('class')
        # Клик по переключателю темы
        WebDriverWait(driver, 10).until(EC.presence_of_element_located(
            (By.XPATH, '//*[@id="root"]/div/div[1]/div/div[1]/div/div/div[2]/div[1]/button'))).click()
        sleep(1)
        # Получение обновленного состояния темы
        updated_theme = driver.find_element(By.TAG_NAME, 'body').get_attribute('class')
        # Проверка, что тема была изменена
        assert updated_theme != current_theme, "ОШИБКА: смена темы не произошла !!!"
    except Exception as e:
        # обработка исключений
        pytest.fail(f"ERROR: {str(e)}")
    finally:
        # закрытие браузера в любом случае
        driver.quit()


# ПРОВЕРКА НАЛИЧИЯ КНОПКИ СМЕНЫ ЯЗЫКА
# Ожид.результат: кнопка есть
def test_language_button_is_displayed(driver):
    """
    Проверка наличия кнопки смены языка
    Ожид.результат: кнопка есть
    """
    try:
        # открытие страницы
        driver.get(link)
        # поиск
        language_button = WebDriverWait(driver, 10).until(EC.presence_of_element_located(
            (By.CSS_SELECTOR, 'div.content__buttons > div.content__brn > div > div > div')))
        # Проверка, что есть на странице
        assert language_button.is_displayed(), 'ОШИБКА: нет кнопки смены языков !!!'
    except Exception as e:
        # обработка исключений
        pytest.fail(f"ERROR: {str(e)}")
    finally:
        # закрытие браузера в любом случае
        driver.quit()


# ПРОВЕРКА НАЛИЧИЯ ДРУГИХ ЯЗЫКОВ(ДРОПДАУН МЕНЮ)
# Ожид.результат: меню есть
def test_language_dropdown_menu_is_displayed(driver):
    """
    Проверка наличия других языков(дропдаун меню)
    Ожид.результат: меню есть
    """
    try:
        # открытие страницы
        driver.get(link)
        # поиск
        language_dropdown_menu = WebDriverWait(driver, 10).until(EC.presence_of_element_located(
            (By.CSS_SELECTOR, 'div.header > div > div > div.content__buttons > div.content__brn > div > div')))
        # Проверка, что есть на странице
        assert language_dropdown_menu.is_displayed(), 'ОШИБКА: нет дропдаун-меню смены языков !!!'
        language_dropdown_menu.click(); sleep(3)
    except Exception as e:
        # обработка исключений
        pytest.fail(f"ERROR: {str(e)}")
    finally:
        # закрытие браузера в любом случае
        driver.quit()


# ПРОВЕРКА НАЛИЧИЯ КНОПКИ "BACK TO CRYPTOMUS"
# Ожид.результат: есть
def test_button_back_to_cryptomus_is_displayed(driver):
    """
    Проверка наличия кнопки "back to cryptomus"
    Ожид.результат: есть
    """
    try:
        # открытие страницы
        driver.get(link)
        # поиск
        button_back_to_cryptomus = WebDriverWait(driver, 10).until(EC.presence_of_element_located(
            (By.CSS_SELECTOR, 'div.header > div > div > div.content__buttons > div.content__login > div')))
        # Проверка, что есть на странице
        assert button_back_to_cryptomus.is_displayed(), 'ОШИБКА: нет button_back_to_cryptomus !!!'
    except Exception as e:
        # обработка исключений
        pytest.fail(f"ERROR: {str(e)}")
    finally:
        # закрытие браузера в любом случае
        driver.quit()


# ПРОВЕРКА РАБОТЫ КНОПКИ "BACK TO CRYPTOMUS"
# Ожид.результат: происходит переход на https://cryptomus.com/
def test_button_back_to_cryptomus_click(driver):
    """
    Проверка работы кнопки "back to cryptomus"
    Ожид.результат: происходит переход на https://cryptomus.com/
    """
    try:
        # открытие страницы
        driver.get(link)
        # запоминаем текущий URL страницы
        current_url = driver.current_url
        # print("current_url: ", current_url) # выводится: https://doc.cryptomus.com/
        # кликаем на кнопку "Back to Cryptomus"
        driver.find_element(By.CSS_SELECTOR,
                            'div.header > div > div > div.content__buttons > div.content__login > div').click()
        # ждем загрузки новой страницы
        WebDriverWait(driver, 10).until(EC.url_changes(current_url))
        # новый URL страницы
        new_url = driver.current_url
        # print("new_url: ", new_url) # выводится: https://cryptomus.com/
        # Проверка, что 1)страницы отличаются и 2)что ссылка ведет на https://cryptomus.com/
        assert new_url != current_url, 'ОШИБКА: нет перехода по кнопке !!!'
        assert new_url == 'https://cryptomus.com/', 'ОШИБКА: страница не загрузилась !!!'
    except Exception as e:
        # обработка исключений
        pytest.fail(f"ERROR: {str(e)}")
    finally:
        # закрытие браузера в любом случае
        driver.quit()


# Проверка модуля "WooCommerce"
# Ожид.результат: можно скачать WooCommerce
def test_download_woocommerce(driver):
    """
    Проверка модуля "WooCommerce"
    Ожид.результат: можно скачать WooCommerce
    """
    try:
        # открытие страницы c модулями для скачивания
        driver.get('https://doc.cryptomus.com/sdks-and-modules/modules')
        # ссылка на кнопку скачать
        download_url = 'https://storage.cryptomus.com/modules/woocommerce_cryptomus.zip'
        # все кнопки по общему селектору
        buttons = driver.find_elements(By.CSS_SELECTOR, 'a.button > button.btn.modules.large')
        # Итерируйтесь по кнопкам и проверьте атрибут href родительского элемента
        for button in buttons:
            parent_element = button.find_element_by_xpath('..')  # Получить родительский элемент
            href = parent_element.get_attribute('href')
            if href == download_url:
                button.click()
                break
        # Дождитесь, пока файл будет загружен:
        WebDriverWait(driver, 10).until(lambda driver: any(
            filename.endswith('woocommerce_cryptomus.zip') for filename in os.listdir('c:\\Users\\РС\\Downloads')))
        # Получите список файлов после скачивания:
        updated_files = os.listdir('c:\\Users\\РС\\Downloads')
        # Проверка, что в списке файлов появился нужный файл, чтобы убедиться, что файл успешно скачался:
        assert 'woocommerce_cryptomus.zip' in updated_files, 'ОШИБКА: файл не скачен !!!'
    except Exception as e:
        # обработка исключений
        pytest.fail(f"ERROR: {str(e)}")
    finally:
        # закрытие браузера в любом случае
        driver.quit()


# Проверка модуля "OpenCart 3"
# Ожид.результат: можно скачать модуль
def test_download_cryptomus_opencart3(driver):
    """
    Проверка модуля "OpenCart 3"
    Ожид.результат: можно скачать модуль
    """
    try:
        # открытие страницы c модулями для скачивания
        driver.get('https://doc.cryptomus.com/sdks-and-modules/modules')
        # ссылка на кнопку скачать
        download_url = 'https://storage.cryptomus.com/modules/cryptomus-opencart3.ocmod.zip'
        # все кнопки по общему селектору
        buttons = driver.find_elements(By.CSS_SELECTOR, 'a.button > button.btn.modules.large')
        # Итерируйтесь по кнопкам и проверьте атрибут href родительского элемента
        for button in buttons:
            parent_element = button.find_element_by_xpath('..')  # Получить родительский элемент
            href = parent_element.get_attribute('href')
            if href == download_url:
                button.click()
                break
        # Дождитесь, пока файл будет загружен:
        WebDriverWait(driver, 10).until(lambda driver: any(
            filename.endswith('cryptomus-opencart3.ocmod.zip') for filename in os.listdir('c:\\Users\\РС\\Downloads')))
        # Получите список файлов после скачивания:
        updated_files = os.listdir('c:\\Users\\РС\\Downloads')
        # Проверка, что в списке файлов появился нужный файл, чтобы убедиться, что файл успешно скачался:
        assert 'cryptomus-opencart3.ocmod.zip' in updated_files, 'ОШИБКА: файл не скачен !!!'
    except Exception as e:
        # обработка исключений
        pytest.fail(f"ERROR: {str(e)}")
    finally:
        # закрытие браузера в любом случае
        driver.quit()


# Проверка модуля "PrestaShop 1"
# Ожид.результат: можно скачать модуль
def test_download_cryptomus_prestashop1(driver):
    """
    Проверка модуля "PrestaShop 1"
    Ожид.результат: можно скачать модуль
    """
    try:
        # открытие страницы c модулями для скачивания
        driver.get('https://doc.cryptomus.com/sdks-and-modules/modules')
        # ссылка на кнопку скачать
        download_url = 'https://storage.cryptomus.com/modules/prestashop.1x.zip'
        # все кнопки по общему селектору
        buttons = driver.find_elements(By.CSS_SELECTOR, 'a.button > button.btn.modules.large')
        # Итерируйтесь по кнопкам и проверьте атрибут href родительского элемента
        for button in buttons:
            parent_element = button.find_element_by_xpath('..')  # Получить родительский элемент
            href = parent_element.get_attribute('href')
            if href == download_url:
                button.click()
                break
        # Дождитесь, пока файл будет загружен:
        WebDriverWait(driver, 10).until(lambda driver: any(
            filename.endswith('prestashop.1x.zip') for filename in os.listdir('c:\\Users\\РС\\Downloads')))
        # Получите список файлов после скачивания:
        updated_files = os.listdir('c:\\Users\\РС\\Downloads')
        # Проверка, что в списке файлов появился нужный файл, чтобы убедиться, что файл успешно скачался:
        assert 'prestashop.1x.zip' in updated_files, 'ОШИБКА: файл не скачен !!!'
    except Exception as e:
        # обработка исключений
        pytest.fail(f"ERROR: {str(e)}")
    finally:
        # закрытие браузера в любом случае
        driver.quit()


# Проверка модуля "WHMCS"
# Ожид.результат: можно скачать модуль
def test_download_cryptomus_whmcs(driver):
    """
    Проверка модуля "WHMCS"
    Ожид.результат: можно скачать модуль
    """
    try:
        # открытие страницы c модулями для скачивания
        driver.get('https://doc.cryptomus.com/sdks-and-modules/modules')
        # ссылка на кнопку скачать
        download_url = 'https://storage.cryptomus.com/modules/cryptomus_whmcs.zip'
        # все кнопки по общему селектору
        buttons = driver.find_elements(By.CSS_SELECTOR, 'a.button > button.btn.modules.large')
        # Итерируйтесь по кнопкам и проверьте атрибут href родительского элемента
        for button in buttons:
            parent_element = button.find_element_by_xpath('..')  # Получить родительский элемент
            href = parent_element.get_attribute('href')
            if href == download_url:
                button.click()
                break
        # Дождитесь, пока файл будет загружен:
        WebDriverWait(driver, 10).until(lambda driver: any(
            filename.endswith('cryptomus_whmcs.zip') for filename in os.listdir('c:\\Users\\РС\\Downloads')))
        # Получите список файлов после скачивания:
        updated_files = os.listdir('c:\\Users\\РС\\Downloads')
        # Проверка, что в списке файлов появился нужный файл, чтобы убедиться, что файл успешно скачался:
        assert 'cryptomus_whmcs.zip' in updated_files, 'ОШИБКА: файл не скачен !!!'
    except Exception as e:
        # обработка исключений
        pytest.fail(f"ERROR: {str(e)}")
    finally:
        # закрытие браузера в любом случае
        driver.quit()


# Проверка модуля "RootPanel"
# Ожид.результат: можно перейти по ссылке (скачать модуль нет)
def test_download_cryptomus_rootpanel(driver):
    """
    Проверка модуля "RootPanel"
    Ожид.результат: переход по ссылке (скачать модуль нет)
    """
    try:
        # открытие страницы c модулями для скачивания
        driver.get('https://doc.cryptomus.com/sdks-and-modules/modules')
        # ссылка на кнопку скачать
        download_url = 'https://rootpanel.net/setup.php?help=cryptomus&lang=english'
        # все кнопки по общему селектору
        buttons = driver.find_elements(By.CSS_SELECTOR, 'a.button > button.btn.modules.large')
        sleep(3)  # надо подождать чтобы прогрузилось
        # Итерируйтесь по кнопкам и проверьте атрибут href родительского элемента
        for button in buttons:
            parent_element = button.find_element_by_xpath('..')  # Получить родительский элемент
            href = parent_element.get_attribute('href')
            if href == download_url:
                button.click()
                break
        # Проверка, что Ожид.результат: переход по ссылке (можно скачать модуль):
        assert driver.current_url == download_url, 'ОШИБКА: не перешли по ссылке!'
    except Exception as e:
        # обработка исключений
        pytest.fail(f"ERROR: {str(e)}")
    finally:
        # закрытие браузера в любом случае
        driver.quit()


# Проверка модуля "OpenCart 2"
# Ожид.результат: можно скачать модуль
def test_download_cryptomus_opencart2(driver):
    """
    Проверка модуля "OpenCart 2"
    Ожид.результат: можно скачать модуль
    """
    try:
        # открытие страницы c модулями для скачивания
        driver.get('https://doc.cryptomus.com/sdks-and-modules/modules')
        # ссылка на кнопку скачать
        download_url = 'https://storage.cryptomus.com/modules/cryptomus-opencart2.ocmod.zip'
        # все кнопки по общему селектору
        buttons = driver.find_elements(By.CSS_SELECTOR, 'a.button > button.btn.modules.large')
        # Итерируйтесь по кнопкам и проверьте атрибут href родительского элемента
        for button in buttons:
            parent_element = button.find_element_by_xpath('..')  # Получить родительский элемент
            href = parent_element.get_attribute('href')
            if href == download_url:
                button.click()
                break
        # Дождитесь, пока файл будет загружен:
        WebDriverWait(driver, 10).until(lambda driver: any(
            filename.endswith('cryptomus-opencart2.ocmod.zip') for filename in os.listdir('c:\\Users\\РС\\Downloads')))
        # Получите список файлов после скачивания:
        updated_files = os.listdir('c:\\Users\\РС\\Downloads')
        # Проверка, что в списке файлов появился нужный файл, чтобы убедиться, что файл успешно скачался:
        assert 'cryptomus-opencart2.ocmod.zip' in updated_files, 'ОШИБКА: файл не скачен !!!'
    except Exception as e:
        # обработка исключений
        pytest.fail(f"ERROR: {str(e)}")
    finally:
        # закрытие браузера в любом случае
        driver.quit()


# Проверка модуля "PrestaShop 8"
# Ожид.результат: можно скачать модуль
def test_download_cryptomus_prestashop8(driver):
    """
    Проверка модуля "PrestaShop 8"
    Ожид.результат: можно скачать модуль
    """
    try:
        # открытие страницы c модулями для скачивания
        driver.get('https://doc.cryptomus.com/sdks-and-modules/modules')
        # ссылка на кнопку скачать
        download_url = 'https://storage.cryptomus.com/modules/prestashop.8x.zip'
        # все кнопки по общему селектору
        buttons = driver.find_elements(By.CSS_SELECTOR, 'a.button > button.btn.modules.large')
        # Итерируйтесь по кнопкам и проверьте атрибут href родительского элемента
        for button in buttons:
            parent_element = button.find_element_by_xpath('..')  # Получить родительский элемент
            href = parent_element.get_attribute('href')
            if href == download_url:
                button.click()
                break
        # Дождитесь, пока файл будет загружен:
        WebDriverWait(driver, 10).until(lambda driver: any(
            filename.endswith('prestashop.8x.zip') for filename in os.listdir('c:\\Users\\РС\\Downloads')))
        # Получите список файлов после скачивания:
        updated_files = os.listdir('c:\\Users\\РС\\Downloads')
        # Проверка, что в списке файлов появился нужный файл, чтобы убедиться, что файл успешно скачался:
        assert 'prestashop.8x.zip' in updated_files, 'ОШИБКА: файл не скачен !!!'
    except Exception as e:
        # обработка исключений
        pytest.fail(f"ERROR: {str(e)}")
    finally:
        # закрытие браузера в любом случае
        driver.quit()


# Проверка модуля "XenForo"
# Ожид.результат: можно скачать модуль
def test_download_cryptomus_xenforo(driver):
    """
    Проверка модуля "XenForo"
    Ожид.результат: можно скачать модуль
    """
    try:
        # открытие страницы c модулями для скачивания
        driver.get('https://doc.cryptomus.com/sdks-and-modules/modules')
        # ссылка на кнопку скачать
        download_url = 'https://storage.cryptomus.com/modules/XenForo.zip'
        # все кнопки по общему селектору
        buttons = driver.find_elements(By.CSS_SELECTOR, 'a.button > button.btn.modules.large')
        sleep(3)  # чтобы не падало
        # Итерируйтесь по кнопкам и проверьте атрибут href родительского элемента
        for button in buttons:
            parent_element = button.find_element_by_xpath('..')  # Получить родительский элемент
            href = parent_element.get_attribute('href')
            if href == download_url:
                button.click()
                break
        # Дождитесь, пока файл будет загружен:
        WebDriverWait(driver, 10).until(lambda driver: any(
            filename.endswith('XenForo.zip') for filename in os.listdir('c:\\Users\\РС\\Downloads')))
        # Получите список файлов после скачивания:
        updated_files = os.listdir('c:\\Users\\РС\\Downloads')
        # Проверка, что в списке файлов появился нужный файл, чтобы убедиться, что файл успешно скачался:
        assert 'XenForo.zip' in updated_files, 'ОШИБКА: файл не скачен !!!'
    except Exception as e:
        # обработка исключений
        pytest.fail(f"ERROR: {str(e)}")
    finally:
        # закрытие браузера в любом случае
        driver.quit()


# Проверка модуля "phpshop-v1.0.zip"
# Ожид.результат: можно скачать модуль
def test_download_cryptomus_phpshop_v1_0(driver):
    """
    Проверка модуля "phpshop-v1.0.zip"
    Ожид.результат: можно скачать модуль
    """
    try:
        # открытие страницы c модулями для скачивания
        driver.get('https://doc.cryptomus.com/sdks-and-modules/modules')
        # ссылка на кнопку скачать
        download_url = 'https://storage.cryptomus.com/modules/phpshop-v1.0.zip'
        # все кнопки по общему селектору
        buttons = driver.find_elements(By.CSS_SELECTOR, 'a.button > button.btn.modules.large')
        # sleep(3)  # чтобы не падало
        # Итерируйтесь по кнопкам и проверьте атрибут href родительского элемента
        for button in buttons:
            parent_element = button.find_element_by_xpath('..')  # Получить родительский элемент
            href = parent_element.get_attribute('href')
            if href == download_url:
                button.click()
                break
        # Дождитесь, пока файл будет загружен:
        WebDriverWait(driver, 10).until(lambda driver: any(
            filename.endswith('phpshop-v1.0.zip') for filename in os.listdir('c:\\Users\\РС\\Downloads')))
        # Получите список файлов после скачивания:
        updated_files = os.listdir('c:\\Users\\РС\\Downloads')
        # Проверка, что в списке файлов появился нужный файл, чтобы убедиться, что файл успешно скачался:
        assert 'phpshop-v1.0.zip' in updated_files, 'ОШИБКА: файл не скачен !!!'
    except Exception as e:
        # обработка исключений
        pytest.fail(f"ERROR: {str(e)}")
    finally:
        # закрытие браузера в любом случае
        driver.quit()


# Проверка модуля "XenForo2.zip"
# Ожид.результат: можно скачать модуль
def test_download_cryptomus_xenforo2(driver):
    """
    Проверка модуля "XenForo2.zip"
    Ожид.результат: можно скачать модуль
    """
    try:
        # открытие страницы c модулями для скачивания
        driver.get('https://doc.cryptomus.com/sdks-and-modules/modules')
        # ссылка на кнопку скачать
        download_url = 'https://storage.cryptomus.com/modules/XenForo2.zip'
        # все кнопки по общему селектору
        buttons = driver.find_elements(By.CSS_SELECTOR, 'a.button > button.btn.modules.large')
        # sleep(3)  # чтобы не падало
        # Итерируйтесь по кнопкам и проверьте атрибут href родительского элемента
        for button in buttons:
            parent_element = button.find_element_by_xpath('..')  # Получить родительский элемент
            href = parent_element.get_attribute('href')
            if href == download_url:
                button.click()
                break
        # Дождитесь, пока файл будет загружен:
        WebDriverWait(driver, 10).until(lambda driver: any(
            filename.endswith('XenForo2.zip') for filename in os.listdir('c:\\Users\\РС\\Downloads')))
        # Получите список файлов после скачивания:
        updated_files = os.listdir('c:\\Users\\РС\\Downloads')
        # Проверка, что в списке файлов появился нужный файл, чтобы убедиться, что файл успешно скачался:
        assert 'XenForo2.zip' in updated_files, 'ОШИБКА: файл не скачен !!!'
    except Exception as e:
        # обработка исключений
        pytest.fail(f"ERROR: {str(e)}")
    finally:
        # закрытие браузера в любом случае
        driver.quit()


# Проверка модуля "Tilda"
# Ожид.результат: переход по ссылке (скачать модуль нет)
def test_download_cryptomus_tilda(driver):
    """
    Проверка модуля "Tilda"
    Ожид.результат: переход по ссылке (скачать модуль нет)
    """
    try:
        # открытие страницы c модулями для скачивания
        driver.get('https://doc.cryptomus.com/sdks-and-modules/modules')
        # ссылка на кнопку скачать
        download_url = 'https://cryptomus.com/blog/how-to-accept-cryptocurrency-payments-with-tilda'
        # все кнопки по общему селектору
        buttons = driver.find_elements(By.CSS_SELECTOR, 'a.button > button.btn.modules.large')
        sleep(3)  # надо подождать чтобы прогрузилось
        # Итерируйтесь по кнопкам и проверьте атрибут href родительского элемента
        for button in buttons:
            parent_element = button.find_element_by_xpath('..')  # Получить родительский элемент
            href = parent_element.get_attribute('href')
            if href == download_url:
                button.click()
                break
        # Проверка, что Ожид.результат: переход по ссылке (можно скачать модуль):
        assert driver.current_url == download_url, 'ОШИБКА: не перешли по ссылке!'
    except Exception as e:
        # обработка исключений
        pytest.fail(f"ERROR: {str(e)}")
    finally:
        # закрытие браузера в любом случае
        driver.quit()


# Проверка модуля "XenForo1.5.zip"
# Ожид.результат: можно скачать модуль
def test_download_cryptomus_xenforo1_5(driver):
    """
    Проверка модуля "XenForo1_5.zip"
    Ожид.результат: можно скачать модуль
    """
    try:
        # открытие страницы c модулями для скачивания
        driver.get('https://doc.cryptomus.com/sdks-and-modules/modules')
        # ссылка на кнопку скачать
        download_url = 'https://storage.cryptomus.com/modules/XenForo1.5.zip'
        # все кнопки по общему селектору
        buttons = driver.find_elements(By.CSS_SELECTOR, 'a.button > button.btn.modules.large')
        # sleep(3)  # чтобы не падало
        # Итерируйтесь по кнопкам и проверьте атрибут href родительского элемента
        for button in buttons:
            parent_element = button.find_element_by_xpath('..')  # Получить родительский элемент
            href = parent_element.get_attribute('href')
            if href == download_url:
                button.click()
                break
        # Дождитесь, пока файл будет загружен:
        WebDriverWait(driver, 10).until(lambda driver: any(
            filename.endswith('XenForo1.5.zip') for filename in os.listdir('c:\\Users\\РС\\Downloads')))
        # Получите список файлов после скачивания:
        updated_files = os.listdir('c:\\Users\\РС\\Downloads')
        # Проверка, что в списке файлов появился нужный файл, чтобы убедиться, что файл успешно скачался:
        assert 'XenForo1.5.zip' in updated_files, 'ОШИБКА: файл не скачен !!!'
    except Exception as e:
        # обработка исключений
        pytest.fail(f"ERROR: {str(e)}")
    finally:
        # закрытие браузера в любом случае
        driver.quit()


# Проверка наличия скрола на странице
# Ожид.результат: скрол есть (разрешение экрана Full HD, масштаб 100%)
def test_scroll_verification(driver):
    """
    Проверка наличия скрола на странице
    Ожид.результат: скрол есть (разрешение экрана Full HD, масштаб 100%)
    """
    try:
        # Открытие страницы
        driver.get('https://doc.cryptomus.com/sdks-and-modules/modules')
        # можно например проверить эту страницу ниже, тут скрола нет, будет ошибка и тест упадет
        # driver.get('http://dev.app.cryptomus.kotyata.space/login')
        # Проверка наличия вертикального скролла
        is_scrollable = driver.execute_script(
            'return document.documentElement.scrollHeight > document.documentElement.clientHeight;')
        assert is_scrollable, "Vertical scroll is not present on the page."
        # Прокрутка вниз
        actions = ActionChains(driver)
        actions.send_keys(Keys.END).perform()
        # Пауза для прокрутки
        sleep(2)
        # Прокрутка вверх
        actions.send_keys(Keys.HOME).perform()
        # Пауза для прокрутки
        sleep(2)
    except Exception as e:
        # обработка исключений
        pytest.fail(f"ERROR: {str(e)}")
    finally:
        # закрытие браузера в любом случае
        driver.quit()


# тест ниже не работает!!! Не находится кнопка((
# --------------------------------        ПРОВЕРКА НАЛИЧИЯ КНОПКИ ОБМЕНА СООБЩЕНИЯМИ ZENDESK  --------------------------------------
# Ожид.результат: кнопка есть
def test_zendesk_button_is_displayed():
    global driver
    try:
        # инициализация драйвера браузера
        driver = webdriver.Chrome()
        # Максимизация окна браузера
        driver.maximize_window()
        # открытие страницы
        driver.get(link)

        # надо подождать пока загрузится zendesk
        sleep(3)
        print('1')
        # поиск
        # zendesk_button = WebDriverWait(driver, 10).until(EC.presence_of_element_located(
        #     (By.CSS_SELECTOR, '.sc-EHOje')))

        # zendesk_button = driver.find_element(By.CLASS_NAME, '.sc-EHOje')
        # driver.find_element(By.CSS_SELECTOR, 'sc-EHOje').click()
        driver.find_element(By.CLASS_NAME, 'button.sc-htpNat.sc-1w3tvxe-1.cbaSPe.sc-EHOje.bsmmQV').click()
        print('2')
        sleep(3)

        # Проверка, что есть на странице
        # assert zendesk_button.is_displayed(), 'ОШИБКА: нет кнопки zendesk_button !!!'

    except Exception as e:
        # обработка исключений
        pytest.fail(f"ERROR: {str(e)}")
    finally:
        # закрытие браузера в любом случае
        driver.quit()
