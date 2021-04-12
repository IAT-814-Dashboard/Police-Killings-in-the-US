import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime,date

import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output
from visualization_helper_functions import *
import dash_bootstrap_components as dbc

app = dash.Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP])

df = pd.read_json('data/police-killings-integrated-dataset-2021-03-20.json.gz')
gun_data = pd.read_csv('data/gun-data-by-year.csv')

viz_states = {'bar_chart_race':0, 'choropleth_map':0, 'line_chart':0, 'bar_chart_age':0, 'bar_chart_mental':0, 'radar_chart_weapons':0, 'gun_chart':0}

#-----------------------------------------------------------------------------------------------------------------------------------

app.layout = html.Div([

#title
    html.Div([
        html.Div([
            html.H1(children='IAT 814: Police Killings in the United States',
                    style = {'textAlign' : 'center',
                             'color': 'white',
                             'font-family': 'Georgia',
                             'font-size': '50px',
                             'font-weight': 'bold',
                             'letter-spacing': '-1px',
                             'line-height': '1' }
            )],
            className='title',
            style = {'padding-top' : '1%',
                     'padding-bottom': '1%'}),
        ],
        className = 'heading-row',
        style = {'height' : '4%',
                'border': 'solid black',
                'border-color': 'black',
                'border-width': ' 10px 10px 10px 10px',
                'background-color' : '#488A99',
                'box-shadow': 'rgb(38, 57, 77) 0px 20px 30px -10px',
                'margin-top': '55px',
                'margin-left': '35px',
                'margin-right': '35px',}
    ),

    html.Div([
                dcc.DatePickerRange(id='my-date-picker-range',
                                    min_date_allowed=date(2015, 1, 1),
                                    max_date_allowed=date(2021, 3, 31),
                                    initial_visible_month=date(2017, 1, 1),
                                    end_date=date(2019, 1, 1),
                                    style={'width':'600px','height':'200px',
                                            'font-size':'30px'}
                                    ),
                html.Div(id='slider-output-container')
    ],style={'margin-left':'100px',}),
#line chart per year+information box+indicator graph
    html.Div([
        html.Div([
                html.H3('Police Killings by Year',
                        style={
                                'textAlign':'center',
                                'color': 'black',
                                'font-family': 'Georgia',
                                'font-size': '38px',
                                'margin-bottom':'10px',
                                'font-weight': 'bold',
                                'line-height': '1',
                                }),
                dcc.Loading(dcc.Graph(
                        id='line-chart',
                        figure=create_line_chart(df)
                ))], style={'flex':'60%',
                            'margin-right':'20px',
                            'border': 'solid white',
                            'border-color': 'white',
                            'border-width': ' 5px 5px 5px 5px',
                            'box-shadow': 'rgb(38, 57, 77) 0px 20px 30px -10px',
                            'padding':'20px', 'background-color':'#c8d7e3'}
                , className='line-chart-block'),




        html.Div([
            html.H3(children='Total Number of Police Killings',
                    style={
                            'textAlign':'center',
                            'color': 'black',
                            'font-family': 'Georgia',
                            'font-size': '38px',
                            'margin-top':'50px',
                            'margin-bottom':'10px',
                            'font-weight': 'bold',
                            'line-height': '1',
                            }),
            html.Div(dcc.Loading(
                        dcc.Graph(
                                id="indicator-graph",
                                figure=indicator_graph(len(df)),
                                )),
                    style={'margin-left':'170px',}
                    ),
            html.Img(src='assets/gun_logo.png',width='50%', height='20%',),
            #html.A(html.Button('Refresh Data'),href='/'),
            html.A(html.Button('RESET ALL',id='reset_button', n_clicks=0,
                        style={'background-color': '#DADADA',
                                'border':'none',
                                'padding': '15px 32px',
                                'box-shadow': 'rgb(38, 57, 77) 0px 20px 30px -10px',
                                'display':'inline-block',
                                'width':'80%',
                                'height':'120px',
                                'margin-top':'30px',
                                'text-align': 'center',
                                'text-decoration': 'none',
                                'display': 'inline-block',
                                'font-size': '30px'}), href='/'),
            ],
            style={'flex':'25%',
                    'background-color': '#c8d7e3',
                    'text-align':'center',
                    'border': 'solid white',
                    'box-shadow': 'rgb(38, 57, 77) 0px 20px 30px -10px',
                    'border-color': 'white',
                    'border-width': ' 5px 5px 5px 5px',
                    'padding':'20px'}),

        html.Div([
            html.P('Police brutality is the use of excessive or unnecessary force by personnel affiliated with law enforcement duties when dealing with suspects and civilians.\
                   Police violence is a leading cause of death for young men in the United States.\
                   This dashboard can be used to explore the possible causes for Police Killings in the United States.',
                   style={'padding-top':'60px'}),
            html.Br(),
            #html.P('There has been 900 fatal police shooting every year since 2005')

            html.P(html.Strong(html.Center('ALL LIVES MATTER')),style={'font-size': '50px'})
        ], style={'float':'left','flex':'25%',
                 'text-align':'center',
                 'background-color':'#c8d7e3',
                 'box-shadow': 'rgb(38, 57, 77) 0px 20px 30px -10px',
                  'font-family': 'Georgia',
                  'font-size': '40px',
                  'padding':'20px',
                  'border': 'solid white',
                  'border-color': 'white',
                  'border-width': '5px 5px 5px 5px',
                  }),
    ],
    className='information-bar',
    style={'display':'flex',
           'height':'50%',
           'margin-top':'30px',
           'margin-left': '35px',
           'margin-right': '35px',
           }
    ),



#gun purchase per year+ choropleth map
    html.Div([
        html.Div([
            html.H3('Purchase of Gun By Year',
                    style={
                            'textAlign':'center',
                            'color': 'black',
                            'font-family': 'Georgia',
                            'font-size': '38px',
                            'margin-bottom':'10px',
                            'font-weight': 'bold',
                            'line-height': '1'}),
            dcc.Loading(dcc.Graph(
                    id='gun-line-chart',
                    figure=create_line_chart_gun_data(gun_data)
            )),
        ], style={'flex':'60%',
                    'background-color':'#c8d7e3',
                    'box-shadow': 'rgb(38, 57, 77) 0px 20px 30px -10px',
                    'border': 'solid white',
                    'border-color': 'white',
                    'border-width': ' 5px 5px 5px 5px',
                    'padding':'20px',
                    'margin-left': '20px',
                    'margin-right': '20px',}),
        html.Div([
                html.H3('Police Killings by State',
                        style={
                                'textAlign' : 'center',
                                'color': 'black',
                                'font-family': 'Georgia',
                                'margin-bottom':'25px',
                                'font-size': '38px','font-weight': 'bold',
                                'line-height': '1'}),
                dcc.Loading(dcc.Graph(
                        id='choropleth-map',
                        figure=create_choropleth_map(df),
                ))], style={'flex':'40%',
                            'margin-right':'20px',
                            'border': 'solid white',
                            'border-color': 'white',
                            'border-width': ' 5px 5px 5px 5px',
                            'box-shadow': 'rgb(38, 57, 77) 0px 20px 30px -10px',
                            'padding':'20px', 'padding-left':'30px','background-color':'#c8d7e3'}
                ,className='map-block'),

    ],
    className='year-state',
    style={'display':'flex',
        'background-color':'#c8d7e3',
           'height':'100%',
           'margin-top':'30px',
           'margin-left': '35px',
           'margin-right': '35px',}
    ),



#race+age-gender+mentalillness
html.Div([
    html.Div([
            html.H3('Police Killings by Race',
                    style={
                            'textAlign' : 'center',
                            'color': 'black',
                            'font-family': 'Georgia',
                            'margin-bottom':'10px',
                            'font-size': '38px',
                            'font-weight': 'bold',
                            'line-height': '1'}),
            dcc.Graph(
                    id='bar-chart-race',
                    figure=create_bar_char_for_race(df),
                    config={'doubleClick':'reset'},
                    #config={#'responsive': True,
                    #            'doubleClick':'reset'},
            )], style={'flex':'34%',
                        'border': 'solid white',
                        'border-color': 'white',
                        'border-width': '5px 5px 5px 5px',
                        'box-shadow': 'rgb(38, 57, 77) 0px 20px 30px -10px',
                        #'padding'
                        'padding':'20px', 'background-color':'#c8d7e3'
                        }
                        #'border-radius': '15px'}

            , className='pie-block'),

    html.Div([
            html.H3('Police Killings by Age and Gender',
                    style={
                            'textAlign' : 'center',
                            'color': 'black',
                            'margin-bottom':'10px',
                            'font-size': '38px',
                            'font-family': 'Georgia',
                            'font-weight': 'bold',
                            'line-height': '1'}),
            dcc.Graph(
                    id='bar-chart-age',
                    figure=create_bar_chart_for_age_and_gender(df),
                    config={'doubleClick':'reset'},
            )], style={'flex':'33%',
                        'border': 'solid white',
                        'border-color': 'white',
                        'border-width': '5px 5px 5px 0px',
                        'box-shadow': 'rgb(38, 57, 77) 0px 20px 30px -10px',
                        'padding':'20px', 'background-color':'#c8d7e3'
                        }
                        #'border-radius': '15px'}

            , className='stacked-bar-block'),

    html.Div([
            html.H3('Police Killings by Signs of Mental Illness',
                    style={
                            'textAlign' : 'center',
                            'color': 'black',
                            'margin-bottom':'10px',
                            'font-size': '38px',
                            'font-family': 'Georgia',
                            'font-weight': 'bold',
                            'line-height': '1'}),
            dcc.Graph(
                    id='mental-illness-bar',
                    figure=create_bar_chart_for_mental_illness(df),
                    config={'doubleClick':'reset'},
            )], style={'flex':'34%',
                        'padding-left':'50px',
                        'border': 'solid white',
                        'border-color': 'white',
                        'border-width': '5px 5px 5px 0px',
                        'box-shadow': 'rgb(38, 57, 77) 0px 20px 30px -10px',
                        'padding':'20px', 'background-color':'#c8d7e3'
                        }

            , className='stacked-bar-block'),

],
className='bar-chart-block',
style={'display':'flex',
       'height':'100%',
       'margin-top':'30px',
       'margin-left': '35px',
       'margin-right': '35px',
       }
),


#radar chart+sankey diagram
    html.Div([
        html.Div([
                html.H3('Police Killings by Weapons',
                        style={
                                'textAlign' : 'center',
                                'color': 'black',
                                'margin-bottom':'10px',
                                'font-size': '38px',
                                'font-family': 'Georgia',
                                'font-weight': 'bold',
                                'line-height': '1'}),
                dcc.Graph(
                id='radar-chart-weapons',
                figure=create_radar_chart_for_weapons(df),
                )], style={'flex':'30%',
                            'border': 'solid white',
                            'border-color': 'white',
                            'border-width': ' 5px 5px 5px 5px',
                            'box-shadow': 'rgb(38, 57, 77) 0px 20px 30px -10px',
                            'padding':'20px', 'background-color':'#c8d7e3'}
                ,className='map-block'),

        html.Div([
                html.H3('Sankey Diagram',
                        style={
                                'textAlign' : 'center',
                                'color': 'black',
                                'margin-bottom':'10px',
                                'font-size': '38px',
                                'font-family': 'Georgia',
                                'font-weight': 'bold',
                                'line-height': '1'}),
                dcc.Graph(
                        id='sankey-diagram',
                        figure=create_sankey_diagram(df),
                        style={'margin-left':'50px', 'margin-right':'50px'}

                )], style={'flex':'80%',
                            'border': 'solid white',
                            'border-color': 'white',
                            'border-width': '5px 5px 5px 0px',
                            'box-shadow': 'rgb(38, 57, 77) 0px 20px 30px -10px',
                            'padding':'20px', 'background-color':'#c8d7e3'
                            }
                , className='sankey-block'),

    ],
    className='sankey-weapon',
    style={'display':'flex',
           'height':'100%',
           'margin-top':'30px',
           'margin-left': '35px',
           'margin-right': '35px',
           'margin-bottom':'70px'}
    ),
#intermediate values
    html.Div(id='triggered_element', style={'display': 'none'}),
    html.Div(id='intermediate-value-line-chart-year', style={'display': 'none'}),
    html.Div(id='intermediate-value-bar-chart-race', style={'display': 'none'}),
    html.Div(id='intermediate-value-choropleth-map', style={'display': 'none'}),
    html.Div(id='intermediate-value-bar-chart-age', style={'display': 'none'}),
    html.Div(id='intermediate-value-bar-chart-mental', style={'display': 'none'}),
    html.Div(id='intermediate-value-radar-chart-weapons', style={'display': 'none'}),
    html.Div(id='reset-viz-states', style={'display': 'none'})



], style={})

