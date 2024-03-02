from dotenv import load_dotenv, find_dotenv
import os
import logging

logging.basicConfig(level=logging.INFO)

SECRET_KEY = '6590357412:AAEnbmg9eKGc-pNnosM_Gky4nxS88Ugxfjo'

DEFAULT_COMMANDS = (
    ('help', "Помощь по командам бота"),
    ('search', "Запуск поиска объявлений"),
    ('view', "Просмотр списка коммутаторов для поиска"),
    ('update', "Обновление названия коммутатора"),
    ('add', "Добавление нового коммутатора в список"),
    ('delete', "Удаление коммутатора из списка"),
    ('stop', "Остановка поиска объявлений")
)

BOT_VERSION = 0.1

REDIS_HOST = 'localhost'
REDIS_PORT = 2395
REDIS_PASSWORD = None
