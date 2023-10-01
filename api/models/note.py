from api import db
from api.models.user import UserModel
from api.models.tags import Tag, note_tag


class NoteModel(db.Model):
    __tablename__ = 'notes'
    id = db.Column(db.Integer, primary_key=True)
    author_id = db.Column(db.Integer, db.ForeignKey(UserModel.id))
    text = db.Column(db.String(255), unique=False, nullable=False)
    private = db.Column(db.Boolean(), default=True, nullable=False)
    tags = db.relationship("Tag", secondary=note_tag, backref=db.backref('notes', lazy='dynamic'))

    def save(self):
        db.session.add(self)
        db.session.commit()

    def delete(self):
        db.session.delete(self)
        db.session.commit()