#-----------------------------------------------------------------------------------------------------------------------------------

def get_viz_info(lineChartClick, gunClick, mapClick, raceBarChartClick, ageBarClick, mentalBarClick):
    startDate=gunStartDate="01/01/2015"
    endDate=gunEndDate="01/01/2021"
    state = df['state'].unique()
    race = df['race'].unique()
    gender = df['gender'].unique()
    age = df['age_bins'].unique()
    mental_illness_value = df['signs_of_mental_illness'].unique()
    if lineChartClick is not None:
        startDate = lineChartClick['xaxis.range[0]']
        endDate = lineChartClick['xaxis.range[1]']
    if gunClick is not None:
        gunStartDate = gunClick['xaxis.range[0]']
        gunEndDate = gunClick['xaxis.range[1]']
    if mapClick is not None:
        state = [mapClick['points'][0]['location']]
    if raceBarChartClick is not None:
        race = [raceBarChartClick['points'][0]['x']]
    if ageBarClick is not None:
        gender, age= get_age_and_gender(ageBarClick)
        gender = [gender]
        age = [age]
    if mentalBarClick is not None:
        mental_illness_value = [mentalBarClick['points'][0]['x']]
    print(startDate, endDate, gunStartDate, gunEndDate, state, race, gender, age, mental_illness_value)
    return startDate, endDate, gunStartDate, gunEndDate, state, race, gender, age, mental_illness_value

