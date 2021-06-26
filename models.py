"""Models for flask-feedback"""

from flask_sqlalchemy import SQLAlchemy 
from flask_bcrypt import Bcrypt

bcrypt = Bcrypt()
db = SQLAlchemy()

def connect_db(app):
    """Connect to database"""

    db.app = app
    db.init_app(app)

class User(db.model):
    """User"""

    __tablename__ = "users"

    username = db.Column(db.string(20), nullable=False, unique=True, primary_key=True)
    password = db.Column(db.Text, nullable=False)
    email = db.Column(db.String(50), nullable=False)
    first_name = db.Column(db.String(30), nullable=False)
    last_name = db.Column(db.String(30), nullable=False)

    feedback = db.relationship("Feedback", backref="user", cascade="all,delete")

    @classmethod
    def register(cls, username, password, first_name, last_name, email):
        """Register a new User"""

        hashed = bcrypt.generate_password_hash(password)
        hashedu8 = hashed.decode("utf8")
        user = cls(username=username, password=hashedu8, first_name=first_name, last_name=last_name, email=email)
        db.session.add(user)
        return user

    @classmethod
    def autheticate(cls, username, password):
        """Check if the username and password are correct"""

        user = User.query.filter_by(username=username).first()
        if user and bcrypt.check_password_hash(user.password, password):
            return user
        else:
            return False

class Feedback(db.model):
    """Feedback"""

    __tablename__ = "feedback"

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable = False)
    description = db.Column(db.Text, nullable=False)
    username = db.Column(db.String(20), db.ForeignKey('users.username'), nullable=False)