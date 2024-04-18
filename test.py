import dash
from dash import dcc, html
from dash.dependencies import Input, Output

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
    html.Div(id='button-clicks-output', style={'textAlign': 'center'})
])

# Define callback to display text when button is clicked
@app.callback(
    Output('button-clicks-output', 'children'),
    [Input('button', 'n_clicks')]
)
def update_output(n_clicks):
    if n_clicks > 0:
        return "Time Taken: 20ms"
    else:
        return ""

if __name__ == '__main__':
    app.run_server(debug=True)
