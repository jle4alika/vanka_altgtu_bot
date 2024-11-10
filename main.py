import os
from aiogram import Bot, Dispatcher
from handlers import homework, others, schedule
#from handlers.time_mes import send_message_cron
from database.models import async_main
import asyncio
import logging
#from apscheduler.schedulers.asyncio import AsyncIOScheduler

from dotenv import find_dotenv, load_dotenv

load_dotenv(find_dotenv())
# Инициализируем логгер
logger = logging.getLogger(__name__)


# Функция конфигурирования и запуска бота
async def main():
    await async_main()
    bot = Bot(token=os.getenv('TOKEN'))
    dp = Dispatcher()
    logging.basicConfig(
        level=logging.INFO,
        format='%(filename)s:%(lineno)d #%(levelname)-8s [%(asctime)s] - %(name)s - %(message)s')
    # Выводим в консоль информацию о начале запуска
    logger.info('Starting BOT')

    # scheduler = AsyncIOScheduler()
    # scheduler.add_job(send_message_cron, trigger='cron', hour=12,
    #                   minute=00, start_date=datetime.datetime.now(), kwargs={'bot': bot})
    #
    # scheduler.add_job(send_message_cron, trigger='cron', hour=20,
    #                   minute=00, start_date=datetime.datetime.now(), kwargs={'bot': bot})
    # scheduler.start()
    dp.include_router(schedule.router)
    dp.include_router(homework.router)
    dp.include_router(others.router)

    await bot.delete_webhook(drop_pending_updates=True)
    await dp.start_polling(bot)


if __name__ == '__main__':
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print('Бот выключен')
