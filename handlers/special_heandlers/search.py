import re

from selenium.webdriver import Keys
from selenium.webdriver.common.by import By
import time

from selenium_stealth import stealth
from telebot.types import Message
from loader import bot
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
# from webdriver_manager.chrome import ChromeDriverManager
# from selenium_stealth import stealth

import sys
import traceback
import random

flag = False
id_admin = [5530555626, 178992550]


def error():
    exc_type, exc_value, exc_traceback = sys.exc_info()
    lines = traceback.format_exception(exc_type, exc_value, exc_traceback)
    text = ''
    for line in lines:
        if 'For documentation on this error, please visit:' not in line:
            text += '!! ' + line
        else:
            text += '!! ' + line[:400]
    text = ''.join(text)
    return text


def check_capch(web_browser) -> bool:
    """
    Функция принимает на вход 1 параметр.
    Проверяет есть ли объявления на сайте.
    Если нет, то возвращает False.
    Если есть, то возвращает True.
    :param web_browser: браузер гугл хром
    :return: bool
    """
    try:
        flag = False
        web_browser.find_element(
            By.CSS_SELECTOR,
            '[class="firewall-container"]'
        )
    except BaseException:
        print('')
    else:
        flag = True
    finally:
        return flag


def check_result(web_browser) -> bool:
    """
    Функция принимает на вход 1 параметр.
    Проверяет есть ли объявления на сайте.
    Если нет, то возвращает False.
    Если есть, то возвращает True.
    :param web_browser: браузер гугл хром
    :return: bool
    """
    try:
        flag = False
        web_browser.find_element(
            By.CSS_SELECTOR,
            '[class="no-results-root-bWQVm"]'
        )
    except BaseException:
        print('')
    else:
        flag = True
    finally:
        return flag


@bot.message_handler(func=lambda message: message.chat.id not in id_admin)
def some(message):
    bot.send_message(message.chat.id, 'У вас нет доступа к данному боту')


