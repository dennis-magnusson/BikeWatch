import logging
import os

from dotenv import load_dotenv
from sqlalchemy.orm import Session
from telegram import InlineKeyboardButton, InlineKeyboardMarkup, Update
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes

from backend.src.database import get_db
from common.models.alert import UserAlert

logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s", level=logging.INFO
)

load_dotenv()

TELEGRAM_BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")

if not TELEGRAM_BOT_TOKEN:
    raise ValueError("TELEGRAM_BOT_TOKEN is not set in .env file")


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    args = context.args

    if len(args) != 0:  # if chat_id argument is given
        alert_id = args[0]
        chat_id = update.effective_chat.id

        db: Session = next(get_db())

        user_alert = db.query(UserAlert).filter(UserAlert.id == alert_id).first()

        if user_alert:
            user_alert.chat_id = chat_id
            db.commit()
            await context.bot.send_message(
                chat_id=chat_id,
                text="Your alert has been successfully registered.",
            )
        else:
            await context.bot.send_message(
                chat_id=chat_id,
                text="The id you provided doesn't exist or then it has already been registered.",
            )
    else:
        keyboard = [
            [
                InlineKeyboardButton("Yes", callback_data="create_filter_yes"),
                InlineKeyboardButton("No", callback_data="create_filter_no"),
            ]
        ]
        reply_markup = InlineKeyboardMarkup(keyboard)
        await update.message.reply_text(
            "Do you want to create a new filter?",
            reply_markup=reply_markup,
        )


if __name__ == "__main__":
    application = ApplicationBuilder().token(TELEGRAM_BOT_TOKEN).build()

    start_handler = CommandHandler("start", start)
    application.add_handler(start_handler)

    application.run_polling()
