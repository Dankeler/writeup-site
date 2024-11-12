from . import db
from sqlalchemy.sql import func
from enum import Enum
from sqlalchemy import Enum as SQLAlchemyEnum

writeup_tag = db.Table(
    'writeup_tag',
    db.Column('writeup_name', db.String, db.ForeignKey('writeup.name'), primary_key=True),
    db.Column('tag_id', db.Integer, db.ForeignKey('tag.id'), primary_key=True)
)

class List(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, unique=True, nullable=False)
    href = db.Column(db.String)
    
    writeup_name = db.Column(db.String, db.ForeignKey('writeup.name'), nullable=False)
    writeup = db.relationship('Writeup', back_populates='lists')

class Tag(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, nullable=False)

    writeups = db.relationship('Writeup', secondary=writeup_tag, back_populates='tags')

class Writeup(db.Model):
    name = db.Column(db.String, primary_key=True)
    date = db.Column(db.DateTime(timezone=True), default=func.now())
    description = db.Column(db.String)
    md_file = db.Column(db.String, nullable=False)

    lists = db.relationship('List', back_populates='writeup')
    tags = db.relationship('Tag', secondary=writeup_tag, back_populates='writeups')
