from telegram.ext import CommandHandler, ConversationHandler, MessageHandler, filters, ContextTypes
from telegram import Update
from conversation_handlers import (
    start,
    bike_category,
    bike_maxprice,
    bike_minprice,
    bike_size,
    cancel,
)
from alert_handlers import (
    list_alerts,
    select_remove_alert,
    confirm_remove_alert,
    remove_alert,
)

(
    BIKE_CATEGORY,
    BIKE_MAXPRICE,
    BIKE_MINPRICE,
    BIKE_SIZE,
    REMOVE_ALERT,
    CONFIRM_REMOVE_ALERT,
) = range(6)

async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    help_text = (
        "ℹ️ <b>BikeWatch Bot Help</b>\n\n"
        "/start - Set up notifications for bike listings.\n"
        "/alerts - List your current alerts.\n"
        "/remove - Remove an existing alert.\n"
        "/cancel - Cancel the current operation.\n"
        "/help - Show this help message."
    )
    await update.message.reply_text(help_text, parse_mode="HTML")

conversation_handler = ConversationHandler(
    entry_points=[
        CommandHandler("start", start),
        CommandHandler("alerts", list_alerts),
        CommandHandler("remove", select_remove_alert),
        CommandHandler("help", help_command),
    ],
    states={
        BIKE_CATEGORY: [MessageHandler(filters.TEXT & ~filters.COMMAND, bike_category)],
        BIKE_MAXPRICE: [MessageHandler(filters.TEXT & ~filters.COMMAND, bike_maxprice)],
        BIKE_MINPRICE: [MessageHandler(filters.TEXT & ~filters.COMMAND, bike_minprice)],
        BIKE_SIZE: [MessageHandler(filters.TEXT & ~filters.COMMAND, bike_size)],
        REMOVE_ALERT: [MessageHandler(filters.TEXT & ~filters.COMMAND, remove_alert)],
        CONFIRM_REMOVE_ALERT: [MessageHandler(filters.TEXT & ~filters.COMMAND, confirm_remove_alert)],
    },
    fallbacks=[CommandHandler("cancel", cancel)],
)
