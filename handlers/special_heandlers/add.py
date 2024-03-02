from .search import id_admin
from states.answer_user import UserAnswerState
from telebot.types import Message
from loader import bot


@bot.message_handler(func=lambda message: message.chat.id not in id_admin)
def some(message):
    bot.send_message(message.chat.id, 'У вас нет доступа к данному боту')


@bot.message_handler(commands=['add'])
def add_new_switch(message: Message) -> None:
    """
    Функция реагирует при вводе команды /custom.
    При вводе команды, выводиться сообщение с вопросом,
    в каком городе пользователь собирается снять номер в отеле
    :param message: Message.text
    :return: None
    """
    bot.set_state(message.from_user.id, UserAnswerState.add_switch, message.chat.id)
    bot.send_message(message.from_user.id, 'Введите какую модель коммутатора желаете добавить')


@bot.message_handler(state=UserAnswerState.add_switch)
def add_switch_in_scroll(message: Message) -> None:
    """
    Функция ожидает от пользователя ввод названия города, в котором он будет бронировать номер в отеле.
    При вводе слова, записывает его в класс состояний для дальнейшего использования в программе.
    :param message: Message.text
    :return: None
    """
    with open(r'handlers/special_heandlers/scroll_switches.txt', 'a', encoding='utf-8') as scroll_switches:
        scroll_switches.write(message.text + ',')

    bot.send_message(message.from_user.id, 'Коммутатор успешно добавлен в список поиска')
    bot.send_message(message.from_user.id, 'Можете выбрать другую команду или ничего не выбирать. '
                                           'Поиск происходит в фоновом режиме')
    bot.set_state(message.from_user.id, UserAnswerState.choice, message.chat.id)