def get_filtered_df(startDate, endDate, gunStartDate, gunEndDate, state, race, gender, age, mental_illness_value):
    filtered_df = pd.DataFrame(
    df[['name','state', 'race','date','signs_of_mental_illness','age_bins','gender','threat_level','flee','armed']][
                         (df['date']>=startDate) &
                         (df['date']<=endDate) &
                         (df['state'].isin(state)) &
                         (df['race'].isin(race)) &
                         (df['gender'].isin(gender)) &
                         (df['age_bins'].isin(age)) &
                         (df['signs_of_mental_illness'].isin(mental_illness_value)) &
                         (df['race'].isin(race))
                         ]).reset_index()
    return filtered_df


@app.callback(
    Output('reset-viz-states','children'),
    [Input('reset_button','n_clicks'),
     Input('line-chart','relayoutData'),
     Input('gun-line-chart', 'relayoutData'),
     Input('choropleth-map', 'clickData'),
     Input('bar-chart-race', 'clickData'),
     Input('bar-chart-age', 'clickData'),
     Input('mental-illness-bar', 'clickData')],prevent_initial_call=True)
def update_viz_states(lineChartClick, gunClick, mapClick, raceBarChartClick, ageBarClick, mentalBarClick, n_clicks):
    changed_id = [p['prop_id'] for p in dash.callback_context.triggered][0].split('.')[0]
    if changed_id=='reset_button':
        viz_states['bar_chart_race'] = 0
        viz_states['choropleth_map'] = 0
        viz_states['line_chart'] = 0
        viz_states['bar_chart_age'] = 0
        viz_states['bar_chart_mental'] = 0
        viz_states['radar_chart_weapons']=0
        viz_states['gun_chart'] = 0
        return 0
    triggered_element = dash.callback_context.triggered[0]['prop_id'].split('.')[0]
    if triggered_element=='line-chart':
        viz_states['line_chart'] = 1
    if triggered_element=='gun-line-chart':
        viz_states['gun_chart'] = 1
    if triggered_element=='choropleth-map':
        viz_states['choropleth_map'] = 1
    if triggered_element=='bar-chart-race':
        viz_states['bar_chart_race'] = 1
    if triggered_element=='bar-chart-age':
        viz_states['bar_chart_age'] = 1
    if triggered_element=='mental-illness-bar':
        viz_states['bar_chart_mental'] = 1
    return 0


