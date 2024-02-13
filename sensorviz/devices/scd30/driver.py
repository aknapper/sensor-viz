import time
from multiprocessing import Process, Queue

import pandas as pd

from helpers import append_row_to_csv, setup_data_file

from sensirion_i2c_driver import LinuxI2cTransceiver, I2cConnection, CrcCalculator
from sensirion_i2c_adapter.i2c_channel import I2cChannel
from sensirion_i2c_scd30.device import Scd30Device

class SCD30:
    def __init__(self, dev_name):
        self.sampleData = ("CO2 Concentration (ppm)")
        self.csvFileLoc = setup_data_file(dev_name, self.sampleData)
        self.dataFrame = pd.DataFrame({'Timestamp': [''], 'Runtime (s)': [''], self.sampleData[0]: ['']})

        # process info
        self.dataLogFreq = 2
        self.dataLogTimeQueue = Queue()
        self.dataLogProc = Process(target=self.dataLogCallback)

        self.i2c_transceiver = LinuxI2cTransceiver('/dev/i2c-1')
        self.channel = I2cChannel(I2cConnection(self.i2c_transceiver), slave_address=0x61,
                             crc=CrcCalculator(8, 0x31, 0xff, 0x0))
        self.sensor = Scd30Device(self.channel)
        try:
            self.sensor.stop_periodic_measurement()
            self.sensor.soft_reset()
            time.sleep(2.0)
        except BaseException:
            ...
        self.sensor.start_periodic_measurement(0)

    def data_capture(self):
        start_time = self.dataLogTimeQueue.get()
        runtime = time.time() - start_time
        timestamp = time.strftime("%H:%M:%S", time.localtime())
        
        (co2_concentration, temperature, humidity) = self.sensor.blocking_read_measurement_data()
        print(f"co2_concentration: {co2_concentration:.2f}ppm")
        print(f"temp: {temperature:.2f} degC")
        print(f"humidity {humidity:.2f} %RH\n")

        # Write data to CSV file
        append_row_to_csv(self.csvFileLoc, timestamp, runtime, co2_concentration)

        # Append data to Pandas DataFrame
        newData = pd.DataFrame({"Timestamp": [timestamp], "Runtime (s)": [runtime],self.sampleData[0]: [co2_concentration]})
        self.dataFrame = pd.concat([self.dataFrame, newData], ignore_index=True)
        self.dataLogTimeQueue.put(start_time)

    def dataLogCallback(self):
        while True:
            if self.dataLogProc.is_alive():
                if self.dataLogTimeQueue.empty():
                    self.dataLogTimeQueue.put(time.time())
                self.data_capture()
            time.sleep(self.dataLogFreq)

    def initProc(self):
        self.dataLogProc.start()

    def resetProc(self):
        self.dataLogProc.terminate()
        self.dataLogProc = Process(target=self.dataLogCallback)
