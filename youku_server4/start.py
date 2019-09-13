# 启动文件

import sys
import os
from tcpserver.socket_server import SocketServer
sys.path.append(os.path.dirname(__file__))

if __name__ == '__main__':
    # 生成个对象run()
    server = SocketServer()
    server.run()
