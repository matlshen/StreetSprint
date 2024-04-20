import dash
from dash import dcc, html
from dash.dependencies import Input, Output, State
import foliummap

# Create a Dash application
app = dash.Dash(__name__)

map = foliummap.Map()

def btnPress(n_clicks, start_location, end_location):
    completion_time = 50

    coords = [
        [26.1 + (n_clicks * 0.1), -82.0 + (n_clicks * 0.1)],
        [26.1 + (n_clicks * 0.1), -82.1 + (n_clicks * 0.1)],
        [26.1 + (n_clicks * 0.1), -82.2 + (n_clicks * 0.1)],
        [26.2 + (n_clicks * 0.1), -82.2 + (n_clicks * 0.1)],
        [26.3 + (n_clicks * 0.1), -82.3 + (n_clicks * 0.1)]
    ]
    map.createMap(coords)

    return f"Completion Time: {completion_time}ms", map.getMap()._repr_html_()

# Define the layout of the Dash application
app.layout = html.Div([
    html.H1("Welcome to StreetSprint", style={'textAlign': 'center'}),
    dcc.Dropdown(
        id='algorithm-dropdown',
        options=[
            {'label': 'Dijkstra', 'value': 'dijkstra'},
            {'label': 'Bellman-Ford', 'value': 'bellman-ford'},
            {'label': 'A*', 'value': 'a-star'}
        ],
        value=None,
        placeholder='Select an algorithm...',  # Custom placeholder text
        style={'width': '50%', 'margin': '25px auto'}
    ),
    dcc.Input(
        id='location1-input',
        type='text',
        placeholder='Enter start location',
        style={'width': '35%', 'margin': '25px auto', 'textAlign': 'center', 'alignItems': 'center', 'display': 'block'}
    ),
    dcc.Input(
        id='location2-input',
        type='text',
        placeholder='Enter end location',
        style={'width': '35%', 'margin': '25px auto', 'textAlign': 'center', 'alignItems': 'center', 'display': 'block'}
    ),
    html.Button('Begin', id='button', n_clicks=0, style={'margin': '20px auto', 'display': 'block'}),
    html.Div(id='text-container', style={'margin': '20px auto', 'textAlign': 'center'}),
    html.Div(id='map-container', children=[html.Iframe(id='map', srcDoc=map.getMap()._repr_html_(), style={'width': '80%', 'height': '100vh', 'border': '0'})], style={'display': 'flex', 'justifyContent': 'center', 'alignItems': 'center', 'height': '100vh'})
])

# Define callback to display text when button is clicked
@app.callback(
    [Output('text-container', 'children'), Output('map', 'srcDoc')],
    [Input('button', 'n_clicks')],
    [State('algorithm-dropdown', 'value'),
     State('location1-input', 'value'),
     State('location2-input', 'value')]
)
def update_text(n_clicks, algorithm, location1, location2):
    if n_clicks > 0 and algorithm and location1 and location2 and location1 != location2:
        return btnPress(n_clicks, location1, location2)
    else:
        return dash.no_update

if __name__ == '__main__':
    app.run_server(debug=True)
