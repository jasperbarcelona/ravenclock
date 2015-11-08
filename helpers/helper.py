from dateutil.parser import parse as parse_date
from flask.ext.sqlalchemy import SQLAlchemy
from sqlalchemy.ext.orderinglist import ordering_list
from flask import render_template, request, jsonify, url_for
from functools import update_wrapper
from flask import session, redirect
from datetime import timedelta
from datetime import datetime
from functools import wraps
import threading
from threading import Timer
from multiprocessing.pool import ThreadPool
import cStringIO
from werkzeug.datastructures import FileStorage
from multiprocessing.pool import ThreadPool
from werkzeug import secure_filename
from models import *
from time import sleep
import requests
import datetime
import time
import json
import uuid
import os
import db_conn as db
import json

db = db.alchemy
now = datetime.datetime.now()

SYNC_URL = 'http://127.0.0.1:5000/schedule/sync'


def get_schedule(sched_type,school_id):
    if sched_type == 'regular':
        sched = Regular.query.filter_by(school_id=school_id).first()
    else:
        sched = Irregular.query.filter_by(school_id=school_id, date=time.strftime("%B %d, %Y")).first()
    data = {
            'school_id':school_id,
            'primary_morning_class': sched.primary_morning_class,
            'primary_afternoon_class': sched.primary_afternoon_class,
            'junior_morning_class': sched.junior_morning_class,
            'junior_afternoon_class': sched.junior_afternoon_class,
            'senior_morning_class': sched.senior_morning_class,
            'senior_afternoon_class': sched.senior_afternoon_class,
            'primary_morning_start':sched.primary_morning_start,
            'primary_morning_end':sched.primary_morning_end,
            'primary_afternoon_start':sched.primary_afternoon_start,
            'primary_afternoon_end':sched.primary_afternoon_end,
            'junior_morning_start':sched.junior_morning_start,
            'junior_morning_end':sched.junior_morning_end,
            'junior_afternoon_start':sched.junior_afternoon_start,
            'junior_afternoon_end':sched.junior_afternoon_end,
            'senior_morning_start':sched.senior_morning_start,
            'senior_morning_end':sched.senior_morning_end,
            'senior_afternoon_start':sched.senior_afternoon_start,
            'senior_afternoon_end':sched.senior_afternoon_end
        }
    return data


def get_events(api_key,month,year):
    event_days=[]
    school = School.query.filter_by(api_key=api_key).first()
    events = Irregular.query.filter_by(school_id=school.id,month=month,year=year).all()
    for event in events:
        event_days.append(event.month)
    return jsonify(days=event_days)


def sync_schedule():
    schools = School.query.all()

    for school in schools:
        irregular_class = Irregular.query.filter_by(school_id=school.id,date=time.strftime("%B %d, %Y")).first()

        sent = False
        while not sent:
            try:
                if irregular_class:
                    r = requests.post(
                        SYNC_URL,
                        get_schedule('irregular',school.id)           
                    )
                    sent =True
                    print 'synced irregular'
                else:
                    r = requests.post(
                        SYNC_URL,
                        get_schedule('regular',school.id)           
                    )
                    sent =True
                    print 'synced regular'

            except requests.exceptions.ConnectionError as e:
                sleep(5)
                print "Disconnected!"
                pass

    start_sync_timer()


def start_sync_timer():
    x = datetime.datetime.now()
    y = x.replace(hour=1, minute=24, second=0, microsecond=0)
    delta_t = y - x
    secs = delta_t.seconds + 1
    t = Timer(secs, sync_schedule)
    t.start()
    print 'time until sync: ' + str(secs/60) + ' min/s'


def change_regular_sched(data):
    sched = Regular.query.filter_by(school_id=data['school_id']).one()

    sched.primary_morning_start = data['primary_morning_start']
    sched.primary_morning_end = data['primary_morning_end']
    sched.junior_morning_start = data['junior_morning_start']
    sched.junior_morning_end = data['junior_morning_end']
    sched.senior_morning_start = data['senior_morning_start']
    sched.senior_morning_end = data['senior_morning_end']
    sched.primary_afternoon_start = data['primary_afternoon_start']
    sched.primary_afternoon_end = data['primary_afternoon_end']
    sched.junior_afternoon_start = data['junior_afternoon_start']
    sched.junior_afternoon_end = data['junior_afternoon_end']
    sched.senior_afternoon_start = data['senior_afternoon_start']
    sched.senior_afternoon_end = data['senior_afternoon_end']

    db.session.commit()
    
    return '',201



