from config import Config
from flask import Flask, request, abort
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_marshmallow import Marshmallow
from flask_httpauth import HTTPBasicAuth, HTTPTokenAuth, MultiAuth
from flask_apispec.extension import FlaskApiSpec

app = Flask(__name__)


app.config.from_object(Config)
app.config.update(Config.API_SPEC)

# ctx = app.app_context()
# ctx.push()
db = SQLAlchemy(app)
migrate = Migrate(app, db)
ma = Marshmallow(app)
basic_auth = HTTPBasicAuth()
token_auth = HTTPTokenAuth('Bearer')
multi_auth = MultiAuth(basic_auth, token_auth)
docs = FlaskApiSpec(app)


@basic_auth.verify_password
def verify_password(username, password):
    from api.models.user import UserModel
    user = UserModel.query.filter_by(username=username).first()
    if not user or not user.verify_password(password):
        return False
    return user


@token_auth.verify_token
def verify_token(token):
    from api.models.user import UserModel
    user = UserModel.verify_auth_token(token)
    print(f"{user=}")
    return user


@basic_auth.get_user_roles
def get_user_roles(user):
    return user.get_roles()


@token_auth.get_user_roles
def get_user_roles(user):
    return user.get_roles()