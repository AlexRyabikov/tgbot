# Простой пример TG-бота на Python

Оригинал был создан по запросу HR-департамент для облегчения сбора первичной информации от кандидатов.
В работе используется JSON-файл с вопросами и ответами, которые направляют человека, взаимодействующего с ботом, далее по воронке.
Данный бот является бета-версией (см. нерешенные проблемы).

## Библиотеки

Бот использует в своей работе библиотеку python-telegram-bot

Установка:

```bash
pip install python-telegram-bot
```
```bash
pip3 install python-telegram-bot
```
### Что нужно для запуска

1. Сервер с ОС Linux (Ubuntu, CentOS)
1. Установленное ПО (Python, необходимые библиотеки)
1. Токен, полученный от @Botfather'а
1. ID Диалога пользователя, который будет получать сообщения, поступающие в бот
1. Скрипт должен быть запущен в Screen или Tmux

#### Нерешенные проблемы
1. Ключи ответов имеют ограничение на длину сообщения, их планируется перевести на числовые значения
1. Присутствует дублирование данных в шаблонных ответах. Их планируется вынести в отельный объект
1. Ввиду первого пункта нерешенных проблем приходится искусственно уникализировать варианты ответов, чтобы не возникало аномалий в логике функционирования бота