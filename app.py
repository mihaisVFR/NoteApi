from api import app, docs, db
from config import Config
from api.handlers import auth, note, user

# CRUD

# Create --> POST
# Read --> GET
# Update --> PUT
# Delete --> DELETE

docs.register(user.get_user_by_id)
docs.register(user.get_users)
docs.register(user.create_user)
docs.register(user.edit_user)
docs.register(user.delete_user)

docs.register(note.get_notes)
docs.register(note.get_note_by_id)
docs.register(note.get_note_by_user_id)
docs.register(note.edit_note)
docs.register(note.get_my_notes)
docs.register(note.delete_note)
docs.register(note.create_note)
docs.register(note.public_notes)
docs.register(note.add_tag_to_note)
docs.register(note.notes_filter_by_args)
docs.register(note.get_notes_by_tags)
docs.register(note.create_tag)

if __name__ == '__main__':
    app.run(debug=Config.DEBUG, port=Config.PORT)
