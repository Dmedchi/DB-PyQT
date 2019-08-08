# Создание и настройка именованного логгера.
import os
import logging
import logging.handlers

# путь до папки где лежит этот модуль
LOG_FOLDER_PATH = os.path.dirname(os.path.abspath(__file__))
# Пусть до серверного лога
SERVER_LOF_FILE_PATH = os.path.join(LOG_FOLDER_PATH, 'server.log')
# Формат сообщения
formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(funcName)s - %(message)s')
# создаем логгер с именем server
server_log = logging.getLogger('server')
# файловый обработчик логгирования:
server_handler = logging.handlers.TimedRotatingFileHandler(SERVER_LOF_FILE_PATH, encoding='utf-8', when='d', interval=1)
# Связываем обработчик с форматером
server_handler.setFormatter(formatter)
# Связываем логгер с обработчиком
server_log.addHandler(server_handler)
# Устанавливаем уровень сообщений
server_log.setLevel(logging.INFO)

# Варианты ответов нв разных уровнях
server_log.debug("Hello! I'm is DEBUG!")
server_log.info("Hello, I'm is INFO!")
server_log.warning('It seems to be a bug...WARNING')
server_log.critical('CRITICAL bug in app! Hello, World!')
