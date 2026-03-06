import os
from flask import Flask, render_template, request, redirect, url_for, send_from_directory
from flask_sqlalchemy import SQLAlchemy
from werkzeug.utils import secure_filename

# Flask app
app = Flask(__name__)

# Configurations
UPLOAD_FOLDER = 'uploads'
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///studyhub.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Database
db = SQLAlchemy(app)

# ------------------ MODELS ------------------

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    role = db.Column(db.String(20), nullable=False)
    name = db.Column(db.String(100), nullable=False)
    branch = db.Column(db.String(50), nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(60), nullable=False)


class Material(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    subject = db.Column(db.String(100), nullable=False)
    filename = db.Column(db.String(100), nullable=False)
    semester = db.Column(db.String(20))

# Create tables
with app.app_context():
    db.create_all()

# ------------------ ROUTES ------------------

@app.route('/')
def home():
    return render_template('login.html')


@app.route('/login', methods=['POST'])
def login():
    user_email = request.form.get('email')
    user_password = request.form.get('password')

    user = User.query.filter_by(email=user_email, password=user_password).first()

    if user:
        return redirect(url_for('dashboard'))
    else:
        return "Invalid Credentials! <a href='/'>Go Back</a>"


@app.route('/register', methods=['POST'])
def register():
    new_user = User(
        role=request.form.get('userRole'),
        name=request.form.get('name'),
        branch=request.form.get('branch'),
        email=request.form.get('reg_email'),
        password=request.form.get('reg_password')
    )

    db.session.add(new_user)
    db.session.commit()

    return redirect(url_for('home'))


@app.route('/dashboard')
def dashboard():
    all_materials = Material.query.all()
    return render_template('index.html', materials=all_materials)


@app.route('/upload')
def upload():
    return render_template('upload.html')


@app.route('/subject')
def subjects():
    return render_template('subject.html')


@app.route('/notes')
def saved_notes():
    return render_template('notes.html')


# Upload file
@app.route('/upload_file', methods=['POST'])
def upload_file():
    file = request.files['file']
    title = request.form.get('title')
    subject = request.form.get('subject')
    semester = request.form.get('semester')

    if file:
        filename = secure_filename(file.filename)

        file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))

        new_material = Material(
            title=title,
            subject=subject,
            filename=filename,
            semester=semester
        )

        db.session.add(new_material)
        db.session.commit()

        return redirect(url_for('dashboard'))

    return "File upload failed"


# Download file
@app.route('/download/<filename>')
def download_file(filename):
    return send_from_directory(app.config['UPLOAD_FOLDER'], filename)


if __name__ == '__main__':
    app.run(debug=True)