import pandas as pd
import plotly.express as px  # (version 4.7.0)
import plotly.graph_objects as go

import dash  # (version 1.12.0) pip install dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output

app = dash.Dash(__name__)

#--------------------------------------------------  ---------------------------------------------------------------------------------

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
            hover_data=['count'], barmode = 'stack', custom_data=['gender'])

 
#line chart
df_group_by_date = df.groupby('date')['name'].agg('count').reset_index().rename(columns={'name':'count'})
line_chart = px.line(df_group_by_date, x='date', y="count")


#-----------------------------------------------------------------------------------------------------------------------------------

app.layout = html.Div([
    
    #html.Div(id='test-output'),
    
    dcc.Graph(
                id='line-chart',
                figure=line_chart
    ),
    
    html.Div([
            dcc.Graph(
                        id='pie-chart-interaction',
                        figure=pie_chart,
                        config={#'responsive': True,
                                'doubleClick':'reset'},
            ),
            
            dcc.Graph(
                        id='stacked-bar-chart',
                        figure=stacked_bar,
                        #config={#'responsive': True,
                        #        'doubleClick':'reset'},
            ),
            
    ], style={'columnCount': 2}),
            
    dcc.Graph(
                id='choropleth-map',
                figure=choropleth_map,
                #config={#'responsive': True,
                #                'doubleClick':'reset'},
    ),
])

#-----------------------------------------------------------------------------------------------------------------------------------

"""
@app.callback(
    Output('test-output','children'),
    [Input('pie-chart-interaction', 'clickData'),
    Input('stacked-bar-chart', 'clickData'),
    Input('line-chart','relayoutData'),
    Input('choropleth-map','clickData')], prevent_initial_call=True)
def update_text_box(pieClick, stackBarClick, lineChartClick, mapClick):
    if pieClick:
        return "Race:{}".format(pieClick['points'][0]['label'])
    if stackBarClick:
        gender_id = stackBarClick['points'][0]['curveNumber']
        if gender_id==0:
            gender='Female'
        else:
            gender='Male'
            
        age = stackBarClick['points'][0]['x'] 
        return "Gender={}\nAge={}".format(gender, age)
"""

@app.callback(
    Output('choropleth-map', 'figure'),
    [Input('pie-chart-interaction', 'clickData'),
    Input('stacked-bar-chart', 'clickData'),
    Input('line-chart','relayoutData')], prevent_initial_call=True)
def update_choropleth_map(pieClick, stackBarClick, lineChartClick):
    print('-------------------------------------')
    print("Inside update choropleth function")
    print("Pie click:",pieClick)
    print("Stacked Bar Click:",stackBarClick)
    print("Line chart click:",lineChartClick)
    
    if pieClick:
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
        
    if stackBarClick:
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
        
    if lineChartClick:
        startDate = lineChartClick['xaxis.range[0]']
        endDate = lineChartClick['xaxis.range[1]']
    
        filter_by_date = df[(df['date']>=startDate) & (df['date']<=endDate)]
        df_group_by_state = filter_by_date.groupby('state')['name'].agg('count').reset_index().rename(columns={'name':'count'})
        
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
     Input('stacked-bar-chart', 'clickData'),
     Input('line-chart','relayoutData')], prevent_initial_call=True)
def update_pie_chart(mapClick, stackBarClick, lineChartClick):
    print('-------------------------------------')
    print("Inside update pie chart function")
    print("Map click:",mapClick)
    print("Stacked Bar Click:",stackBarClick)
    print("Line chart click:",lineChartClick)
    if mapClick:
        filter_by_location = df[df['state']==mapClick['points'][0]['location']]
        df_group_by_race = filter_by_location.groupby('race')['name'].agg('count').reset_index().rename(columns={'name':'count'})
        pie_chart = go.Figure(data=[go.Pie(labels=df_group_by_race['race'], values=df_group_by_race['count'], title='Ethnicity Versus Killings', textinfo='label+percent',
                                 insidetextorientation='radial')])
    
    if stackBarClick:
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
        
    if lineChartClick:
  
        startDate = lineChartClick['xaxis.range[0]']
        endDate = lineChartClick['xaxis.range[1]']
    
        filter_by_date = df[(df['date']>=startDate) & (df['date']<=endDate)]
        df_group_by_race = filter_by_date.groupby('race')['name'].agg('count').reset_index().rename(columns={'name':'count'})
    
        pie_chart = go.Figure(data=[go.Pie(labels=df_group_by_race['race'], values=df_group_by_race['count'], title='Ethnicity Versus Killings', textinfo='label+percent',
                                        insidetextorientation='radial')])
        
       
            
    return pie_chart