#update choropleth map
@app.callback(
    Output('choropleth-map', 'figure'),
    [Input('bar-chart-race', 'clickData'),
    Input('bar-chart-age', 'clickData'),
    Input('line-chart','relayoutData'),
    Input('mental-illness-bar', 'clickData'),
    Input('gun-line-chart', 'relayoutData'),
    Input('intermediate-value-bar-chart-mental','children'),
    Input('intermediate-value-line-chart-year','children'),
    Input('intermediate-value-bar-chart-race','children'),
    Input('intermediate-value-bar-chart-age','children'),
    Input('reset_button','n_clicks')], prevent_initial_call=True)
def update_choropleth_map(raceBarChartClick, ageBarClick, lineChartClick, mentalBarClick, gunClick, intermediateBarChartMental, intermediateLineYearData, intermediateBarChartRace, intermediateBarChartAge, n_clicks):
    changed_id = [p['prop_id'] for p in dash.callback_context.triggered][0].split('.')[0]
    print(viz_states)
    if changed_id=='reset_button':
        viz_states['choropleth_map']=0
        return create_choropleth_map(df)
    if viz_states['choropleth_map']==1:
        return dash.no_update

    startDate, endDate, gunStartDate, gunEndDate, state, race, gender, age, mental_illness_value = \
                get_viz_info(lineChartClick, gunClick, None, raceBarChartClick, ageBarClick, mentalBarClick)
    filtered_df = get_filtered_df(startDate, endDate, gunStartDate, gunEndDate, state, race, gender, age, mental_illness_value)
    choropleth_map = create_choropleth_map(filtered_df)
    return choropleth_map

