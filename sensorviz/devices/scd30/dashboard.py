from devices.scd30.driver import SCD30
from dash import html, dcc, callback, Output, Input, ctx
import plotly.express as px
import pandas as pd

SCD30_GRAPH_REFRESH_MS = 1000       # graph refresh rate (ms)
scd30_dev = SCD30(dev_name="scd30-1")

# Callback for starting stopping data capture, updating button text
@callback(
    [Output('scd30_start_btn', 'children'),
     Output('scd30_stop_btn', 'children')],
    [Input('scd30_start_btn', 'n_clicks'),
     Input('scd30_stop_btn', 'n_clicks')],
    prevent_initial_call=True
)
def startstop_sampling(start, stop):
    if 'scd30_start_btn' in ctx.triggered_id:
        if not scd30_dev.dataLogProc.is_alive():
            scd30_dev.initProc()
        return 'Recording started...', 'Stop recording'
    elif 'scd30_stop_btn' in ctx.triggered_id:
        if scd30_dev.dataLogProc.is_alive():
            scd30_dev.resetProc()
        return 'Start recording', 'Recording stopped...'
    
# Callback for updating graph based at fixed interval and on new x-asix selection
@callback(
    Output(component_id="scd30_graph", component_property="figure"),
    [Input(component_id="scd30_graph_refresh", component_property="n_intervals"),
     Input(component_id="scd30_dropdown", component_property="value")]
)
def update_graph(n_intervals, axisSeries):
    df = pd.DataFrame({'Timestamp': [''], 'Runtime (s)': [''], scd30_dev.sampleData[0]: ['']})
    df = pd.read_csv(scd30_dev.csvFileLoc)
    fig = px.line(df, x=axisSeries, y=scd30_dev.sampleData, title="SCD30 Data")
    return fig

@callback(
    Output("scd30_sample_rate", "value"),
    Input("scd30_sample_rate", "value"),
)
def sync_input(sample_rate):
    scd30_dev.dataLogFreq = sample_rate/1000
    return sample_rate

# scd30 layout
scd30_layout = html.Div(children=[
    html.H1(" "),
    html.Div("Sampling Frequency", style={"font-size": "18px"}),
    "CO2 Concentration ",
    dcc.Input(id="scd30_sample_rate", value = 1500, type="number", step=100), " ms",
    html.H1(" "),
    html.Button("Start recording", n_clicks=0, id="scd30_start_btn"),
    html.Button("Stop recording", n_clicks=0, id="scd30_stop_btn"),
    dcc.Graph(figure={}, id="scd30_graph"),
    html.P("Select time axis:"),
    dcc.Dropdown(
        id="scd30_dropdown",
        options=["Timestamp",
                    "Runtime (s)"],
                    value="Runtime (s)",
                    clearable=False,
    ),
    dcc.Interval(id="scd30_graph_refresh", interval=SCD30_GRAPH_REFRESH_MS, n_intervals=0),
])