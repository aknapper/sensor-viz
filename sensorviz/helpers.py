import csv
import logging
import os
import datetime

import globals

def append_row_to_csv(file_loc, timestamp, data):
    logging.info(f"data written to {file_loc}.")
    with open(file_loc, 'a', newline='') as csv_file:
        csv_writer = csv.writer(csv_file)
        csv_writer.writerow([timestamp, data])

def setup_data_file(folder_name, device_name, datatype):
    # CSV data store file setup
    data_subdir = f'{os.getcwd()}/{folder_name}'
    if not os.path.exists(data_subdir):
        os.makedirs(data_subdir)
    data_csv_filename = "{}-{}".format(datetime.datetime.now().strftime('%y-%m-%d-%X'), device_name)
    data_csv_file_loc = f'{data_subdir}/{data_csv_filename}'
    globals.data_csv_file_loc = data_csv_file_loc
    append_row_to_csv(data_csv_file_loc, 'Timestamp', datatype)