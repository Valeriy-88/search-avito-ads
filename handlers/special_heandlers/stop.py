from loader import bot
from . import search
from telebot.types import Message


@bot.message_handler(func=lambda message: message.chat.id not in search.id_admin)
def some(message):
    bot.send_message(message.chat.id, 'У вас нет доступа к данному боту')


@bot.message_handler(commands=['stop'])
def stop_search_switches(message: Message) -> None:
    """
    Функция реагирует при вводе команды /stop.
    При вводе команды, останавливается поиск объявлений
    :return: none
    """
    search.flag = True
    bot.send_message(message.from_user.id, 'Поиск объявлений остановлен')