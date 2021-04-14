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

viz_states = {'bar_chart_race':0, 'choropleth_map':0, 'line_chart':0, \
              'bar_chart_age':0, 'bar_chart_mental':0, 'radar_chart_weapons':0, \
              'gun_chart':0, 'bar_chart_threat':0, 'bar_chart_flee':0, \
              'map_dropdown':0}

#-----------------------------------------------------------------------------------------------------------------------------------

app.layout = html.Div([

html.Div([

    html.Div([
    html.A(html.Button('GITHUB', id='github_link', n_clicks=0,
                style={'background-color': '#c8d7e3',
                        'border':'none',
                        'padding': '15px 32px',
                        'border-radius': '25px',
                        'display':'inline-block',
                        'width':'60%',
                        'height':'100px',
                        'text-align': 'center',
                        'margin-left':'35px',
                        'font-weight':'bold',
                        'text-decoration': 'none',
                        'display': 'inline-block',
                        'font-size': '40px'}), href='https://github.com/IAT-814-Dashboard/Police-Killings-in-the-US'),
    ],style={'flex':'10%'}),

    html.Div([
        html.H1(children='IAT 814',
                style = {'textAlign' : 'center',
                         'color': 'black',
                         'font-family': 'Proxima Nova',
                         'margin-top':'40px',
                         'font-size': '50px',
                         'font-weight': 'bold',
                         'letter-spacing': '-1px',
                         'line-height': '1' }
        )],
        className='title',
        style = {
                 'flex':'80%'}),

    html.Div([
    html.A(html.Button('PROJECT REPORT', id='report_button', n_clicks=0,
                style={'background-color': '#c8d7e3',
                        'border':'none',
                        'padding': '15px 32px',
                        #'box-shadow': 'rgb(38, 57, 77) 0px 20px 30px -10px',
                        'border-radius': '25px',
                        'display':'inline-block',
                        'width':'400px',
                        'height':'100px',
                        'text-align': 'center',
                        'margin-left':'70px',
                        'font-weight':'bold',
                        'text-decoration': 'none',
                        'display': 'inline-block',
                        'font-size': '40px'}), href='/'),
    ],style={'flex':'10%'}),
    ],
    className = 'heading-row',
    style = {'height' : '4%',
            'display':'flex',
            'margin-top': '15px',
            'margin-left': '50px',
            'margin-right': '80px',}
),

#title
    html.Div([

        html.Div([
            html.H1(children='Police Killings in the United States',
                    style = {'textAlign' : 'center',
                             'color': 'white',
                             'font-family': 'Proxima Nova',
                             'font-size': '50px',
                             #'font-weight': 'bold',
                             'letter-spacing': '-1px',
                             'line-height': '1' }
            )],
            className='title',
            style = {'padding-top' : '1%',
                     'padding-bottom': '1%',
                     'flex':'80%'}),
        ],
        className = 'heading-row',
        style = {'height' : '4%',
                'display':'flex',
                'border-radius': '25px',
                #'border': 'solid black',
                #'border-color': 'black',
                #'border-width': ' 10px 10px 10px 10px',
                'background-color' : '#4a90a1',
                'box-shadow': 'rgb(38, 57, 77) 0px 20px 30px -10px',
                'margin-top': '25px',
                'margin-left': '80px',
                'margin-right': '80px',}
    ),


#line chart per year+information box+indicator graph
    html.Div([
        html.Div([
                html.H3('Police Killings by Year',
                        style={
                                'textAlign':'center',
                                'color': 'black',
                                'font-family': 'Proxima Nova',
                                'font-size': '38px',
                                'margin-bottom':'10px',
                                'font-weight': 'bold',
                                'line-height': '1',
                                }),
                dcc.Graph(
                        id='line-chart',
                        figure=create_line_chart(df),
                        config = {'displayModeBar': False}
                )], style={'flex':'60%',
                            'margin-right':'20px',
                            'border': 'solid white',
                            'border-color': 'white',
                            'border-width': ' 5px 5px 5px 5px',
                            'box-shadow': 'rgb(38, 57, 77) 0px 20px 30px -10px',
                            'padding':'20px',
                            'background-color':'#c8d7e3'}
                , className='line-chart-block'),

        html.Div([
            html.Div([
            html.H3(children= 'TOTAL NUMBER OF POLICE KILLINGS',#'Total Number of Police Killings',
                    style={
                            'textAlign':'center',
                            'color': 'black',
                            'font-family': 'Proxima Nova',
                            'font-size': '38px',
                            'margin-top':'20px',
                            'margin-bottom':'30px',
                            'font-weight': 'bold',
                            'line-height': '1',
                            }),
            html.H1(id='indicator-graph',
                    style={
                            'font_size':'70px'
                    }),
            ], style={'flex':'25%',
                      'margin-bottom':'40px',
                      'padding-top':'50px',
                      'padding-bottom':'50px',
                      'border-radius': '25px',
                      'background-color': '#c8d7e3',
                      'text-align':'center',
                      'border': 'solid white',
                      'box-shadow': 'rgb(38, 57, 77) 0px 20px 30px -10px',
                      'border-color': 'white',
                      'border-width': ' 5px 5px 5px 5px',
                      'padding':'20px'},),

            html.A(html.Button('RESET ALL', id='reset_button', n_clicks=0,
                        style={'background-color': '#c8d7e3',
                                'border':'none',
                                'border-radius': '25px',
                                'padding': '15px 32px',
                                'box-shadow': 'rgb(38, 57, 77) 0px 20px 30px -10px',
                                'display':'inline-block',
                                'width':'80%',
                                'height':'150px',
                                'text-align': 'center',
                                'margin-left':'70px',
                                'font-weight':'bold',
                                'margin-bottom':'50px',
                                'text-decoration': 'none',
                                'display': 'inline-block',
                                'font-size': '40px'}), href='/'),
            html.Img(src='https://i.etsystatic.com/17857814/r/il/267c7e/1832681232/il_570xN.1832681232_lcsc.jpg',width='500px', height='350px',
                     style={'margin-left':'200px',
                            'mix-blend-mode':'multiply',
                            'margin-right':'40px'}),
            ],
            style={'flex':'25%',
                   'padding':'20px'}),

        html.Div([
            html.P('Police brutality is the use of excessive or unnecessary force by personnel affiliated with law enforcement duties when dealing with suspects and civilians.\
                   Police violence is a leading cause of death for young men in the United States.\
                   This dashboard can be used to explore the possible causes for Police Killings in the United States.',
                   style={'padding-top':'60px'}),
            html.Br(),

            html.P(html.Strong(html.Center('ALL LIVES MATTER')),style={'font-size': '50px'}),

        ], style={'float':'left','flex':'25%',
                  'text-align':'center',
                  'border-radius': '25px',
                  'background-color':'#c8d7e3',
                  'box-shadow': 'rgb(38, 57, 77) 0px 20px 30px -10px',
                  'font-family': 'Proxima Nova',
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
           'margin-left': '80px',
           'margin-right': '80px',
           }
    ),

#map dropdown
    html.Div([
            html.Div(id='dummy1',
                     style={'flex':'90%',
                            'margin-right':'60px',
                    }),
            html.Div([
                dcc.Dropdown(id='map-dropdown', options=get_country_list_for_dropdown(df),
                            placeholder='Select a State',
                            multi=True,
                            style={'height':'90px',
                                   'width':'500px',
                                   'font-size':'40px',
                                   #'border-radius': '25px',
                                   'background-color':'#c8d7e3',
                                   'box-shadow': 'rgb(38, 57, 77) 0px 20px 30px -10px'
                            }),
                ], style={'flex':'10%'}),
    ],
    className='dropwdown-bar',
    style={'display':'flex',
           'height':'20%',
           'margin-top':'30px',
           'margin-left': '80px',
           'margin-right': '80px',
    }),

#gun purchase per year+ choropleth map
    html.Div([
        html.Div([
            html.H3('Purchase of Gun By Year',
                    style={
                            'textAlign':'center',
                            'color': 'black',
                            'font-family': 'Proxima Nova',
                            'font-size': '38px',
                            'margin-bottom':'10px',
                            'font-weight': 'bold',
                            'line-height': '1'}),
            dcc.Graph(
                    id='gun-line-chart',
                    figure=create_line_chart_gun_data(gun_data),
                    config = {'displayModeBar': False}

            ),
        ], style={'flex':'60%',
                    'background-color':'#c8d7e3',
                    'box-shadow': 'rgb(38, 57, 77) 0px 20px 30px -10px',
                    'border': 'solid white',
                    'border-color': 'white',
                    'border-width': ' 5px 5px 5px 5px',
                    'padding':'20px',
                    #'margin-left': '50px',
                    'margin-right': '20px',}),
        html.Div([
                html.H3('Police Killings by State',
                        style={
                                'textAlign' : 'center',
                                'color': 'black',
                                'font-family': 'Proxima Nova',
                                'margin-bottom':'25px',
                                'font-size': '38px','font-weight': 'bold',
                                'line-height': '1'}),
                dcc.Graph(
                        id='choropleth-map',
                        figure=create_choropleth_map(df),
                        config = {'displayModeBar': False}
                )], style={'flex':'40%',
                            #'margin-right':'20px',
                            'border': 'solid white',
                            'border-color': 'white',
                            'border-width': ' 5px 5px 5px 5px',
                            'box-shadow': 'rgb(38, 57, 77) 0px 20px 30px -10px',
                            'padding':'20px', 'padding-left':'30px','background-color':'#c8d7e3'}
                ,className='map-block'),

    ],
    className='year-state',
    style={'display':'flex',
           'height':'100%',
           'margin-top':'30px',
           'margin-left': '80px',
           'margin-right': '80px',}
    ),



#race+age-gender+mentalillness
html.Div([
    html.Div([
            html.H3('Police Killings by Race',
                    style={
                            'textAlign' : 'center',
                            'color': 'black',
                            'font-family': 'Proxima Nova',
                            'margin-bottom':'10px',
                            'font-size': '38px',
                            'font-weight': 'bold',
                            'line-height': '1'}),
            dcc.Graph(
                    id='bar-chart-race',
                    figure=create_bar_chart_for_race(df),
                    config={'doubleClick':'reset',
                            'displayModeBar': False},
            )], style={'flex':'34%',
                        'border': 'solid white',
                        'border-color': 'white',
                        'border-width': '5px 5px 5px 5px',
                        'box-shadow': 'rgb(38, 57, 77) 0px 20px 30px -10px',
                        'margin-right':'40px',
                        'padding':'20px',
                        'background-color':'#c8d7e3'
                        }
            , className='race-block'),

    html.Div([
            html.H3('Police Killings by Age and Gender',
                    style={
                            'textAlign' : 'center',
                            'color': 'black',
                            'margin-bottom':'10px',
                            'font-size': '38px',
                            'font-family': 'Proxima Nova',
                            'font-weight': 'bold',
                            'line-height': '1'}),
            dcc.Graph(
                    id='bar-chart-age',
                    figure=create_bar_chart_for_age_and_gender(df),
                    config={'doubleClick':'reset', 'displayModeBar': False},
            )], style={'flex':'33%',
                        'border': 'solid white',
                        'border-color': 'white',
                        'margin-right':'40px',
                        'border-width': '5px 5px 5px 0px',
                        'box-shadow': 'rgb(38, 57, 77) 0px 20px 30px -10px',
                        'padding':'20px', 'background-color':'#c8d7e3'
                        }
            , className='age-block'),

    html.Div([
            html.H3('Police Killings by Signs of Mental Illness',
                    style={
                            'textAlign' : 'center',
                            'color': 'black',
                            'margin-bottom':'10px',
                            'font-size': '38px',
                            'font-family': 'Proxima Nova',
                            'font-weight': 'bold',
                            'line-height': '1'}),
            dcc.Graph(
                    id='mental-illness-bar',
                    figure=create_bar_chart_for_mental_illness(df),
                    config={'doubleClick':'reset',
                            'displayModeBar': False},
            )], style={'flex':'34%',
                        'padding-left':'50px',
                        'border': 'solid white',
                        'border-color': 'white',
                        'border-width': '5px 5px 5px 0px',
                        'box-shadow': 'rgb(38, 57, 77) 0px 20px 30px -10px',
                        'padding':'20px', 'background-color':'#c8d7e3'
                        }

            , className='mental-block'),

],
className='bar-chart-block',
style={'display':'flex',
       'height':'100%',
       'margin-top':'30px',
       'margin-left': '80px',
       'margin-right': '80px',
       }
),

#weapon+ threat level+ flee
html.Div([
    html.Div([
            html.H3('Police Killings by Weapons',
                    style={
                            'textAlign' : 'center',
                            'color': 'black',
                            'margin-bottom':'10px',
                            'font-size': '38px',
                            'font-family': 'Proxima Nova',
                            'font-weight': 'bold',
                            'line-height': '1'}),
            dcc.Graph(
            id='radar-chart-weapons',
            figure=create_bar_chart_for_weapons(df),
            )], style={'flex':'30%',
                        'border': 'solid white',
                        'border-color': 'white',
                        'margin-right':'40px',
                        'border-width': ' 5px 5px 5px 5px',
                        'box-shadow': 'rgb(38, 57, 77) 0px 20px 30px -10px',
                        'padding':'20px',
                        'background-color':'#c8d7e3'}
            ,className='weapon-block'),

    html.Div([
            html.H3('Police Killings by Threat Level',
                    style={
                            'textAlign' : 'center',
                            'color': 'black',
                            'margin-bottom':'10px',
                            'font-size': '38px',
                            'font-family': 'Proxima Nova',
                            'font-weight': 'bold',
                            'line-height': '1'}),
            dcc.Graph(
                    id='bar-chart-threat-level',
                    figure=create_bar_chart_for_threat_level(df),
                    config={'doubleClick':'reset',
                            'displayModeBar': False},
            )], style={'flex':'33%',
                        'border': 'solid white',
                        'margin-right':'40px',
                        'border-color': 'white',
                        'border-width': '5px 5px 5px 0px',
                        'box-shadow': 'rgb(38, 57, 77) 0px 20px 30px -10px',
                        'padding':'20px', 'background-color':'#c8d7e3'
                        }
            , className='threat-level-block'),

    html.Div([
            html.H3('Police Killings by Type of Fleeing',
                    style={
                            'textAlign' : 'center',
                            'color': 'black',
                            'margin-bottom':'10px',
                            'font-size': '38px',
                            'font-family': 'Proxima Nova',
                            'font-weight': 'bold',
                            'line-height': '1'}),
            dcc.Graph(
                    id='bar-chart-fleeing',
                    figure=create_bar_chart_for_fleeing(df),
                    config={'doubleClick':'reset',
                            'displayModeBar': False},
            )], style={'flex':'34%',
                        'padding-left':'50px',
                        'border': 'solid white',
                        'border-color': 'white',
                        'border-width': '5px 5px 5px 0px',
                        'box-shadow': 'rgb(38, 57, 77) 0px 20px 30px -10px',
                        'padding':'20px', 'background-color':'#c8d7e3'
                        }

            , className='fleeing-block'),

],
className='bar-chart-block-2',
style={'display':'flex',
       'height':'100%',
       'margin-top':'30px',
       'margin-left': '80px',
       'margin-right': '80px',
       }
),

#sankey diagram
    html.Div([
        html.Div([
                dcc.Graph(
                        id='sankey-diagram',
                        figure=create_sankey_diagram(df),
                        style={'margin-left':'50px', 'margin-right':'50px'},
                        config={'doubleClick':'reset',
                                'displayModeBar': False},

                ),
                html.H3('Sankey Diagram',
                        style={
                                'textAlign' : 'center',
                                'color': 'black',
                                'font-family': 'Proxima Nova',
                                'margin-top':'20px',
                                'margin-bottom':'25px',
                                'font-size': '38px','font-weight': 'bold',
                                'line-height': '1'}),
                ], style={'flex':'100%',
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
           'margin-left': '80px',
           'margin-right': '80px',
           'margin-bottom':'40px'}
    ),

#intermediate values
    html.Div(id='triggered_element', style={'display': 'none'}),
    html.Div(id='reset-viz-states', style={'display': 'none'})

], style={})

#-----------------------------------------------------------------------------------------------------------------------------------

def get_viz_info(lineChartClick, gunClick, mapClick, raceBarChartClick, ageBarClick, mentalBarClick, threatBarClick, fleeBarClick):
    startDate=gunStartDate="01/01/2015"
    endDate=gunEndDate="01/01/2021"
    state = dropdown_value = df['state'].unique()
    race = df['race'].unique()
    gender = df['gender'].unique()
    age = df['age_bins'].unique()
    mental_illness_value = df['signs_of_mental_illness'].unique()
    threat_value = df['threat_level'].unique()
    flee_value = df['flee'].unique()
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
    if threatBarClick is not None:
        threat_value = [threatBarClick['points'][0]['x']]
    if fleeBarClick is not None:
        flee_value = [fleeBarClick['points'][0]['x']]
    return startDate, endDate, gunStartDate, gunEndDate, state, race, gender, age, mental_illness_value, threat_value, flee_value

def get_filtered_df(startDate, endDate, gunStartDate, gunEndDate, state, race, gender, age, mental_illness_value, threat_value, flee_value):
    filtered_df = pd.DataFrame(
    df[['name','state', 'race','date','signs_of_mental_illness','age_bins','gender','threat_level','flee','armed']][
                         (df['date']>=startDate) &
                         (df['date']<=endDate) &
                         (df['state'].isin(state)) &
                         (df['race'].isin(race)) &
                         (df['gender'].isin(gender)) &
                         (df['age_bins'].isin(age)) &
                         (df['signs_of_mental_illness'].isin(mental_illness_value)) &
                         (df['race'].isin(race)) &
                         (df['threat_level'].isin(threat_value)) &
                         (df['flee']).isin(flee_value)
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
     Input('bar-chart-threat-level','clickData'),
     Input('bar-chart-fleeing','clickData'),
     Input('mental-illness-bar', 'clickData')],prevent_initial_call=True)
def update_viz_states(lineChartClick, gunClick, mapClick, raceBarChartClick, ageBarClick, threatBarClick, fleeBarClick, mentalBarClick, n_clicks):
    global viz_states
    changed_id = [p['prop_id'] for p in dash.callback_context.triggered][0].split('.')[0]
    if changed_id=='reset_button':
        viz_states = viz_states.fromkeys(viz_states, 0)
    triggered_element = dash.callback_context.triggered[0]['prop_id'].split('.')[0]
    if triggered_element=='choropleth-map':
        viz_states['choropleth_map'] = 1
    if triggered_element=='bar-chart-race':
        viz_states['bar_chart_race'] = 1
    if triggered_element=='bar-chart-age':
        viz_states['bar_chart_age'] = 1
    if triggered_element=='mental-illness-bar':
        viz_states['bar_chart_mental'] = 1
    if triggered_element=='bar-chart-threat-level':
        viz_states['bar_chart_threat'] = 1
    if triggered_element=='bar-chart-fleeing':
        viz_states['bar_chart_flee'] = 1
    return 0

#update choropleth map
@app.callback(
    Output('choropleth-map', 'figure'),
    [Input('bar-chart-race', 'clickData'),
    Input('map-dropdown', 'value'),
    Input('bar-chart-age', 'clickData'),
    Input('line-chart','relayoutData'),
    Input('mental-illness-bar', 'clickData'),
    Input('gun-line-chart', 'relayoutData'),
    Input('bar-chart-threat-level','clickData'),
    Input('bar-chart-fleeing','clickData'),
    Input('reset_button','n_clicks')], prevent_initial_call=True)
def update_choropleth_map(raceBarChartClick, mapDropdown, ageBarClick, lineChartClick, mentalBarClick, gunClick, threatBarClick, fleeBarClick, n_clicks):
    changed_id = [p['prop_id'] for p in dash.callback_context.triggered][0].split('.')[0]
    if changed_id=='reset_button':
        return create_choropleth_map(df)
    if viz_states['choropleth_map']==1:
        return dash.no_update
    startDate, endDate, gunStartDate, gunEndDate, state, race, gender, age, mental_illness_value, threat_value, flee_value = \
                get_viz_info(lineChartClick, gunClick, None, raceBarChartClick, ageBarClick, mentalBarClick, threatBarClick, fleeBarClick)
    triggered_element = dash.callback_context.triggered[0]['prop_id'].split('.')[0]
    if triggered_element=='map-dropdown' or viz_states['map_dropdown']==1:
        state = mapDropdown
    filtered_df = get_filtered_df(startDate, endDate, gunStartDate, gunEndDate, state, race, gender, age, mental_illness_value, threat_value, flee_value)
    choropleth_map = create_choropleth_map(filtered_df)
    return choropleth_map

#update bar chart race
@app.callback(
    Output('bar-chart-race', 'figure'),
    [Input('choropleth-map', 'clickData'),
     Input('map-dropdown', 'value'),
     Input('bar-chart-age', 'clickData'),
     Input('line-chart','relayoutData'),
     Input('mental-illness-bar', 'clickData'),
     Input('gun-line-chart', 'relayoutData'),
     Input('bar-chart-threat-level','clickData'),
     Input('bar-chart-fleeing','clickData'),
     Input('reset_button','n_clicks')], prevent_initial_call=True)
def update_bar_chart_race(mapClick, mapDropdown, ageBarClick, lineChartClick, mentalBarClick, gunClick, threatBarClick, fleeBarClick, n_clicks):
    changed_id = [p['prop_id'] for p in dash.callback_context.triggered][0].split('.')[0]
    if changed_id=='reset_button':
        return create_bar_chart_for_race(df)
    if viz_states['bar_chart_race']==1:
        return dash.no_update
    startDate, endDate, gunStartDate, gunEndDate, state, race, gender, age, mental_illness_value, threat_value, flee_value = \
                get_viz_info(lineChartClick, gunClick, mapClick, None, ageBarClick, mentalBarClick, threatBarClick, fleeBarClick)
    triggered_element = dash.callback_context.triggered[0]['prop_id'].split('.')[0]
    if triggered_element=='map-dropdown' or viz_states['map_dropdown']==1:
        state = mapDropdown
        viz_states['map_dropdown'] = 1
    filtered_df = get_filtered_df(startDate, endDate, gunStartDate, gunEndDate, state, race, gender, age, mental_illness_value, threat_value, flee_value)
    bar_chart_race = create_bar_chart_for_race(filtered_df)
    return bar_chart_race

#update threat level bar chart
@app.callback(
    Output('bar-chart-threat-level', 'figure'),
    [Input('choropleth-map', 'clickData'),
     Input('map-dropdown', 'value'),
     Input('bar-chart-age', 'clickData'),
     Input('line-chart','relayoutData'),
     Input('mental-illness-bar', 'clickData'),
     Input('bar-chart-race','clickData'),
     Input('bar-chart-fleeing','clickData'),
     Input('gun-line-chart', 'relayoutData'),
     Input('reset_button','n_clicks')], prevent_initial_call=True)
def update_bar_chart_threat_level(mapClick, mapDropdown, ageBarClick, lineChartClick, mentalBarClick, raceBarClick, fleeBarClick, gunClick, n_clicks):
    changed_id = [p['prop_id'] for p in dash.callback_context.triggered][0].split('.')[0]
    if changed_id=='reset_button':
        return create_bar_chart_for_threat_level(df)
    if viz_states['bar_chart_threat']==1:
        return dash.no_update
    startDate, endDate, gunStartDate, gunEndDate, state, race, gender, age, mental_illness_value, threat_value, flee_value = \
                get_viz_info(lineChartClick, gunClick, mapClick, raceBarClick, ageBarClick, mentalBarClick, None, fleeBarClick)
    triggered_element = dash.callback_context.triggered[0]['prop_id'].split('.')[0]
    if triggered_element=='map-dropdown' or viz_states['map_dropdown']==1:
        state = mapDropdown
        viz_states['map_dropdown'] = 1
    filtered_df = get_filtered_df(startDate, endDate, gunStartDate, gunEndDate, state, race, gender, age, mental_illness_value, threat_value, flee_value)
    bar_chart_threat_level = create_bar_chart_for_threat_level(filtered_df)
    return bar_chart_threat_level

#update flee level bar chart
@app.callback(
    Output('bar-chart-fleeing', 'figure'),
    [Input('choropleth-map', 'clickData'),
     Input('map-dropdown', 'value'),
     Input('bar-chart-age', 'clickData'),
     Input('line-chart','relayoutData'),
     Input('mental-illness-bar', 'clickData'),
     Input('bar-chart-race','clickData'),
     Input('bar-chart-threat-level','clickData'),
     Input('gun-line-chart', 'relayoutData'),
     Input('reset_button','n_clicks')], prevent_initial_call=True)
def update_bar_chart_fleeing(mapClick, mapDropdown, ageBarClick, lineChartClick, mentalBarClick, raceBarClick, threatBarClick, gunClick, n_clicks):
    changed_id = [p['prop_id'] for p in dash.callback_context.triggered][0].split('.')[0]
    if changed_id=='reset_button':
        return create_bar_chart_for_fleeing(df)
    if viz_states['bar_chart_flee']==1:
        return dash.no_update
    startDate, endDate, gunStartDate, gunEndDate, state, race, gender, age, mental_illness_value, threat_value, flee_value = \
                get_viz_info(lineChartClick, gunClick, mapClick, raceBarClick, ageBarClick, mentalBarClick, threatBarClick, None)
    triggered_element = dash.callback_context.triggered[0]['prop_id'].split('.')[0]
    if triggered_element=='map-dropdown' or viz_states['map_dropdown']==1:
        state = mapDropdown
        viz_states['map_dropdown'] = 1
    filtered_df = get_filtered_df(startDate, endDate, gunStartDate, gunEndDate, state, race, gender, age, mental_illness_value, threat_value, flee_value)
    bar_chart_fleeing = create_bar_chart_for_fleeing(filtered_df)
    return bar_chart_fleeing

#update bar chart age and gender
@app.callback(
    Output('bar-chart-age', 'figure'),
    [Input('choropleth-map', 'clickData'),
     Input('map-dropdown', 'value'),
     Input('bar-chart-race', 'clickData'),
     Input('line-chart','relayoutData'),
     Input('mental-illness-bar', 'clickData'),
     Input('gun-line-chart', 'relayoutData'),
     Input('bar-chart-threat-level','clickData'),
     Input('bar-chart-fleeing','clickData'),
     Input('reset_button','n_clicks')], prevent_initial_call=True)
def update_bar_chart_age_and_gender(mapClick, mapDropdown, raceBarChartClick, lineChartClick, mentalBarClick, gunClick, threatBarClick, fleeBarClick, n_clicks):
    changed_id = [p['prop_id'] for p in dash.callback_context.triggered][0].split('.')[0]
    if changed_id=='reset_button':
        return create_bar_chart_for_age_and_gender(df)
    if viz_states['bar_chart_age']==1:
        return dash.no_update
    startDate, endDate, gunStartDate, gunEndDate, state, race, gender, age, mental_illness_value, threat_value, flee_value = \
                get_viz_info(lineChartClick, gunClick, mapClick, raceBarChartClick, None, mentalBarClick, threatBarClick, fleeBarClick)
    triggered_element = dash.callback_context.triggered[0]['prop_id'].split('.')[0]
    if triggered_element=='map-dropdown' or viz_states['map_dropdown']==1:
        state = mapDropdown
        viz_states['map_dropdown'] = 1
    filtered_df = get_filtered_df(startDate, endDate, gunStartDate, gunEndDate, state, race, gender, age, mental_illness_value, threat_value, flee_value)
    bar_chart_by_age = create_bar_chart_for_age_and_gender(filtered_df)
    return bar_chart_by_age

#update mental illness bar chart
@app.callback(
    Output('mental-illness-bar', 'figure'),
    [Input('choropleth-map', 'clickData'),
     Input('map-dropdown', 'value'),
     Input('bar-chart-race', 'clickData'),
     Input('line-chart','relayoutData'),
     Input('bar-chart-age', 'clickData'),
     Input('gun-line-chart', 'relayoutData'),
     Input('bar-chart-threat-level','clickData'),
     Input('bar-chart-fleeing','clickData'),
     Input('reset_button','n_clicks')], prevent_initial_call=True)
def update_bar_chart_mental_illness(mapClick, mapDropdown, raceBarChartClick, lineChartClick, ageBarClick, gunClick, threatBarClick, fleeBarClick, n_clicks):
    changed_id = [p['prop_id'] for p in dash.callback_context.triggered][0].split('.')[0]
    if changed_id=='reset_button':
        return create_bar_chart_for_mental_illness(df)
    if viz_states['bar_chart_mental']==1:
        return dash.no_update
    startDate, endDate, gunStartDate, gunEndDate, state, race, gender, age, mental_illness_value, threat_value, flee_value = \
                get_viz_info(lineChartClick, gunClick, mapClick, raceBarChartClick, ageBarClick, None, threatBarClick, fleeBarClick)
    triggered_element = dash.callback_context.triggered[0]['prop_id'].split('.')[0]
    if triggered_element=='map-dropdown' or viz_states['map_dropdown']==1:
        state = mapDropdown
        viz_states['map_dropdown'] = 1
    filtered_df = get_filtered_df(startDate, endDate, gunStartDate, gunEndDate, state, race, gender, age, mental_illness_value, threat_value, flee_value)
    bar_chart_by_mental_illness = create_bar_chart_for_mental_illness(filtered_df)
    return bar_chart_by_mental_illness

#update weapon radar chart
@app.callback(
    Output('radar-chart-weapons', 'figure'),
    [Input('choropleth-map', 'clickData'),
     Input('map-dropdown', 'value'),
     Input('bar-chart-race', 'clickData'),
     Input('line-chart','relayoutData'),
     Input('bar-chart-age', 'clickData'),
     Input('mental-illness-bar','clickData'),
     Input('gun-line-chart', 'relayoutData'),
     Input('bar-chart-threat-level','clickData'),
     Input('bar-chart-fleeing','clickData'),
     Input('reset_button','n_clicks')], prevent_initial_call=True)
def update_radar_chart_weapons(mapClick, mapDropdown, raceBarChartClick, lineChartClick, ageBarClick, mentalBarClick, gunClick, threatBarClick, fleeBarClick, n_clicks):
    changed_id = [p['prop_id'] for p in dash.callback_context.triggered][0].split('.')[0]
    if changed_id=='reset_button':
        return create_bar_chart_for_weapons(df)
    if viz_states['radar_chart_weapons']==1:
        return dash.no_update
    startDate, endDate, gunStartDate, gunEndDate, state, race, gender, age, mental_illness_value, threat_value, flee_value = \
                    get_viz_info(lineChartClick, gunClick, mapClick, raceBarChartClick, ageBarClick, mentalBarClick, threatBarClick, fleeBarClick)
    triggered_element = dash.callback_context.triggered[0]['prop_id'].split('.')[0]
    if triggered_element=='map-dropdown' or viz_states['map_dropdown']==1:
        state = mapDropdown
        viz_states['map_dropdown'] = 1
    filtered_df = get_filtered_df(startDate, endDate, gunStartDate, gunEndDate, state, race, gender, age, mental_illness_value, threat_value, flee_value)
    bar_chart_for_weapons = create_bar_chart_for_weapons(filtered_df)
    return bar_chart_for_weapons

#update line chart for gun purchase
@app.callback(
    Output('gun-line-chart', 'figure'),
    [Input('line-chart','relayoutData'),
     Input('reset_button','n_clicks')], prevent_initial_call=True)
def update_gun_data_line_chart(lineChartClick, n_clicks):
    triggered_element = dash.callback_context.triggered[0]['prop_id'].split('.')[0]
    changed_id = [p['prop_id'] for p in dash.callback_context.triggered][0].split('.')[0]
    if changed_id=='reset_button':
        return create_line_chart_gun_data(gun_data)
    if viz_states['gun_chart']==1:
        return dash.no_update

    startDate, endDate, gunStartDate, gunEndDate, state, race, gender, age, mental_illness_value, threat_value, flee_value = \
                get_viz_info(lineChartClick, None, None, None, None, None, None, None)
    filter_gun_data_by_date = gun_data[(gun_data['date']>=startDate) & (gun_data['date']<=endDate)]
    gun_data_line_chart = create_line_chart_gun_data(filter_gun_data_by_date)
    return gun_data_line_chart

#update line chart
@app.callback(
    Output('line-chart', 'figure'),
    [Input('choropleth-map', 'clickData'),
     Input('map-dropdown', 'value'),
     Input('bar-chart-race', 'clickData'),
     Input('bar-chart-age','clickData'),
     Input('mental-illness-bar', 'clickData'),
     Input('gun-line-chart', 'relayoutData'),
     Input('bar-chart-threat-level','clickData'),
     Input('bar-chart-fleeing','clickData'),
     Input('reset_button','n_clicks')], prevent_initial_call=True)
def update_line_chart(mapClick, mapDropdown, raceBarChartClick, ageBarClick, mentalBarClick, gunClick, threatBarClick, fleeBarClick, n_clicks):
    changed_id = [p['prop_id'] for p in dash.callback_context.triggered][0].split('.')[0]
    if changed_id=='reset_button':
        return create_line_chart(df), create_line_chart_gun_data(gun_data)
    if viz_states['line_chart']==1:
        return dash.no_update
    startDate, endDate, gunStartDate, gunEndDate, state, race, gender, age, mental_illness_value, threat_value, flee_value = \
                get_viz_info(None, gunClick, mapClick, raceBarChartClick, ageBarClick, mentalBarClick, threatBarClick, fleeBarClick)
    triggered_element = dash.callback_context.triggered[0]['prop_id'].split('.')[0]
    if triggered_element=='gun-line-chart':
        filtered_df = get_filtered_df(gunStartDate, gunEndDate, gunStartDate, gunEndDate, state, race, gender, age, mental_illness_value, threat_value, flee_value)
    else:
        filtered_df = get_filtered_df(startDate, endDate, gunStartDate, gunEndDate, state, race, gender, age, mental_illness_value, threat_value, flee_value)
    if triggered_element=='map-dropdown' or viz_states['map_dropdown']==1:
        state = mapDropdown
        viz_states['map_dropdown'] = 1
    line_chart = create_line_chart(filtered_df)
    return line_chart

#update sankey diagram
@app.callback(
    Output('sankey-diagram', 'figure'),
    [Input('bar-chart-race', 'clickData'),
    Input('bar-chart-age', 'clickData'),
    Input('line-chart','relayoutData'),
    Input('choropleth-map','clickData'),
    Input('map-dropdown', 'value'),
    Input('mental-illness-bar','clickData'),
    Input('gun-line-chart', 'relayoutData'),
    Input('bar-chart-threat-level','clickData'),
    Input('bar-chart-fleeing','clickData'),
    Input('reset_button','n_clicks')], prevent_initial_call=True)
def update_sankey_diagram(raceBarChartClick, ageBarClick, lineChartClick, mapClick, mapDropdown, mentalBarClick, gunClick, threatBarClick, fleeBarClick, n_clicks):
    changed_id = [p['prop_id'] for p in dash.callback_context.triggered][0].split('.')[0]
    if changed_id=='reset_button':
        return create_sankey_diagram(df)
    startDate, endDate, gunStartDate, gunEndDate, state, race, gender, age, mental_illness_value, threat_value, flee_value = \
                    get_viz_info(lineChartClick, gunClick, mapClick, raceBarChartClick, ageBarClick, mentalBarClick, threatBarClick, fleeBarClick)
    triggered_element = dash.callback_context.triggered[0]['prop_id'].split('.')[0]
    if triggered_element=='map-dropdown' or viz_states['map_dropdown']==1:
        state = mapDropdown
        viz_states['map_dropdown'] = 1
    filtered_df = get_filtered_df(startDate, endDate, gunStartDate, gunEndDate, state, race, gender, age, mental_illness_value, threat_value, flee_value)
    sankey_diagram = create_sankey_diagram(filtered_df)
    return sankey_diagram

#update indicator graph
@app.callback(
    Output('indicator-graph','children'),
    [Input('line-chart','relayoutData'),
     Input('bar-chart-race', 'clickData'),
     Input('bar-chart-age', 'clickData'),
     Input('choropleth-map','clickData'),
     Input('map-dropdown', 'value'),
     Input('mental-illness-bar', 'clickData'),
     Input('gun-line-chart', 'relayoutData'),
     Input('bar-chart-threat-level','clickData'),
     Input('bar-chart-fleeing','clickData'),
     Input('reset_button','n_clicks')])
def update_indicator_graph(lineChartClick, raceBarChartClick, ageBarClick, mapClick, mapDropdown, mentalBarClick, gunClick, threatBarClick, fleeBarClick, n_clicks):
    changed_id = [p['prop_id'] for p in dash.callback_context.triggered][0].split('.')[0]
    if changed_id=='reset_button':
        return len(df)

    startDate, endDate, gunStartDate, gunEndDate, state, race, gender, age, mental_illness_value, threat_value, flee_value = \
                    get_viz_info(lineChartClick, gunClick, mapClick, raceBarChartClick, ageBarClick, mentalBarClick, threatBarClick, fleeBarClick)
    triggered_element = dash.callback_context.triggered[0]['prop_id'].split('.')[0]
    if triggered_element=='map-dropdown' or viz_states['map_dropdown']==1:
        state = mapDropdown
        viz_states['map_dropdown'] = 1
    if triggered_element=='gun-line-chart':
        filtered_df = get_filtered_df(gunStartDate, gunEndDate, gunStartDate, gunEndDate, state, race, gender, age, mental_illness_value, threat_value, flee_value)
    else:
        filtered_df = get_filtered_df(startDate, endDate, gunStartDate, gunEndDate, state, race, gender, age, mental_illness_value, threat_value, flee_value)

    return len(filtered_df)

#-----------------------------------------------------------------------------------------------------------------------------------


if __name__ == '__main__':
    app.run_server(debug=True)