@app.callback(
    Output('bar-chart-race', 'figure'),
    [Input('choropleth-map', 'clickData'),
     Input('bar-chart-age', 'clickData'),
     Input('line-chart','relayoutData'),
     Input('mental-illness-bar', 'clickData'),
     Input('gun-line-chart', 'relayoutData'),
     Input('intermediate-value-bar-chart-mental','children'),
     Input('intermediate-value-bar-chart-age','children'),
     Input('intermediate-value-choropleth-map','children'),
     Input('intermediate-value-line-chart-year','children'),
     Input('reset_button','n_clicks')], prevent_initial_call=True)
def update_bar_chart_race(mapClick, ageBarClick, lineChartClick, mentalBarClick, gunClick, intermediateBarChartMental, intermediateBarChartAge, intermediateChoroplethMap, intermediateLineYearData, n_clicks):
    changed_id = [p['prop_id'] for p in dash.callback_context.triggered][0].split('.')[0]
    if changed_id=='reset_button':
        viz_states['bar_chart_race']=0
        return create_bar_char_for_race(df)
    if viz_states['bar_chart_race']==1:
        return dash.no_update
    startDate, endDate, gunStartDate, gunEndDate, state, race, gender, age, mental_illness_value = \
                get_viz_info(lineChartClick, gunClick, mapClick, None, ageBarClick, mentalBarClick)
    filtered_df = get_filtered_df(startDate, endDate, gunStartDate, gunEndDate, state, race, gender, age, mental_illness_value)
    bar_chart_race = create_bar_char_for_race(filtered_df)
    return bar_chart_race

