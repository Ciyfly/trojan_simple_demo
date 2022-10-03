#!/usr/bin/python
# coding=utf-8
'''
Author: Recar
Date: 2022-10-03 08:15:47
LastEditors: Recar
LastEditTime: 2022-10-03 08:17:15
'''

from flask import Flask
from flask_sqlalchemy import SQLAlchemy
import os

app = Flask(__name__)

base_dir = os.path.abspath(os.path.dirname(__file__))
app.config["SQLALCHEMY_DATABASE_URI"] = 'sqlite:///' + os.path.join(base_dir, "../", 'miansha3.db')
app.config["SQLALCHEMY_COMMIT_ON_TEARDOWN"] = True

db = SQLAlchemy(app)
from app import router

with app.app_context(): 
    db.init_app(app)
    db.create_all()
