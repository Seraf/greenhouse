#!/usr/bin/python3
# -*- coding: utf-8 -*-

import pigpio
import time
import string

class atlas_i2c:
    
    def __init__(self, pi):
        self.pi = pi
        self.addr = 0x66
        self.bus = 1

        self.long_timeout = 1.5  # the timeout needed to query readings and calibrations
        self.short_timeout = 0.5  # timeout for regular commands
    
    def write(self, string):
        # appends the null character and sends the string over I2C
        string += "\00"
       
        handle = self.pi.i2c_open(self.bus, self.addr)
        self.pi.i2c_write_device(handle, bytes(string, 'UTF-8'))  # send reset command
        self.pi.i2c_close(handle)

    def read(self, num_of_bytes=31):
        handle = self.pi.i2c_open(self.bus, self.addr)
        (count, byteArray) = self.pi.i2c_read_device(handle, num_of_bytes)
        self.pi.i2c_close(handle)  # close the i2c bus
        if(byteArray[0]):  # if the response isnt an error
            return byteArray[1:6].decode("utf-8")
        else:
            return "Error " + str(ord(response[0]))

    def query(self, string):
        # write a command to the board, wait the correct timeout,
        #and read the response
        self.write(string)

        # the read and calibration commands require a longer timeout
        if((string.upper().startswith("R")) or
           (string.upper().startswith("CAL"))):
            time.sleep(self.long_timeout)
        elif((string.upper().startswith("SLEEP"))):
            return "sleep mode"
        else:
            time.sleep(self.short_timeout)

        return self.read()

if __name__ == '__main__':
    ts = int(round(time.time()) * 1000000000)
    device = atlas_i2c(pigpio.pi())
    print("ezotemp  temperature={0} {1}".format(device.query("R"), ts))
    exit(0)
