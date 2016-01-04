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
            'kinder_morning_class': sched.kinder_morning_class,
            'kinder_afternoon_class': sched.kinder_afternoon_class,
            'primary_morning_class': sched.primary_morning_class,
            'primary_afternoon_class': sched.primary_afternoon_class,
            'junior_morning_class': sched.junior_morning_class,
            'junior_afternoon_class': sched.junior_afternoon_class,
            'senior_morning_class': sched.senior_morning_class,
            'senior_afternoon_class': sched.senior_afternoon_class,
            'kinder_morning_start':sched.kinder_morning_start,
            'kinder_morning_end':sched.kinder_morning_end,
            'kinder_afternoon_start':sched.kinder_afternoon_start,
            'kinder_afternoon_end':sched.kinder_afternoon_end,
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
        event_days.append(event.day)
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


def get_irregular_schedule(api_key,month,day,year):
    school = School.query.filter_by(api_key=api_key).first()
    schedule = Irregular.query.filter_by(school_id=school.id,month=month,day=day,year=year).first()
    return jsonify(
        kinder_morning_class=schedule.kinder_morning_class,
        kinder_afternoon_class=schedule.kinder_afternoon_class,
        primary_morning_class=schedule.primary_morning_class,
        primary_afternoon_class=schedule.primary_afternoon_class,
        junior_morning_class=schedule.junior_morning_class,
        junior_afternoon_class=schedule.junior_afternoon_class,
        senior_morning_class=schedule.senior_morning_class,
        senior_afternoon_class=schedule.senior_afternoon_class,
        kinder_morning_start=schedule.kinder_morning_start,
        kinder_morning_end=schedule.kinder_morning_end,
        kinder_afternoon_start=schedule.kinder_afternoon_start,
        kinder_afternoon_end=schedule.kinder_afternoon_end,
        primary_morning_start=schedule.primary_morning_start,
        primary_morning_end=schedule.primary_morning_end,
        primary_afternoon_start=schedule.primary_afternoon_start,
        primary_afternoon_end=schedule.primary_afternoon_end,
        junior_morning_start=schedule.junior_morning_start,
        junior_morning_end=schedule.junior_morning_end,
        junior_afternoon_start=schedule.junior_afternoon_start,
        junior_afternoon_end=schedule.junior_afternoon_end,
        senior_morning_start=schedule.senior_morning_start,
        senior_morning_end=schedule.senior_morning_end,
        senior_afternoon_start=schedule.senior_afternoon_start,
        senior_afternoon_end=schedule.senior_afternoon_end
        ),201


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

    sched.kinder_morning_start = data['kinder_morning_start']
    sched.kinder_morning_end = data['kinder_morning_end']
    sched.primary_morning_start = data['primary_morning_start']
    sched.primary_morning_end = data['primary_morning_end']
    sched.junior_morning_start = data['junior_morning_start']
    sched.junior_morning_end = data['junior_morning_end']
    sched.senior_morning_start = data['senior_morning_start']
    sched.senior_morning_end = data['senior_morning_end']
    sched.kinder_afternoon_start = data['kinder_afternoon_start']
    sched.kinder_afternoon_end = data['kinder_afternoon_end']
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

    irreg2 = Irregular(
        school_id=123456789,
        date=time.strftime("%B %d, %Y"),
        day=5,
        month=1,
        year=2016,
        kinder_morning_class=False,
        kinder_afternoon_class=False,
        primary_morning_class=False,
        primary_afternoon_class=False,
        junior_morning_class=False,
        junior_afternoon_class=False,
        senior_morning_class=False,
        senior_afternoon_class=False,
        kinder_morning_start=str(now.replace(hour=7, minute=30, second=0))[11:16],
        kinder_morning_end=str(now.replace(hour=7, minute=30, second=0))[11:16],
        kinder_afternoon_start=str(now.replace(hour=7, minute=30, second=0))[11:16],
        kinder_afternoon_end=str(now.replace(hour=7, minute=30, second=0))[11:16],
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

    sched2 = Regular(
        school_id=123456789,
        kinder_morning_class=True,
        kinder_afternoon_class=True,
        primary_morning_class=True,
        primary_afternoon_class=True,
        junior_morning_class=True,
        junior_afternoon_class=True,
        senior_morning_class=True,
        senior_afternoon_class=True,
        kinder_morning_start=str(now.replace(hour=8, minute=0, second=0))[11:16],
        kinder_morning_end=str(now.replace(hour=8, minute=0, second=0))[11:16],
        kinder_afternoon_start=str(now.replace(hour=8, minute=0, second=0))[11:16],
        kinder_afternoon_end=str(now.replace(hour=8, minute=0, second=0))[11:16],
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

    school2 = School(
        id=123456789,
        api_key='ecc67d28db284a2fb351d58fe18965f9',
        name='Sacred Heart College'
        )

    db.session.add(sched2)
    db.session.add(irreg2)
    db.session.add(school2)
    db.session.commit()

    return jsonify(status='success'), 201