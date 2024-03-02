from selenium import webdriver
from selenium.webdriver import Keys
from selenium.webdriver.common.by import By
import time
from telebot.types import Message
from loader import bot
from selenium.webdriver.chrome.options import Options
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


@bot.message_handler(func=lambda message: message.chat.id not in id_admin)
def some(message):
    bot.send_message(message.chat.id, 'У вас нет доступа к данному боту')


@bot.message_handler(commands=['search'])
def search_switch(message: Message) -> None:
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
    with open(r'handlers/special_heandlers/scroll_switches.txt', 'r', encoding='utf-8') as scroll_switches:
        switches = scroll_switches.read()

    scroll_switch = switches.split(',')
    amount_switches = len(scroll_switch)
    half_list = amount_switches // 2
    first_half = scroll_switch[:half_list]
    second_half = scroll_switch[half_list:]
    while True:
        scroll_new_ads = []
        if flag:
            flag = False
            break
        count = 0
        bot.send_message(message.from_user.id, 'Начинаю поиск объявлений')

        # chrome_options = Options()
        # chrome_options.add_argument("--headless")
        # browser = webdriver.Chrome(options=chrome_options)
        browser = webdriver.Chrome()
        browser.get('https://www.avito.ru/')
        if not first_half:
            if not second_half:
                first_half = scroll_switch[:half_list]
                second_half = scroll_switch[half_list:]
            else:
                first_half = second_half
        try:
            for _ in range(len(first_half)):
                name_switch = random.choice(first_half)
                index = first_half.index(name_switch)
                del first_half[index]
                if flag:
                    break
                if name_switch != '':
                    search_input = browser.find_element(
                        By.CLASS_NAME,
                        "input-input-Zpzc1"
                    )
                    search_input.send_keys(name_switch)
                    time.sleep(10)
                    search_button = browser.find_element(
                        By.CLASS_NAME,
                        "desktop-15w37ob"
                    )
                    search_button.click()
                    time.sleep(5)
                    if count == 0:
                        search_button_sort = browser.find_element(
                            By.CSS_SELECTOR,
                            '[class="sort-icon-AA_yE sort-icon_rotate-fvL9p"]'
                        )
                        search_button_sort.click()
                        time.sleep(10)
                        search_button_date = browser.find_element(
                            By.CSS_SELECTOR,
                            '[data-marker="sort/custom-option(104)"]'
                        )
                        search_button_date.click()
                        count = 1
                        time.sleep(10)
                    search_url = browser.find_elements(
                        By.CSS_SELECTOR,
                        '[data-marker="item-title"]'
                        )

                    if len(found_switch_ads) >= 1000:
                        found_switch_ads = []
                    check_ads = []
                    search_url = search_url[:15]
                    for new_switch in search_url:
                        if new_switch.get_attribute('href') not in found_switch_ads:
                            found_switch_ads.append(new_switch.get_attribute('href'))
                            scroll_new_ads.append(new_switch.get_attribute('href'))
                            check_ads.append(new_switch.get_attribute('href'))

                    if check_ads:
                        time.sleep(10)
                    search_input = browser.find_element(
                        By.CLASS_NAME,
                        "input-input-Zpzc1"
                    )
                    search_input.send_keys(Keys.CONTROL + "a")
                    search_input.send_keys(Keys.DELETE)
        except BaseException:
            answer = error()
            bot.send_message(5530555626, answer)
        finally:
            browser.close()

        if scroll_new_ads:
            switches = '\n\n'.join(scroll_new_ads)
            bot.send_message(178992550, switches)

        time.sleep(2400)
