import dash
from dash import dcc, html
from dash.dependencies import Input, Output, State
import foliummap
from street_sprint import StreetSprint

app = dash.Dash(__name__)
s = StreetSprint()
map = foliummap.Map()

def btnPress(algorithm, start_location, end_location):
    s.add_start_location(start_location + ", Gainesville, Florida")
    s.add_end_location(end_location + ", Gainesville, Florida")

    path, dist, completion_time = s.run_algorithm(algorithm)

    map.createMap(path)

    return f"Completion Time: {completion_time} seconds", f"Total Distance: {dist} meters", map.getMap()._repr_html_()

# Define the layout of the Dash application
app.layout = html.Div(
    [
        # Title, Inputs, and Results
        html.Div(
            [
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
                    style={'width': '70%', 'margin': '20px auto'}
                ),
                dcc.Input(
                    id='location1-input',
                    type='text',
                    placeholder='Enter start location',
                    style={'width': '55%', 'margin': '20px auto', 'textAlign': 'center', 'display': 'block'}
                ),
                dcc.Input(
                    id='location2-input',
                    type='text',
                    placeholder='Enter end location',
                    style={'width': '55%', 'margin': '20px auto', 'textAlign': 'center', 'display': 'block'}
                ),
                html.Button('Begin', id='button', n_clicks=0, style={'margin': '20px auto', 'display': 'block'}),
                html.Div(id='text-container', style={'margin': '20px auto', 'textAlign': 'center'}),
                html.Div(id='distance-container', style={'margin': '20px auto', 'textAlign': 'center'}),
            ], style={'float': 'left', 'width': '30%', 'margin-top': '10%'}
        ),

        # Map
        html.Div(
            [
                html.Div(id='map-container', children=[html.Iframe(id='map', srcDoc=map.getMap()._repr_html_(), style={'width': '100%', 'height': '100vh', 'border': '0'})],
                        style={'height': '100vh'})
            ], style={'float': 'right', 'width': '70%'}
        ),

        # Instruction Text
        html.Div(
            [
                html.P(
                    "Instructions: Select an Algorithm along with two locations inside of the black outline. These locations can be a known location (e.g. 'The Hub'), an address (e.g. '1765 Stadium Road'), or a street name (e.g. 'Stadium Road'). Any labeled street or building you can find on the map is a valid input as well.",
                    style={'position': 'absolute', 'bottom': '45px', 'left': '50%', 'transform': 'translateX(-50%)', 'font-size': '20px'}
                )
            ],
            style={'width': '100%', 'textAlign': 'center'}
        )
    ]
)

@app.callback(
    [Output('text-container', 'children'),
     Output('distance-container', 'children'),
     Output('map', 'srcDoc')],
    [Input('button', 'n_clicks')],
    [State('algorithm-dropdown', 'value'),
     State('location1-input', 'value'),
     State('location2-input', 'value')]
)

def update_text(n_clicks, algorithm, location1, location2):
    if n_clicks > 0 and algorithm and location1 and location2 and location1 != location2:
        return btnPress(algorithm, location1, location2)
    else:
        return dash.no_update

if __name__ == '__main__':
    app.run_server(debug=True)
