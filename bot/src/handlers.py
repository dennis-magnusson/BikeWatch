from alert_handlers import (
    confirm_remove_alert,
    list_alerts,
    remove_alert,
    select_remove_alert,
)
from constants import (
    BIKE_CATEGORY,
    BIKE_MAXPRICE,
    BIKE_MINPRICE,
    BIKE_REGION,
    BIKE_SIZE,
    CONFIRM_REMOVE_ALERT,
    REMOVE_ALERT,
    SELECT_REMOVE_ALERT,
)
from conversation_handlers import (
    bike_category,
    bike_maxprice,
    bike_minprice,
    bike_region,
    bike_size,
    cancel,
    start,
)
from telegram import Update
from telegram.ext import (
    CommandHandler,
    ContextTypes,
    ConversationHandler,
    MessageHandler,
    filters,
)


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
        BIKE_REGION: [MessageHandler(filters.TEXT & ~filters.COMMAND, bike_region)],
        SELECT_REMOVE_ALERT: [
            MessageHandler(filters.TEXT & ~filters.COMMAND, select_remove_alert)
        ],
        CONFIRM_REMOVE_ALERT: [
            MessageHandler(filters.TEXT & ~filters.COMMAND, confirm_remove_alert)
        ],
        REMOVE_ALERT: [MessageHandler(filters.TEXT & ~filters.COMMAND, remove_alert)],
    },
    fallbacks=[CommandHandler("cancel", cancel)],
)
