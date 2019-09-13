import json
import socket
import struct
from concurrent.futures import ThreadPoolExecutor
from interface import common_interface,admin_interface,user_interface
from db import user_date


func_dic = {
    'register':common_interface.register,
    'login':common_interface.login,
    'check_movie':admin_interface.check_movie,
    'upload_movie':admin_interface.upload_movie,
    'get_movie_list':common_interface.get_movie_list,
    'delete_movie':admin_interface.delete_movie,
    'release_notice':admin_interface.release_notice,
    'buy_vip':user_interface.buy_vip,
    'download_movie':user_interface.download_movie,
    'check_download_record':user_interface.check_download_record,
    'check_notice':user_interface.check_notice,


}

class SocketServer(object):
    def __init__(self):
        self.server = socket.socket()
        self.server.bind(('127.0.0.1', 8080))
        self.server.listen(5)
        self.pool = ThreadPoolExecutor(50)

    def run(self):
        # 链接
        while True:
            conn, addr = self.server.accept()
            self.pool.submit(self.working,conn,addr)

    def working(self,conn,addr):
        # 通信循环
        while True:
            try:
                # 接收信息
                header = conn.recv(4)
                # print(header,'666')
                header_len = struct.unpack('i',header)[0]
                header_size = conn.recv(header_len)
                recv_dic = json.loads(header_size.decode('utf-8'))
                recv_dic['addr'] = str(addr)
                self.dispatcher(recv_dic,conn)
            except BaseException as e:
                print(e)
                # 删除用户的addr alive_dic
                common_interface.mutex.acquire()
                user_date.alive_dic.pop('addr')
                common_interface.mutex.release()
                conn.close()
                break

    def dispatcher(self,recv_dic,conn):

        if recv_dic['type'] in func_dic:
            func_dic.get(recv_dic['type'])(recv_dic,conn)
        else:
            print('无此功能')












