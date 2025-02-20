import asyncio
import logging
import os

from alert_listener import AlertListener
from dotenv import load_dotenv
from handlers import conv_handlers
from telegram import Update
from telegram.ext import ApplicationBuilder

logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s", level=logging.INFO
)

load_dotenv()
TELEGRAM_BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")
if not TELEGRAM_BOT_TOKEN:
    raise ValueError("TELEGRAM_BOT_TOKEN is not set in .env file")


async def main():
    application = ApplicationBuilder().token(TELEGRAM_BOT_TOKEN).build()
    application.add_handler(conv_handlers.conversation_handler)

    alert_listener = AlertListener(application.bot)

    try:
        alert_task = asyncio.create_task(alert_listener.start_listening())

        await application.initialize()
        await application.updater.start_polling()
        await application.start()

        # Keep the bot running indefinitely
        while True:
            await asyncio.sleep(1)

    except (KeyboardInterrupt, SystemExit):
        logging.info("Shutting down...")
    finally:
        alert_task.cancel()
        try:
            await alert_task
        except asyncio.CancelledError:
            pass

        await application.updater.stop()
        await application.stop()
        await application.shutdown()


if __name__ == "__main__":
    asyncio.run(main())
