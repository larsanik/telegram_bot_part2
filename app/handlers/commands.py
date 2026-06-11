from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ContextTypes


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    if update.effective_chat and update.effective_user:
        await context.application.user_service.register_visitor(update.effective_user.id)  # type: ignore[attr-defined]
        keyboard = [
            [InlineKeyboardButton("Сделать заказ", callback_data=("order_create",))],
        ]
        markup = InlineKeyboardMarkup(keyboard)

        await context.bot.send_message(
            chat_id=update.effective_chat.id,
            text="Добро пожаловать! =o)",
            reply_markup=markup
        )


async def stop(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:  # todo убрать - это прикол
    if update.effective_chat and update.effective_user:
        await context.application.user_service.register_visitor(update.effective_user.id)  # type: ignore[attr-defined]
        await context.bot.send_message(
            chat_id=update.effective_chat.id,
            text="Добро отжаловать! =/)"
        )
