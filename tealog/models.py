"""Database models."""
from flask_login import UserMixin
from werkzeug.security import check_password_hash, generate_password_hash

from . import db


class User(UserMixin, db.Model):
    """User account model."""

    __tablename__ = "flasklogin-users"
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False, unique=False)
    email = db.Column(db.String(40), unique=True, nullable=False)
    password = db.Column(
        db.String(200), primary_key=False, unique=False, nullable=False
    )
    created_on = db.Column(db.DateTime, index=False, unique=False, nullable=True)
    last_login = db.Column(db.DateTime, index=False, unique=False, nullable=True)
    tea_log = db.relationship("TeaLog", backref="user", lazy=True)

    def set_password(self, password):
        """Create hashed password."""
        self.password = generate_password_hash(password, method="sha256")

    def check_password(self, password):
        """Check hashed password."""
        return check_password_hash(self.password, password)

    def __repr__(self):
        return "<User {}>".format(self.email)


class Tea(db.Model):
    """Tea model."""

    __tablename__ = "tea"
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False, unique=False)
    price_per_gram = db.Column(
        db.Float,
    )
    tea_log = db.relationship("TeaLog", backref="tea", lazy=True)
    created_on = db.Column(db.DateTime, index=False, unique=False, nullable=True)


class TeaLog(db.Model):
    __tablename__ = "tealog"
    id = db.Column(db.Integer, primary_key=True)
    tea_id = db.Column(db.Integer, db.ForeignKey("tea.id"), nullable=False)
    user_id = db.Column(
        db.Integer,
        db.ForeignKey("flasklogin-users.id"),
    )
    date = db.Column(db.DateTime)
    created_on = db.Column(db.DateTime, index=False, unique=False, nullable=True)
