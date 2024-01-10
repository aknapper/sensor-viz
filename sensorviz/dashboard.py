from dash import html, dcc, callback, Output, Input
import pandas as pd
import plotly.express as px

from devices.tmp102 import tmp102_read

tmp102_df = pd.DataFrame({'Timestamp (s)': [''], "Temperature (°C)": ['']})

@callback(
    Output(component_id="tmp102-temperature", component_property="figure"),
    Input(component_id="interval-component", component_property="n_intervals"),
)
def update_line_chart(n_intervals):
    global tmp102_df
    # Read data from I2C device
    time, temp = tmp102_read()

    # Append data to Pandas DataFrame
    newData = pd.DataFrame({"Timestamp (s)": [time], "Temperature (°C)": [temp]})
    tmp102_df = pd.concat([tmp102_df, newData], ignore_index=True)

    fig = px.line(tmp102_df, x="Timestamp (s)", y="Temperature (°C)", title="tmp102 data viz")
    return fig

def setup_dashboard(dashboard):
    dashboard.layout = html.Div(children=[
        html.H1(children='Sensorviz'),
        dcc.Graph(figure={}, id="tmp102-temperature"),
        dcc.Interval(id="interval-component", interval=1000 * 1, n_intervals=0),
        ])
