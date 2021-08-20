from . import db, login_manager
from flask_login import UserMixin


class User(UserMixin, db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    social_id = db.Column(db.String(64), nullable=False, unique=True)
    social_token = db.Column(db.String(64), nullable=False)

    def __repr__(self):
        return '<User id=%r; social_id=%r>' % (self.id, self.social_id)


@login_manager.user_loader
def load_user(_user_id):
    if _user_id == 'None':
        return
    return User.query.get(int(_user_id))


