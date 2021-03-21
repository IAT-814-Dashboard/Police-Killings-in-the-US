import pandas as pd
import plotly.express as px  # (version 4.7.0)
import plotly.graph_objects as go

import dash  # (version 1.12.0) pip install dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output

app = dash.Dash(__name__)

#-----------------------------------------------------------

df = pd.read_csv('fatal-police-shootings-data.csv')
df['year'] = pd.DatetimeIndex(df['date']).year
df = df.groupby(['state','year'])['id'].count().reset_index().rename(columns={'id':'count'})

unique_years = list(df['year'].unique())
year_marks = {}
for i in range(len(unique_years)):
    year_marks[unique_years[i]] = unique_years[i]

#-----------------------------------------------------------

app.layout = html.Div([
    html.H1("Starting with the Project", style={'text_align':'center'}),
    
    
     html.P([
                    html.Label("Year"),
                     dcc.RangeSlider(
                    id = 'year_select',
                    min=2015,
                    max=2021,
                    step=None,
                    marks={
                                2015: '2015',
                                2016: '2016',
                                2017: '2017',
                                2018: '2018',
                                2019: '2019',
                                2020: '2020',
                                2021: '2021'
                    },
                    value=[2015, 2021]
    )], style = {'width' : '80%',
                                    'fontSize' : '20px',
                                    'padding-left' : '100px',
                                    'display': 'inline-block'}),
    html.Div(id='output_container', children=[]),
    html.Br(),
    
    dcc.Graph(id='my_map',figure={})
      
])

#-------------------------------------------------------------------

@app.callback(
    [Output(component_id='output_container', component_property='children'),
     Output(component_id='my_map', component_property='figure')],
    [Input(component_id='year_select', component_property='value')]
)
def update_graph(option_slctd):

    container = str(option_slctd[0]) + "to" + str(option_slctd[1])

    
    dff = df.copy()
    dff = dff[(dff["year"] >=option_slctd[0]) & (dff["year"] >=option_slctd[1])]

    # Plotly Express
    fig = px.choropleth(
        data_frame=dff,
        locationmode='USA-states',
        locations='state',
        scope="usa",
        color='count',
        hover_data=['state'],
        color_continuous_scale=px.colors.sequential.YlOrRd,
        labels={'state': 'count'},
        template='plotly_dark'
    )
    
    return container, fig

#--------------------------------------------------------------------
if __name__ == '__main__':
    app.run_server(debug=True)
    
