from devices.tmp102.driver import TMP102

from dash import html, dcc, callback, Output, Input, ctx
import plotly.express
import pandas as pd

TMP102_GRAPH_REFRESH_MS = 1000       # graph refresh rate (ms)
tmp102_dev = TMP102(dev_name="tmp102-1", bus_num=1, address=0x48)

# Callback for starting stopping data capture, updating button text
@callback(
    [Output('tmp102_start_btn', 'children'),
     Output('tmp102_stop_btn', 'children')],
    [Input('tmp102_start_btn', 'n_clicks'),
     Input('tmp102_stop_btn', 'n_clicks')],
    prevent_initial_call=True
)
def startstop_sampling(start, stop):
    if 'tmp102_start_btn' in ctx.triggered_id:
        if not tmp102_dev.dataLogProc.is_alive():
            tmp102_dev.initProc()
        return 'Recording started...', 'Stop recording'
    elif 'tmp102_stop_btn' in ctx.triggered_id:
        if tmp102_dev.dataLogProc.is_alive():
            tmp102_dev.resetProc()
        return 'Start recording', 'Recording stopped...'

# Callback for updating graph based at fixed interval and on new x-asix selection
@callback(
    Output(component_id="tmp102_graph", component_property="figure"),
    [Input(component_id="tmp102_graph_refresh", component_property="n_intervals"),
     Input(component_id="tmp102_dropdown", component_property="value")]
)
def update_graph(n_intervals, axisSeries):
    df = pd.DataFrame({'Timestamp': [''], 'Runtime (s)': [''], tmp102_dev.sampleData[0]: ['']})
    df = pd.read_csv(tmp102_dev.csvFileLoc)
    fig = plotly.express.line(df, x=axisSeries, y=tmp102_dev.sampleData[0], title="TMP102 Data")
    return fig

@callback(
    Output("tmp102_sample_rate", "value"),
    Input("tmp102_sample_rate", "value"),
)
def sync_input(sample_rate):
    tmp102_dev.dataLogFreq = sample_rate/1000
    return sample_rate

# tmp102 layout
tmp102_layout = html.Div(children=[
    html.H1(" "),
    html.Div("Sampling Frequency", style={"font-size": "18px"}),
    "Temperature ",
    dcc.Input(id="tmp102_sample_rate", value = 1000, type="number", step=100), " ms",
    html.H1(" "),
    html.Button("Start recording", n_clicks=0, id="tmp102_start_btn"),
    html.Button("Stop recording", n_clicks=0, id="tmp102_stop_btn"),
    dcc.Graph(figure={}, id="tmp102_graph"),
    html.P("Select time axis:"),
    dcc.Dropdown(
        id="tmp102_dropdown",
        options=["Timestamp",
                    "Runtime (s)"],
                    value="Runtime (s)",
                    clearable=False,
    ),
    dcc.Interval(id="tmp102_graph_refresh", interval=TMP102_GRAPH_REFRESH_MS, n_intervals=0),
])
