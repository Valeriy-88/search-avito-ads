from telebot.handler_backends import State, StatesGroup


class UserAnswerState(StatesGroup):
    add_switch = State()
    delete_switch = State()
    name_old_switch = State()
    name_new_switch = State()
    choice = State()
