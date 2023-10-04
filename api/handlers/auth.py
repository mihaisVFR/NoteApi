from api import app, multi_auth, basic_auth


@app.route('/auth/token')
@multi_auth.login_required
def get_auth_token():
    user = multi_auth.current_user()
    token = user.generate_auth_token()
    return {'token': token}
