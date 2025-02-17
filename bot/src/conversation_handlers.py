from constants import (
    BIKE_CATEGORY,
    BIKE_MAXPRICE,
    BIKE_MINPRICE,
    BIKE_REGION,
    BIKE_SIZE,
    REGION_OPTIONS,
)
from telegram import ReplyKeyboardMarkup, ReplyKeyboardRemove, Update
from telegram.ext import ContextTypes, ConversationHandler

from common.database import get_db
from common.models.alert import UserAlert


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    reply_keyboard = [
        ["🚴 Road", "🚵 Gravel", "🚲 Hybrid", "☑️ Any"],
    ]
    await update.message.reply_text(
        "👋 To set up notifications for bike listings, let's set some filters.\n\nWhat category of bike are you looking for?",
        parse_mode="HTML",
        reply_markup=ReplyKeyboardMarkup(
            reply_keyboard, one_time_keyboard=True, resize_keyboard=True
        ),
    )
    return BIKE_CATEGORY


async def bike_category(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    valid_categories = ["Road", "Gravel", "Hybrid", "Any"]
    category_chosen = (
        update.message.text.encode("ascii", "ignore").decode("ascii").strip()
    )
    if category_chosen not in valid_categories:
        await update.message.reply_text(
            "❌ Invalid category. Please choose a category from the keyboard.",
            reply_markup=ReplyKeyboardMarkup(
                [["🚴 Road", "🚵 Gravel", "🚲 Hybrid", "☑️ Any"]],
                one_time_keyboard=True,
                resize_keyboard=True,
            ),
        )
        return BIKE_CATEGORY

    context.user_data["bike_category"] = category_chosen
    await update.message.reply_text(
        "💶 What maximum price (€)?",
        reply_markup=ReplyKeyboardMarkup(
            [["500", "1000", "2000", "5000"]],
            one_time_keyboard=True,
            resize_keyboard=True,
        ),
    )
    return BIKE_MAXPRICE


async def bike_maxprice(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    try:
        max_price = int(update.message.text)
        if max_price > 0:
            context.user_data["bike_maxprice"] = max_price
            await update.message.reply_text(
                "💶 What minimum price (€)?",
                reply_markup=ReplyKeyboardMarkup(
                    [["0", "200", "500", "1000"]],
                    one_time_keyboard=True,
                    resize_keyboard=True,
                ),
            )
            return BIKE_MINPRICE
        else:
            await update.message.reply_text(
                "❌ Invalid price. Please enter a non-negative number."
            )
    except ValueError:
        await update.message.reply_text(
            "❌ Invalid price. Please enter a valid number."
        )
    return BIKE_MAXPRICE


async def bike_minprice(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    try:
        min_price = int(update.message.text)
        if (
            min_price >= 0
            and min_price < context.user_data["bike_maxprice"]
            and min_price != "inf"
        ):
            context.user_data["bike_minprice"] = min_price
            await update.message.reply_text(
                "📏 What size? \n\nPlease provide the tube length in centimeters or 'any' if you don't want to filter by size.",
                reply_markup=ReplyKeyboardMarkup(
                    [["52", "54", "56", "58", "Any"]],
                    one_time_keyboard=True,
                    resize_keyboard=True,
                ),
            )
            return BIKE_SIZE
        else:
            await update.message.reply_text(
                "❌ Invalid price. Please enter a non-negative number that less than your max price."
            )
    except ValueError:
        await update.message.reply_text(
            "❌ Invalid price. Please enter a valid number."
        )
    return BIKE_MINPRICE


async def bike_size(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    text = update.message.text
    try:
        if text == "Any":
            size = None
        else:
            size = float(text)
            if size <= 0:
                await update.message.reply_text(
                    "❌ Invalid size. Please enter a positive number."
                )
                return BIKE_SIZE

        context.user_data["bike_size"] = text
        await update.message.reply_text(
            "📍 Which region are you interested in?",
            reply_markup=ReplyKeyboardMarkup(
                [REGION_OPTIONS],
                one_time_keyboard=True,
                resize_keyboard=True,
            ),
        )
        return BIKE_REGION

    except ValueError:
        await update.message.reply_text(
            "❌ Invalid size. Please enter a valid number or 'Any'."
        )
        return BIKE_SIZE


async def bike_region(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    region_chosen = update.message.text.strip()
    if region_chosen not in REGION_OPTIONS:
        await update.message.reply_text(
            "❌ Invalid region. Please choose a region from the keyboard.",
            reply_markup=ReplyKeyboardMarkup(
                [REGION_OPTIONS],
                one_time_keyboard=True,
                resize_keyboard=True,
            ),
        )
        return BIKE_REGION

    gave_number = context.user_data["bike_size"].isdigit()

    category_text = context.user_data["bike_category"].capitalize()
    price_text = (
        f"{context.user_data['bike_minprice']}-{context.user_data['bike_maxprice']} €"
    )
    size_text = context.user_data["bike_size"] + " cm" if gave_number else "Any"
    region_text = region_chosen

    await update.message.reply_text(
        "✅ I will send you listings matching that match these: \n"
        f"🚴 {category_text}\n"
        f"💶 {price_text}\n"
        f"📏 {size_text}\n"
        f"📍 {region_text}"
    )

    alert = UserAlert(
        chat_id=update.effective_user.id,
        category=context.user_data["bike_category"].lower()
        if context.user_data["bike_category"] != "Any"
        else None,
        min_price=context.user_data["bike_minprice"],
        max_price=context.user_data["bike_maxprice"],
        size=context.user_data["bike_size"]
        if context.user_data["bike_size"] != "Any"
        else None,
        region=region_chosen if region_chosen != "Any" else None,
    )

    db_session = next(get_db())
    db_session.add(alert)
    db_session.commit()

    return ConversationHandler.END


async def cancel(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    context.user_data.clear()
    await update.message.reply_text("Bye!", reply_markup=ReplyKeyboardRemove())
    return ConversationHandler.END
