from flask import Flask, render_template, request, redirect, url_for, session, flash
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from werkzeug.security import generate_password_hash, check_password_hash

app = Flask(__name__)
app.secret_key = 'oiahre3ijrsdmvlskhfskdncvpaokfanfaslmclkanfjsdnflskdjvisl'

# PostgreSQL database configuration
username = 'Aman_Mittal'
password = 'Password@123'
host = 'localhost'  
dbname = 'registered_users'
app.config['SQLALCHEMY_DATABASE_URI'] = f'postgresql://{username}:{password}@{host}/{dbname}'

db = SQLAlchemy(app)
migrate = Migrate(app, db)


class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(50), unique=True, nullable=False)
    password_hash = db.Column(db.String(80))

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)


@app.route('/register', methods=['POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        user = User(username=username)
        user.set_password(password)
        db.session.add(user)
        db.session.commit()

        flash('Registered successfully! Please login.')
        return redirect(url_for('login'))

    return render_template('register.html')

@app.route('/login', methods=['POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        user = User.query.filter_by(username=username).first()
        if user and user.check_password(password):
            session['loggedin'] = True
            session['username'] = username
            return redirect(url_for('index'))

        flash('Invalid username or password')
    return render_template('login.html')

form_data = {}

@app.route('/detect', methods=['POST'])
def detect():
    global form_data
    form_data['blockchain'] = request.form['blockchain']
    form_data['num_transactions'] = int(request.form['num_transactions'])
    form_data['email'] = request.form['email']

    # Call a function from data_gathering.py or handle data processing here
    # For example: data_gathering.process_data(form_data)

    return 'Anomaly Detection Started'

