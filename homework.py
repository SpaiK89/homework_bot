import logging
import sys
import time
import os
import requests
from http import HTTPStatus
from dotenv import load_dotenv
import telegram

load_dotenv()

PRACTICUM_TOKEN = os.getenv('PRACTICUM_TOKEN')
TELEGRAM_TOKEN = os.getenv('TELEGRAM_TOKEN')
TELEGRAM_CHAT_ID = os.getenv('TELEGRAM_CHAT_ID')

RETRY_PERIOD = 600
ENDPOINT = 'https://practicum.yandex.ru/api/user_api/homework_statuses/'
HEADERS = {'Authorization': PRACTICUM_TOKEN}

HOMEWORK_VERDICTS = {
    'approved': 'Работа проверена: ревьюеру всё понравилось. Ура!',
    'reviewing': 'Работа взята на проверку ревьюером.',
    'rejected': 'Работа проверена: у ревьюера есть замечания.'
}


def check_tokens():
    """Проверка доступности переменных окружения."""
<<<<<<< HEAD
    tokens_list = (PRACTICUM_TOKEN, TELEGRAM_TOKEN, TELEGRAM_CHAT_ID)
    return all(tokens_list)
=======
    tokens_dict = {
        'PRACTICUM_TOKEN': PRACTICUM_TOKEN,
        'TELEGRAM_TOKEN': TELEGRAM_TOKEN,
        'TELEGRAM_CHAT_ID': TELEGRAM_CHAT_ID,
    }
    for index, token in tokens_dict.items():
        if token == '':
            logging.critical(
                'Ошибка доступности переменных окружения к основному API: '
                f'"{index}". Программа принудительно остановлена.'
            )
            return False
    logging.info('Проверка переменных окружения прошла успешно.')
    return True
>>>>>>> b02e2bfdddb9be23c7749775582984ef5cbf35d3


def send_message(bot, message):
    """Отправка сообщения в Telegram чат."""
    try:
        bot.send_message(TELEGRAM_CHAT_ID, message)
        logging.debug('Сообщение успешно отправлено')
    except telegram.error.TelegramError as error:
        logging.error(f'Ошибка отправки сообщения: {error}')


def get_api_answer(timestamp):
    """Запрос к эндпоинту API-сервиса."""
    payload = {'from_date': timestamp}
    try:
        response = requests.get(ENDPOINT, headers=HEADERS, params=payload)
    except Exception as error:
        logging.error(f'Ошибка ответа API: {error}')
        raise Exception(f'Ошибка ответа API: {error}')
    if response.status_code != HTTPStatus.OK:
        logging.error(
            f'Эндпоинт {ENDPOINT} недоступен. '
            f'Код ответа API: {response.status_code}'
        )
        raise Exception(
            f'Эндпоинт {ENDPOINT} недоступен. '
            f'Код ответа API:{response.status_code}'
        )
    try:
        return response.json()
    except ValueError:
        logging.error('Ошибка формата JSON')
        raise ValueError('Ошибка формата JSON')


def check_response(response):
    """Проверка ответа API на соответствие документации."""
    if not isinstance(response, dict) or not response:
        logging.error('Ответ API не соответствет ожиданиям')
        raise TypeError('Ответ API не соответствет ожиданиям')
    if 'homeworks' not in response:
        logging.error('В ответе API отсутствует список домашних работ с ключом'
                      ' "homeworks"')
        raise TypeError('В ответе API отсутствует список домашних работ '
                        'с ключом "homeworks"')
    if not isinstance(response['homeworks'], list):
        logging.error('Тип значения ключа "homeworks" не соответствует '
                      'ожидаемому')
        raise TypeError('Тип значения ключа "homeworks" не соответствует '
                        'ожидаемому')
    homeworks = response.get('homeworks')
    if homeworks:
        return homeworks[0]


def parse_status(homework):
    """Извлечение из информации о последней домашней работе её статуса."""
    if 'homework_name' not in homework:
        logging.error('В ответе API отсутствует ключ "homework_name"')
        raise KeyError('В ответе API отсутствует ключ "homework_name"')
    if 'status' not in homework:
        logging.error('В ответе API отсутствует ключ "status"')
        raise KeyError('В ответе API отсутствует ключ "status"')
    if homework['status'] not in HOMEWORK_VERDICTS:
        logging.error(
            f'Статус "{homework["status"]}" в ответе API '
            f'не соответствует ожидаемым')
        raise Exception(f'Статус "{homework["status"]}" в ответе API '
                        'не соответствует ожидаемым')
    verdict = HOMEWORK_VERDICTS[homework['status']]
    logging.info('Обновлен статус домашней работы')
    return ('Изменился статус проверки работы '
            f'"{homework["homework_name"]}". {verdict}')


def main():
    """Основная логика работы бота."""
    if not check_tokens():
        exit(
            logging.critical(
                'Ошибка доступности переменных окружения к основному API. '
                'Программа принудительно остановлена.'
            )
        )
    logging.info('Проверка переменных окружения прошла успешно.')
    bot = telegram.Bot(token=TELEGRAM_TOKEN)
    timestamp = int(time.time())
    cache = {'last_response': 0, 'last_error': 0}
    while True:
        try:
            response = get_api_answer(timestamp)
            homework = check_response(response)
            if cache['last_response'] != homework:
                try:
                    message = parse_status(homework)
                except TypeError:
                    message = 'Работа еще не принята на проверку'
                send_message(bot, message)
                cache['last_response'] = homework
            logging.debug('Статус ответа не изменился')
        except Exception as error:
            message = f'Сбой в работе программы: {error}'
            logging.info(f'{message}')
            if cache['last_error'] != f'{error}':
                send_message(bot, message)
                cache['last_error'] = f'{error}'
        finally:
            timestamp = response.get('current_date')
            time.sleep(RETRY_PERIOD)


if __name__ == '__main__':
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s, %(levelname)s, %(name)s, %(message)s',
        handlers=[logging.StreamHandler(stream=sys.stdout)]
    )
    main()
