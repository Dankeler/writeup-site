from . import db
from sqlalchemy.sql import func
from enum import Enum
from sqlalchemy import Enum as SQLAlchemyEnum

writeup_tag = db.Table(
    'writeup_tag',
    db.Column('writeup_url', db.String, db.ForeignKey('writeup.url'), primary_key=True),
    db.Column('tag_id', db.Integer, db.ForeignKey('tag.id'), primary_key=True)
)

class List(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String, nullable=False)
    href = db.Column(db.String)

    writeup_url = db.Column(db.String, db.ForeignKey('writeup.url'), nullable=False)
    writeup = db.relationship('Writeup', back_populates='lists')

class Tag(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, nullable=False)

    writeups = db.relationship('Writeup', secondary=writeup_tag, back_populates='tags')

class Writeup(db.Model):
    url = db.Column(db.String, primary_key=True)
    name = db.Column(db.String)
    posted = db.Column(db.DateTime(timezone=True), default=func.now())
    description = db.Column(db.String)
    tryhackme_url = db.Column(db.String)
    difficulty = db.Column(db.String)

    lists = db.relationship('List', back_populates='writeup')
    tags = db.relationship('Tag', secondary=writeup_tag, back_populates='writeups')
