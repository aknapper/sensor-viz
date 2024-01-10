#!/usr/bin/env python3

import smbus2
import time
import csv
import datetime
import os
import logging

from dash import Dash, html, dcc, callback, Output, Input
import pandas as pd
import plotly.express as px

DEVICE_BUS = 1
TMP102_ADDRESS = 0x48
TEMP_REG = 0x00
CONFIG_REG = 0x01
T_LOW_REG = 0x02
T_HIGH_REG = 0x03
res = 0.0625
bus = smbus2.SMBus(DEVICE_BUS)

class SensorViz:
    def __init__ (self):
        self.dashboard = Dash(__name__)

    def start_server(self):
        self.dashboard.run_server(debug=True)        

tmp102_df = pd.DataFrame({'Timestamp': [''], 'Temperature': ['']})

@callback(
    Output(component_id="tmp102-data", component_property="figure"),
    Input(component_id="interval-component", component_property="n_intervals"),
)
def update_line_chart(n_intervals):
    global tmp102_df
    # Read data from I2C device
    time, temp = read_sensor()

    # Append data to Pandas DataFrame
    newData = pd.DataFrame({"Timestamp": [time], "Temperature": [temp]})
    tmp102_df = pd.concat([tmp102_df, newData], ignore_index=True)

    fig = px.line(tmp102_df, x="Timestamp", y="Temperature", title="tmp102 data viz")
    return fig

def read_temperature():
    # Read the temperature register (2 bytes)
    temperature_data = bus.read_i2c_block_data(TMP102_ADDRESS, TEMP_REG, 2)
    logging.info("tmp102 i2c temperature read.")
    # Combine the two bytes to get the 12-bit temperature value
    raw_temperature = (temperature_data[0] << 4) | (temperature_data[1] >> 4)
    # Convert the raw temperature value to Celsius
    return raw_temperature * res

def read_sensor():
    try:
        timestamp = time.time() - start_time
        temperature = read_temperature()
        print(f"Temperature: {temperature:.2f} °C")

        # Write data to CSV file
        append_row_to_csv(data_csv_file_loc, timestamp, temperature)

        return timestamp, temperature

    except KeyboardInterrupt:
        # Close the SMBus connection when the program is interrupted
        bus.close()

def append_row_to_csv(file_loc, timestamp, data):
    logging.info(f"data written to {file_loc}.")
    with open(file_loc, 'a', newline='') as csv_file:
        csv_writer = csv.writer(csv_file)
        csv_writer.writerow([timestamp, data])

def main():
    # # turn on for info logging verbosity
    # format = "%(asctime)s: %(message)s"
    # logging.basicConfig(format=format, level=logging.INFO,
    #                     datefmt="%H:%M:%S")

    app = SensorViz()

    app.dashboard.layout = html.Div(children=[
        html.H1(children='Sensorviz'),
        html.H1(children="tmp102"),
        dcc.Graph(figure={}, id="tmp102-data"),
        dcc.Interval(id="interval-component", interval=1000 * 1, n_intervals=0),
        ])
    
    app.start_server()

if __name__ == '__main__':
    start_time = time.time()

    # CSV file setup
    data_dir_name = "data"
    data_subdir = f'{os.getcwd()}/{data_dir_name}'
    if not os.path.exists(data_subdir):
        os.makedirs(data_subdir)
    data_csv_filename = "{}-tmp102.csv".format(datetime.datetime.now().strftime('%y-%m-%d-%X'))
    data_csv_file_loc = f'{data_subdir}/{data_csv_filename}'
    append_row_to_csv(data_csv_file_loc, 'Timestamp', 'Temperature (°C)')

    main()
