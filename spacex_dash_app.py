import dash
from dash import dcc, html
from dash.dependencies import Input, Output
import pandas as pd
import plotly.express as px

# Read the dataset
spacex_df = pd.read_csv('spacex_launch_dash.csv')

# Generate the options list for the dropdown
launch_sites = spacex_df['Launch Site'].unique()
options = [{'label': 'All Sites', 'value': 'ALL'}] + [{'label': site, 'value': site} for site in launch_sites]

# Initialize the Dash app
app = dash.Dash(__name__)

# Define the layout of the app
app.layout = html.Div([
    # Dropdown component
    dcc.Dropdown(
        id='site-dropdown',
        options=options,
        value='ALL',
        placeholder='Select a Launch Site here',
        searchable=True
    ),
    # Pie chart component
    html.Div(dcc.Graph(id='success-pie-chart')),
    # Range slider component
    dcc.RangeSlider(
        id='payload-slider',
        min=0, max=10000, step=1000,
        marks={i: str(i) for i in range(0, 10001, 1000)},
        value=[spacex_df['Payload Mass (kg)'].min(), spacex_df['Payload Mass (kg)'].max()]
    ),
    # Scatter plot component
    html.Div(dcc.Graph(id='success-payload-scatter-chart'))
])

# Callback to update the success pie chart based on the selected launch site
@app.callback(
    Output(component_id='success-pie-chart', component_property='figure'),
    [Input(component_id='site-dropdown', component_property='value')]
)
def get_pie_chart(entered_site):
    if entered_site == 'ALL':
        fig = px.pie(
            spacex_df,
            names='class',
            title='Total Success Launches for All Sites',
            labels={'class': 'Launch Outcome'},
            hole=0.3
        )
    else:
        filtered_df = spacex_df[spacex_df['Launch Site'] == entered_site]
        fig = px.pie(
            filtered_df,
            names='class',
            title=f'Total Success Launches for site {entered_site}',
            labels={'class': 'Launch Outcome'},
            hole=0.3
        )
    return fig

# Callback to update the success-payload scatter plot based on the selected launch site and payload range
@app.callback(
    Output(component_id='success-payload-scatter-chart', component_property='figure'),
    [Input(component_id='site-dropdown', component_property='value'),
     Input(component_id='payload-slider', component_property='value')]
)
def update_scatter_chart(selected_site, selected_payload):
    filtered_df = spacex_df[
        (spacex_df['Payload Mass (kg)'] >= selected_payload[0]) &
        (spacex_df['Payload Mass (kg)'] <= selected_payload[1])
    ]
    
    if selected_site != 'ALL':
        filtered_df = filtered_df[filtered_df['Launch Site'] == selected_site]
    
    fig = px.scatter(
        filtered_df,
        x='Payload Mass (kg)',
        y='class',
        color='Booster Version Category',
        title='Payload vs. Outcome Scatter Plot',
        labels={'class': 'Launch Outcome'}
    )
    return fig

# Run the app
if __name__ == '__main__':
    app.run_server(debug=True)
