from api import app, multi_auth, request, db
from api.models.note import NoteModel
from api.models.tags import Tag, note_tag
from api.schemas.note import note_schema, notes_schema
from api.schemas.tags import tag_schema
from utility.helpers import get_object_or_404
from sqlalchemy import or_


@app.route("/notes/<int:note_id>", methods=["GET"])
@multi_auth.login_required
def get_note_by_id(note_id):
    user = multi_auth.current_user()
    note = get_object_or_404(NoteModel, note_id)
    if note.author_id == user.id or not note.private:
        return note_schema.dump(note), 200
    return {"Error": "This note can't be showed, because it owned other person"}, 403


@app.route("/tags", methods=["POST"])
@multi_auth.login_required
def create_tag():
    # DONE: Создание категорий
    user = multi_auth.current_user()
    tag_data = request.json
    tag = Tag(user=user.id, **tag_data)
    print(tag_data)
    tag.save()
    return tag_schema.dump(tag), 201


@app.route("/notes/search", methods=["GET"])
@multi_auth.login_required
def get_notes_by_tags():
    args = request.args
    tags = args.getlist("tag", type=str)
    user = multi_auth.current_user()
    notes = NoteModel.query.filter(
        or_(NoteModel.author_id == user.id, NoteModel.private == False))
    notes_result = []
    # Получаем список тэгов
    for tag in tags:

        tag_object = Tag.query.filter_by(name=tag).first()

        # Получим все зависимости
        dependencies = db.session.query(note_tag).filter_by(tag_id=tag_object.id).all()
        # Получим заметки по id тэгов используя полученные зависимости
        for dependence in dependencies:
            note = notes.filter_by(id=dependence.note_id).first()
            serialized_note = note_schema.dump(note)
            if serialized_note not in notes_result:
                notes_result.append(serialized_note)

    return notes_result, 200


@app.route("/notes/<int:note_id>/tags", methods=["PUT"])
@multi_auth.login_required
def add_tags_to_note(note_id):
    # DONE назначение категорий заметкам
    args = request.args
    tags = args.getlist("tags", type=int)
    user = multi_auth.current_user()
    note = get_object_or_404(NoteModel, note_id)
    if note.author_id == user.id or not note.private:
        for tag in tags:
            tag_object = get_object_or_404(Tag, tag)
            note.tags.append(tag_object)
            note.save()
        return note_schema.dump(note), 200
    return {"Error": "This note can't be showed, because it owned other person"}, 403


@app.route("/notes/<int:note_id>", methods=["PUT"])
@multi_auth.login_required
def edit_note(note_id):
    user = multi_auth.current_user()

    note = get_object_or_404(NoteModel, note_id)
    if note.author_id == user.id:
        note_data = request.json
        note.text = note_data["text"]
        note.private = note_data.get("private") or note.private
        note.save()
        return note_schema.dump(note), 200
    return {"Error": "This note can't be changed, because it owned other person"}, 403


@app.route("/notes/my_notes", methods=["GET"])
@multi_auth.login_required
def get_my_notes():
    user = multi_auth.current_user()
    notes = NoteModel.query.filter(NoteModel.author_id == user.id)
    return notes_schema.dump(notes), 200


@app.route("/notes", methods=["GET"])
@multi_auth.login_required
def get_notes():
    user = multi_auth.current_user()
    notes = NoteModel.query.filter(
        or_(NoteModel.author_id == user.id, NoteModel.private == False))

    return notes_schema.dump(notes), 200


@app.route("/notes/public", methods=["GET"])
@multi_auth.login_required
def public_notes():
    notes = NoteModel.query.filter(NoteModel.private == False)
    return notes_schema.dump(notes), 200


@app.route("/notes", methods=["POST"])
@multi_auth.login_required
def create_note():
    user = multi_auth.current_user()
    note_data = request.json
    note = NoteModel(author_id=user.id, **note_data)
    note.save()
    return note_schema.dump(note), 201


@app.route("/notes/<int:note_id>", methods=["DELETE"])
@multi_auth.login_required
def delete_note(note_id):
    user = multi_auth.current_user()
    note = get_object_or_404(NoteModel, note_id)
    if note.author_id == user.id:
        note.delete()
        return {"Success": f"Note with id={note_id} has deleted"}, 200
    return {"Error": "This note can't be deleted, because it owned other person"}, 403
