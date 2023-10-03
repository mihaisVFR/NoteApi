from api import app, request, multi_auth
from api.models.user import UserModel
from api.schemas.user import user_schema, users_schema, UserSchema, UserRequestSchema
from utility.helpers import get_object_or_404
from flask_apispec import doc, marshal_with, use_kwargs


@app.route("/users/<int:user_id>")
@doc(description='Get user by id', tags=['Users'], summary="Get user by id")
@marshal_with(UserSchema, code=200)
def get_user_by_id(user_id):
    user = get_object_or_404(UserModel, user_id)
    if user is None:
        return {"error": "User not found"}, 404
    return user, 200


@app.route("/users")
@doc(description='Get all users', tags=['Users'], summary="Get all users")
@marshal_with(UserSchema(many=True), code=200)
def get_users():
    users = UserModel.query.all()
    return users_schema.dump(users), 200


@app.route("/users", methods=["POST"])
@doc(description='Create user', tags=['Users'], summary="Create users")
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
@doc(description='Change user by id', tags=['Users'], summary="Change user by id")
@use_kwargs(UserRequestSchema, location="json")
@doc(security=[{"basicAuth": []}])
@doc(responses={"401": {"description": "Unauthorized"}})
@doc(responses={"404": {"description": "Not found"}})
@multi_auth.login_required(role="admin")
def edit_user(user_id, **kwargs):
    user = get_object_or_404(UserModel, user_id)
    for key, value in kwargs.items():
        setattr(user, key, value)
    user.save()
    return user, 200


@app.route("/users/<int:user_id>", methods=["DELETE"])
@doc(description='Delete user by id', tags=['Users'], summary="Delete user by id")
@multi_auth.login_required(role="admin")
def delete_user(user_id):
    """
    Админ удаляет Пользователя  ТОЛЬКО со своими заметками
    """
    user = get_object_or_404(UserModel, user_id)
    user.delete()
    return {"Success": f"User {user.username} deleted"}, 200
