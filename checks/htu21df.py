#!/usr/bin/env python3
import time
import pigpio


class TempHumid:
    """
    The class for our combination temperature/humidity sensor. 
    **Methods:** 
    
    * :func:`htu_reset`
    * :func:`read_temperature`
    * :func:`read_humidity`
    
    Initialized during initialization of the main control loop. Periodic calls to the methods will be made in the main control loop.
    """

    def __init__(self,pi):
        """
        The constructor for a Sensor.
        Args:
            pi (gpio target): takes a pigpio objet to interface with the i2C system.
        """
        self.pi = pi
        self.addr = 0x40

        self.bus = 1

        # HTU21D-F Commands
        self.cmds = { "readtemp": 0xE3, "readhumi": 0xE5, "writetreg": 0xE6, "readreg": 0xE7, "reset": 0xFE }

    def htu_reset(self):
        """
        The reset method
        """

        handle = self.pi.i2c_open(self.bus, self.addr)
        self.pi.i2c_write_byte(handle, self.cmds["reset"])  # send reset command
        self.pi.i2c_close(handle)
        time.sleep(0.2)  # reset takes 15ms so let's give it some time

    def read_temperature(self):
        """
        Instructs the sensor to measure the environment temperature. 
        Returns:
            float: The temperature of the environment
        
        TODO implement CRC check        
        """
        handle = self.pi.i2c_open(self.bus, self.addr)
        self.pi.i2c_write_byte(handle, self.cmds["readtemp"])  # send read temp command
        time.sleep(0.055)  # readings take up to 50ms, lets give it some time
        (count, byteArray) = self.pi.i2c_read_device(handle, 3)
        self.pi.i2c_close(handle)  # close the i2c bus
        msb = byteArray[0]  # most significant byte msb
        lsb = byteArray[1]  # least significant byte lsb
        temp_reading = float(((msb << 8) + lsb) & 0xFFFC)

        temperature = ((temp_reading / 65536) * 175.72) - 46.85  # formula from datasheet
        return round(temperature, 2)

    def read_humidity(self):
        """
        Instructs the sensor to measure the environment humidity and calculates the adjusted humidity. 
        Returns:
            float: The temperature of the environment
        
        TODO implement CRC check        
        """
        handle = self.pi.i2c_open(self.bus, self.addr)
        self.pi.i2c_write_byte(handle, self.cmds["readhumi"])  # send read humi command
        time.sleep(0.055)  # readings take up to 50ms, lets give it some time
        (count, byteArray) = self.pi.i2c_read_device(handle, 3)  # vacuum up those bytes
        self.pi.i2c_close(handle)  # close the i2c bus
        msb = byteArray[0]  # most significant byte msb
        lsb = byteArray[1]  # least significant byte lsb
        humi_reading = float(((msb << 8) + lsb) & 0xFFFC)

        uncomp_humidity = ((humi_reading / 65536) * (float(125)/4)) - 6
        temperature = self.read_temperature()
        humidity = ((25 - temperature) * -0.15) + uncomp_humidity
        return round(humidity, 2)

if __name__ == "__main__":
    Sensor = TempHumid(pigpio.pi())
    Sensor.htu_reset()
    print("htu21df  temperature={0},humidity={1}".format(Sensor.read_temperature(), Sensor.read_humidity()))
    exit(0)

