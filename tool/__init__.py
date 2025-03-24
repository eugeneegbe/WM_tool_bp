from dotenv import dotenv_values, find_dotenv
from flask import Flask, request, session
from flask_cors import CORS
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.sql import text
from flask_login import LoginManager


config = dotenv_values('.env')
app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = config['SQLALCHEMY_DATABASE_URI']
db = SQLAlchemy(app)


app.secret_key = config["SECRET_KEY"]


login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'main.home'
login_manager.login_message = 'You Need to Login to Access This Page!'
login_manager.login_message_category = 'danger'


def get_locale():
    if request.args.get('lang'):
        session['lang'] = request.args.get('lang')
    return session.get('lang', 'en')


@app.before_request
def before_request():
    try:
        db.session.execute(text("SELECT 1;"))
        db.session.commit()
    except Exception as e:
        db.session.rollback()
    # Update session language
    get_locale()


CORS(app, resources={r"/tool*": {"origins": "*"}})


from tool.main.routes import main
from tool.users.routes import users

app.register_blueprint(main)
app.register_blueprint(users)

app.app_context().push()
