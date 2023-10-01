from api import db
from api.models.user import UserModel


class NoteModel(db.Model):
    # __name = "Author"
    id = db.Column(db.Integer, primary_key=True)
    author_id = db.Column(db.Integer, db.ForeignKey(UserModel.id))
    text = db.Column(db.String(255), unique=False, nullable=False)
    private = db.Column(db.Boolean(), default=True, nullable=False)
    category = db.Column(db.String(255), unique=False, nullable=False,
                         server_default="No_tags", default="No_tags")

    def save(self):
        db.session.add(self)
        db.session.commit()

    def delete(self):
        db.session.delete(self)
        db.session.commit()
