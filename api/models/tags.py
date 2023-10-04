from api import db
from api.models.user import UserModel

note_tag = db.Table('note_tag',
                    db.Column('note_id', db.Integer, db.ForeignKey("notes.id")),
                    db.Column('tag_id', db.Integer, db.ForeignKey("tag.id")),
                    )


class Tag(db.Model):
    __tablename__ = 'tag'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), unique=True)
    user = db.Column(db.Integer)

    def save(self):
        db.session.add(self)
        db.session.commit()

    def delete(self):
        db.session.delete(self)
        db.session.commit()

    def __repr__(self):
        return f'<Tag "{self.name}">'
