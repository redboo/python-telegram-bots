from aiogram import Bot, types
from aiogram.dispatcher import Dispatcher, filters
from aiogram.utils import executor
from environs import Env
from googlesheet import GoogleSheet
from loguru import logger

path = ".env"
env = Env()
env.read_env()

logger.add(
    env.str("LOG_FILE"),
    format="{time} {level} {message}",
    level="DEBUG",
    rotation="1 week",
    compression="tar.xz",
)


class TelegramBot(Bot):
    def __init__(
        self,
        token,
        parse_mode,
        googlesheet: GoogleSheet | None = None,
    ):
        super().__init__(token, parse_mode)
        if googlesheet:
            self.googlesheet: GoogleSheet = googlesheet


bot: TelegramBot = TelegramBot(
    token=env.str("TOKEN"),
    parse_mode=types.ParseMode.HTML,
    googlesheet=GoogleSheet(
        "credentials.json",
        "17Pfljiy2W9jDt050MgFNFgYnoZ4vp_U8_n3yO8dnM_w",
    ),
)
dp = Dispatcher(bot)


@dp.message_handler(filters.Regexp(regexp=r"абонемент\s\d{1,5}"))
async def subscription_handler(message_from: types.Message) -> None:
    user_id: str = str(message_from.from_id)
    text_msg: str = message_from.md_text.strip(" @#")
    command, number = text_msg.lower().split(" ")
    print(f"Вход: команда '{command}', опция '{number}'")

    values = bot.googlesheet.search_subscription(number)

    message = "Такого абонемента не существует, либо его срок действия истек 😰"

    if values:
        end_date_value, balance_value = values
        last_digit = balance_value % 10

        suffix = "й"
        if last_digit == 1 and balance_value != 11:
            suffix = "е"
        elif last_digit in (2, 3, 4) and balance_value not in (12, 13, 14):
            suffix = "я"

        message = (
            f"🗓 Ваш абонемент заканчивается {end_date_value}\n"
            f"💃 У вас осталось {balance_value} заняти{suffix}"
        )

    try:
        await message_from.reply(message)
    except Exception as send_error:
        logger.debug(f"{str(send_error)}: Trouble id: {user_id}")
        return


@dp.message_handler(filters.Regexp(regexp=r"^бот$"))
async def bot_commands_handler(message_from: types.Message) -> None:
    user_id: str = str(message_from.from_id)
    text_msg: str = message_from.md_text.strip(" @#")
    command: str = text_msg.lower()
    print(f"Вход: команда '{command}'")

    message: str = (
        "🤖 КОМАНДЫ ДЛЯ ЧАТ-БОТА: 🤖\n\n"
        "❗ Бот ❗\n"
        "-- все доступные команды чат-бота 📣\n\n"
        "❗ Абонемент *** ❗\n"
        "-- (*** - № абонемента) информация о Вашем абонементе (дата "
        "окончания и количество оставшихся занятий) 🔖\n\n"
        "❗ Как добраться ❗\n"
        "-- наш адрес, карта и инструкция, как нас найти 🗺\n\n"
        "❗ Цены ❗\n"
        "-- цены на занятия и программа лояльности 💰\n\n"
        "❗ Расписание дети ❗\n"
        "-- расписание детских занятий (от 5 до 13 лет) 📆\n\n"
        "❗ Расписание взрослые ❗\n"
        "-- расписание взрослых занятий (13+) 📆\n\n"
        "Если у Вас иной вопрос, то напишите и вам ответит администратор 👤"
    )

    try:
        await message_from.reply(message)
    except Exception as send_error:
        logger.debug(f"{str(send_error)}: Trouble id: {user_id}")
        return


@dp.message_handler(filters.Regexp(regexp=r"^цен[аы]$"))
async def prices_handler(message_from: types.Message) -> None:
    user_id: str = str(message_from.from_id)
    text_msg: str = message_from.md_text.strip(" @#")
    command: str = text_msg.lower()
    print(f"Вход: команда '{command}'")
    try:
        with open("assets/price.jpg", "rb") as photo:
            await bot.send_photo(user_id, photo)
    except Exception as send_error:
        logger.debug(f"{str(send_error)}: Trouble id: {user_id}")
        return


@dp.message_handler(filters.Regexp(regexp=r"расписание\sвзрослые"))
async def schedule_adults_handler(message_from: types.Message) -> None:
    user_id: str = str(message_from.from_id)
    text_msg: str = message_from.md_text.strip(" @#")
    command: str = text_msg.lower()
    print(f"Вход: команда '{command}'")
    try:
        with open("assets/timetable.jpg", "rb") as photo:
            await bot.send_photo(user_id, photo)
    except Exception as send_error:
        logger.debug(f"{str(send_error)}: Trouble id: {user_id}")
        return


if __name__ == "__main__":
    executor.start_polling(dp, skip_updates=True)
