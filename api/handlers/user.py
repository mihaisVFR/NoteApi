from api import app, request, multi_auth
from api.models.user import UserModel
from api.schemas.user import user_schema, users_schema, UserSchema, UserRequestSchema
from utility.helpers import get_object_or_404
from flask_apispec import doc, marshal_with, use_kwargs


@app.route("/users/<int:user_id>")
@doc(description='Api for one user', tags=['Users'], summary="Get user by id")
@marshal_with(UserSchema, code=200)
def get_user_by_id(user_id):
    user = get_object_or_404(UserModel, user_id)
    if user is None:
        return {"error": "User not found"}, 404
    return user, 200


@app.route("/users")
@doc(description='Api for all users', tags=['Users'], summary="Get all users")
@marshal_with(UserSchema(many=True), code=200)
def get_users():
    users = UserModel.query.all()
    return users_schema.dump(users), 200


@app.route("/users", methods=["POST"])
@doc(description='Api for one user', tags=['Users'], summary="Create user")
@marshal_with(UserSchema, code=201)
@use_kwargs(UserRequestSchema, location="json")
def create_user(**kwargs):
    # user_data = request.json
    # user = UserModel(**user_data)
    user = UserModel(**kwargs)
    if UserModel.query.filter_by(username=user.username).one_or_none():
        return {"error": "User already exist"}, 409
    user.save()
    return user, 201


@app.route("/users/<int:user_id>", methods=["PUT"])
@marshal_with(UserSchema, code=200)
#@use_kwargs(UserRequestSchema, location="json")
@multi_auth.login_required(role="admin")
def edit_user(user_id):
    user_data = request.json
    user = get_object_or_404(UserModel, user_id)
    user.username = user_data["username"]
    user.save()
    return user, 200


@app.route("/users/<int:user_id>", methods=["DELETE"])
@multi_auth.login_required(role="admin")
def delete_user(user_id):
    """
    Админ удаляет Пользователя  ТОЛЬКО со своими заметками
    """
    user = get_object_or_404(UserModel, user_id)
    user.delete()
    return {"Success": f"User {user.username} deleted"}, 200
