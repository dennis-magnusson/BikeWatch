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

from common.database import get_db
from common.models.alert import UserAlert

(
    BIKE_CATEGORY,
    BIKE_MAXPRICE,
    BIKE_MINPRICE,
    BIKE_SIZE,
    REMOVE_ALERT,
    CONFIRM_REMOVE_ALERT,
) = range(6)


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
    # remove emojis from message.text and lowercase it
    category_chosen = (
        update.message.text.encode("ascii", "ignore").decode("ascii").strip().lower()
    )

    context.user_data["bike_category"] = category_chosen
    await update.message.reply_text(
        "💶 What maximum price (€)?",
    )

    return BIKE_MAXPRICE


async def bike_maxprice(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    try:
        max_price = int(update.message.text)
        if max_price > 0:
            context.user_data["bike_maxprice"] = max_price
            await update.message.reply_text(
                "💶 What minimum price (€)?",
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
        if min_price >= 0 and min_price < context.user_data["bike_maxprice"] and min_price != "inf":
            context.user_data["bike_minprice"] = min_price
            await update.message.reply_text(
                "📏 What size? \n\nPlease provide the tube length in centimeters or 'any' if you don't want to filter by size.",
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
    text = update.message.text.lower()
    try:
        # Check for 'any' first to avoid ValueError on float conversion
        if text == "any":
            size = None
            gave_number = False
        else:
            size = float(text)
            if size <= 0:
                await update.message.reply_text(
                    "❌ Invalid size. Please enter a positive number."
                )
                return BIKE_SIZE
            gave_number = True

        context.user_data["bike_size"] = text
        await update.message.reply_text(
            "✅ I will send you bikes that match these criteria.\n\n"
            f"🚴 {context.user_data['bike_category'].capitalize()}\n"
            f"💶 {context.user_data['bike_minprice']}-{context.user_data['bike_maxprice']} €\n"
            f"📏 {(context.user_data['bike_size'].capitalize() if not gave_number else context.user['bike_size'])} {('cm' if gave_number else '')}"
        )

        alert = UserAlert(
            chat_id=update.effective_user.id,
            category=context.user_data["bike_category"] if context.user_data["bike_category"] != "any" else None,
            min_price=context.user_data["bike_minprice"],
            max_price=context.user_data["bike_maxprice"],
            size=size,
        )

        db_session = next(get_db())
        db_session.add(alert)
        db_session.commit()

        return ConversationHandler.END

    except ValueError:
        await update.message.reply_text("❌ Invalid size. Please enter a valid number or 'any'.")
        return BIKE_SIZE


async def list_alerts(update: Update, context: ContextTypes.DEFAULT_TYPE):
    chat_id = str(update.effective_user.id)
    db_session = next(get_db())
    alerts = db_session.query(UserAlert).filter(UserAlert.chat_id == chat_id).all()

    if not alerts:
        await update.message.reply_text("ℹ️ You have no alerts set up.")
        return

    response = ""
    for alert in alerts:
        details = []
        if alert.category:
            details.append(f"🚴 {alert.category.capitalize()}")
        if alert.min_price or alert.max_price:
            details.append(f"💶 {alert.min_price}-{alert.max_price}€")
        if alert.size:
            flexibility = "±1" if alert.size_flexibility else "exact"
            details.append(f"📏 {alert.size} cm ({flexibility})")
        if alert.city:
            details.append(f"🏙️ {alert.city}")
        if alert.region:
            details.append(f"📍 {alert.region}")

        response += (
            f"<b>{alert.id}</b>:\n"
            + "\n".join(f"{detail}" for detail in details)
            + "\n\n"
        )

    await update.message.reply_text(response, parse_mode="HTML")


async def select_remove_alert(update: Update, context: ContextTypes.DEFAULT_TYPE):
    chat_id = str(update.effective_user.id)
    db_session = next(get_db())
    alerts = db_session.query(UserAlert).filter(UserAlert.chat_id == chat_id).all()

    if not alerts:
        await update.message.reply_text("You have no alerts set up.")
        return

    alert_ids = [alert.id for alert in alerts]
    await update.message.reply_text(
        "Which alert would you like to remove?",
        reply_markup=ReplyKeyboardMarkup(
            [[str(alert_id) for alert_id in alert_ids]], one_time_keyboard=True
        ),
    )

    return CONFIRM_REMOVE_ALERT


async def confirm_remove_alert(update: Update, context: ContextTypes.DEFAULT_TYPE):
    alert_id = int(update.message.text)
    chat_id = str(update.effective_user.id)
    db_session = next(get_db())
    alert = db_session.query(UserAlert).filter(UserAlert.id == alert_id).first()

    if not alert:
        await update.message.reply_text("❌ Invalid alert ID.")
        return

    if alert.chat_id != chat_id:
        await update.message.reply_text(
            "❌ You do not have permission to remove this alert."
        )
        return

    context.user_data["alert_id"] = alert_id  # Store alert_id in user_data

    await update.message.reply_text(
        f"⚠️ Are you sure you want to remove alert #{alert_id}?",
        reply_markup=ReplyKeyboardMarkup([["Yes", "No"]], one_time_keyboard=True),
    )

    return REMOVE_ALERT  # Correct state transition


async def remove_alert(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if update.message.text == "Yes":
        alert_id = context.user_data["alert_id"]  # Retrieve alert_id from user_data
        db_session = next(get_db())
        db_session.query(UserAlert).filter(UserAlert.id == alert_id).delete()
        db_session.commit()
        await update.message.reply_text(f"✅ Alert #{alert_id} removed.")
    else:
        await update.message.reply_text("ℹ️ Alert removal cancelled.")

    return ConversationHandler.END


async def cancel(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    context.user_data.clear()
    await update.message.reply_text("Bye!", reply_markup=ReplyKeyboardRemove())
    return ConversationHandler.END


conversation_handler = ConversationHandler(
    entry_points=[
        CommandHandler("start", start),
        CommandHandler("alerts", list_alerts),
        CommandHandler("remove", select_remove_alert),
        # TODO: CommandHandler("help", help)
    ],
    states={
        BIKE_CATEGORY: [MessageHandler(filters.TEXT & ~filters.COMMAND, bike_category)],
        BIKE_MAXPRICE: [MessageHandler(filters.TEXT & ~filters.COMMAND, bike_maxprice)],
        BIKE_MINPRICE: [MessageHandler(filters.TEXT & ~filters.COMMAND, bike_minprice)],
        BIKE_SIZE: [MessageHandler(filters.TEXT & ~filters.COMMAND, bike_size)],
        REMOVE_ALERT: [MessageHandler(filters.TEXT & ~filters.COMMAND, remove_alert)],  # Correct filter
        CONFIRM_REMOVE_ALERT: [MessageHandler(filters.TEXT & ~filters.COMMAND, confirm_remove_alert)],  # Correct filter
    },
    fallbacks=[CommandHandler("cancel", cancel)],
)