#update line chart
@app.callback(
    Output('line-chart', 'figure'),
    [Input('choropleth-map', 'clickData'),
     Input('bar-chart-race', 'clickData'),
     Input('bar-chart-age','clickData'),
     Input('mental-illness-bar', 'clickData'),
     Input('gun-line-chart', 'relayoutData'),
     Input('intermediate-value-bar-chart-mental','children'),
     Input('intermediate-value-bar-chart-age','children'),
     Input('intermediate-value-bar-chart-race','children'),
     Input('intermediate-value-choropleth-map','children'),
     Input('reset_button','n_clicks')], prevent_initial_call=True)
def update_line_chart(mapClick, raceBarChartClick, ageBarClick, mentalBarClick, gunClick, intermediateBarChartMental, intermediateBarChartAge, intermediateBarChartRace, intermediateChoroplethMap, n_clicks):
    changed_id = [p['prop_id'] for p in dash.callback_context.triggered][0].split('.')[0]
    if changed_id=='reset_button':
        viz_states['line_chart']=0
        return create_line_chart(df)
    if viz_states['line_chart']==1:
        return dash.no_update
    startDate, endDate, gunStartDate, gunEndDate, state, race, gender, age, mental_illness_value = \
                get_viz_info(None, gunClick, mapClick, raceBarChartClick, ageBarClick, mentalBarClick)

    filtered_df = get_filtered_df(startDate, endDate, gunStartDate, gunEndDate, state, race, gender, age, mental_illness_value)
    line_chart = create_line_chart(filtered_df)
    return line_chart

#update bar chart age and gender
@app.callback(
    Output('bar-chart-age', 'figure'),
    [Input('choropleth-map', 'clickData'),
     Input('bar-chart-race', 'clickData'),
     Input('line-chart','relayoutData'),
     Input('mental-illness-bar', 'clickData'),
     Input('gun-line-chart', 'relayoutData'),
     Input('intermediate-value-bar-chart-mental','children'),
     Input('intermediate-value-line-chart-year','children'),
     Input('intermediate-value-bar-chart-race','children'),
     Input('intermediate-value-choropleth-map','children'),
     Input('reset_button','n_clicks')], prevent_initial_call=True)
def update_bar_chart_age_and_gender(mapClick, raceBarChartClick, lineChartClick, mentalBarClick, gunClick, intermediateBarChartMental, intermediateLineYearData, intermediateBarChartRace, intermediateChoroplethMap, n_clicks):
    changed_id = [p['prop_id'] for p in dash.callback_context.triggered][0].split('.')[0]
    if changed_id=='reset_button':
        viz_states['bar_chart_age']=0
        return create_bar_chart_for_age_and_gender(df)
    if viz_states['bar_chart_age']==1:
        return dash.no_update
    startDate, endDate, gunStartDate, gunEndDate, state, race, gender, age, mental_illness_value = \
                get_viz_info(lineChartClick, gunClick, mapClick, raceBarChartClick, None, mentalBarClick)
    filtered_df = get_filtered_df(startDate, endDate, gunStartDate, gunEndDate, state, race, gender, age, mental_illness_value)
    bar_chart_by_age = create_bar_chart_for_age_and_gender(filtered_df)
    return bar_chart_by_age

