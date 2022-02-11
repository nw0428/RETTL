#!/opt/local/bin/python3

import serial
import atexit
import json
import base64
import json, os, re

# import matplotlib.pyplot as plt
# import matplotlib.animation as animation
# from matplotlib import style

# style.use('fivethirtyeight')


def init_serial(port, bps = 9600, to = 0):
    ser = serial.Serial(port, bps, timeout = to)  # open serial port
    ser.flushInput()
    ser.flushOutput()
    return ser



def read_serial(ser):
    try:
        ret = b''
        while True:
            new = ser.read(1)
            if new == b'\r':
                return ret
            ret += new
    except Exception as e:
        return 'ERR: ' +  str(e)

def get_prints(ser):
    while True:
        message = ''
        try:
            message = json.loads(read_serial(ser))
#            print(message)
            if message["m"] == "userProgram.print":
                payload = json.loads(base64.b64decode(message["p"]["value"]))
                print(payload)
        except Exception as e:
            print(e)
            print(message)




def CloseSerial():
    return('done')
    try:
        ser.flush()
        ser.close()
        return 'done'
    except Exception as e:
        return 'ERR: ' + str(e)

atexit.register(CloseSerial)

tty_regex = re.compile('tty\..*')
usb_regex = re.compile('tty\.usb.*')
ports =  list(filter(lambda f : tty_regex.match(f), os.listdir('/dev/')))

print("Which one of these is the spike prime? ")
if any(usb_regex.match(p) for p in ports):
  print("When spike prime is attached by USB you don't see its name")
for i in range(len(ports)):
  print(str(i) + ":", ports[i])

choice = int(input("0-" + str(len(ports)-1) + ": "))

ser = init_serial('/dev/' + ports[choice])
get_prints(ser)


