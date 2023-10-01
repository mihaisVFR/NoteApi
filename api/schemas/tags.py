from api import ma
from api.models.note import Tag


class TagSchema(ma.SQLAlchemySchema):
    class Meta:
        model = Tag

    id = ma.auto_field()
    name = ma.auto_field()
    user = ma.auto_field()


tag_schema = TagSchema()
tags_schema = TagSchema(many=True)