#update mental illness bar chart
@app.callback(
    Output('mental-illness-bar', 'figure'),
    [Input('choropleth-map', 'clickData'),
     Input('bar-chart-race', 'clickData'),
     Input('line-chart','relayoutData'),
     Input('bar-chart-age', 'clickData'),
     Input('gun-line-chart', 'relayoutData'),
     Input('intermediate-value-bar-chart-age','children'),
     Input('intermediate-value-line-chart-year','children'),
     Input('intermediate-value-bar-chart-race','children'),
     Input('intermediate-value-choropleth-map','children'),
     Input('reset_button','n_clicks')], prevent_initial_call=True)
def update_bar_chart_mental_illness(mapClick, raceBarChartClick, lineChartClick, ageBarClick, gunClick, intermediateBarChartAge, intermediateLineYearData, intermediateBarChartRace, intermediateChoroplethMap, n_clicks):
    changed_id = [p['prop_id'] for p in dash.callback_context.triggered][0].split('.')[0]
    if changed_id=='reset_button':
        viz_states['bar_chart_mental']=0
        return create_bar_chart_for_mental_illness(df)
    if viz_states['bar_chart_mental']==1:
        return dash.no_update
    startDate, endDate, gunStartDate, gunEndDate, state, race, gender, age, mental_illness_value = \
                get_viz_info(lineChartClick, gunClick, mapClick, raceBarChartClick, ageBarClick, None)
    filtered_df = get_filtered_df(startDate, endDate, gunStartDate, gunEndDate, state, race, gender, age, mental_illness_value)
    bar_chart_by_mental_illness = create_bar_chart_for_mental_illness(filtered_df)
    return bar_chart_by_mental_illness

#update weapon radar chart
@app.callback(
    Output('radar-chart-weapons', 'figure'),
    [Input('choropleth-map', 'clickData'),
     Input('bar-chart-race', 'clickData'),
     Input('line-chart','relayoutData'),
     Input('bar-chart-age', 'clickData'),
     Input('mental-illness-bar','clickData'),
     Input('gun-line-chart', 'relayoutData'),
     Input('intermediate-value-bar-chart-age','children'),
     Input('intermediate-value-line-chart-year','children'),
     Input('intermediate-value-bar-chart-race','children'),
     Input('intermediate-value-choropleth-map','children'),
     Input('intermediate-value-bar-chart-mental','children'),
     Input('reset_button','n_clicks')], prevent_initial_call=True)
def update_radar_chart_weapons(mapClick, raceBarChartClick, lineChartClick, ageBarClick, mentalBarClick, gunClick, intermediateBarChartAge, intermediateLineYearData, intermediateBarChartRace, intermediateChoroplethMap, intermediateBarChartMental, n_clicks):
    changed_id = [p['prop_id'] for p in dash.callback_context.triggered][0].split('.')[0]
    if changed_id=='reset_button':
        viz_states['radar_chart_weapons']=0
        return create_radar_chart_for_weapons(df)
    if viz_states['radar_chart_weapons']==1:
        return dash.no_update
    startDate, endDate, gunStartDate, gunEndDate, state, race, gender, age, mental_illness_value = \
                    get_viz_info(lineChartClick, gunClick, mapClick, raceBarChartClick, ageBarClick, mentalBarClick)
    filtered_df = get_filtered_df(startDate, endDate, gunStartDate, gunEndDate, state, race, gender, age, mental_illness_value)
    radar_chart_for_weapons = create_radar_chart_for_weapons(filtered_df)
    return radar_chart_for_weapons

#update line chart for gun purchase
@app.callback(
    Output('gun-line-chart', 'figure'),
    [Input('line-chart','relayoutData'),
     Input('reset_button','n_clicks')], prevent_initial_call=True)
