from aiogram.client.default import DefaultBotProperties
from dotenv import load_dotenv
from os import getenv
from asyncio import run
from aiogram import Bot, Dispatcher
import logging

from src import student_router, start_router, learning_router, subject_router, admin_router, teacher_router, \
    menu_router, support_router, interview_router, product_router, interview_questions_router
from src import create_tables
from src import UserCheckMiddleware, GroupMessageMiddleware, GroupCallbackMiddleware, DeletePhotosMiddleware

load_dotenv()

BOT_TOKEN = getenv('TEST_BOT_TOKEN')
STUDENT_GROUP_ID = getenv('STUDENT_GROUP_ID')
TEACHER_GROUP_ID = getenv('TEACHER_GROUP_ID')
RECRUITERS_GROUP_ID = getenv('RECRUITERS_GROUP_ID')

bot = Bot(token=BOT_TOKEN, default=DefaultBotProperties(parse_mode='HTML'))
dp = Dispatcher()

dp.message.middleware.register(UserCheckMiddleware())

dp.message.middleware.register(GroupMessageMiddleware(
    group_id_student=int(STUDENT_GROUP_ID),
    group_id_teacher=int(TEACHER_GROUP_ID),
    group_id_recruiter=int(RECRUITERS_GROUP_ID),
))


dp.callback_query.middleware.register(GroupCallbackMiddleware(
    group_id_student=int(STUDENT_GROUP_ID),
    group_id_teacher=int(TEACHER_GROUP_ID),
    group_id_recruiter=int(RECRUITERS_GROUP_ID),
    allowed_callback_data={"candidate_accept", "candidate_decline"}
))

dp.callback_query.middleware.register(DeletePhotosMiddleware())

logging.basicConfig(
        level=logging.INFO,
        # filename="bot.log",
        # filemode="a",
        # format="%(asctime)s %(levelname)s %(message)s"
    )

logger = logging.getLogger("Main")


async def bot_start():
    await create_tables()
    logger.info("Bot is starting...")
    try:
        dp.include_routers(
            admin_router
            # start_router,
            # menu_router,
            # student_router,
            # learning_router,
            # subject_router,
            # teacher_router,
            # support_router,
            # interview_router,
            # product_router,
            # interview_questions_router,
        )
        await dp.start_polling(bot)
    except KeyboardInterrupt:
        return
    except Exception as e:
        logger.error(f"Bot encountered an error: {e}")


if __name__ == "__main__":
    logger.info("Initializing bot...")
    run(bot_start())
