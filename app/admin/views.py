from app.core.users.models import User
from sqladmin import ModelView

class UserAdmin(ModelView):
    column_list = [User.id, User.is_waiter]
