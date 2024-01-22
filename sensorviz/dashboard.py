from dash import dash, html, dcc, callback, Output, Input, ctx
import pandas as pd
import plotly.express as px

from devices.tmp102 import tmp102_read

tmp102_recording = False
tmp102_df = pd.DataFrame({'Timestamp': [''], 'Runtime (s)': [''],"Temperature (°C)": ['']})

@callback(
    [Output('start_btn', 'children'),
     Output('stop_btn', 'children')],
    [Input('start_btn', 'n_clicks'),
     Input('stop_btn', 'n_clicks')],
    prevent_initial_call=True
)
def update_recording(start, stop):
    global tmp102_recording
    triggered_id = ctx.triggered_id

    if 'start_btn' in triggered_id:
        tmp102_recording = True
        return 'Recording started...', 'Stop recording'
    else:
        tmp102_recording = False
        return 'Start recording', 'Recording stopped...'

@callback(
    Output(component_id="tmp102-temperature", component_property="figure"),
    [Input(component_id="interval-component", component_property="n_intervals"),
     Input(component_id="dropdown", component_property="value")]
)
def update_line_chart(n_intervals, axisSeries):
    global tmp102_df

    if tmp102_recording:
        # Read data from I2C device
        timestamp, runtime, temp = tmp102_read()

        # Append data to Pandas DataFrame
        newData = pd.DataFrame({"Timestamp": [timestamp], "Runtime (s)": [runtime],"Temperature (°C)": [temp]})
        tmp102_df = pd.concat([tmp102_df, newData], ignore_index=True)

    fig = px.line(tmp102_df, x=axisSeries, y="Temperature (°C)", title="TMP102 Data")
    return fig

def setup_dashboard(dashboard):
    dashboard.layout = html.Div(children=[
        html.H1(children='Sensorviz'),
        html.Button("Start recording", n_clicks=0, id="start_btn"),
        html.Button("Stop recording", n_clicks=0, id="stop_btn"),
        dcc.Graph(figure={}, id="tmp102-temperature"),
        html.P("Select time axis:"),
        dcc.Dropdown(
            id="dropdown",
            options=["Timestamp",
                     "Runtime (s)"],
                     value="Timestamp",
                     clearable=False,
        ),
        dcc.Interval(id="interval-component", interval=1000 * 1, n_intervals=0),
        ])
