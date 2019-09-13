import struct
import time
import json
import hashlib
import uuid
from db import user_date
from functools import wraps
def get_time():
    now_time = time.strftime('%Y-%m-%d %X')
    return now_time


# 发
def send_msg(send_dic,conn,file=None):
    send_bytes = json.dumps(send_dic).encode('utf-8')
    # 报头
    header = struct.pack('i',len(send_bytes))

    conn.send(header)
    conn.send(send_bytes)
    # print(file)
    if file:
        with open(file,'rb')as f:
            for line in f:
                conn.send(line)

def get_session():
    md = hashlib.md5()
    md.update(str(uuid.uuid4()).encode('utf-8'))
    return md.hexdigest()


# 用户装饰器

def login_auth(func):
    @wraps(func)
    def inner(*args,**kwargs):
        for v in user_date.alive_dic.values():
            # 先比较session 值
            if args[0].get('session') == v[0]:
                # 赋值
                args[0]['user_id'] = v[1]
        if args[0].get('user_id'):
            func(*args,**kwargs)
        else:
            send_dic = {"flag":False,'msg':'未登录，请去登陆'}
            send_msg(send_dic,args[1])
    return inner


