# 0001 Danceclub Bot

Python Telegram Бот для студии танцев. Python + Aiogram + Pygsheets. Работает с Google Sheets API

Данные хранятся в гугл-таблице. Обязательные поля: ID абонемента, количество оставшихся занятий, дата окончания абонемента.

## Функциональное задание

- Как пользователь я могу посмотреть все доступные команды бота
- Как клиент я могу посмотреть данные о своем абонементе:
  - я могу видеть количество оставшихся занятий;
  - я могу видеть дату окончания абонемента.
- Как клиент я могу посмотреть цены
- Как клиент я могу посмотреть расписание
  - я могу видеть расписание для взрослых
  - я могу видеть расписание для детей
- Как клиент я могу посмотреть маршрут до места

## Запуск

```sh
python -m venv env
. ./env/bin/activate 
python -m pip install -r requirements.txt
python bot.py
```

## Используемые технологии

- <https://www.youtube.com/watch?v=bu5wXjz2KvU>
- <https://pygsheets.readthedocs.io/en/stable/index.html>
- <https://medium.com/game-of-data/play-with-google-spreadsheets-with-python-301dd4ee36eb>
- <https://docs.aiogram.dev/en/latest/quick_start.html>
- <https://youtu.be/3ndEeGDVqD4>
- <https://loguru.readthedocs.io/en/stable/>
- <https://youtu.be/FlPd1BP_cVc>
- <https://youtu.be/PJz_tMIo_nM>
