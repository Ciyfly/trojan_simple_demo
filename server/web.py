#!/usr/bin/python
# coding=utf-8
'''
Author: Recar
Date: 2022-10-03 08:16:11
LastEditors: Recar
LastEditTime: 2022-10-03 08:17:57
'''
from app import app

if __name__ == "__main__":
    app.run("0.0.0.0", 5050, debug=True)