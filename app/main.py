import logging

from telegram.ext import Application as PTBApplication, ApplicationBuilder

from settings.config import AppSettings

class Application(PTBApplication):
    def __init__(self, app_settings: AppSettings, **kwargs):
        super().__init__(**kwargs)
        self.app_settings = app_settings


    def run(self) -> None:
        self.run_polling()


def configure_logging():
    logging.basicConfig(
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
        level=logging.INFO
    )
    logging.getLogger('httpx').setLevel(logging.WARNING)
