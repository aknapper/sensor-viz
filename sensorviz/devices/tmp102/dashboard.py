from dash import html, dcc, callback, Output, Input, ctx
import plotly.express as px
from devices.tmp102.driver import TMP102
from multiprocessing import Process

import pandas as pd

tmp102_dev = TMP102(dev_name="tmp102-1", bus_num=1, address=0x48)

# Callback for starting stopping data capture, updating button text
@callback(
    [Output('start_btn', 'children'),
     Output('stop_btn', 'children')],
    [Input('start_btn', 'n_clicks'),
     Input('stop_btn', 'n_clicks')],
    prevent_initial_call=True
)
def startstop_sampling(start, stop):
    if 'start_btn' in ctx.triggered_id:
        if not tmp102_dev.logProcess.is_alive():
            tmp102_dev.logProcess.start()
        return 'Recording started...', 'Stop recording'
    else:
        if tmp102_dev.logProcess.is_alive():
            tmp102_dev.logProcess.terminate()
            tmp102_dev.logProcess = Process(target=tmp102_dev.dataLoggerCallback)
        return 'Start recording', 'Recording stopped...'

# Callback for updating graph based at fixed interval and on new x-asix selection
@callback(
    Output(component_id="tmp102-temperature", component_property="figure"),
    [Input(component_id="interval-component", component_property="n_intervals"),
     Input(component_id="dropdown", component_property="value")]
)
def update_line_chart(n_intervals, axisSeries):
    df = pd.DataFrame({'Timestamp': [''], 'Runtime (s)': [''], tmp102_dev.sampleData[0]: ['']})
    df = pd.read_csv(tmp102_dev.csvFileLoc)
    fig = px.line(df, x=axisSeries, y=tmp102_dev.sampleData, title="TMP102 Data")
    return fig

@callback(
    Output("meter", "value"),
    Input("meter", "value"),
)
def sync_input(meter):
    tmp102_dev.logFreq = meter/1000
    return meter

# tmp102 layout
tmp102_layout = html.Div(children=[
    html.H1(" "),
    html.Div("Sampling Frequency", style={"font-size": "18px"}),
    "Temperature ",
    dcc.Input(id="meter", value = 1000, type="number", step=100), " ms",
    html.H1(" "),
    html.Button("Start recording", n_clicks=0, id="start_btn"),
    html.Button("Stop recording", n_clicks=0, id="stop_btn"),
    dcc.Graph(figure={}, id="tmp102-temperature"),
    html.P("Select time axis:"),
    dcc.Dropdown(
        id="dropdown",
        options=["Timestamp",
                    "Runtime (s)"],
                    value="Runtime (s)",
                    clearable=False,
    ),
    dcc.Interval(id="interval-component", interval=1000 * 1, n_intervals=0),
])
