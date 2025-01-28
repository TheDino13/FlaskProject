from flask import Flask, render_template, request, redirect, url_for, flash
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_login import LoginManager, UserMixin, login_user, logout_user, login_required, current_user
import logging

logging.basicConfig(level=logging.DEBUG)

app = Flask(__name__, template_folder='templates', static_folder='static')
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SECRET_KEY'] = 'your_secret_key'

db = SQLAlchemy(app)
bcrypt = Bcrypt(app)
login_manager = LoginManager(app)
login_manager.login_view = 'login'
# User Model
class User(db.Model, UserMixin):
   id = db.Column(db.Integer, primary_key=True)
   username = db.Column(db.String(80), unique=True, nullable=False)
   password = db.Column(db.String(120), nullable=False)

@login_manager.user_loader
def load_user(user_id):
   return db.session.get(User, int(user_id))

# Routes
@app.route('/')
@app.route('/login', methods=['GET', 'POST'])
def login():
   logging.debug("Entering login route")
   if request.method == 'POST':
       logging.debug("Handling POST request")
       username = request.form.get('username')
       password = request.form.get('password')
       
       user = db.session.execute(
           db.select(User).filter_by(username=username)
       ).scalar_one_or_none()
       
       if user and bcrypt.check_password_hash(user.password, password):
           logging.debug("User authenticated")
           login_user(user)
           flash('Logged in successfully!', 'success')
           return redirect(url_for('languages'))
       else:
           logging.debug("Authentication failed")
           flash('Login failed. Check username and password.', 'danger')
   logging.debug("Rendering login.html")
   return render_template('login.html')

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        print(f"Received registration: {username}")  
        existing_user = db.session.execute(
            db.select(User).filter_by(username=username)
        ).scalar_one_or_none()
        if len(password) < 8:
            flash('Password too short. It must be at least 8 characters long.', 'danger')
            return render_template('register.html')
        if existing_user:
            print(f"User {username} already exists") 
            flash('Username already exists', 'danger')
            return render_template('register.html')
        hashed_password = bcrypt.generate_password_hash(password).decode('utf-8')
        new_user = User(username=username, password=hashed_password)
        try:
            db.session.add(new_user)
            db.session.commit()
            print(f"User {username} successfully registered")
            
            flash('Registration successful', 'success')
            return redirect(url_for('login'))
        except Exception as e:
            db.session.rollback()
            print(f"Registration error: {e}")
            flash(f'Registration error: {str(e)}', 'danger')
    return render_template('register.html')

@app.route('/logout')
@login_required
def logout():
   logout_user()
   flash('You have been logged out.', 'info')
   return redirect(url_for('login'))

@app.route('/languages', methods=['POST'])
@login_required
def languages():
    username = request.form['username']
    password = request.form['password']
    # Add authentication logic here
    return render_template('languages.html')

@app.route('/levels/<language>')
@login_required
def levels(language):
    return render_template('levels.html', language=language)

@app.route('/resources/<language>/<level>')
@login_required
def resources(language, level):
    return render_template('resources.html', language=language, level=level)

# Utility route to view all users (for testing purposes)
@app.route('/users')
def get_users():
   users = db.session.execute(db.select(User)).scalars().all()
   return "<br>".join([f"{user.username}" for user in users])

if __name__ == '__main__':
   with app.app_context():
       db.create_all()
   app.run(debug=True)
