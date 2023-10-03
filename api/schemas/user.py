from api import ma
from api.models.user import UserModel


#       schema        flask-restful
# object ------>  dict ----------> json


# Сериализация ответа(response)
class UserSchema(ma.SQLAlchemySchema):
    class Meta:
        model = UserModel
        fields = ('id', 'username', "role")


class UserRequestSchema(ma.SQLAlchemySchema):
    class Meta:
        model =UserModel

    username = ma.Str(required=True)
    password = ma.Str(required=True)
    role = ma.Str()


user_schema = UserSchema()
users_schema = UserSchema(many=True)

