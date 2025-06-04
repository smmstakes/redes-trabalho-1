from flask_wtf.csrf import CSRFProtect

# Other imports
from markdown import markdown

# Importing flask dependencies
from flask import (
    session,
    render_template,
    request,
    redirect,
    url_for,
    after_this_request,
)

# Importing classes and
from models import DB, User, Note, AssistantBot, app


@app.after_this_request
def add_header(response):
    response.headers['X-Server-Software'] = 'Flask/2.3.2'
    return response


# Onboarding
@app.route('/')
def index():
    # Redirecting to login page
    return redirect(url_for('login'))


# Sign-up
@app.route('/sign_up', methods=['GET', 'POST'])
def sign_up():
    if request.method == 'POST':
        # Getting data from page
        name: str = request.form['name']
        password: str = request.form['password']

        # Checking whether username is already used
        if User.verify_credentials_sign_up(name=name):
            # Creating user instance
            user = User(name=name, password=password)

            # Adding user to db
            user.db.add_data(user)
            user.db.commit_session()

            # Adding name to session
            session['name'] = request.form['name']

            # Redirecting to private page
            return redirect(url_for('notes'))

        # Rendering home page with invalid credentials
        return render_template(
            'home.html',
            invalid_credentials=True,
            sign_up=True,
        )

    # Rendering home page if user is not logged in else returning to private page
    return (
        redirect(url_for('notes'))
        if 'name' in session
        else render_template('home.html', sign_up=True)
    )


# Log-in
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        # Getting data from page
        name: str = request.form['name']
        password: str = request.form['password']

        # Validating login
        if User.verify_credentials_login(name=name, password=password):

            # Adding name to session
            session['name'] = request.form['name']

            # Redirecting to private page
            return redirect(url_for('notes'))

        # Rendering home page with invalid credentials
        return render_template('home.html', invalid_credentials=True)

    # Rendering home page if user is not logged in else returning to private page
    return (
        redirect(url_for('notes'))
        if 'name' in session
        else render_template('home.html')
    )


# Log-out
@app.route('/logout')
def logout():
    # Checking whether the user is logged in
    if 'name' in session:
        # Removing 'name' from session
        session.pop('name', None)

        # Redirecting to /login
    return redirect(url_for('login'))


# Notes page
@app.route('/notes', methods=['POST', 'GET'])
def notes():
    # Checking if user is logged in
    if 'name' in session:
        # Getting user's data
        user = User.get_user(session['name'])
        notes = Note.query.filter_by(author_id=user.id).all()
        notes.reverse()

        for note in notes:
            note.assistant_bot_notes_html = markdown(note.assistant_bot_notes)

        # Rendering template with user's notes and id
        return render_template('notes.html', notes=notes)

    # Rendering notes page with not login set to true
    return render_template('notes.html', not_login=True)


# New note page
@app.route('/new', methods=['POST', 'GET'])
def new_note():
    # Checking whether the user is logged in
    if 'name' in session:
        if request.method == 'POST':
            # Getting user
            user = User.get_user(session['name'])

            # Creating AssistantBot instance
            assistant_bot = AssistantBot()

            # Creating note instance
            note = Note(
                name=request.form['name'],
                author_id=user.id,
                notes=request.form['notes'],
                assistant_bot=assistant_bot,
            )

            # Creating prompt
            note.create_prompt()

            # Adding note to db
            note.db.add_data(note)
            note.db.commit_session()

            # Redirecting back to notes page
            return redirect(url_for('notes'))

        # Rendering form for creating new note
        return render_template('form.html')

    # Rendering notes page with not login set to true
    return render_template('notes.html', not_login=True)


# Edit note page
@app.route('/edit/<id>', methods=['POST', 'GET'])
def edit_note(id):
    # Checking whether user is logged in
    if 'name' in session:
        # Getting note by id
        note = Note.query.get(id)

        if request.method == 'POST':
            # Renaming note
            note.name = request.form['name']

            # Committing changes to db
            db = DB()
            db.commit_session()

            # Redirecting back to notes page
            return redirect(url_for('notes'))

        # Rendering form for editing note
        return render_template('form.html', edit=True, note=note)

    # Rendering notes page with not login set to true
    return render_template('notes.html', not_login=True)


# Delete note
@app.route('/delete/<id>')
def delete(id):
    # Checking whether user is logged in
    if 'name' in session:
        # Getting note by id
        note = Note.query.get(id)

        # Deleting note from db
        db = DB()
        db.delete_data(note)
        db.commit_session()

        # Redirecting back to notes page
        return redirect(url_for('notes'))

    # Rendering notes page with not login set to true
    return render_template('notes.html', not_login=True)


if __name__ == '__main__':
    db = DB()
    db.create_all()

    app.run(
        host='0.0.0.0',
        port=5000,
        debug=True,
    )
