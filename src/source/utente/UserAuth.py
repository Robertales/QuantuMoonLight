from flask_login import UserMixin
from sqlalchemy.util import text_type

from src import login_manager


@login_manager.user_loader
def load_user(user_email):
    from src.source.model.models import User

    return User.query.get(str(user_email))


class UserAuth(UserMixin):
    def get_id(self):
        try:
            return text_type(self.email)
        except AttributeError:
            raise NotImplementedError("No `id` attribute - override `get_id`")
