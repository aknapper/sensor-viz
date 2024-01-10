#!/usr/bin/env python3

import time

from dash import Dash
from dashboard import setup_dashboard
from helpers import setup_data_file

import globals

class SensorViz:
    def __init__ (self):
        self.dashboard = Dash(__name__)

    def start_server(self):
        self.dashboard.run_server(debug=True)

def main():
    # # turn on for info logging verbosity
    # format = "%(asctime)s: %(message)s"
    # logging.basicConfig(format=format, level=logging.INFO,
    #                     datefmt="%H:%M:%S")

    globals.start_time = time.time()

    setup_data_file("data", "tmp102", "Temperature (°C)")

    app = SensorViz()

    setup_dashboard(app.dashboard)

    app.start_server()

if __name__ == '__main__':
    main()
