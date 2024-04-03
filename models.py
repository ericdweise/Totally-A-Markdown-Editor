from flask_login import UserMixin
from sqlalchemy import (
    Column,
    Integer,
    String,
)
from werkzeug.security import (
    generate_password_hash,
    check_password_hash,
)

from database import Base


class User(Base, UserMixin):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True)
    username = Column(String(50), unique=True)
    hashpass = Column(String(120), unique=True)

    def __init__(self, username=None):
        self.username = username

    def __repr__(self):
        return f"<User {self.username!r}>"

    def set_password(self, password):
        self.hashpass = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.hashpass, password)
