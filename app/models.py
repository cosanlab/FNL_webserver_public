#models.py

"""
Models used by SQLAlchemy to create database
"""

from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import create_engine, Table, Column
from app import db

class ep1(db.Model):
    __tablename__ = 'ep1'
    id = db.Column(db.Integer, primary_key=True, unique=True)
    timestart = db.Column(db.Text(15))
    timeend = db.Column(db.Text(15))
    dialogue = db.Column(db.Text(255))

class ep2(db.Model):
    __tablename__ = 'ep2'
    id = db.Column(db.Integer, primary_key=True, unique=True)
    timestart = db.Column(db.Text(15))
    timeend = db.Column(db.Text(15))
    dialogue = db.Column(db.Text(255))

class ep3(db.Model):
    __tablename__ = 'ep3'
    id = db.Column(db.Integer, primary_key=True, unique=True)
    timestart = db.Column(db.String(15))
    timeend = db.Column(db.String(15))
    dialogue = db.Column(db.String(255))

class ep4(db.Model):
    __tablename__ = 'ep4'
    id = db.Column(db.Integer, primary_key=True, unique=True)
    timestart = db.Column(db.String(15))
    timeend = db.Column(db.String(15))
    dialogue = db.Column(db.String(255))

class ep1_annotations(db.Model):
    __tablename__ = 'ep1_annotations'
    id = db.Column(db.Integer, primary_key=True, unique=True)
    category_name = db.Column(db.String(20))
    character_name = db.Column(db.String(20))
    timestart = db.Column(db.String(15))
    timeend = db.Column(db.String(15))
    durration = db.Column(db.String(15))
    type = db.Column(db.String(20))


'===================================================================='

class user(db.Model):
    __tablename__ = 'user'
    id = db.Column(db.Integer, primary_key=True, unique = True)
    name = db.Column(db.String(80))
    email = db.Column(db.String(80))

    def __init__(self, name, email):
        self.name = name
        self.email = email
    def __repr__(self):
        return '%d, %r, %r' % (self.id, self.name, self.email)

# def make_shell_context():
#     return dict(app=app, db=db, user=user, ep1=ep1, ep2=ep2, ep3=ep3, ep4=ep4)
# manager.add_command('shell', Shell(make_context=make_shell_context))