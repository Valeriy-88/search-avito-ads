import logging
from typing import Literal, Any
import redis
import ujson
from config_data import config


class Cache(redis.StrictRedis):
    """
    Класс Кэш. Родитель: redis.StrictRedis

    Args:
    host (str): передает имя хоста redis сервера
    port (int): передает номер порта redis сервера
    password (str): передает пароль от redis сервера
    charset (str): передает способ кодирования символов
    decode_responses (bool): передает истину для расшифровки каждого значения из базы данных
    """

    def __init__(self, host: str, port: int, password: str,
                 charset: str = "utf-8",
                 decode_responses: Literal[True] = True):
        super(Cache, self).__init__(host, port,
                                    password=password,
                                    charset=charset,
                                    decode_responses=decode_responses)
        logging.info("Redis start")

    def getting_json_file(self, name: str, value, time: int = 0) -> bool:
        """
        Функция конвертирует python-объект в Json и сохраняет его
        name str: имя пользователя
        value int: выбранная пользователем услуга
        time int: время истечения срока действия запроса в секундах
        :return: bool
        """
        return self.setex(name, time, ujson.dumps(value))

    def getting_python_object(self, name: str) -> Any | None:
        """
        Функция возвращает Json и конвертирует в python-объект
        name str: имя пользователя
        :return: Any | None
        """
        scroll_service = self.get(name)
        if scroll_service is None:
            return scroll_service
        return ujson.loads(scroll_service)


cache = Cache(
    host=config.REDIS_HOST,
    port=config.REDIS_PORT,
    password=config.REDIS_PASSWORD
)