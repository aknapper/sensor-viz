#!/usr/bin/env python3

import smbus2
import time
import logging

from helpers import append_row_to_csv

from dash import html, dcc, callback, Output, Input
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
        from globals import start_time, data_csv_file_loc
        timestamp = time.time() - start_time
        temperature = read_temperature()
        print(f"Temperature: {temperature:.2f} °C")

        # Write data to CSV file
        file_loc = data_csv_file_loc
        append_row_to_csv(file_loc, timestamp, temperature)

        return timestamp, temperature

    except KeyboardInterrupt:
        # Close the SMBus connection when the program is interrupted
        bus.close()

def setup_dashboard(dashboard):
    dashboard.layout = html.Div(children=[
        html.H1(children='Sensorviz'),
        html.H1(children="tmp102"),
        dcc.Graph(figure={}, id="tmp102-data"),
        dcc.Interval(id="interval-component", interval=1000 * 1, n_intervals=0),
        ])
