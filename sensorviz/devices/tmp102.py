import time
import logging
import smbus2

from helpers import append_row_to_csv

TMP102_ADDRESS = 0x48
TEMP_REG = 0x00
CONFIG_REG = 0x01
T_LOW_REG = 0x02
T_HIGH_REG = 0x03
res = 0.0625

DEVICE_BUS = 1
bus = smbus2.SMBus(DEVICE_BUS)  

def read_temperature():
    # Read the temperature register (2 bytes)
    temperature_data = bus.read_i2c_block_data(TMP102_ADDRESS, TEMP_REG, 2)
    logging.info("tmp102 i2c temperature read.")
    # Combine the two bytes to get the 12-bit temperature value
    raw_temperature = (temperature_data[0] << 4) | (temperature_data[1] >> 4)
    # Convert the raw temperature value to Celsius
    return raw_temperature * res

def tmp102_read():
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