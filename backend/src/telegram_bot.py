import logging
import os

from dotenv import load_dotenv
from sqlalchemy.orm import Session
from telegram import InlineKeyboardButton, InlineKeyboardMarkup, Update
from telegram.ext import (
    ApplicationBuilder,
    CallbackQueryHandler,
    CommandHandler,
    ContextTypes,
)

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


async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    await update.message.reply_text("Use /start to test this bot.")


async def button(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    query = update.callback_query

    if query.data == "create_filter_yes":
        await query.answer()
        keyboard = [
            [InlineKeyboardButton("All sizes", callback_data="size_filter_all")],
            [InlineKeyboardButton("Small", callback_data="size_filter_small")],
            [InlineKeyboardButton("Medium", callback_data="size_filter_medium")],
            [InlineKeyboardButton("Large", callback_data="size_filter_large")],
        ]
        reply_markup = InlineKeyboardMarkup(keyboard)
        await query.edit_message_text(
            text="Please choose a size filter or select 'All sizes'.",
            reply_markup=reply_markup,
        )
        return
    elif query.data == "create_filter_no":
        await query.answer()
        await query.edit_message_text(
            text="You can create a new filter later. Just use the command /start."
        )
        return

    # Handle size filter response
    if query.data.startswith("size_filter_"):
        await query.answer()
        keyboard = [
            [InlineKeyboardButton("Category 1", callback_data="category_filter_1")],
            [InlineKeyboardButton("Category 2", callback_data="category_filter_2")],
            [InlineKeyboardButton("Category 3", callback_data="category_filter_3")],
        ]
        reply_markup = InlineKeyboardMarkup(keyboard)
        await query.edit_message_text(
            text="Please choose categories to filter.", reply_markup=reply_markup
        )
        return

    # Handle category filter response
    if query.data.startswith("category_filter_"):
        await query.answer()
        keyboard = [
            [InlineKeyboardButton("$0 - $50", callback_data="price_range_0_50")],
            [InlineKeyboardButton("$50 - $100", callback_data="price_range_50_100")],
            [InlineKeyboardButton("$100 - $200", callback_data="price_range_100_200")],
        ]
        reply_markup = InlineKeyboardMarkup(keyboard)
        await query.edit_message_text(
            text="Please enter the price range.", reply_markup=reply_markup
        )
        return

    # Handle price range response
    if query.data.startswith("price_range_"):
        await query.answer()
        keyboard = [
            [InlineKeyboardButton("Location 1", callback_data="location_filter_1")],
            [InlineKeyboardButton("Location 2", callback_data="location_filter_2")],
            [InlineKeyboardButton("Location 3", callback_data="location_filter_3")],
        ]
        reply_markup = InlineKeyboardMarkup(keyboard)
        await query.edit_message_text(
            text="Please choose locations to filter.", reply_markup=reply_markup
        )
        return

    # Handle location filter response
    if query.data.startswith("location_filter_"):
        await query.answer()
        await query.edit_message_text(text="Your filter has been created.")
        # TODO: Save the filter to the database
        return

    await query.answer()
    await query.edit_message_text(text=f"Selected option: {query.data}")


if __name__ == "__main__":
    application = ApplicationBuilder().token(TELEGRAM_BOT_TOKEN).build()

    start_handler = CommandHandler("start", start)
    application.add_handler(start_handler)
    application.add_handler(CallbackQueryHandler(button))
    application.add_handler(CommandHandler("help", help_command))

    application.run_polling()
