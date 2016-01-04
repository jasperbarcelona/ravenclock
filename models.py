import flask, flask.views
from flask import Flask, request
from flask.ext.sqlalchemy import SQLAlchemy
from sqlalchemy import Boolean
import helpers.db_conn as db

db = db.alchemy

class Irregular(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    school_id = db.Column(db.String(32))
    date = db.Column(db.String(20))
    day = db.Column(db.Integer)
    month = db.Column(db.Integer)
    year = db.Column(db.Integer)

    kinder_morning_class = db.Column(Boolean, unique=False)
    kinder_afternoon_class = db.Column(Boolean, unique=False)
    primary_morning_class = db.Column(Boolean, unique=False)
    primary_afternoon_class = db.Column(Boolean, unique=False)
    junior_morning_class = db.Column(Boolean, unique=False)
    junior_afternoon_class = db.Column(Boolean, unique=False)
    senior_morning_class = db.Column(Boolean, unique=False)
    senior_afternoon_class = db.Column(Boolean, unique=False)

    kinder_morning_start = db.Column(db.String(30))
    kinder_morning_end = db.Column(db.String(30))
    kinder_afternoon_start = db.Column(db.String(30))
    kinder_afternoon_end = db.Column(db.String(30))
    primary_morning_start = db.Column(db.String(30))
    primary_morning_end = db.Column(db.String(30))
    primary_afternoon_start = db.Column(db.String(30))
    primary_afternoon_end = db.Column(db.String(30))
    junior_morning_start = db.Column(db.String(30))
    junior_morning_end = db.Column(db.String(30))
    junior_afternoon_start = db.Column(db.String(30))
    junior_afternoon_end = db.Column(db.String(30))
    senior_morning_start = db.Column(db.String(30))
    senior_morning_end = db.Column(db.String(30))
    senior_afternoon_start = db.Column(db.String(30))
    senior_afternoon_end = db.Column(db.String(30))

    def serialize(self):
        return {
        'id': self.id,
        'school_id': self.school_id,
        'date': self.date,
        'month': self.month,
        'year': self.year,
        'kinder_morning_class': self.kinder_morning_class,
        'kinder_afternoon_class': self.kinder_afternoon_class,
        'primary_morning_class': self.primary_morning_class,
        'primary_afternoon_class': self.primary_afternoon_class,
        'junior_morning_class': self.junior_morning_class,
        'junior_afternoon_class': self.junior_afternoon_class,
        'senior_morning_class': self.senior_morning_class,
        'senior_afternoon_class': self.senior_afternoon_class,
        'kinder_morning_start': self.kinder_morning_start,
        'kinder_morning_end': self.kinder_morning_end,
        'kinder_afternoon_start': self.kinder_afternoon_start,
        'kinder_afternoon_end': self.kinder_afternoon_end,
        'primary_morning_start': self.primary_morning_start,
        'primary_morning_end': self.primary_morning_end,
        'primary_afternoon_start': self.primary_afternoon_start,
        'primary_afternoon_end': self.primary_afternoon_end,
        'junior_morning_start': self.junior_morning_start,
        'junior_morning_end': self.junior_morning_end,
        'junior_afternoon_start': self.junior_afternoon_start,
        'junior_afternoon_end': self.junior_afternoon_end,
        'senior_morning_start': self.senior_morning_start,
        'senior_morning_end': self.senior_morning_end,
        'senior_afternoon_start': self.senior_afternoon_start,
        'senior_afternoon_end': self.senior_afternoon_end
        }

class Regular(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    school_id = db.Column(db.String(32))

    kinder_morning_class = db.Column(Boolean, unique=False)
    kinder_afternoon_class = db.Column(Boolean, unique=False)
    primary_morning_class = db.Column(Boolean, unique=False)
    primary_afternoon_class = db.Column(Boolean, unique=False)
    junior_morning_class = db.Column(Boolean, unique=False)
    junior_afternoon_class = db.Column(Boolean, unique=False)
    senior_morning_class = db.Column(Boolean, unique=False)
    senior_afternoon_class = db.Column(Boolean, unique=False)

    kinder_morning_start = db.Column(db.String(30))
    kinder_morning_end = db.Column(db.String(30))
    kinder_afternoon_start = db.Column(db.String(30))
    kinder_afternoon_end = db.Column(db.String(30))
    primary_morning_start = db.Column(db.String(30))
    primary_morning_end = db.Column(db.String(30))
    primary_afternoon_start = db.Column(db.String(30))
    primary_afternoon_end = db.Column(db.String(30))
    junior_morning_start = db.Column(db.String(30))
    junior_morning_end = db.Column(db.String(30))
    junior_afternoon_start = db.Column(db.String(30))
    junior_afternoon_end = db.Column(db.String(30))
    senior_morning_start = db.Column(db.String(30))
    senior_morning_end = db.Column(db.String(30))
    senior_afternoon_start = db.Column(db.String(30))
    senior_afternoon_end = db.Column(db.String(30))

    def serialize(self):
        return {
        'id': self.id,
        'school_id': self.school_id,
        'kinder_morning_class': self.kinder_morning_class,
        'kinder_afternoon_class': self.kinder_afternoon_class,
        'primary_morning_class': self.primary_morning_class,
        'primary_afternoon_class': self.primary_afternoon_class,
        'junior_morning_class': self.junior_morning_class,
        'junior_afternoon_class': self.junior_afternoon_class,
        'senior_morning_class': self.senior_morning_class,
        'senior_afternoon_class': self.senior_afternoon_class,
        'kinder_morning_start': self.kinder_morning_start,
        'kinder_morning_end': self.kinder_morning_end,
        'kinder_afternoon_start': self.kinder_afternoon_start,
        'kinder_afternoon_end': self.kinder_afternoon_end,
        'primary_morning_start': self.primary_morning_start,
        'primary_morning_end': self.primary_morning_end,
        'primary_afternoon_start': self.primary_afternoon_start,
        'primary_afternoon_end': self.primary_afternoon_end,
        'junior_morning_start': self.junior_morning_start,
        'junior_morning_end': self.junior_morning_end,
        'junior_afternoon_start': self.junior_afternoon_start,
        'junior_afternoon_end': self.junior_afternoon_end,
        'senior_morning_start': self.senior_morning_start,
        'senior_morning_end': self.senior_morning_end,
        'senior_afternoon_start': self.senior_afternoon_start,
        'senior_afternoon_end': self.senior_afternoon_end
        }

class School(db.Model):
    id = db.Column(db.String(32),primary_key=True)
    api_key = db.Column(db.String(32))
    name = db.Column(db.String(50))