def rebuild_database():
    db.drop_all()
    db.create_all()

    sched = Regular(
        school_id=1234,
        primary_morning_class=True,
        primary_afternoon_class=True,
        junior_morning_class=True,
        junior_afternoon_class=True,
        senior_morning_class=True,
        senior_afternoon_class=True,
        primary_morning_start=str(now.replace(hour=16, minute=28, second=0))[11:16],
        primary_morning_end=str(now.replace(hour=7, minute=0, second=0))[11:16],
        primary_afternoon_start=str(now.replace(hour=7, minute=0, second=0))[11:16],
        primary_afternoon_end=str(now.replace(hour=7, minute=0, second=0))[11:16],
        junior_morning_start=str(now.replace(hour=7, minute=0, second=0))[11:16],
        junior_morning_end=str(now.replace(hour=7, minute=0, second=0))[11:16],
        junior_afternoon_start=str(now.replace(hour=7, minute=0, second=0))[11:16],
        junior_afternoon_end=str(now.replace(hour=7, minute=0, second=0))[11:16],
        senior_morning_start=str(now.replace(hour=7, minute=0, second=0))[11:16],
        senior_morning_end=str(now.replace(hour=7, minute=0, second=0))[11:16],
        senior_afternoon_start=str(now.replace(hour=7, minute=0, second=0))[11:16],
        senior_afternoon_end=str(now.replace(hour=7, minute=0, second=0))[11:16]
        )

    sched1 = Regular(
        school_id=4321,
        primary_morning_class=True,
        primary_afternoon_class=True,
        junior_morning_class=True,
        junior_afternoon_class=True,
        senior_morning_class=True,
        senior_afternoon_class=True,
        primary_morning_start=str(now.replace(hour=8, minute=0, second=0))[11:16],
        primary_morning_end=str(now.replace(hour=8, minute=0, second=0))[11:16],
        primary_afternoon_start=str(now.replace(hour=8, minute=0, second=0))[11:16],
        primary_afternoon_end=str(now.replace(hour=8, minute=0, second=0))[11:16],
        junior_morning_start=str(now.replace(hour=8, minute=0, second=0))[11:16],
        junior_morning_end=str(now.replace(hour=8, minute=0, second=0))[11:16],
        junior_afternoon_start=str(now.replace(hour=8, minute=0, second=0))[11:16],
        junior_afternoon_end=str(now.replace(hour=8, minute=0, second=0))[11:16],
        senior_morning_start=str(now.replace(hour=8, minute=0, second=0))[11:16],
        senior_morning_end=str(now.replace(hour=8, minute=0, second=0))[11:16],
        senior_afternoon_start=str(now.replace(hour=8, minute=0, second=0))[11:16],
        senior_afternoon_end=str(now.replace(hour=8, minute=0, second=0))[11:16]
        )


    irreg = Irregular(
        school_id=1234,
        date=time.strftime("%B %d, %Y"),
        month=11,
        year=2015,
        primary_morning_class=False,
        primary_afternoon_class=False,
        junior_morning_class=False,
        junior_afternoon_class=False,
        senior_morning_class=False,
        senior_afternoon_class=False,
        primary_morning_start=str(now.replace(hour=7, minute=30, second=0))[11:16],
        primary_morning_end=str(now.replace(hour=7, minute=30, second=0))[11:16],
        primary_afternoon_start=str(now.replace(hour=7, minute=30, second=0))[11:16],
        primary_afternoon_end=str(now.replace(hour=7, minute=30, second=0))[11:16],
        junior_morning_start=str(now.replace(hour=7, minute=30, second=0))[11:16],
        junior_morning_end=str(now.replace(hour=7, minute=30, second=0))[11:16],
        junior_afternoon_start=str(now.replace(hour=7, minute=30, second=0))[11:16],
        junior_afternoon_end=str(now.replace(hour=7, minute=30, second=0))[11:16],
        senior_morning_start=str(now.replace(hour=7, minute=30, second=0))[11:16],
        senior_morning_end=str(now.replace(hour=7, minute=30, second=0))[11:16],
        senior_afternoon_start=str(now.replace(hour=7, minute=30, second=0))[11:16],
        senior_afternoon_end=str(now.replace(hour=7, minute=30, second=0))[11:16]
        )


    school = School(
        id=1234,
        api_key='ecc67d28db284a2fb351d58fe18965f9',
        name='Scuola Gesu Bambino'
        )

    school1 = School(
        id=4321,
        api_key='ecc67d28db284a2fb351d58fe18965f0',
        name='Sacred Heart College'
        )

    db.session.add(irreg)
    db.session.add(school)
    db.session.add(school1)
    db.session.add(sched)
    db.session.add(sched1)
    db.session.commit()

    return jsonify(status=201), 201