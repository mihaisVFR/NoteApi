from api import app, multi_auth, request
from api.models.note import NoteModel
from api.models.tags import Tag
from api.schemas.note import NoteSchema, NoteRequestSchema
from api.schemas.tags import TagRequestSchema, TagSchema
from utility.helpers import get_object_or_404
from sqlalchemy import or_, and_
from flask_apispec import doc, marshal_with, use_kwargs


@app.route("/tags", methods=["POST"])
@doc(description='Create tag', tags=['Notes'], summary="Create tag")
@marshal_with(TagSchema, code=201)
@use_kwargs(TagRequestSchema, location="json")
@multi_auth.login_required
def create_tag(**kwargs):
    # DONE: Создание категорий
    user = multi_auth.current_user()
    tag = Tag(user=user.id, **kwargs)
    tag.save()
    return tag, 201


@app.route("/notes/search", methods=["GET"])
@doc(description='Get notes by tags can be public or own', tags=['Notes'], summary='Get notes by tags')
@marshal_with(NoteSchema(many=True), code=200)
@multi_auth.login_required
def get_notes_by_tags():
    """Возвращает заметки по тэгу"""
    args = request.args
    tags = args.getlist("tag", type=str)
    user = multi_auth.current_user()
    notes = NoteModel.query.filter(
        or_(NoteModel.author_id == user.id, NoteModel.private == False))
    notes_result = []
    for tag in tags:
        filtered_notes = notes.filter(NoteModel.tags.any(name=tag)).all()
        notes_result += filtered_notes
    return notes_result, 200


@app.route("/notes/filter", methods=["GET"])
@doc(description='Get notes by arguments from query params.'
                 ' \nPossible tags: 1.tag 2.username.'
                 '\nExample: /notes/filter?username=admin',
     tags=['Notes'], summary="Get notes by arguments from query params.")
@doc(responses={"404": {"Error": "Search request not found"}})
@marshal_with(NoteSchema(many=True), code=200)
@multi_auth.login_required
def notes_filter_by_args():
    """Возвращает результат поиска по тэгу для авторизованного пользователя
     и публичные цытаты для запрошенного пользователя"""
    args = request.args
    arg_teg = args.get("tag", type=str)
    arg_user = args.get("username", type=str)
    user = multi_auth.current_user()
    if arg_teg:
        notes = NoteModel.query.filter(
            and_(NoteModel.author_id == user.id, NoteModel.tags.any(name=arg_teg)))
        return notes
    elif arg_user:

        notes = NoteModel.query.filter(
            and_(NoteModel.author.has(username=arg_user), NoteModel.private == False))
        return notes
    else:
        return {"Error": "Search request not found"}, 404


@app.route("/notes/<int:note_id>/tag", methods=["PUT"])
@marshal_with(NoteSchema, code=200)
@doc(description='Add tags to note', tags=['Notes'], summary="Add tags to note")
@doc(security=[{"basicAuth": []}])
@doc(responses={"403": {"Error": "This note can't be changed, because it owned other person"}})
@multi_auth.login_required
def add_tag_to_note(note_id):
    # DONE назначение категорий заметкам
    args = request.args
    tags = args.getlist("tag", type=int)
    user = multi_auth.current_user()
    note = get_object_or_404(NoteModel, note_id)
    if note.author_id == user.id or not note.private:
        for tag in tags:
            tag_object = get_object_or_404(Tag, tag)
            note.tags.append(tag_object)
            note.save()
        return note, 200
    return {"Error": "This note can't be showed, because it owned other person"}, 403


@app.route("/notes/<int:note_id>", methods=["GET"])
@doc(description='Get note by id', tags=['Notes'], summary="Get note by id")
@marshal_with(NoteSchema, code=200)
@multi_auth.login_required
def get_note_by_id(note_id):
    user = multi_auth.current_user()
    note = get_object_or_404(NoteModel, note_id)
    if note.author_id == user.id or not note.private:
        return note, 200
    return {"Error": "This note can't be showed, because it owned other person"}, 403


@app.route("/users/<user_id>/notes", methods=["GET"])
@doc(description='Get note by user id', tags=['Notes'], summary="Get note by user id")
@marshal_with(NoteSchema(many=True), code=200)
def get_note_by_user_id(user_id):
    """Обработчик для всех заметок пользователя, Авторизация не требуется"""
    notes = NoteModel.query.filter(NoteModel.author_id == user_id).all()
    if notes:
        return notes, 200
    return {"Error": "This note can't be showed, because it owned other person"}, 403


@app.route("/notes/<int:note_id>", methods=["PUT"])
@marshal_with(NoteSchema, code=200)
@doc(description='Change note by id', tags=['Notes'], summary="Change note by id")
@use_kwargs(NoteRequestSchema, location="json")
@doc(security=[{"basicAuth": []}])
@doc(responses={"403": {"Error": "This note can't be changed, because it owned other person"}})
@multi_auth.login_required
def edit_note(note_id, **kwargs):
    user = multi_auth.current_user()
    note = get_object_or_404(NoteModel, note_id)
    if note.author_id == user.id:
        for key, value in kwargs.items():
            setattr(note, key, value)
        note.save()
        return note, 200
    return {"Error": "This note can't be changed, because it owned other person"}, 403


@app.route("/notes/my_notes", methods=["GET"])
@doc(description='Get all notes of current user', tags=['Notes'], summary="Get all notes of current user")
@marshal_with(NoteSchema(many=True), code=200)
@multi_auth.login_required
def get_my_notes():
    user = multi_auth.current_user()
    notes = NoteModel.query.filter(NoteModel.author_id == user.id)
    return notes, 200


@app.route("/notes", methods=["GET"])
@doc(description='Get all notes', tags=['Notes'], summary="Get all notes")
@marshal_with(NoteSchema(many=True), code=200)
@multi_auth.login_required
def get_notes():
    user = multi_auth.current_user()
    notes = NoteModel.query.filter(
        or_(NoteModel.author_id == user.id, NoteModel.private == False))
    return notes, 200


@app.route("/notes/public", methods=["GET"])
@doc(description='Get all public notes', tags=['Notes'], summary="Get all public notes")
@marshal_with(NoteSchema(many=True), code=200)
@multi_auth.login_required
def public_notes():
    notes = NoteModel.query.filter_by(private=False).all()
    return notes, 200


@app.route("/notes", methods=["POST"])
@doc(description='Create note', tags=['Notes'], summary="Create notes")
@marshal_with(NoteSchema, code=201)
@use_kwargs(NoteRequestSchema, location="json")
@multi_auth.login_required
def create_note(**kwargs):
    user = multi_auth.current_user()
    note = NoteModel(author_id=user.id, **kwargs)
    note.save()
    return note, 201


@app.route("/notes/<int:note_id>", methods=["DELETE"])
@doc(description='Delete note by id', tags=['Notes'], summary="Delete note by id")
@multi_auth.login_required
def delete_note(note_id):
    user = multi_auth.current_user()
    note = get_object_or_404(NoteModel, note_id)
    if note.author_id == user.id:
        note.delete()
        return {"Success": f"Note with id={note_id} has deleted"}, 200
    return {"Error": "This note can't be deleted, because it owned other person"}, 403
