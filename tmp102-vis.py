#!/usr/bin/env python3

import smbus2
import time
import csv
import matplotlib.pyplot as plt

import logging
import threading

DEVICE_BUS = 1
TMP102_ADDRESS = 0x48
TEMP_REG = 0x00
CONFIG_REG = 0x01
T_LOW_REG = 0x02
T_HIGH_REG = 0x03
res = 0.0625
bus = smbus2.SMBus(DEVICE_BUS)

# Initialize plot
plt.ion()  # Turn on interactive mode
fig, ax = plt.subplots()
x_data, y_data = [], []
line, = ax.plot(x_data, y_data, label='Temperature (°C)')
ax.set_xlabel('Time (s)')
ax.set_ylabel('Temperature (°C)')
ax.legend()

# CSV file setup
csv_filename = 'temp102-data.csv'
csv_header = ['Timestamp', 'Temperature (°C)']

def read_temperature():
    # Read the temperature register (2 bytes)
    temperature_data = bus.read_i2c_block_data(TMP102_ADDRESS, TEMP_REG, 2)
    # Combine the two bytes to get the 12-bit temperature value
    raw_temperature = (temperature_data[0] << 4) | (temperature_data[1] >> 4)
    # Convert the raw temperature value to Celsius
    return raw_temperature * res

def get_data():
    try:
        start_time = time.time()
        while True:
            timestamp = time.time() - start_time
            temperature = read_temperature()
            print(f"Temperature: {temperature:.2f} °C")
            
            # Update plot
            x_data.append(timestamp)
            y_data.append(temperature)
            line.set_xdata(x_data)
            line.set_ydata(y_data)
            ax.relim()
            ax.autoscale_view()

            # Write data to CSV file
            with open(csv_filename, 'a', newline='') as csv_file:
                csv_writer = csv.writer(csv_file)
                csv_writer.writerow([timestamp, temperature])

            # Pause to control the rate of updates
            plt.pause(.5)

    except KeyboardInterrupt:
        # Close the SMBus connection when the program is interrupted
        bus.close()
        plt.ioff()  # Turn off interactive mode
        plt.show()  # Display the final plot

if __name__ == '__main__':
    format = "%(asctime)s: %(message)s"
    logging.basicConfig(format=format, level=logging.INFO,
                        datefmt="%H:%M:%S")
    
    threads = list()
    x = threading.Thread(target=get_data)
    threads.append(x)
    x.start()
    