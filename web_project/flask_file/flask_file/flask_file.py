from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)
@app.route('/')
def login():
    print("Rendering login.html")
    return render_template('login.html')

class LoginData(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), nullable=False)  
    password = db.Column(db.String(120), nullable=False)  

    def __repr__(self):
        return f"<LoginData {self.name}>"


@app.route('/languages', methods=['POST'])
def languages():
    username = request.form.get('username')
    password = request.form.get('password')

    if not username or not password:
        print("Username or password is missing")
        return "Username and password are required!", 400

    try:
        new_login = LoginData(name=username, password=password)
        db.session.add(new_login)
        db.session.commit()
        print(f"User {username} added successfully!")
    except Exception as e:
        db.session.rollback()
        print(f"Error while adding user: {e}")
        return "Error while adding user!", 500

    return render_template('languages.html')



@app.route('/levels/<language>')
def levels(language):
    return render_template('levels.html', language=language)


@app.route('/resources/<language>/<level>')
def resources(language, level):
    return render_template('resources.html', language=language, level=level)


@app.route('/users')
def get_users():
    users = LoginData.query.all()
    return "<br>".join([f"{user.name}: {user.password}" for user in users])


if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True)

