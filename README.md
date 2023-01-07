# Проект Яндекс.Практикума "homework_bot"

## Описание
Бот создан для проверки статуса сданной на ревью домашней работы путем многократного обращения к API сервису Яндекс.Практикум. Бот узнает статус Вашей домашней работы, следит за обновлениями ее статуса и уведомляет Вас в случае его изменения в указанный телеграмм канал.

### Стек:
```
Python 3.8, python-telegram-bot.
```

### Запуск проекта:
Необходимо:
1) Клонировать данный репозиторий:
```bash
git clone git@github.com:SpaiK89/homework_bot.git
```

2) Создать и активировать виртуальное окружение:
для Mac/Linux
```bash
python3 -m venv venv
source venv/bin/activate
```
для Windows
```bash
python -m venv venv
source venv/Scripts/activate
```

3) Установить зависимости из requirements.txt:
```bash
pip install -r requirements.txt
```

4) Создать файл .env и добавить в него ключ и значение для каждой переменной:
```bash
PRACTICUM_TOKEN = 'XXX' - Токен длядоступа к API Яндекс.Практикум
TELEGRAM_TOKEN = 'XXX' - Токен Телеграм-бота
TELEGRAM_CHAT_ID = 'XXX' - Идентификатор телеграм-канала/пользователя
```

5) Запустить проект:
```bash
homework.py
```

### Разработчик проекта
- Богомолов Игорь
- https://github.com/SpaiK89