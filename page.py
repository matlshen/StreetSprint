import dash
from dash import dcc, html
from dash.dependencies import Input, Output
from foliummap import getMap

# Create a Dash application
app = dash.Dash(__name__)

# Define the layout of the Dash application
app.layout = html.Div([
    html.H1("Welcome to StreetSprint", style={'textAlign': 'center'}),
    dcc.Dropdown(
        id='algorithm-dropdown',
        options=[
            {'label': 'Dijkstra', 'value': 'dijkstra'},
            {'label': 'Bellman-Ford', 'value': 'bellman-ford'}
        ],
        value=None,
        placeholder='Select an algorithm...',  # Custom placeholder text
        style={'width': '50%', 'margin': '20px auto'}
    ),
    html.Button('Begin', id='button', n_clicks=0, style={'margin': '20px auto', 'display': 'block'}),
    html.Div(id='map-container', children=[html.Iframe(id='map', srcDoc=getMap()._repr_html_(), style={'width': '80%', 'height': '100vh', 'border': '0'})], style={'display': 'flex', 'justifyContent': 'center', 'alignItems': 'center', 'height': '100vh'})
])

# Define callback to display Folium map when button is clicked
@app.callback(
    Output('folium-map', 'srcDoc'),
    [Input('button', 'n_clicks')]
)
def update_folium_map(n_clicks):
    if n_clicks > 0:
        return "You clicked the 'Begin' button!"
    else:
        return ''

if __name__ == '__main__':
    app.run_server(debug=True)
