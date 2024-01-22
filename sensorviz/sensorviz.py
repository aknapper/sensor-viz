#!/usr/bin/env python3

import time

from dash import Dash
from dashboard import setup_dashboard
from helpers import setup_data_file, cli_init

import globals

class SensorViz:
    def __init__ (self):
        self.dashboard = Dash(__name__)

    def start_server(self):
        self.dashboard.run_server(debug=True)

def main():
    cli_init()
    globals.start_time = time.time()

    setup_data_file("data", "tmp102", "Temperature (°C)")

    app = SensorViz()

    setup_dashboard(app.dashboard)

    app.start_server()

if __name__ == '__main__':
    main()
