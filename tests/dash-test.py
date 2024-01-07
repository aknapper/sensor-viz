from dash import Dash, html, dcc, dash_table, callback, Output, Input
import pandas as pd
import plotly.express as px

# Incorporate data
dataframe = pd.read_csv('https://raw.githubusercontent.com/plotly/datasets/master/gapminder2007.csv')

app = Dash(__name__)

app.layout = html.Div(children=[
    html.H1(children='Sensorviz'),

    dcc.Graph(
        id='example-graph',
        figure={
            'data': [
                {'x': [1, 2, 3], 'y': [4, 1, 2], 'type': 'bar', 'name': 'Category 1'},
                {'x': [1, 2, 3], 'y': [2, 4, 5], 'type': 'bar', 'name': 'Category 2'},
            ],
            'layout': {
                'title': 'Bar Chart Example'
            }
        }
    ),

    # table from csv
    html.Div(children='table View'),
    dash_table.DataTable(data=dataframe.to_dict('records'), page_size=10),

    # ex histogram graph from csv
    html.Div(children='interactive histogram'),
    dcc.Graph(figure=px.histogram(dataframe, x='continent', y='lifeExp', histfunc='avg')),

    #  with controls
    html.Div(children='My First App with Data, Graph, and Controls'),
    html.Hr(),
    dcc.RadioItems(options=['pop', 'lifeExp', 'gdpPercap'], value='lifeExp', id='controls-and-radio-item'),
    dash_table.DataTable(data=dataframe.to_dict('records'), page_size=10),
    dcc.Graph(figure={}, id='controls-and-graph')
])

# Add controls to build the interaction
@callback(
    Output(component_id='controls-and-graph', component_property='figure'),
    Input(component_id='controls-and-radio-item', component_property='value')
)
def update_graph(col_chosen):
    fig = px.histogram(dataframe, x='continent', y=col_chosen, histfunc='avg')
    return fig

if __name__ == '__main__':
    app.run_server(debug=True)