def update_gun_data_line_chart(lineChartClick, n_clicks):
    triggered_element = dash.callback_context.triggered[0]['prop_id'].split('.')[0]
    changed_id = [p['prop_id'] for p in dash.callback_context.triggered][0].split('.')[0]
    if changed_id=='reset_button':
        viz_states['gun_chart'] = 0
        return create_line_chart_gun_data(gun_data)
    if viz_states['gun_chart']==1:
        return dash.no_update
    if triggered_element=='line-chart':
        startDate = lineChartClick['xaxis.range[0]']
        endDate = lineChartClick['xaxis.range[1]']
        filter_gun_data_by_date = gun_data[(gun_data['date']>=startDate) & (gun_data['date']<=endDate)]
        gun_data_line_chart = create_line_chart_gun_data(filter_gun_data_by_date)
        viz_states['line_chart'] = 1
        viz_states['gun_chart'] = 1
        return gun_data_line_chart

@app.callback(
    Output('sankey-diagram', 'figure'),
    [Input('bar-chart-race', 'clickData'),
    Input('bar-chart-age', 'clickData'),
    Input('line-chart','relayoutData'),
    Input('choropleth-map','clickData'),
    Input('mental-illness-bar','clickData'),
    Input('gun-line-chart', 'relayoutData'),
    Input('intermediate-value-bar-chart-age','children'),
    Input('intermediate-value-line-chart-year','children'),
    Input('intermediate-value-bar-chart-race','children'),
    Input('intermediate-value-choropleth-map','children'),
    Input('intermediate-value-bar-chart-mental','children'),
    Input('reset_button','n_clicks')], prevent_initial_call=True)
def update_sankey_diagram(raceBarChartClick, ageBarClick, lineChartClick, mapClick, mentalBarClick, gunClick, intermediateBarChartAge, intermediateLineYearData, intermediateBarChartRace, intermediateChoroplethMap, intermediateBarChartMental, n_clicks):
    changed_id = [p['prop_id'] for p in dash.callback_context.triggered][0].split('.')[0]
    if changed_id=='reset_button':
        viz_states['bar_chart_age']=0
        return create_sankey_diagram(df)
    startDate, endDate, gunStartDate, gunEndDate, state, race, gender, age, mental_illness_value = \
                    get_viz_info(lineChartClick, gunClick, mapClick, raceBarChartClick, ageBarClick, mentalBarClick)
    filtered_df = get_filtered_df(startDate, endDate, gunStartDate, gunEndDate, state, race, gender, age, mental_illness_value)
    sankey_diagram = create_sankey_diagram(filtered_df)
    return sankey_diagram

#update indicator graph
@app.callback(
    Output('indicator-graph','figure'),
    [Input('line-chart','relayoutData'),
     Input('bar-chart-race', 'clickData'),
     Input('bar-chart-age', 'clickData'),
     Input('choropleth-map','clickData'),
     Input('mental-illness-bar', 'clickData'),
     Input('gun-line-chart', 'relayoutData'),
     Input('reset_button','n_clicks')], prevent_initial_call=True)
def update_indicator_graph(lineChartClick, raceBarChartClick, ageBarClick, mapClick, mentalBarClick, gunClick, n_clicks):
    changed_id = [p['prop_id'] for p in dash.callback_context.triggered][0].split('.')[0]
    if changed_id=='reset_button':
        return indicator_graph(len(df))

    startDate, endDate, gunStartDate, gunEndDate, state, race, gender, age, mental_illness_value = \
                    get_viz_info(lineChartClick, gunClick, mapClick, raceBarChartClick, ageBarClick, mentalBarClick)
    filtered_df = get_filtered_df(startDate, endDate, gunStartDate, gunEndDate, state, race, gender, age, mental_illness_value)
    updated_indicator_graph = indicator_graph(len(filtered_df))
    return updated_indicator_graph

#-----------------------------------------------------------------------------------------------------------------------------------


if __name__ == '__main__':
    app.run_server(debug=True)
    #app.run_server(debug=False)
