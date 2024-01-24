import pandas as pd

from helpers import setup_data_file

class Device:
    def __init__(self, dev_name, sampleData):
        self.recording_data = False
        self.csvFileLoc = setup_data_file(dev_name, sampleData)
        self.dataFrame = pd.DataFrame({'Timestamp': [''], 'Runtime (s)': [''], sampleData[0]: ['']})
    