import asyncio
import logging
import os

from aiogram import Dispatcher, types, Bot
from aiogram.fsm.storage.memory import MemoryStorage
from dotenv import load_dotenv

from handlers import router

# Проверяем, запущено ли приложение в докере
is_running_in_docker = os.path.exists('/.dockerenv') or os.path.exists('/proc/1/cgroup')

# Устанавливаем уровень логирования в зависимости от окружения.
if is_running_in_docker:
    log_level = logging.INFO
else:
    log_level = logging.DEBUG

logging.basicConfig(level=log_level)

# Получаем токен из окружения
# load_dotenv()
TOKEN = os.getenv("TOKEN")

# Создаем бота
dp = Dispatcher(storage=MemoryStorage())
bot = Bot(token=TOKEN)

# Устанавливаем команды
commands = [
    types.BotCommand(command="/start", description="Начать диалог"),
    types.BotCommand(command="/messages", description="Получить все сообщения"),
    types.BotCommand(command="/create", description="Создать сообщение"),
]

async def main():
    await bot.set_my_commands(commands)
    dp.include_router(router)
    await bot.delete_webhook(drop_pending_updates=True)
    try:
        await dp.start_polling(bot,
                               allowed_updates=dp.resolve_used_update_types(),
                               close_bot_session=True)
    except Exception as e:
        logging.error("Bot can't be started, error: {}".format(str(e)))


if __name__ == '__main__':
    asyncio.run(main())
