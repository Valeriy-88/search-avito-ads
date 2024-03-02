from states.answer_user import UserAnswerState
from telebot.types import Message
from loader import bot
from .search import id_admin


@bot.message_handler(func=lambda message: message.chat.id not in id_admin)
def some(message):
    bot.send_message(message.chat.id, 'У вас нет доступа к данному боту')


@bot.message_handler(commands=['view'])
def view_scroll_switch(message: Message) -> None:
    """
    Функция реагирует при вводе команды /view.
    При вводе команды, выводиться список свичей
    :param message: Message.text
    :return: None
    """
    with open(r'handlers/special_heandlers/scroll_switches.txt', 'r', encoding='utf-8') as scroll_switches:
        switches = scroll_switches.read()
        list_switches = switches.split(',')
        switches = ', '.join(list_switches)

    user_id = message.from_user.id
    print(user_id)
    bot.send_message(message.from_user.id, 'Список коммутаторов для поиска:')
    bot.send_message(message.from_user.id, switches)
    bot.send_message(message.from_user.id, 'Выберите другую команду или запустите поиск объявлений')
    bot.set_state(message.from_user.id, UserAnswerState.choice, message.chat.id)
