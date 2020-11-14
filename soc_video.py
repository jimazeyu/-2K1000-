###监控视频通信
import socket
import threading
import cv2
import numpy
from time import sleep


def recv_all(sock, count):
    buf = ''
    while count:
        newbuf = sock.recv(count)
        if not newbuf: return None
        buf += newbuf.decode()
        count -= len(newbuf)
    return buf


# 线程锁
threadLock = threading.Lock()
# 视频buf
# videoDatastr = ''
# 客户端套接字
conn_list = []

def robotVideoThread(sock):
    global videoDatastr
    # 接受TCP链接并返回（conn, addr），其中conn是新的套接字对象，可以用来接收和发送数据，addr是链接客户端的地址。
    conn, addr = sock.accept()
    print ('robot Connected with' + ' ' + addr[0] + ':' + str(addr[1]))
    conn_list.append(conn)
    while True:
        length = recv_all(conn, 16)  # 首先接收来自客户端发送的大小信息
        # 若成功接收到大小信息，进一步再接收整张图片
        threadLock.acquire()
        videoDatastr = recv_all(conn, int(length))
        threadLock.release()


def userVideoThread(sock):
    global videoDatastr
    # 接受TCP链接并返回（conn, addr），其中conn是新的套接字对象，可以用来接收和发送数据，addr是链接客户端的地址。
    conn, addr = sock.accept()
    print ('user Connected with' + ' ' + addr[0] + ':' + str(addr[1]))
    conn_list.append(conn)
    while True:
        #threadLock.acquire()
        conn.send(str(len(videoDatastr)).ljust(16))
        conn.send(videoDatastr)
        #threadLock.release()
        sleep(0.1)


if __name__ == '__main__':

    s_robot = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    address = ('192.168.3.3', 8888)
    s_robot.bind(address)
    s_robot.listen(True)
    print ('robot服务器初始化成功')

    s_user = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    address = ('192.168.3.3', 9999)
    s_user.bind(address)
    s_user.listen(True)
    print ('user服务器初始化成功')

    threading.Thread(target=robotVideoThread, args=(s_robot, )).start()
    threading.Thread(target=userVideoThread, args=(s_user,)).start()
