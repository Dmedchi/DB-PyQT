# Класс декоратор для логирования функций

from functools import wraps


class Log:
    """ Класс декоратор для логирования функций """

    def __init__(self, logger):
        # запоминаем логгер, чтобы можно было применить к серверу и к клиенту
        self.logger = logger

    @staticmethod
    def _create_message(result=None, *args, **kwargs):
        """
        Формирует сообщение для записи в лог
        :param result: результат работы функции
        :param args: любые параметры по порядку
        :param kwargs: любые именованные параметры
        :return:
        """
        message = ''
        if args:
            message += 'args: {} '.format(args)
        if kwargs:
            message += 'kwargs: {} '.format(kwargs)
        if result:
            message += 'result: {} '.format(result)
        # Возвращаем итоговое сообщение
        return message

    def __call__(self, func):
        """
        Определяем __call__ для возможности вызова экземпляра как декоратора
        :param func: функция которую будем декорировать
        :return: новая функция
        """

        @wraps(func)
        def decorated(*args, **kwargs):
            # Выполняем функцию и получаем результат
            result = func(*args, **kwargs)

            # Формируем сообщение в лог
            message = Log._create_message(result, *args, **kwargs)

            # Пишем сообщение в лог
            self.logger.info('{} - {} - {}'.format(message, decorated.__name__, decorated.__module__))
            return result

        return decorated
