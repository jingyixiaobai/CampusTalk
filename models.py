from datetime import datetime
from extension import db


class User(db.Model):
    __tablename__ = 'user'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), unique=True, nullable=False)
    pwd = db.Column(db.String(128), nullable=False)


class Article(db.Model):
    __tablename__ = 'article'
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(128))
    content = db.Column(db.Text)
    create_time = db.Column(db.DateTime, default=datetime.now)
    author_id = db.Column(db.Integer, db.ForeignKey("user.id"))
    author = db.relationship('User', backref="articles")


class Reply(db.Model):
    __tablename__ = 'reply'
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), index=True)
    target_user_id = db.Column(db.Integer, db.ForeignKey('user.id'), index=True)
    content = db.Column(db.String(300))
    timestamp = db.Column(db.DateTime, index=True, default=datetime.now)
    article_id = db.Column(db.Integer, db.ForeignKey('article.id'), index=True)
    reply_id = db.Column(db.Integer, index=True)