# @bot.message_handler(commands=['search'])
def search_switch() -> None:
    """
    Функция реагирует при вводе команды /search.
    При вводе команды, запускается поиск коммутаторов на сайте авито через селениум.
    Берется список коммутаторов из txt файла.
    Делиться на 2 части.
    Сначала поиск идет по первой части,
    после, по второй.
    Случайно выбирается коммутатор из списка и вставляется в строку поиска.
    Далее удаляется из списка и выбор повторяется
    до тех пор, пока список не будет пуст.
    Затем берется список из второй части присваивается первому
    и повторно выбирается коммутатор.
    Когда оба списка становятся пустыми, они обновляются теми,
    что были изначально.
    Поиск коммутаторов ведется раз в 1 час.
    Прерывается командой /stop.
    :param message: Message.text
    :return: None
    """
    global flag
    found_switch_ads = []
    number = 0
    while True:
        with open(r'handlers/special_heandlers/scroll_switches.txt',
                  'r', encoding='utf-8') as scroll_switches:
            switches = scroll_switches.read()
        if number == 0:
            scroll_switch = switches.split(',')
            amount_switches = len(scroll_switch)
            half_list = amount_switches // 2
            first_half = scroll_switch[half_list:]
            print(first_half)
            number = 1
        if not first_half:
            first_half = scroll_switch[half_list:]
            number = 0

        with open(r'handlers/special_heandlers/found_all_ads.txt',
                  'r', encoding='utf-8') as array_found_ads:
            text_scroll_ads = array_found_ads.read()
        scroll_ads = text_scroll_ads.split('\n')

        if len(scroll_ads) >= 1000:
            with open(r'handlers/special_heandlers/found_all_ads.txt',
                      'w', encoding='utf-8') as array_found_ads:
                array_found_ads.write('\n'.join(scroll_ads[500:]))

        scroll_new_ads = []
        if flag:
            flag = False
            break
        count = 0
        try:
            options = Options()
            # options.add_argument('--headless')
            options.add_argument('--no-sandbox')
            options.add_argument("--window-size=1280,1024")
            options.add_argument('--disable-dev-shm-usage')
            options.add_experimental_option(
                "excludeSwitches",
                ["enable-automation"]
            )
            options.add_experimental_option(
                'useAutomationExtension',
                False
            )
            browser = webdriver.Chrome(
                options=options
            )
            '[class="no-results-root-bWQVm"]'
            stealth(
                browser,
                user_agent='Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.53 Safari/537.36',
                languages=["en-US", "en"],
                vendor="Google Inc.",
                platform="Win32",
                webgl_vendor="Intel Inc.",
                renderer="Intel Iris OpenGL Engine",
                fix_hairline=False,
                run_on_insecure_origins=False,
            )
            browser.get('https://www.avito.ru/')
            if check_capch(browser):
                browser.close()
                continue
            time.sleep(15)
            print('15')
        except BaseException:
            answer = error()
            bot.send_message(5530555626, answer)
        for _ in range(len(first_half)):
            name_switch = random.choice(first_half)
            index = first_half.index(name_switch)
            del first_half[index]
            if flag:
                break
            if name_switch != '':
                try:
                    browser.save_screenshot("До ввода.png")
                    search_input = browser.find_element(
                        By.CSS_SELECTOR,
                        '[class="styles-module-input-Lisnt"]'
                    )
                    print(name_switch)
                    search_input.send_keys('hello')
                    search_input.send_keys(Keys.CONTROL + 'a')
                    search_input.send_keys(Keys.DELETE)
                    search_input.send_keys(Keys.SPACE)
                    search_input.send_keys(name_switch)
                    time.sleep(10)
                    search_button = browser.find_element(
                        By.CSS_SELECTOR,
                        '[data-marker="search-form/submit-button"]'
                    )
                    browser.execute_script("arguments[0].click();", search_button)
                    time.sleep(10)
                    if count == 0:
                        try:
                            button_only_names = browser.find_element(
                                By.CSS_SELECTOR,
                                '[data-marker="filters/byTitle/byTitle"]'
                            )
                            browser.execute_script(
                                "arguments[0].click();",
                                button_only_names
                            )
                            time.sleep(10)
                            browser.save_screenshot("после применения only name.png")

                            search_text_ads = browser.find_element(
                                By.CSS_SELECTOR,
                                '[class="styles-module-text-G2ghF styles-module-text_size_m-DUDcO"]'
                            )

                            if search_text_ads.text != 'Ничего не найдено':
                                search_apply = browser.find_element(
                                    By.CSS_SELECTOR,
                                    '[data-marker="search-filters/submit-button"]'
                                )
                                search_apply.click()
                                time.sleep(10)
                            count = 1
                            time.sleep(10)
                        except BaseException:
                            answer = error()
                            print(answer)
                            #bot.send_message(5530555626, answer)
                            break

                    search_button_sort = browser.find_element(
                        By.CSS_SELECTOR,
                        '[data-marker="sort/title"]'
                    )
                    search_button_sort.click()
                    time.sleep(10)
                    search_button_date = browser.find_element(
                        By.CSS_SELECTOR,
                        '[data-marker="sort/custom-option(104)"]'
                    )
                    search_button_date.click()

                except BaseException:
                    answer = error()
                    bot.send_message(5530555626, answer)
                time.sleep(10)

                search_url = browser.find_elements(
                    By.CSS_SELECTOR,
                    '[data-marker="item-title"]'
                )

                if len(found_switch_ads) >= 1000:
                    del found_switch_ads[:500]
                check_ads = []
                if check_result(browser):
                    search_input = browser.find_element(
                        By.CSS_SELECTOR,
                        '[data-marker="search-form/suggest/input"]'
                    )
                    search_input.send_keys(Keys.CONTROL + "a")
                    search_input.send_keys(Keys.DELETE)
                    time.sleep(10)
                    continue
                try:
                    search_text_amount_ads = browser.find_element(
                        By.CSS_SELECTOR,
                        '[data-marker="page-title/count"]'
                    )
                    time.sleep(10)
                    amount_ads = re.sub(r"\D", "", search_text_amount_ads.text)
                    if int(amount_ads) > 10:
                        amount_ads = 10
                    else:
                        amount_ads = int(amount_ads)
                except BaseException:
                    amount_ads = 1
                    answer = error()
                    print(answer)
                    #bot.send_message(5530555626, answer)
                search_url = search_url[:amount_ads]
                for new_switch in search_url:
                    if (new_switch.get_attribute('href') not in found_switch_ads
                            and ('/oborudovanie_dlya_biznesa/' in new_switch.get_attribute('href')
                                 or '/tovary_dlya_kompyutera/' in new_switch.get_attribute('href'))):
                        found_switch_ads.append(new_switch.get_attribute('href'))
                        scroll_new_ads.append(new_switch.get_attribute('href'))
                        check_ads.append(new_switch.get_attribute('href'))

                if check_ads:
                    time.sleep(10)
                else:
                    time.sleep(10)
                browser.save_screenshot("После ввода, до удаления.png")
                search_input = browser.find_element(
                    By.CSS_SELECTOR,
                    '[data-marker="search-form/suggest/input"]'
                )
                search_input.send_keys(Keys.CONTROL + "a")
                search_input.send_keys(Keys.DELETE)
                print(found_switch_ads)
                time.sleep(10)
        print('ушел спать')
        browser.close()
        time.sleep(1000000)
        with open(r'handlers/special_heandlers/found_all_ads.txt',
                  'r', encoding='utf-8') as all_ads:
            scroll_found_ads = all_ads.read()

        switches = '\n\n'.join(scroll_new_ads)
        if scroll_new_ads and switches not in scroll_found_ads:
            with open(r'handlers/special_heandlers/found_all_ads.txt',
                      'a', encoding='utf-8') as all_ads:
                all_ads.write('\n')
                all_ads.write('\n'.join(scroll_new_ads))
            try:
                amount_switches = len(switches)
                amount_messages = len(scroll_new_ads) // 35
                if amount_switches > 4096:
                    for _ in range(amount_messages + 1):
                        switches = '\n\n'.join(scroll_new_ads[:35])
                        del scroll_new_ads[:35]
                        bot.send_message(178992550, switches)
                else:
                    bot.send_message(178992550, switches)
            except BaseException:
                answer = error()
                bot.send_message(5530555626, answer)
        time.sleep(3000)


search_switch()
