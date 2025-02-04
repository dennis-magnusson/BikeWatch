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
    MessageHandler,
    filters,
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
        await query.edit_message_text(
            text="What frame size are you looking for? Give the tube length in centimeters (eg. 54 if you are looking for a 54cm frame)."
        )
        context.user_data["filter_stage"] = "size"
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
            [InlineKeyboardButton("Road", callback_data="category_filter_road")],
            [InlineKeyboardButton("Gravel", callback_data="category_filter_gravel")],
            [InlineKeyboardButton("Hybrid", callback_data="category_filter_hybrid")],
            [
                InlineKeyboardButton(
                    "Triathlon", callback_data="category_filter_triathlon"
                )
            ],
            [InlineKeyboardButton("Fatbike", callback_data="category_filter_fatbike")],
            [
                InlineKeyboardButton(
                    "Electric", callback_data="category_filter_electric_flat"
                )
            ],
        ]
        reply_markup = InlineKeyboardMarkup(keyboard)
        await query.edit_message_text(
            text="What category of bike?", reply_markup=reply_markup
        )
        return

    # Handle category filter response
    if query.data.startswith("category_filter_"):
        await query.answer()
        keyboard = [
            [InlineKeyboardButton("Any", callback_data="price_range_any")],
            [InlineKeyboardButton("0€ - 500€", callback_data="price_range_0_500")],
            [
                InlineKeyboardButton(
                    "500€ - 1000€", callback_data="price_range_500_1000"
                )
            ],
            [
                InlineKeyboardButton(
                    "1000€ - 2000€", callback_data="price_range_1000_2000"
                )
            ],
            [
                InlineKeyboardButton(
                    "2000€ - 5000€", callback_data="price_range_2000_5000"
                )
            ],
            [InlineKeyboardButton("5000€ +", callback_data="price_range_5000_plus")],
        ]
        reply_markup = InlineKeyboardMarkup(keyboard)
        await query.edit_message_text(
            text="What price range?", reply_markup=reply_markup
        )
        return

    # Handle price range response
    if query.data.startswith("price_range_"):
        await query.answer()
        keyboard = [
            [InlineKeyboardButton("Any", callback_data="location_filter_any")],
            [InlineKeyboardButton("Uusimaa", callback_data="location_filter_uusimaa")],
        ]
        reply_markup = InlineKeyboardMarkup(keyboard)
        await query.edit_message_text(text="What location?", reply_markup=reply_markup)
        return

    # Handle location filter response
    if query.data.startswith("location_filter_"):
        await query.answer()
        await query.edit_message_text(text="Your filter has been created.")
        # TODO: Save the filter to the database
        return

    await query.answer()
    await query.edit_message_text(text=f"Selected option: {query.data}")


async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    if "filter_stage" in context.user_data:
        if context.user_data["filter_stage"] == "size":
            size = update.message.text
            try:
                size = int(size)
                if 42 <= size <= 68:
                    context.user_data["size"] = size
                    await update.message.reply_text(
                        f"Size '{size}' added. Now, please choose categories to filter."
                    )
                    context.user_data["filter_stage"] = "category"
                    keyboard = [
                        [
                            InlineKeyboardButton(
                                "Road", callback_data="category_filter_road"
                            )
                        ],
                        [
                            InlineKeyboardButton(
                                "Gravel", callback_data="category_filter_gravel"
                            )
                        ],
                        [
                            InlineKeyboardButton(
                                "Hybrid", callback_data="category_filter_hybrid"
                            )
                        ],
                        [
                            InlineKeyboardButton(
                                "Triathlon", callback_data="category_filter_triathlon"
                            )
                        ],
                        [
                            InlineKeyboardButton(
                                "Fatbike", callback_data="category_filter_fatbike"
                            )
                        ],
                        [
                            InlineKeyboardButton(
                                "Electric",
                                callback_data="category_filter_electric_flat",
                            )
                        ],
                    ]
                    reply_markup = InlineKeyboardMarkup(keyboard)
                    await update.message.reply_text(
                        text="Please choose categories to filter.",
                        reply_markup=reply_markup,
                    )
                else:
                    await update.message.reply_text(
                        "Invalid size. Please enter a number between 42 and 68."
                    )
            except ValueError:
                await update.message.reply_text("Invalid size. Please enter a number.")
        return


if __name__ == "__main__":
    application = ApplicationBuilder().token(TELEGRAM_BOT_TOKEN).build()

    start_handler = CommandHandler("start", start)
    application.add_handler(start_handler)
    application.add_handler(CallbackQueryHandler(button))
    application.add_handler(CommandHandler("help", help_command))
    application.add_handler(
        MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message)
    )

    application.run_polling()