@app.callback(
    Output('stacked-bar-chart', 'figure'),
    [Input('choropleth-map', 'clickData'),
     Input('pie-chart-interaction', 'clickData'),
     Input('line-chart','relayoutData')], prevent_initial_call=True)
def update_bar_chart(mapClick, pieClick, lineChartClick):
    print('-------------------------------------')
    print("Inside update bar chart function")
    print("Map click:",mapClick)
    print("Pie click:",pieClick)
    print("Line chart click:",lineChartClick)
    
    if mapClick:
        filter_by_location = df[df['state']==mapClick['points'][0]['location']]
        df_group_by_age_gender = filter_by_location.groupby(['age_bins','gender'])['name'].agg('count').reset_index().rename(columns={'name':'count'})
        stacked_bar = px.bar(df_group_by_age_gender, x="age_bins", y="count", color="gender",
                            hover_data=['count'], barmode = 'stack', custom_data=['gender'])

    if pieClick:
        filter_by_race = df[df['race']==str(pieClick['points'][0]['label'])]
        df_group_by_age_gender = filter_by_race.groupby(['age_bins','gender'])['name'].agg('count').reset_index().rename(columns={'name':'count'})
        
        stacked_bar = px.bar(df_group_by_age_gender, x="age_bins", y="count", color="gender",
                            hover_data=['count'], barmode = 'stack' , custom_data=['gender'])
        
    if lineChartClick:     
        startDate = lineChartClick['xaxis.range[0]']
        endDate = lineChartClick['xaxis.range[1]']
    
        filter_by_date = df[(df['date']>=startDate) & (df['date']<=endDate)]
        df_group_by_age_gender = filter_by_date.groupby(['age_bins','gender'])['name'].agg('count').reset_index().rename(columns={'name':'count'})
    
        stacked_bar = px.bar(df_group_by_age_gender, x="age_bins", y="count", color="gender",
                            hover_data=['count'], barmode = 'stack' , custom_data=['gender'])
      
                
    return stacked_bar

@app.callback(
    Output('line-chart', 'figure'),
    [Input('choropleth-map', 'clickData'),
     Input('pie-chart-interaction', 'clickData'),
     Input('stacked-bar-chart','clickData')], prevent_initial_call=True)
def update_line_chart(mapClick, pieClick, stackBarClick):
    print('-------------------------------------')
    print("Inside update line chart function")
    print("Map click:",mapClick)
    print("Pie click:",pieClick)
    print("Stacked Bar Click:",stackBarClick)
    
    if mapClick:
        filter_by_location = df[df['state']==mapClick['points'][0]['location']]
        df_group_by_date = filter_by_location.groupby('date')['name'].agg('count').reset_index().rename(columns={'name':'count'})
        line_chart = px.line(df_group_by_date, x='date', y="count")
       

    if pieClick:
        filter_by_race = df[df['race']==str(pieClick['points'][0]['label'])]
        df_group_by_date = filter_by_race.groupby('date')['name'].agg('count').reset_index().rename(columns={'name':'count'})
        line_chart = px.line(df_group_by_date, x='date', y="count")
        
    if stackBarClick:
        gender_id = stackBarClick['points'][0]['curveNumber']
        if gender_id==0:
            gender='Female'
        else:
            gender='Male'
            
        age = stackBarClick['points'][0]['x']
        filter_by_age_gender = df[(df['gender']==gender) & (df['age_bins']==age)]
        df_group_by_date = filter_by_age_gender.groupby('date')['name'].agg('count').reset_index().rename(columns={'name':'count'})
        line_chart = px.line(df_group_by_date, x='date', y="count")
        
    return line_chart

#-----------------------------------------------------------------------------------------------------------------------------------

if __name__ == '__main__':
    #app.run_server(debug=True)
    app.run_server(debug=True, dev_tools_ui=False)

    
