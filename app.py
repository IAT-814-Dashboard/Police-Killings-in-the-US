import pandas as pd
import plotly.express as px  # (version 4.7.0)
import plotly.graph_objects as go

import dash  # (version 1.12.0) pip install dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output

app = dash.Dash(__name__)

#-----------------------------------------------------------------------------------------------------------------------------------

styles = {
    'pre': {
        'border': 'thin lightgrey solid',
        'overflowX': 'scroll'
    }
}


df = pd.read_json('police-killings-integrated-dataset-2021-03-20.json.gz')

#Pie chart
df_group_by_race = df.groupby('race')['name'].agg('count').reset_index().rename(columns={'name':'count'})
pie_chart = go.Figure(data=[go.Pie(labels=df_group_by_race['race'], values=df_group_by_race['count'], title='Ethnicity Versus Killings', textinfo='label+percent',
                             insidetextorientation='radial')])

#Choropleth map
df_group_by_state = df.groupby('state')['name'].agg('count').reset_index().rename(columns={'name':'count'})
choropleth_map = go.Figure(data=go.Choropleth(
    locations=df_group_by_state['state'],
    z = df_group_by_state['count'],
    locationmode = 'USA-states',
    colorscale = 'Blues',
    colorbar_title = "Number of Deaths"
))
choropleth_map.update_layout(
    title_text = 'Police Shooting Deaths by US States',
    geo_scope='usa'
)
choropleth_map.update_layout(clickmode='event+select')

#stacked bar chart
df_group_by_age_gender = df.groupby(['age_bins','gender'])['name'].agg('count').reset_index().rename(columns={'name':'count'})
stacked_bar = px.bar(df_group_by_age_gender, x="age_bins", y="count", color="gender",
            hover_data=['count'], barmode = 'stack')
 

#-----------------------------------------------------------------------------------------------------------------------------------

app.layout = html.Div([
    
    html.Div([
            dcc.Graph(
                        id='pie-chart-interaction',
                        figure=pie_chart
            ),
            
            dcc.Graph(
                        id='stacked-bar-chart',
                        figure=stacked_bar
            ),
    ], style={'columnCount': 2}),
            
    dcc.Graph(
                id='choropleth-map',
                figure=choropleth_map
    ),
])

#-----------------------------------------------------------------------------------------------------------------------------------

@app.callback(
    Output('choropleth-map', 'figure'),
    [Input('pie-chart-interaction', 'clickData'),
    Input('stacked-bar-chart', 'clickData')], prevent_initial_call=True)
def update_choropleth_map(pieClick, stackBarClick):
    
    print("Inside update choropleth function")
    print(pieClick)
    print(stackBarClick)
    
    if pieClick is not None:
        filter_by_race = df[df['race']==str(pieClick['points'][0]['label'])]
        df_group_by_state = filter_by_race.groupby('state')['name'].agg('count').reset_index().rename(columns={'name':'count'})
        choropleth_map = go.Figure(data=go.Choropleth(
        locations=df_group_by_state['state'],
        z = df_group_by_state['count'],
        locationmode = 'USA-states',
        colorscale = 'Blues',
        colorbar_title = "Deaths"
        ))
        choropleth_map.update_layout(
            title_text = 'Police Shooting Deaths by US States',
            geo_scope='usa'
        )
        
    if stackBarClick is not None:
        gender_id = stackBarClick['points'][0]['curveNumber']
        if gender_id==0:
            gender='Female'
        else:
            gender='Male'
            
        age = stackBarClick['points'][0]['x']
        filter_by_age_gender = df[(df['gender']==gender) & (df['age_bins']==age)]
        df_group_by_state = filter_by_age_gender.groupby('state')['name'].agg('count').reset_index().rename(columns={'name':'count'})
        
        choropleth_map = go.Figure(data=go.Choropleth(
        locations=df_group_by_state['state'],
        z = df_group_by_state['count'],
        locationmode = 'USA-states',
        colorscale = 'Blues',
        colorbar_title = "Deaths"
        ))
        choropleth_map.update_layout(
            title_text = 'Police Shooting Deaths by US States',
            geo_scope='usa'
        )
    return choropleth_map
        
@app.callback(
    Output('pie-chart-interaction', 'figure'),
    [Input('choropleth-map', 'clickData'),
     Input('stacked-bar-chart', 'clickData')], prevent_initial_call=True)
def update_pie_chart(mapClick, stackBarClick):
    print("Inside update pie chart function")
    print(mapClick)
    print(stackBarClick)
    if mapClick is not None:
        filter_by_location = df[df['state']==mapClick['points'][0]['location']]
        df_group_by_race = filter_by_location.groupby('race')['name'].agg('count').reset_index().rename(columns={'name':'count'})
        pie_chart = go.Figure(data=[go.Pie(labels=df_group_by_race['race'], values=df_group_by_race['count'], title='Ethnicity Versus Killings', textinfo='label+percent',
                                 insidetextorientation='radial')])
    
    if stackBarClick is not None:
        gender_id = stackBarClick['points'][0]['curveNumber']
        if gender_id==0:
            gender='Female'
        else:
            gender='Male'
            
        age = stackBarClick['points'][0]['x']
        filter_by_age_gender = df[(df['gender']==gender) & (df['age_bins']==age)]
        df_group_by_race = filter_by_age_gender.groupby('race')['name'].agg('count').reset_index().rename(columns={'name':'count'})
        
        pie_chart = go.Figure(data=[go.Pie(labels=df_group_by_race['race'], values=df_group_by_race['count'], title='Ethnicity Versus Killings', textinfo='label+percent',
                                 insidetextorientation='radial')])
    return pie_chart

@app.callback(
    Output('stacked-bar-chart', 'figure'),
    [Input('choropleth-map', 'clickData'),
     Input('pie-chart-interaction', 'clickData')], prevent_initial_call=True)
def update_bar_chart(mapClick, pieClick):
    print("Inside update bar chart function")
    print(mapClick)
    print(pieClick)
    
    if mapClick is not None:
        filter_by_location = df[df['state']==mapClick['points'][0]['location']]
        df_group_by_age_gender = filter_by_location.groupby(['age_bins','gender'])['name'].agg('count').reset_index().rename(columns={'name':'count'})
        stacked_bar = px.bar(df_group_by_age_gender, x="age_bins", y="count", color="gender",
                            hover_data=['count'], barmode = 'stack')
        
        
    if pieClick is not None:
        filter_by_race = df[df['race']==str(pieClick['points'][0]['label'])]
        df_group_by_age_gender = filter_by_race.groupby(['age_bins','gender'])['name'].agg('count').reset_index().rename(columns={'name':'count'})
        
        stacked_bar = px.bar(df_group_by_age_gender, x="age_bins", y="count", color="gender",
                            hover_data=['count'], barmode = 'stack')
        
    return stacked_bar


#-----------------------------------------------------------------------------------------------------------------------------------
if __name__ == '__main__':
    app.run_server(debug=True)
    
