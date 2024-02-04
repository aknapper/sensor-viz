import time
from multiprocessing import Process, Queue

import pandas as pd

from helpers import append_row_to_csv, setup_data_file

class SCD30:
    def __init__(self, dev_name):
        self.sampleData = ("CO2 Concentration (ppm)")
        self.csvFileLoc = setup_data_file(dev_name, self.sampleData)
        self.dataFrame = pd.DataFrame({'Timestamp': [''], 'Runtime (s)': [''], self.sampleData[0]: ['']})

        # process info
        self.dataLogFreq = 1
        self.dataLogTimeQueue = Queue()
        self.dataLogProc = Process(target=self.dataLogCallback)

    def data_capture(self):
        start_time = self.dataLogTimeQueue.get()
        runtime = time.time() - start_time
        timestamp = time.strftime("%H:%M:%S", time.localtime())
        
        co2_conc = 550.55555
        print(f"Co2 conc: {co2_conc:.2f}ppm")

        # Write data to CSV file
        append_row_to_csv(self.csvFileLoc, timestamp, runtime, co2_conc)

        # Append data to Pandas DataFrame
        newData = pd.DataFrame({"Timestamp": [timestamp], "Runtime (s)": [runtime],self.sampleData[0]: [co2_conc]})
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
