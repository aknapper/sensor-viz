from dash import html, dcc, callback, Output, Input, ctx
import plotly.express as px
from devices.tmp102.driver import TMP102

tmp102_dev = TMP102(dev_name="tmp102-1", bus_num=1, address=0x48)

# Callback for starting stopping data capture
@callback(
    [Output('start_btn', 'children'),
     Output('stop_btn', 'children')],
    [Input('start_btn', 'n_clicks'),
     Input('stop_btn', 'n_clicks')],
    prevent_initial_call=True
)
def update_recording(start, stop):
    if 'start_btn' in ctx.triggered_id:
        tmp102_dev.recording_data = True
        return 'Recording started...', 'Stop recording'
    else:
        tmp102_dev.recording_data = False
        return 'Start recording', 'Recording stopped...'

# Callback for data recording and updating grpah based on button data
@callback(
    Output(component_id="tmp102-temperature", component_property="figure"),
    [Input(component_id="interval-component", component_property="n_intervals"),
     Input(component_id="dropdown", component_property="value")]
)
def update_line_chart(n_intervals, axisSeries):
    if tmp102_dev.recording_data:
        # Read data from I2C device
        tmp102_dev.temp_data_capture()

    fig = px.line(tmp102_dev.dataFrame, x=axisSeries, y=tmp102_dev.sampleData[0], title="TMP102 Data")
    return fig

# tmp102 layout
tmp102_layout = html.Div(children=[
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
