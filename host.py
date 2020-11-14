##socket通信##
##上位机##
import socket
import time
HOST = '192.168.3.3'
PORT = 8001
sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)  
sock.bind((HOST, PORT))  
sock.listen(5)  
connection,address = sock.accept()  
# 通讯循环
while True:
    # 接收消息
    msg = connection.recv(1024)  # 最大接收字节数为1024
    if not msg:
        continue
    print('client is sending: ' + msg.decode('utf-8'))

# 断开连接
connection.close()

# 关闭套接字
sock.close()
