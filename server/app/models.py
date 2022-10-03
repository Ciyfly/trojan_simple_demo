#!/usr/bin/python
# coding=utf-8
'''
Author: Recar
Date: 2022-10-03 08:15:54
LastEditors: Recar
LastEditTime: 2022-10-03 08:25:42
'''

from app import db
from datetime import datetime
class Clients(db.Model):
     __tablename__ = 'clients'
     id = db.Column(db.Integer, primary_key=True)
     name = db.Column(db.String(255))
     ip = db.Column(db.String(255))
     create_time = db.Column(db.DateTime, default=datetime.now)
     update_time = db.Column(db.DateTime, default=datetime.now)

class EchoResult(db.Model):
     __tablename__ = 'echo_result'
     id = db.Column(db.Integer, primary_key=True)
     client_name = db.Column(db.String(255))
     ip = db.Column(db.String(255))
     cmd = db.Column(db.String(255))
     result = db.Column(db.Text())
     create_time = db.Column(db.DateTime, default=datetime.now)
     update_time = db.Column(db.DateTime, default=datetime.now)

