from telegram import (
    InlineKeyboardButton,
    InlineKeyboardMarkup,
    ReplyKeyboardMarkup,
    ReplyKeyboardRemove,
    Update,
)
from telegram.ext import ContextTypes

BIKE_CATEGORY, BIKE_MAXPRICE, BIKE_SIZE = range(3)


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    reply_keyboard = [
        ["Road", "Gravel", "Hybrid", "Triathlon", "Fatbike", "Electric"],
    ]

    await update.message.reply_text(
        "<b>Welcome to the BikeWatch Bot!\n"
        "Let's get some details about the bikes you want me to watch for\n"
        "What type of bike are you looking for?</b>",
        parse_mode="HTML",
        reply_markup=ReplyKeyboardMarkup(
            reply_keyboard, one_time_keyboard=True, resize_keyboard=True
        ),
    )

    return BIKE_CATEGORY


async def bike_category(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    context.user_data["bike_category"] = update.message.text
    await update.message.reply_text(
        f"<b>You selected {update.message.text}.\n" f"What is your budget?</b>",
        parse_mode="HTML",
        reply_markup=ReplyKeyboardRemove(),
    )

    keyboard = [
        [InlineKeyboardButton("Any price", callback_data="maxprice_any")],
        [InlineKeyboardButton("100€", callback_data="maxprice_100")],
        [InlineKeyboardButton("500€", callback_data="maxprice_500")],
        [InlineKeyboardButton("1000€", callback_data="maxprice_1000")],
        [InlineKeyboardButton("2000€", callback_data="maxprice_2000")],
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)

    await update.message.reply_text(
        "<b>Please choose:</b>", parse_mode="HTML", reply_markup=reply_markup
    )

    return BIKE_MAXPRICE


async def bike_maxprice(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    query = update.callback_query
    query.answer()

    context.user_data["bike_maxprice"] = query.data
    await query.message.reply_text(
        f"<b>You selected {query.data}.\n" f"What size are you looking for?</b>",
        parse_mode="HTML",
    )

    return BIKE_SIZE


async def bike_size(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    context.user_data["bike_size"] = update.message.text
    await update.message.reply_text(
        f"<b>You selected {update.message.text}.\n"
        f"Great! I will start looking for bikes that match your criteria.</b>",
        parse_mode="HTML",
    )

    return BIKE_SIZE
