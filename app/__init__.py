from flask import Flask ## import Flask
from flask_login import LoginManager
from mongoengine import connect
from werkzeug.security import generate_password_hash


app = Flask(__name__)
from app.models.ib_interface import connect_to_ib
print("Connecting to IB")
connect_to_ib()
print("Connected to IB")
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'

app.secret_key = 'your_secret_key' 
from app.controllers import *
from app.models.user import User

@login_manager.user_loader
def load_user(user_id):
    user_obj = User.objects(pk=user_id).first()
    return user_obj

def create_app():

    # MongoDB Configuration
    connect(db='mydatabase', 
        host='localhost', 
        port=27017,
        username = 'rootuser',
        password = 'rootpass')

    # Import and register Blueprints
    # from yourapplication.some_module import some_blueprint
    # app.register_blueprint(some_blueprint)

    # Call the function to create an admin user if it doesn't exist
    create_admin_user()

    return app

def create_admin_user():
    # Check if any admin exists
    admin_exists = User.objects(is_admin=True).first()
    if not admin_exists:
        # Create a new admin user
        admin_user = User(
            username='admin',
            password_hash=generate_password_hash('adminpass'),
            is_admin=True
        )
        admin_user.save()
        print('Admin user created with username "admin" and password "adminpass"')

create_app()

