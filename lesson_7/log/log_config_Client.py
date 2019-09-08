# Создание и настройка именованного логгера.
import logging
import logging.handlers
import os


# путь до папки где лежит этот модуль
LOG_FOLDER_PATH = os.path.dirname(os.path.abspath(__file__))
# путь до файла с логом
CLIENT_LOG_FILE_PATH = os.path.join(LOG_FOLDER_PATH, 'client.log')

# создаем логгер с именем client
client_logger = logging.getLogger('client')
# формат сообщения
formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(funcName)s - %(message)s')
#файловый обработчик логгирования:
client_handler = logging.FileHandler(CLIENT_LOG_FILE_PATH, encoding='utf-8')
# задаем уровень обработчика
client_handler.setLevel(logging.INFO)
# связываем с форматером
client_handler.setFormatter(formatter)
# связываем логгер с обработчиком
client_logger.addHandler(client_handler)
# устанавливаем уровень логгера
client_logger.setLevel(logging.INFO)

# Варианты ответов нв разных уровнях
client_logger.debug("Hello! I'm is DEBUG!" )
client_logger.info("Hello, I'm is INFO!")
client_logger.warning('It seems to be a bug...WARNING')
client_logger.critical('CRITICAL bug in app! Hello, World!')


