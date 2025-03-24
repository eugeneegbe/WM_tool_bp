from datetime import datetime
from tool.serializer.serializer import Serializer
from tool import db, login_manager
from flask_login import UserMixin



@login_manager.user_loader
def load_user(user_id):
    return User.query.filter(User.id == user_id).first()


class User(db.Model,UserMixin, Serializer):
    id = db.Column(db.Integer, primary_key=True, index=True)
    username = db.Column(db.String(20), unique=True, nullable=False)
    pref_lang = db.Column(db.String(10), default='en')

    def serialize(self):
        return Serializer.serialize(self)

    def __repr__(self):
        # This is what is shown when object is printed
        return "User({}, {})".format(
                self.username,
                self.pref_lang)
