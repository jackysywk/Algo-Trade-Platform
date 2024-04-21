from flask_login import UserMixin
from mongoengine import Document, StringField, ReferenceField, CASCADE, BooleanField
from werkzeug.security import generate_password_hash, check_password_hash

class User(UserMixin, Document):
    meta = {'collection': 'users'}
    username = StringField(required=True, unique=True)
    password_hash = StringField(required=True)
    is_admin = BooleanField()

    def verify_password(self, password):
        return check_password_hash(self.password_hash, password)
    
    def get_user(username):
        user = User.objects(username=username).first()
        return user