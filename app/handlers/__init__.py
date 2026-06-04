from telegram.ext import BaseHandler, CommandHandler
from app.handlers.commands import start, stop

HANDLERS: tuple[BaseHandler, ...] = (
    CommandHandler('start', start),
    CommandHandler('stop', stop), # todo убрать - это прикол
)
