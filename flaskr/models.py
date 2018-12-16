from flaskr.database import Base
from sqlalchemy import Table, Column, Integer, String, ForeignKey, TIMESTAMP
from sqlalchemy.orm import mapper, relationship
from flaskr.database import metadata, db_session


class User(Base):
    __tablename__ = 'user'
    id = Column(Integer, primary_key=True)
    username = Column(String(50), unique=True)
    password = Column(String(120), unique=True)
    posts = relationship("Post", back_populates='user', cascade='all, delete, delete-orphan')

    def __init__(self, username=None, password=None):
        self.username = username
        self.password = password

    def __repr__(self):
        return '<User %r>' % (self.username,)


class Post(Base):
    __tablename__ = 'post'
    id = Column(Integer, primary_key=True)
    author_id = Column(Integer, ForeignKey('user.id'))
    user = relationship("User", back_populates='posts')

    title = Column(String(100))
    body = Column(String(500))
    created = Column(TIMESTAMP)

    def __init__(self, title=None, body=None, author_id=None):
        self.title = title
        self.body = body
        self.author_id = author_id

    def __repr__(self):
        return '<Post %r>' % (self.title,)


# user = Table('user', metadata,
#     Column('id', Integer, primary_key=True),
#     Column('username', String(50), unique=True),
#     Column('password', String(120), unique=True)
# )
# mapper(User, user)
