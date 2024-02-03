#!/usr/bin/env python3

import time
from dash import Dash, dcc, html
import devices.tmp102.dashboard as dashboard
from helpers import cli_init

class SensorViz:
    def __init__ (self):
        self.dashboard = Dash(__name__)
        self.app_start_time = time.time()

    def start_server(self):
        self.dashboard.run_server(debug=True)


layout2 = html.Div([
    html.H2(children='layout2 test data')
])

def main():
    cli_init()

    app = SensorViz()

    app.dashboard.layout = html.Div([
        html.Header(children='Sensorviz', style={"font-size": "30px", "textAlign": "center"}),
        dcc.Tabs([
            dcc.Tab(label='TMP102', children=dashboard.tmp102_layout),
            dcc.Tab(label='Layout2', children=layout2),
            dcc.Tab(label='Layout3', children=layout2),
        ])
    ])

    app.start_server()

if __name__ == '__main__':
    main()
