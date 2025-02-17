from telegram import ReplyKeyboardMarkup, Update
from telegram.ext import ContextTypes, ConversationHandler
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
        await update.message.reply_text("❌ You do not have permission to remove this alert.")
        return

    context.user_data["alert_id"] = alert_id

    await update.message.reply_text(
        f"⚠️ Are you sure you want to remove alert #{alert_id}?",
        reply_markup=ReplyKeyboardMarkup([["Yes", "No"]], one_time_keyboard=True),
    )

    return REMOVE_ALERT

async def remove_alert(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if update.message.text == "Yes":
        alert_id = context.user_data["alert_id"]
        db_session = next(get_db())
        db_session.query(UserAlert).filter(UserAlert.id == alert_id).delete()
        db_session.commit()
        await update.message.reply_text(f"✅ Alert #{alert_id} removed.")
    else:
        await update.message.reply_text("ℹ️ Alert removal cancelled.")

    return ConversationHandler.END
