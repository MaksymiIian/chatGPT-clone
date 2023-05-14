from flask import Flask, render_template, request, flash, redirect, url_for, session
import conversation
from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash
from flask_session import Session
from flask_mail import Mail, Message
from forms import LoginForm, RegisterForm, ContactForm

# Create a Flask instance
app = Flask(__name__)
app.config.from_pyfile('config.py')
# Initialize the session
Session(app)
# Initialize the database
db = SQLAlchemy(app)
mail = Mail(app)


# Create db model
class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    login = db.Column(db.String(100), nullable=False, unique=True)
    password = db.Column(db.String(100), nullable=False)
    responses_count = db.Column(db.Integer, nullable=False, default=0)

    def __repr__(self):
        return f'<User {self.login}>'

    def __init__(self, password, login):
        self.login = login
        self.password = password


@app.route('/', methods=['GET', 'POST'])
def index():
    if 'logged_in' in session and session['logged_in']:
        if request.method == 'POST':
            user = User.query.filter_by(login=session['username']).first()
            prompt = request.form['prompt']
            response = conversation.main(prompt)
            user.responses_count += 1
            db.session.commit()
            return render_template('index.html', prompt=prompt, response=response)
        else:
            return render_template('index.html')
    else:
        return redirect(url_for('login'))


@app.route('/login', methods=['GET', 'POST'])
def login():
    if 'logged_in' in session and session['logged_in']:
        return redirect(url_for('index'))
    form = LoginForm()
    if form.validate_on_submit():
        login = form.login.data
        password = form.password.data
        user = User.query.filter_by(login=login).first()
        if user and check_password_hash(user.password, password):
            session['logged_in'] = True
            session['username'] = login
            return redirect(url_for('index'))
        else:
            flash("Invalid credentials")
    return render_template('login.html', form=form)


@app.route('/register', methods=['GET', 'POST'])
def register():
    if 'logged_in' in session and session['logged_in']:
        return redirect(url_for('index'))
    form = RegisterForm()
    if form.validate_on_submit():
        hashed_password = generate_password_hash(form.password.data, method='sha256')
        login = form.login.data
        password = hashed_password
        user = User.query.filter_by(login=login).first()
        if user:
            flash("User already exists.")
            return redirect(url_for('register'))

        new_register = User(login=login, password=password)
        db.session.add(new_register)
        db.session.commit()
        flash("Registration was successful, please login")
        return redirect(url_for('login'))
    return render_template('register.html', form=form)


@app.route('/account')
def account():
    if 'logged_in' in session:
        user = User.query.filter_by(login=session['username']).first()
        return render_template('account.html', responses_count=user.responses_count)
    else:
        return redirect(url_for('login'))


@app.route('/contact', methods=['GET', 'POST'])
def contact():
    if 'logged_in' in session:
        form = ContactForm()
        if form.validate_on_submit():
            name = form.name.data
            email = form.email.data
            message = form.message.data
            msg = Message('New Message from Contact Form',
                          recipients=['#Your mail'])
            msg.body = f'Name: {name}\nEmail: {email}\nMessage: {message}'
            mail.send(msg)

            flash('Message sent successfully!')
            return redirect(url_for('index'))
        return render_template('contact.html', form=form)
    else:
        return redirect(url_for('login'))


@app.route('/logout')
def logout():
    session.pop('logged_in', None)
    flash('You have been logged out.')
    return redirect(url_for('login'))


if __name__ == "__main__":
    app.run(debug=True)
