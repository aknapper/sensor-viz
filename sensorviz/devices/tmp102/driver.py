import time
import logging
import smbus2
import pandas as pd
from devices.device import Device
from helpers import append_row_to_csv

TEMP_REG = 0x00
CONFIG_REG = 0x01
T_LOW_REG = 0x02
T_HIGH_REG = 0x03
res = 0.0625 

class TMP102(Device):
    def __init__(self, dev_name, bus_num, address):
        self.bus_num = bus_num
        self.bus = smbus2.SMBus(self.bus_num)
        self.address = address
        self.data_capture_start_time = 0
        self.sampleData = ("Temperature (°C)")
        super().__init__(dev_name, self.sampleData)

    def get_temperature(self):
        # Read the temperature register (2 bytes)
        temperature_data = self.bus.read_i2c_block_data(self.address, TEMP_REG, 2)
        logging.info("tmp102 i2c temp read.")
        # Combine the two bytes to get the 12-bit temperature value
        raw_temperature = (temperature_data[0] << 4) | (temperature_data[1] >> 4)
        # Convert the raw temperature value to Celsius
        return raw_temperature * res

    def temp_data_capture(self):
        try:
            if self.data_capture_start_time == 0:
                self.data_capture_start_time = time.time()
            runtime = time.time() - self.data_capture_start_time
            timestamp = time.strftime("%H:%M:%S", time.localtime())
            
            temperature = self.get_temperature()
            print(f"Temperature: {temperature:.2f} °C")

            # Write data to CSV file
            append_row_to_csv(self.csvFileLoc, timestamp, runtime, temperature)

            # Append data to Pandas DataFrame
            newData = pd.DataFrame({"Timestamp": [timestamp], "Runtime (s)": [runtime],self.sampleData[0]: [temperature]})
            self.dataFrame = pd.concat([self.dataFrame, newData], ignore_index=True)

        except KeyboardInterrupt:
            # Close the SMBus connection when the program is interrupted
            self.bus.close()
