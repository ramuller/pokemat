#!/bin/env python

import time
import serial
import argparse
import logging

# configure the serial connections (the parameters differs on the device you are connecting to)

def catch_client(port, speed = 38400):
    ser = serial.Serial(
        port=port,
        baudrate=speed,
        parity=serial.PARITY_NONE,
        stopbits=serial.STOPBITS_ONE,
        bytesize=serial.EIGHTBITS
        )

    # ser.isOpen()
    # Send a message
    # ser.write(b"left\n")  # Send as bytes


    dir = 0
    while(1):
        out = ''
        # let's wait one second before reading output (let's give device time to answer)
        time.sleep(2)
        # while ser.inWaiting() > 0:
        #     b = ser.read(1)
        #     out += b.decode()
        

        if dir % 2 != 0:
            print("send left")
            ser.write(b"left\n")
        else: 
            print("send right")
            bs = "right\n".encode()
            ser.write(b"right\n")
        dir += 1
        resp = ser.readline().decode().strip()
        print(f"Received: {resp}")

def main():

    parser = argparse.ArgumentParser()
    # parser.add_argument("mode", help="Operation mode. Tell pokemate what you want to do\n" + \
    #                     "evolve - send and receive gifts")
    parser.add_argument('--loglevel', '-l', action='store', default=logging.INFO)
    parser.add_argument("-p", "--port", action="store", default="/dev/ttyUSB0", \
                        help="TCP port for the connection.")
    global args
    args = parser.parse_args()
    global log 
    log = logging.getLogger("evolve")
    logging.basicConfig(level=args.loglevel)
    log.debug("args {}".format(args))
    catch_client(args.port)
    # ts.click(200,200)
    print("end")
    # ts.click(200,y)
if __name__ == "__main__":
    main()
