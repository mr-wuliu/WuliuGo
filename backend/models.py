from backend.extension import SQLAlchemy
from flask_migrate import Migrate
from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash

db : SQLAlchemy = SQLAlchemy()
migrate = Migrate()

class User(db.Model, UserMixin):
    """用户表""" 
    __tablename__ = "users"
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(50), unique=True, nullable=False)
    email = db.Column(db.String(50), unique=True, nullable=True)
    _password = db.Column(db.String(1024), nullable=True)

    @property
    def password(self):
        return self._password
    @password.setter
    def password(self, password):
        self._password = generate_password_hash(password)
    def verify_password(self, password):
        return check_password_hash(self._password, password) # type: ignore
    def __repr__(self):
        return f"<User {self.username} email:{self.email}"
