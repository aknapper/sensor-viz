#!/usr/bin/env python3

import smbus2
import time
import csv

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

# CSV file setup
csv_filename = 'temp102-data.csv'
csv_header = ['Timestamp', 'Temperature (°C)']

tmp102_df = pd.DataFrame({'Timestamp': [''], 'Temperature': ['']})

app = Dash(__name__)

app.layout = html.Div(children=[
    html.H1(children='Sensorviz'),
    html.H1(children="tmp102"),
    dcc.Graph(figure={}, id="tmp102-data"),
    dcc.Interval(id="interval-component", interval=1000 * 1, n_intervals=0),
])

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
        with open(csv_filename, 'a', newline='') as csv_file:
            csv_writer = csv.writer(csv_file)
            csv_writer.writerow([timestamp, temperature])

        return timestamp, temperature

    except KeyboardInterrupt:
        # Close the SMBus connection when the program is interrupted
        bus.close()

def start_server():
    app.run_server(debug=True)

if __name__ == '__main__':
    start_time = time.time()        
    app.run_server(debug=True)
