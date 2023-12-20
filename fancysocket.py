#!/usr/bin/env python3

import bluetooth
import json
from RpiMotorLib import rpi_dc_lib

left_motor = rpi_dc_lib.L298NMDc(24 ,23 ,12 ,60 ,False, "left_motor")
right_motor = rpi_dc_lib.L298NMDc(17 ,27 ,13 ,60 ,False, "right_motor")

def set_left(p):
    if p >= 0:
        left_motor.forward(p)
    else:
        left_motor.backward(abs(p))

def set_right(p):
    if p >= 0:
        right_motor.forward(p)
    else:
        right_motor.backward(abs(p))


server_sock = bluetooth.BluetoothSocket(bluetooth.RFCOMM)
server_sock.bind(("", bluetooth.PORT_ANY))
server_sock.listen(1)

port = server_sock.getsockname()[1]

uuid = "94f39d29-7d6d-437d-973b-fba39e49d4ee"

bluetooth.advertise_service(server_sock, "ControlServer", service_id=uuid,
                            service_classes=[uuid, bluetooth.SERIAL_PORT_CLASS],
                            profiles=[bluetooth.SERIAL_PORT_PROFILE],
                            )

while True:
    try:
        print("Waiting for connection on RFCOMM channel", port)
        client_sock, client_info = server_sock.accept()
        print("Accepted connection from", client_info)

        try:
            while True:
                data = client_sock.recv(1024)
                if not data:
                    break
                try:
                    motor_spec = json.loads(data)
                    set_left(int(motor_spec['l']))
                    set_right(int(motor_spec['r']))
                except Exception as e:
                    print(e)
                client_sock.send(b'a')
            print("Disconnected.")
        except OSError:
            pass
    except KeyboardInterrupt:
        break



client_sock.close()
server_sock.close()
print("All done.")
