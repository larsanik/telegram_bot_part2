import logging

from telegram.ext import Application as PTBApplication, ApplicationBuilder

from app.core.users.constants import RolesEnum
from app.core.users.repositories import UserRepository
from app.core.users.services import UserService
from app.handlers import HANDLERS
from app.infra.postgres.base import Base
from app.infra.postgres.db import Database
from settings.config import AppSettings
from ptbcontrib.roles import setup_roles, RolesHandler


class Application(PTBApplication):
    def __init__(self, app_settings: AppSettings, **kwargs):
        super().__init__(**kwargs)
        self._settings = app_settings
        self._roles = setup_roles(self)
        self.database = Database(app_settings.POSTGRES_DSN, declarative_base=Base())

        user_repository = UserRepository(database=self.database)
        self.user_service = UserService(repository=user_repository)

    def register_handlers(self):
        for handler in HANDLERS:
            if handler.role:
                if self._roles is None:
                    raise Exception('Roles are not set up')
                self.add_handler(RolesHandler(handler.handler, roles=self._roles[handler.role]))
            else:
                self.add_handler(handler.handler)

    async def setup_roles(self):
        for role in RolesEnum:
            if role not in self._roles:
                self._roles.add_role(role)

            for user_id in await self.user_service.get_user_ids_for_role(RolesEnum[role]):
                self._roles[role].add_member(user_id)

    @staticmethod
    async def application_startup(application: "Application") -> None:
        await application.database.create_tables()
        await application.setup_roles()
        application.register_handlers()

    @staticmethod
    async def application_shutdown(application: "Application") -> None:
        await application.database.shutdown()

    def run(self) -> None:
        self.run_polling()


def configure_logging():
    logging.basicConfig(
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
        level=logging.INFO
    )
    logging.getLogger('httpx').setLevel(logging.WARNING)


def create_app(app_settings: AppSettings) -> Application:
    application = (ApplicationBuilder().application_class(Application, kwargs={"app_settings": app_settings})
                   .post_init(Application.application_startup).  # type: ignore[arg-type]
                   post_shutdown(Application.application_shutdown)  # type: ignore[arg-type]
                   .token(app_settings.TELEGRAM_API_KEY.get_secret_value()).build())
    return application


if __name__ == '__main__':
    configure_logging()
    settings = AppSettings()
    app = create_app(settings)
    app.run()
