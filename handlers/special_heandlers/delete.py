from .search import id_admin
from states.answer_user import UserAnswerState
from telebot.types import Message
from loader import bot


@bot.message_handler(func=lambda message: message.chat.id not in id_admin)
def some(message):
    bot.send_message(message.chat.id, 'У вас нет доступа к данному боту')


@bot.message_handler(commands=['delete'])
def delete_switch(message: Message) -> None:
    """
    Функция реагирует при вводе команды /high.
    При вводе команды, выводиться сообщение с вопросом,
    в каком городе пользователь собирается снять номер в отеле
    :param message: Message.text
    :return: None
    """
    bot.set_state(message.from_user.id, UserAnswerState.delete_switch, message.chat.id)
    bot.send_message(message.from_user.id, 'Введите какую модель коммутатора желаете удалить')


@bot.message_handler(state=UserAnswerState.delete_switch)
def delete_switch_in_scroll(message: Message) -> None:
    """
    Функция ожидает от пользователя ввод названия города, в котором он будет бронировать номер в отеле.
    При вводе слова, записывает его в класс состояний для дальнейшего использования в программе.
    :param message: Message.text
    :return: None
    """
    try:
        with open(r'handlers/special_heandlers/scroll_switches.txt', 'r', encoding='utf-8') as scroll_switches:
            switches = scroll_switches.read()
            list_switches = switches.split(',')

        if message.text in switches:
            list_switches.remove(message.text)

            with open(r'handlers/special_heandlers/scroll_switches.txt', 'w', encoding='utf-8') as scroll_switches:
                for switch in list_switches:
                    if switch != '':
                        scroll_switches.write(switch + ',')

            bot.send_message(message.from_user.id, 'Выбранный Вами коммутатор успешно удален из списка')
            bot.send_message(message.from_user.id, 'Можете выбрать другую команду или ничего не выбирать. '
                                                   'Поиск происходит в фоновом режиме')
            bot.set_state(message.from_user.id, UserAnswerState.choice, message.chat.id)

        else:
            switches = ', '.join(list_switches)
            bot.send_message(message.from_user.id, 'Некорректный ввод названия свича. Ознакомьтесь со списком:')
            bot.send_message(message.from_user.id, switches)
            bot.send_message(message.from_user.id, 'Введите точное название коммутатора который желаете удалить')

    except (TypeError, SyntaxError) as error:
        print(error)
