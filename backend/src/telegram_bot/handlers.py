from telegram import (
    ReplyKeyboardMarkup,
    ReplyKeyboardRemove,
    Update,
)
from telegram.ext import (
    CommandHandler,
    ContextTypes,
    ConversationHandler,
    MessageHandler,
    filters,
)

from common.models.alert import UserAlert

from ..database import get_db

BIKE_CATEGORY, BIKE_MAXPRICE, BIKE_MINPRICE, BIKE_SIZE = range(4)


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    reply_keyboard = [
        ["Road", "Gravel", "Hybrid", "All"],
    ]

    await update.message.reply_text(
        "Welcome to the BikeWatch Bot!\n"
        "Let's get some details about the bikes you want me to watch for.\n\n"
        "What type of bike are you looking for?",
        parse_mode="HTML",
        reply_markup=ReplyKeyboardMarkup(
            reply_keyboard, one_time_keyboard=True, resize_keyboard=True
        ),
    )

    return BIKE_CATEGORY


async def bike_category(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    context.user_data["bike_category"] = update.message.text
    await update.message.reply_text(
        "What is your budget in euros?",
    )

    return BIKE_MAXPRICE


async def bike_maxprice(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    try:
        max_price = float(update.message.text)
        if max_price >= 0:
            context.user_data["bike_maxprice"] = max_price
            await update.message.reply_text(
                "What is the minimum value in euros of bikes you are interested in?",
            )
            return BIKE_MINPRICE
        else:
            await update.message.reply_text(
                "Invalid price. Please enter a non-negative number."
            )
    except ValueError:
        await update.message.reply_text("Invalid price. Please enter a valid number.")
    return BIKE_MAXPRICE


async def bike_minprice(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    try:
        # TODO: Handle "inf"
        min_price = float(update.message.text)
        if min_price >= 0 and min_price < context.user_data["bike_maxprice"]:
            context.user_data["bike_minprice"] = min_price
            await update.message.reply_text(
                "What size are you looking for? Please provide the tube length in centimeters.",
            )
            return BIKE_SIZE
        else:
            await update.message.reply_text(
                "Invalid price. Please enter a non-negative number that less than your max price."
            )
    except ValueError:
        await update.message.reply_text("Invalid price. Please enter a valid number.")
    return BIKE_MINPRICE


async def bike_size(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    try:
        size = float(update.message.text)
        if size > 0:
            context.user_data["bike_size"] = update.message.text
            await update.message.reply_text(
                "Great! I will send you bikes that match these criteria.\n\n"
                f"Category: {context.user_data['bike_category']}\n"
                f"Price range: {context.user_data['bike_minprice']}-{context.user_data['bike_maxprice']} €\n"
                f"Size: {context.user_data['bike_size']} cm"
            )

            alert = UserAlert(
                chat_id=update.effective_user.id,
                category=context.user_data["bike_category"],
                min_price=context.user_data["bike_minprice"],
                max_price=context.user_data["bike_maxprice"],
                size=context.user_data["bike_size"],
            )

            db_session = next(get_db())
            db_session.add(alert)
            db_session.commit()

        else:
            await update.message.reply_text(
                "Invalid size. Please enter a positive number."
            )
    except ValueError:
        await update.message.reply_text("Invalid size. Please enter a valid number.")

    return ConversationHandler.END


async def list_alerts(update: Update, context: ContextTypes.DEFAULT_TYPE):
    chat_id = str(update.effective_user.id)
    db_session = next(get_db())
    alerts = db_session.query(UserAlert).filter(UserAlert.chat_id == chat_id).all()

    if not alerts:
        await update.message.reply_text("You have no alerts set up.")
        return

    response = "Your alerts:\n"
    for alert in alerts:
        details = []
        if alert.category:
            details.append(f"Category: {alert.category}")
        if alert.min_price:
            details.append(f"Min price: {alert.min_price}€")
        if alert.max_price:
            details.append(f"Max price: {alert.max_price}€")
        if alert.size:
            flexibility = "±1" if alert.size_flexibility else "exact"
            details.append(f"Size: {alert.size} ({flexibility})")
        if alert.city:
            details.append(f"City: {alert.city}")
        if alert.region:
            details.append(f"Region: {alert.region}")

        response += (
            f"Alert #{alert.id}:\n"
            + "\n".join(f"• {detail}" for detail in details)
            + "\n\n"
        )

    await update.message.reply_text(response)


async def cancel(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    context.user_data.clear()
    await update.message.reply_text("Bye!", reply_markup=ReplyKeyboardRemove())
    return ConversationHandler.END


conversation_handler = ConversationHandler(
    entry_points=[
        CommandHandler("start", start),
        CommandHandler("alerts", list_alerts),
        # TODO: CommandHandler("remove", remove_alert),
        # TODO: CommandHandler("help", help)
    ],
    states={
        BIKE_CATEGORY: [MessageHandler(filters.TEXT & ~filters.COMMAND, bike_category)],
        BIKE_MAXPRICE: [MessageHandler(filters.TEXT & ~filters.COMMAND, bike_maxprice)],
        BIKE_MINPRICE: [MessageHandler(filters.TEXT & ~filters.COMMAND, bike_minprice)],
        BIKE_SIZE: [MessageHandler(filters.TEXT & ~filters.COMMAND, bike_size)],
    },
    fallbacks=[CommandHandler("cancel", cancel)],
)
