from . import db
from flask_login import UserMixin
from sqlalchemy.sql import func
from sqlalchemy import DateTime
import cx_Oracle


class DateTasks(db.Model):
    __tablename__ = 'DateTasks'
    id = db.Column('id_date',db.Integer, db.Sequence('DateTasks_seq', start=1, increment=1), primary_key=True, autoincrement=True)
    date_task = db.Column('date_task',db.DateTime)
    start_task = db.Column('start_time',db.TIMESTAMP)
    end_task = db.Column('end_time',db.TIMESTAMP)
    id_task = db.Column('id_task',db.Integer,db.ForeignKey('Tasks.id_task'))


class PeriodTasks(db.Model):
    __tablename__ = 'PeriodTasks'
    id = db.Column('id_day',db.Integer, db.Sequence('PeriodTasks_seq', start=1, increment=1), primary_key=True, autoincrement=True)
    day_task = db.Column('day_week',db.String(20))
    start_task = db.Column('start_time',db.TIMESTAMP)
    end_task = db.Column('end_time',db.TIMESTAMP)
    id_task = db.Column('id_task',db.Integer,db.ForeignKey('Tasks.id_task'))


class Tasks(db.Model):
    __tablename__ = 'Tasks'
    id = db.Column('id_task',db.Integer, db.Sequence('Tasks_seq', start=1, increment=1), primary_key=True, autoincrement=True)
    task = db.Column('task',db.String(500))
    #type_task = db.Column('type_task',db.String(20))
    id_user = db.Column('id_user',db.Integer,db.ForeignKey('UserAccount.id_user'))
    period_of_tasks = db.relationship('PeriodTasks')
    dates_of_tasks = db.relationship('DateTasks')


class User(db.Model, UserMixin):
    __tablename__ = 'UserAccount'
    id = db.Column('id_user',db.Integer, db.Sequence('UserAccount_seq', start=1, increment=1), primary_key=True, autoincrement=True)
    username = db.Column('user_app',db.String(50), unique=True)
    email = db.Column('email',db.String(150), unique=True)
    password = db.Column('pass_user',db.String(150))
    user_tasks = db.relationship('Tasks')
