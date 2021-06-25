import os
import sys
import threading

import socket
import time
import threading
import datetime

import datetime
import os

import pygame as pygame
from .models import Course, Lesson, Attendance, User

# from manage import sk
width = 320
height = 240

local_ip = "0.0.0.0"
local_port = 3456



ip_port = (local_ip, local_port)
sk = socket.socket()
sk.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
sk.bind(ip_port)
sk.listen(50)
dict = {}
print("accept now,wait for client")

# jpeg 20 fpsls

# esp32 spi dma temp buffer MAX Len: 4k

def server():
    while True:
        conn, addr = sk.accept()
        print("hello client, ip:")
        print(addr)
        t = threading.Thread(target=receiveThread, args=(conn, addr,))
        t.setDaemon(True)
        t.start()
def receive_data(conn, lenght):
    result = b''
    while lenght != len(result):
        try:
            result += conn.recv(lenght - len(result))
        except Exception as e:
            print(e, "\nClose connection")
            conn.close()
            return b'False'
    return result


def get_dir(ID):
    now = datetime.datetime.now()
    dir = "media\\" + ID[:2] + '\\' + ID[0:] + '\\' + str(now.year) + '\\' + str(now.month) + '\\' + str(now.day)
    if not os.path.exists(dir):
        os.makedirs(dir)
    return dir


def receiveThread(conn, addr):
    conn.settimeout(200)
    conn_end = False
    pack_size = 1024*5

    while True:
        if conn_end:
            break
        token = ""
        data = b''
        while True:
            try:
                data = receive_data(conn, 2)
                if data == b'False':
                    return
            except socket.timeout:
                conn_end = True
                break
            print(data)
            if data == b'DV':
                token = receive_data(conn, 10).decode()  # ABCDHKHDJH
                print("Device token: " + token)
                dict[token] = conn
                # conn.send(b'ID09IT001.K21')
                # conn.send(b'ACK')
                break

            elif data == b'TK':
                token = receive_data(conn, 10).decode()
                print("TOKEN: " + token)
                size = receive_data(conn, 2)  # length of ID
                ID = conn.recv(int(size.decode()))

                con = dict.get(token)

                if con:
                    conn.send(b'ACK')
                    conn.close()
                    try:
                        print(b'ID' + size + ID)
                        con.send(b'ID' + size + ID)
                    except Exception as e:
                        conn.close()
                        print(e)
                        return
                else:
                    print("Token not exist")
                    conn.send(b"Device haven't connected to server")
                return
            # đăng ký mã số thẻ cho RFID
            elif data == b'DK':
                token = receive_data(conn, 10).decode()
                print("TOKEN: " + token)
                size = receive_data(conn, 2)  # length of ID
                ID = conn.recv(int(size.decode()))

                con = dict.get(token)

                if con:
                    conn.send(b'ACK')
                    conn.close()
                    try:
                        print(b'DK' + size + ID)
                        con.send(b'DK' +  ID)
                    except Exception as e:
                        conn.close()
                        print(e)
                        return
                else:
                    print("Token not exist")
                    conn.send(b"Device haven't connected to server")
                return
            elif data==b'DE':
                token=receive_data(conn,10).decode()
                dict.pop(token, 1)
                conn.close()
                print("Disconnected")
                return
            elif data==b'EN':
                token=receive_data(conn,10).decode()
                con = dict.get(token)
                conn.send(b'ACK')
                if con:
                    try:
                        con.send(b'EN')
                        dict.pop(token)
                    except Exception as e:
                        print(e)
                else:
                    print("Token not exist")

                conn.close()
                return

            elif data == b'ID':
                print(data)
                size_ID = int(receive_data(conn, 2).decode())
                ID = receive_data(conn, size_ID).decode()
                size_img = int(receive_data(conn, 4).decode())

                img = receive_data(conn, size_img)
                print(img)
                if not img.startswith(b'\xFF\xD8') or not img.endswith(b'\xFF\xD9'):
                    print("image error")
                    conn_end = True
                    return
                    continue
                print("len receive: ", len(img))
                now = datetime.datetime.now()
                imagename=str(now.microsecond)
                # create url to save image
                dir = get_dir(ID)
                # url to save image for attendance
                urlimage="/media/"+ID[:2]+"/"+ID[0:]+"/"+str(now.year)+"/"+str(now.month)+"/"+str(now.day)+"/"+imagename+".jpg"
                # create a attendance in database
                Attendance.objects.create(code_course=ID[0:],
                                          code_student=imagename,
                                          date=datetime.date.today(),
                                          url_image=urlimage)
                # save image to file
                f = open(dir+'\\' + imagename+".jpg", "wb")
                f.write(img)
                f.close()
                try:
                    surface = pygame.image.load(dir).convert()
                    screen.blit(surface, (0, 0))
                    pygame.display.update()
                    print("recieve ok")
                except Exception as e:
                    print(e)
    conn.close()
    print("receive thread end")



# print("createsocket")
# tmp = threading.Thread(target=server, args=())
# tmp.setDaemon(True)
# tmp.start()
# pygame.init()
# screen = pygame.display.set_mode((width, height), 0, 32)
#
# pygame.display.set_caption("pic from client")
# while True:
#     for event in pygame.event.get():
#         if event.type == pygame.QUIT:
#             exit()

def create_socket():

    print("createsocket")
    tmp = threading.Thread(target=server, args=())
    tmp.setDaemon(True)
    tmp.start()
    pygame.init()
    screen = pygame.display.set_mode((width, height), 0, 32)

    pygame.display.set_caption("pic from client")
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                exit()





