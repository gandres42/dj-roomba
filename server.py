import socket
import netifaces as ni
from RpiMotorLib import rpi_dc_lib

left_motor = rpi_dc_lib.L298NMDc(24 ,23 ,12 ,60 ,False, "left_motor")
right_motor = rpi_dc_lib.L298NMDc(17 ,27 ,13 ,60 ,False, "right_motor")

def set_left(p):
    if p >= 0:
        left_motor.forward(p)
    else:
        left_motor.backward(p)

def set_right(p):
    if p >= 0:
        right_motor.forward(p)
    else:
        right_motor.backward(p)

HOST = "0.0.0.0"
PORT = 8080
sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
sock.bind((HOST, PORT))

try:
    while True:
        print('Listening at ', end="")
        print(ni.ifaddresses('wlan0')[ni.AF_INET][0]['addr'])
        sock.listen()
        conn, addr = sock.accept()
        with conn:
            print(f"Connected by {addr}")
            while True:
                data = conn.recv(3)
                if not data:
                    break
                else:
                    print(int(data))
                    if int(data) <= 100 and int(data) >= 0:
                        set_left(int(data))
                    # set_right(int(data))
except KeyboardInterrupt:
    print("Quitting...")
    if sock is not None:
        sock.close()