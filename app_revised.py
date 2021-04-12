import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from datetime import date

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
            html.Button('RESET ALL',id='reset_button', n_clicks=0,
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
                                'font-size': '30px'}),
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
    html.Div(id='intermediate-value-line-chart-year', style={'display': 'none'}),
    html.Div(id='intermediate-value-bar-chart-race', style={'display': 'none'}),
    html.Div(id='intermediate-value-choropleth-map', style={'display': 'none'}),
    html.Div(id='intermediate-value-bar-chart-age', style={'display': 'none'}),
    html.Div(id='intermediate-value-bar-chart-mental', style={'display': 'none'}),
    html.Div(id='intermediate-value-radar-chart-weapons', style={'display': 'none'}),
    html.Div(id='reset-viz-states', style={'display': 'none'})



], style={})

#-----------------------------------------------------------------------------------------------------------------------------------



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
    if changed_id=='reset_button':
        viz_states['choropleth_map']==0
        return create_choropleth_map(df)
    if viz_states['choropleth_map']==1:
        return dash.no_update
    triggered_element = dash.callback_context.triggered[0]['prop_id'].split('.')[0]
    if triggered_element == 'gun-line-chart':
        if viz_states['gun_chart']==1:
            return dash.no_update
        startDate = gunClick['xaxis.range[0]']
        endDate = gunClick['xaxis.range[1]']
        filter_by_date = df[(df['date']>=startDate) & (df['date']<=endDate)]
        choropleth_map = create_choropleth_map(filter_by_date)
        return choropleth_map
    if triggered_element =='line-chart':
        if viz_states['bar_chart_race']==1:
            intermediateBarChartRace = pd.read_json(intermediateBarChartRace)
            startDate = lineChartClick['xaxis.range[0]']
            endDate = lineChartClick['xaxis.range[1]']
            filter_by_date = intermediateBarChartRace[(intermediateBarChartRace['date']>=startDate) & (intermediateBarChartRace['date']<=endDate)]
            choropleth_map = create_choropleth_map(filter_by_date)
            viz_states['line_chart'] = 1
            viz_states['gun_chart'] = 1
            return choropleth_map
        elif viz_states['bar_chart_age']==1:
            intermediateBarChartAge = pd.read_json(intermediateBarChartAge)
            startDate = lineChartClick['xaxis.range[0]']
            endDate = lineChartClick['xaxis.range[1]']
            filter_by_date = intermediateBarChartAge[(intermediateBarChartAge['date']>=startDate) & (intermediateBarChartAge['date']<=endDate)]
            choropleth_map = create_choropleth_map(filter_by_date)
            viz_states['line_chart'] = 1
            viz_states['gun_chart'] = 1
            return choropleth_map
        elif viz_states['bar_chart_mental']==1:
            intermediateBarChartMental = pd.read_json(intermediateBarChartMental)
            startDate = lineChartClick['xaxis.range[0]']
            endDate = lineChartClick['xaxis.range[1]']
            filter_by_date = intermediateBarChartMental[(intermediateBarChartMental['date']>=startDate) & (intermediateBarChartMental['date']<=endDate)]
            choropleth_map = create_choropleth_map(filter_by_date)
            viz_states['line_chart'] = 1
            viz_states['gun_chart'] = 1
            return choropleth_map
        else:
            startDate = lineChartClick['xaxis.range[0]']
            endDate = lineChartClick['xaxis.range[1]']
            filter_by_date = df[(df['date']>=startDate) & (df['date']<=endDate)]
            choropleth_map = create_choropleth_map(filter_by_date)
            viz_states['line_chart'] = 1
            viz_states['gun_chart'] = 1
            return choropleth_map
    if triggered_element =='bar-chart-race':
        if viz_states['line_chart']==1:
            intermediateLineYearData = pd.read_json(intermediateLineYearData)
            race = raceBarChartClick['points'][0]['x']
            filter_by_race = intermediateLineYearData[intermediateLineYearData['race']==race]
            choropleth_map = create_choropleth_map(filter_by_race)
            viz_states['bar_chart_race'] = 1
            return choropleth_map
        elif viz_states['bar_chart_age']==1:
            intermediateBarChartAge = pd.read_json(intermediateBarChartAge)
            race = raceBarChartClick['points'][0]['x']
            filter_by_race = intermediateBarChartAge[intermediateBarChartAge['race']==race]
            choropleth_map = create_choropleth_map(filter_by_race)
            viz_states['bar_chart_race'] = 1
            return choropleth_map
        elif viz_states['bar_chart_mental']==1:
            intermediateBarChartMental = pd.read_json(intermediateBarChartMental)
            race = raceBarChartClick['points'][0]['x']
            filter_by_race = intermediateBarChartMental[intermediateBarChartMental['race']==race]
            choropleth_map = create_choropleth_map(filter_by_race)
            viz_states['bar_chart_race'] = 1
            return choropleth_map
        else:
            race = raceBarChartClick['points'][0]['x']
            filter_by_race = df[df['race']==race]
            choropleth_map = create_choropleth_map(filter_by_race)
            viz_states['bar_chart_race'] = 1
            return choropleth_map

    if triggered_element == "bar-chart-age":
        if viz_states['line_chart']==1:
            intermediateLineYearData = pd.read_json(intermediateLineYearData)
            gender, age= get_age_and_gender(ageBarClick)
            filter_by_age_gender = intermediateLineYearData[(intermediateLineYearData['gender']==gender) & (intermediateLineYearData['age_bins']==age)]
            choropleth_map = create_choropleth_map(filter_by_age_gender)
            viz_states['bar_chart_age'] = 1
            return choropleth_map
        elif viz_states['bar_chart_race']==1:
            intermediateBarChartRace = pd.read_json(intermediateBarChartRace)
            gender, age= get_age_and_gender(ageBarClick)
            filter_by_age_gender = intermediateBarChartRace[(intermediateBarChartRace['gender']==gender) & (intermediateBarChartRace['age_bins']==age)]
            choropleth_map = create_choropleth_map(filter_by_age_gender)
            viz_states['bar_chart_age'] = 1
            return choropleth_map
        elif viz_states['bar_chart_mental']==1:
            intermediateBarChartMental = pd.read_json(intermediateBarChartMental)
            gender, age= get_age_and_gender(ageBarClick)
            filter_by_age_gender = intermediateBarChartMental[(intermediateBarChartMental['gender']==gender) & (intermediateBarChartMental['age_bins']==age)]
            choropleth_map = create_choropleth_map(filter_by_age_gender)
            viz_states['bar_chart_age'] = 1
            return choropleth_map
        else:
            gender, age= get_age_and_gender(ageBarClick)
            filter_by_age_gender = df[(df['gender']==gender) & (df['age_bins']==age)]
            choropleth_map = create_choropleth_map(filter_by_age_gender)
            viz_states['bar_chart_age'] = 1
            return choropleth_map

    if triggered_element == 'mental-illness-bar':
        if viz_states['line_chart']==1:
            intermediateLineYearData = pd.read_json(intermediateLineYearData)
            mental_illness_value = mentalBarClick['points'][0]['x']
            filter_by_mental_illness = intermediateLineYearData[intermediateLineYearData['signs_of_mental_illness']==mental_illness_value]
            choropleth_map = create_choropleth_map(filter_by_mental_illness)
            viz_states['bar_chart_mental'] = 1
            return choropleth_map
        elif viz_states['bar_chart_race']==1:
            intermediateBarChartRace = pd.read_json(intermediateBarChartRace)
            mental_illness_value = mentalBarClick['points'][0]['x']
            filter_by_mental_illness = intermediateBarChartRace[intermediateBarChartRace['signs_of_mental_illness']==mental_illness_value]
            choropleth_map = create_choropleth_map(filter_by_mental_illness)
            viz_states['bar_chart_mental'] = 1
            return choropleth_map
        elif viz_states['bar_chart_age']==1:
            intermediateBarChartAge = pd.read_json(intermediateBarChartAge)
            mental_illness_value = mentalBarClick['points'][0]['x']
            filter_by_mental_illness = intermediateBarChartAge[intermediateBarChartAge['signs_of_mental_illness']==mental_illness_value]
            choropleth_map = create_choropleth_map(filter_by_mental_illness)
            viz_states['bar_chart_mental'] = 1
            return choropleth_map
        else:
            mental_illness_value = mentalBarClick['points'][0]['x']
            filter_by_mental_illness = df[df['signs_of_mental_illness']==mental_illness_value]
            choropleth_map = create_choropleth_map(filter_by_mental_illness)
            viz_states['bar_chart_mental'] = 1
            return choropleth_map

#update bar chart race
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
        viz_states['bar_chart_race']==0
        return create_bar_char_for_race(df)
    if viz_states['bar_chart_race']==1:
        return dash.no_update
    triggered_element = dash.callback_context.triggered[0]['prop_id'].split('.')[0]
    if triggered_element == 'gun-line-chart':
        if viz_states['gun_chart']==1:
            return dash.no_update
        startDate = gunClick['xaxis.range[0]']
        endDate = gunClick['xaxis.range[1]']
        filter_by_date = df[(df['date']>=startDate) & (df['date']<=endDate)]
        bar_chart_race = create_bar_char_for_race(filter_by_date)
        return bar_chart_race

    if triggered_element =='line-chart':
        if viz_states['choropleth_map']==1:
            intermediateChoroplethData = pd.read_json(intermediateChoroplethMap)
            startDate = lineChartClick['xaxis.range[0]']
            endDate = lineChartClick['xaxis.range[1]']
            filter_by_date = intermediateChoroplethData[(intermediateChoroplethData['date']>=startDate) & (intermediateChoroplethData['date']<=endDate)]
            bar_chart_race = create_bar_char_for_race(filter_by_date)
            viz_states['line_chart'] = 1
            viz_states['gun_chart'] = 1
            return bar_chart_race
        elif viz_states['bar_chart_age']==1:
            intermediateBarChartAge = pd.read_json(intermediateBarChartAge)
            startDate = lineChartClick['xaxis.range[0]']
            endDate = lineChartClick['xaxis.range[1]']
            filter_by_date = intermediateBarChartAge[(intermediateBarChartAge['date']>=startDate) & (intermediateBarChartAge['date']<=endDate)]
            bar_chart_race = create_bar_char_for_race(filter_by_date)
            viz_states['line_chart'] = 1
            viz_states['gun_chart'] = 1
            return bar_chart_race
        elif viz_states['bar_chart_mental']==1:
            intermediateBarChartMental = pd.read_json(intermediateBarChartMental)
            startDate = lineChartClick['xaxis.range[0]']
            endDate = lineChartClick['xaxis.range[1]']
            filter_by_date = intermediateBarChartMental[(intermediateBarChartMental['date']>=startDate) & (intermediateBarChartMental['date']<=endDate)]
            bar_chart_race = create_bar_char_for_race(filter_by_date)
            viz_states['line_chart'] = 1
            viz_states['gun_chart'] = 1
            return bar_chart_race
        else:
            startDate = lineChartClick['xaxis.range[0]']
            endDate = lineChartClick['xaxis.range[1]']
            filter_by_date = df[(df['date']>=startDate) & (df['date']<=endDate)]
            bar_chart_race = create_bar_char_for_race(filter_by_date)
            viz_states['line_chart'] = 1
            viz_states['gun_chart'] = 1
            return bar_chart_race

    if triggered_element=='choropleth-map':
        if viz_states['line_chart']== 1:
            intermediateLineYear = pd.read_json(intermediateLineYearData)
            filter_by_location = intermediateLineYear[intermediateLineYear['state']==mapClick['points'][0]['location']]
            bar_chart_race = create_bar_char_for_race(filter_by_location)
            viz_states['choropleth_map'] = 1
            return bar_chart_race
        elif viz_states['bar_chart_age']==1:
            intermediateBarChartAge = pd.read_json(intermediateBarChartAge)
            filter_by_location = intermediateBarChartAge[intermediateBarChartAge['state']==mapClick['points'][0]['location']]
            bar_chart_race = create_bar_char_for_race(filter_by_location)
            viz_states['choropleth_map'] = 1
            return bar_chart_race
        elif viz_states['bar_chart_mental']==1:
            intermediateBarChartMental = pd.read_json(intermediateBarChartMental)
            filter_by_location = intermediateBarChartMental[intermediateBarChartMental['state']==mapClick['points'][0]['location']]
            bar_chart_race = create_bar_char_for_race(filter_by_location)
            viz_states['choropleth_map'] = 1
            return bar_chart_race
        else:
            filter_by_location = df[df['state']==mapClick['points'][0]['location']]
            bar_chart_race = create_bar_char_for_race(filter_by_location)
            viz_states['choropleth_map'] = 1
            return bar_chart_race

    if triggered_element == 'bar-chart-age':
        if viz_states['line_chart']==1:
            intermediateLineYearData = pd.read_json(intermediateLineYearData)
            gender, age= get_age_and_gender(ageBarClick)
            filter_by_age_gender = intermediateLineYearData[(intermediateLineYearData['gender']==gender) & (intermediateLineYearData['age_bins']==age)]
            bar_chart_race = create_bar_char_for_race(filter_by_age_gender)
            viz_states['bar_chart_age'] = 1
            return bar_chart_race
        elif viz_states['choropleth_map']==1:
            intermediateChoroplethMap = pd.read_json(intermediateChoroplethMap)
            gender, age= get_age_and_gender(ageBarClick)
            filter_by_age_gender = intermediateChoroplethMap[(intermediateChoroplethMap['gender']==gender) & (intermediateChoroplethMap['age_bins']==age)]
            bar_chart_race = create_bar_char_for_race(filter_by_age_gender)
            viz_states['bar_chart_age'] = 1
            return bar_chart_race
        elif viz_states['bar_chart_mental']==1:
            intermediateBarChartMental = pd.read_json(intermediateBarChartMental)
            gender, age= get_age_and_gender(ageBarClick)
            filter_by_age_gender = intermediateBarChartMental[(intermediateBarChartMental['gender']==gender) & (intermediateBarChartMental['age_bins']==age)]
            bar_chart_race = create_bar_char_for_race(filter_by_age_gender)
            viz_states['bar_chart_age'] = 1
            return bar_chart_race
        else:
            gender, age= get_age_and_gender(ageBarClick)
            filter_by_age_gender = df[(df['gender']==gender) & (df['age_bins']==age)]
            bar_chart_race = create_bar_char_for_race(filter_by_age_gender)
            viz_states['bar_chart_age'] = 1
            return bar_chart_race

    if triggered_element == 'mental-illness-bar':
        if viz_states['line_chart']==1:
            intermediateLineYearData = pd.read_json(intermediateLineYearData)
            mental_illness_value = mentalBarClick['points'][0]['x']
            filter_by_mental_illness = intermediateLineYearData[intermediateLineYearData['signs_of_mental_illness']==mental_illness_value]
            bar_chart_race = create_bar_char_for_race(filter_by_mental_illness)
            viz_states['bar_chart_mental'] = 1
            return bar_chart_race
        elif viz_states['choropleth_map']==1:
            intermediateChoroplethMap = pd.read_json(intermediateChoroplethMap)
            mental_illness_value = mentalBarClick['points'][0]['x']
            filter_by_mental_illness = intermediateChoroplethMap[intermediateChoroplethMap['signs_of_mental_illness']==mental_illness_value]
            bar_chart_race = create_bar_char_for_race(filter_by_mental_illness)
            viz_states['bar_chart_mental'] = 1
            return bar_chart_race
        elif viz_states['bar_chart_age']==1:
            intermediateBarChartAge = pd.read_json(intermediateBarChartAge)
            mental_illness_value = mentalBarClick['points'][0]['x']
            filter_by_mental_illness = intermediateBarChartAge[intermediateBarChartAge['signs_of_mental_illness']==mental_illness_value]
            bar_chart_race = create_bar_char_for_race(filter_by_mental_illness)
            viz_states['bar_chart_mental'] = 1
            return bar_chart_race
        else:
            mental_illness_value = mentalBarClick['points'][0]['x']
            filter_by_mental_illness = df[df['signs_of_mental_illness']==mental_illness_value]
            bar_chart_race = create_bar_char_for_race(filter_by_mental_illness)
            viz_states['bar_chart_mental'] = 1
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
        viz_states['line_chart']==0
        return create_line_chart(df)
    triggered_element = dash.callback_context.triggered[0]['prop_id'].split('.')[0]
    if viz_states['line_chart']==1:
        return dash.no_update
    if triggered_element == 'gun-line-chart':
        if viz_states['gun_chart']==1:
            return dash.no_update
        startDate = gunClick['xaxis.range[0]']
        endDate = gunClick['xaxis.range[1]']
        filter_by_date = df[(df['date']>=startDate) & (df['date']<=endDate)]
        line_chart = create_line_chart(filter_by_date)
        return line_chart
    if triggered_element =='bar-chart-race':
        if viz_states['choropleth_map']==1:
            intermediateChoroplethData = pd.read_json(intermediateChoroplethMap)
            race = raceBarChartClick['points'][0]['x']
            filter_by_race = intermediateChoroplethData[intermediateChoroplethData['race']==race]
            line_chart = create_line_chart(filter_by_race)
            viz_states['bar_chart_race'] = 1
            return line_chart
        elif viz_states['bar_chart_age']==1:
            intermediateBarChartAge = pd.read_json(intermediateBarChartAge)
            race = raceBarChartClick['points'][0]['x']
            filter_by_race = intermediateBarChartAge[intermediateBarChartAge['race']==race]
            line_chart = create_line_chart(filter_by_race)
            viz_states['bar_chart_race'] = 1
            return line_chart
        elif viz_states['bar_chart_mental']==1:
            intermediateBarChartMental = pd.read_json(intermediateBarChartMental)
            race = raceBarChartClick['points'][0]['x']
            filter_by_race = intermediateBarChartMental[intermediateBarChartMental['race']==race]
            line_chart = create_line_chart(filter_by_race)
            viz_states['bar_chart_race'] = 1
            return line_chart
        else:
            race = raceBarChartClick['points'][0]['x']
            filter_by_race = df[df['race']==race]
            line_chart = create_line_chart(filter_by_race)
            viz_states['bar_chart_race'] = 1
            return line_chart

    if triggered_element == 'choropleth-map':
        if viz_states['bar_chart_race']==1:
            intermediateBarRace = pd.read_json(intermediateBarChartRace)
            filter_by_location = intermediateBarRace[intermediateBarRace['state']==mapClick['points'][0]['location']]
            line_chart = create_line_chart(filter_by_location)
            viz_states['choropleth_map'] = 1
            return line_chart
        elif viz_states['bar_chart_age']==1:
            intermediateBarChartAge = pd.read_json(intermediateBarChartAge)
            filter_by_location = intermediateBarChartAge[intermediateBarChartAge['state']==mapClick['points'][0]['location']]
            line_chart = create_line_chart(filter_by_location)
            viz_states['choropleth_map'] = 1
            return line_chart
        elif viz_states['bar_chart_mental']==1:
            intermediateBarChartMental = pd.read_json(intermediateBarChartMental)
            filter_by_location = intermediateBarChartMental[intermediateBarChartMental['state']==mapClick['points'][0]['location']]
            line_chart = create_line_chart(filter_by_location)
            viz_states['choropleth_map'] = 1
            return line_chart
        else:
            filter_by_location = df[df['state']==mapClick['points'][0]['location']]
            line_chart = create_line_chart(filter_by_location)
            viz_states['choropleth_map'] = 1
            return line_chart

    if triggered_element == "bar-chart-age":
        if viz_states['choropleth_map']==1:
            intermediateChoroplethMap = pd.read_json(intermediateChoroplethMap)
            gender, age= get_age_and_gender(ageBarClick)
            filter_by_age_gender = intermediateChoroplethMap[(intermediateChoroplethMap['gender']==gender) & (intermediateChoroplethMap['age_bins']==age)]
            line_chart = create_line_chart(filter_by_age_gender)
            viz_states['bar_chart_age'] = 1
            return line_chart
        elif viz_states['bar_chart_race']==1:
            intermediateBarChartRace = pd.read_json(intermediateBarChartRace)
            gender, age= get_age_and_gender(ageBarClick)
            filter_by_age_gender = intermediateBarChartRace[(intermediateBarChartRace['gender']==gender) & (intermediateBarChartRace['age_bins']==age)]
            line_chart = create_line_chart(filter_by_age_gender)
            viz_states['bar_chart_age'] = 1
            return line_chart
        elif viz_states['bar_chart_mental']==1:
            intermediateBarChartMental = pd.read_json(intermediateBarChartMental)
            gender, age= get_age_and_gender(ageBarClick)
            filter_by_age_gender = intermediateBarChartMental[(intermediateBarChartMental['gender']==gender) & (intermediateBarChartMental['age_bins']==age)]
            line_chart = create_line_chart(filter_by_age_gender)
            viz_states['bar_chart_age'] = 1
            return line_chart
        else:
            gender, age= get_age_and_gender(ageBarClick)
            filter_by_age_gender = df[(df['gender']==gender) & (df['age_bins']==age)]
            line_chart = create_line_chart(filter_by_age_gender)
            viz_states['bar_chart_age'] = 1
            return line_chart

    if triggered_element == 'mental-illness-bar':
        if viz_states['bar_chart_race']==1:
            intermediateBarChartRace = pd.read_json(intermediateBarChartRace)
            mental_illness_value = mentalBarClick['points'][0]['x']
            filter_by_mental_illness = intermediateBarChartRace[intermediateBarChartRace['signs_of_mental_illness']==mental_illness_value]
            line_chart = create_line_chart(filter_by_mental_illness)
            viz_states['bar_chart_mental'] = 1
            return line_chart
        elif viz_states['choropleth_map']==1:
            intermediateChoroplethMap = pd.read_json(intermediateChoroplethMap)
            mental_illness_value = mentalBarClick['points'][0]['x']
            filter_by_mental_illness = intermediateChoroplethMap[intermediateChoroplethMap['signs_of_mental_illness']==mental_illness_value]
            line_chart = create_line_chart(filter_by_mental_illness)
            viz_states['bar_chart_mental'] = 1
            return line_chart
        elif viz_states['bar_chart_age']==1:
            intermediateBarChartAge = pd.read_json(intermediateBarChartAge)
            mental_illness_value = mentalBarClick['points'][0]['x']
            filter_by_mental_illness = intermediateBarChartAge[intermediateBarChartAge['signs_of_mental_illness']==mental_illness_value]
            line_chart = create_line_chart(filter_by_mental_illness)
            viz_states['bar_chart_mental'] = 1
            return line_chart
        else:
            mental_illness_value = mentalBarClick['points'][0]['x']
            filter_by_mental_illness = df[df['signs_of_mental_illness']==mental_illness_value]
            line_chart = create_line_chart(filter_by_mental_illness)
            viz_states['bar_chart_mental'] = 1
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
        viz_states['bar_chart_age']==0
        return create_bar_chart_for_age_and_gender(df)
    if viz_states['bar_chart_age']==1:
        return dash.no_update
    triggered_element = dash.callback_context.triggered[0]['prop_id'].split('.')[0]
    if triggered_element == 'gun-line-chart':
        if viz_states['gun_chart']==1:
            return dash.no_update
        startDate = gunClick['xaxis.range[0]']
        endDate = gunClick['xaxis.range[1]']
        filter_by_date = df[(df['date']>=startDate) & (df['date']<=endDate)]
        bar_chart_by_age = create_bar_chart_for_age_and_gender(filter_by_date)
        return bar_chart_by_age
    if triggered_element == 'choropleth-map':
        if viz_states['bar_chart_race']==1:
            intermediateBarRace = pd.read_json(intermediateBarChartRace)
            filter_by_location = intermediateBarRace[intermediateBarRace['state']==mapClick['points'][0]['location']]
            bar_chart_by_age = create_bar_chart_for_age_and_gender(filter_by_location)
            viz_states['choropleth_map'] = 1
            return bar_chart_by_age
        elif viz_states['line_chart']==1:
            intermediateLineYearData = pd.read_json(intermediateLineYearData)
            filter_by_location = intermediateLineYearData[intermediateLineYearData['state']==mapClick['points'][0]['location']]
            bar_chart_by_age = create_bar_chart_for_age_and_gender(filter_by_location)
            viz_states['choropleth_map'] = 1
            return bar_chart_by_age
        elif viz_states['bar_chart_mental']==1:
            intermediateBarChartMental = pd.read_json(intermediateBarChartMental)
            filter_by_location = intermediateBarChartMental[intermediateBarChartMental['state']==mapClick['points'][0]['location']]
            bar_chart_by_age = create_bar_chart_for_age_and_gender(filter_by_location)
            viz_states['choropleth_map'] = 1
            return bar_chart_by_age
        else:
            filter_by_location = df[df['state']==mapClick['points'][0]['location']]
            bar_chart_by_age = create_bar_chart_for_age_and_gender(filter_by_location)
            viz_states['choropleth_map'] = 1
            return bar_chart_by_age

    if triggered_element =='bar-chart-race':
        if viz_states['choropleth_map']==1:
            intermediateChoroplethMap = pd.read_json(intermediateChoroplethMap)
            race = raceBarChartClick['points'][0]['x']
            filter_by_race = intermediateChoroplethMap[intermediateChoroplethMap['race']==race]
            bar_chart_by_age = create_bar_chart_for_age_and_gender(filter_by_race)
            viz_states['bar_chart_race'] = 1
            return bar_chart_by_age
        elif viz_states['line_chart']==1:
            intermediateLineYearData = pd.read_json(intermediateLineYearData)
            race = raceBarChartClick['points'][0]['x']
            filter_by_race = intermediateLineYearData[intermediateLineYearData['race']==race]
            bar_chart_by_age = create_bar_chart_for_age_and_gender(filter_by_race)
            viz_states['bar_chart_race'] = 1
            return bar_chart_by_age
        elif viz_states['bar_chart_mental']==1:
            intermediateBarChartMental = pd.read_json(intermediateBarChartMental)
            race = raceBarChartClick['points'][0]['x']
            filter_by_race = intermediateBarChartMental[intermediateBarChartMental['race']==race]
            bar_chart_by_age = create_bar_chart_for_age_and_gender(filter_by_race)
            viz_states['bar_chart_race'] = 1
            return bar_chart_by_age
        else:
            race = raceBarChartClick['points'][0]['x']
            filter_by_race = df[df['race']==race]
            bar_chart_by_age = create_bar_chart_for_age_and_gender(filter_by_race)
            viz_states['bar_chart_race'] = 1
            return bar_chart_by_age

    if triggered_element == 'line-chart':
        if viz_states['choropleth_map']==1:
            intermediateChoroplethMap = pd.read_json(intermediateChoroplethMap)
            startDate = lineChartClick['xaxis.range[0]']
            endDate = lineChartClick['xaxis.range[1]']
            filter_by_date = intermediateChoroplethMap[(intermediateChoroplethMap['date']>=startDate) & (intermediateChoroplethMap['date']<=endDate)]
            bar_chart_by_age = create_bar_chart_for_age_and_gender(filter_by_date)
            viz_states['line_chart'] = 1
            viz_states['gun_chart'] = 1
            return bar_chart_by_age
        elif viz_states['bar_chart_race']==1:
            intermediateBarChartRace = pd.read_json(intermediateBarChartRace)
            startDate = lineChartClick['xaxis.range[0]']
            endDate = lineChartClick['xaxis.range[1]']
            filter_by_date = intermediateBarChartRace[(intermediateBarChartRace['date']>=startDate) & (intermediateBarChartRace['date']<=endDate)]
            bar_chart_by_age = create_bar_chart_for_age_and_gender(filter_by_date)
            viz_states['line_chart'] = 1
            viz_states['gun_chart'] = 1
            return bar_chart_by_age
        elif viz_states['bar_chart_mental']==1:
            intermediateBarChartMental = pd.read_json(intermediateBarChartMental)
            startDate = lineChartClick['xaxis.range[0]']
            endDate = lineChartClick['xaxis.range[1]']
            filter_by_date = intermediateBarChartMental[(intermediateBarChartMental['date']>=startDate) & (intermediateBarChartMental['date']<=endDate)]
            bar_chart_by_age = create_bar_chart_for_age_and_gender(filter_by_date)
            viz_states['line_chart'] = 1
            viz_states['gun_chart'] = 1
            return bar_chart_by_age
        else:
            startDate = lineChartClick['xaxis.range[0]']
            endDate = lineChartClick['xaxis.range[1]']
            filter_by_date = df[(df['date']>=startDate) & (df['date']<=endDate)]
            bar_chart_by_age = create_bar_chart_for_age_and_gender(filter_by_date)
            viz_states['line_chart'] = 1
            viz_states['gun_chart'] = 1
            return bar_chart_by_age

    if triggered_element == 'mental-illness-bar':
        if viz_states['bar_chart_race']==1:
            intermediateBarChartRace = pd.read_json(intermediateBarChartRace)
            mental_illness_value = mentalBarClick['points'][0]['x']
            filter_by_mental_illness = intermediateBarChartRace[intermediateBarChartRace['signs_of_mental_illness']==mental_illness_value]
            bar_chart_by_age = create_bar_chart_for_age_and_gender(filter_by_mental_illness)
            viz_states['bar_chart_mental'] = 1
            viz_states['gun_chart'] = 1
            return bar_chart_by_age
        elif viz_states['choropleth_map']==1:
            intermediateChoroplethMap = pd.read_json(intermediateChoroplethMap)
            mental_illness_value = mentalBarClick['points'][0]['x']
            filter_by_mental_illness = intermediateChoroplethMap[intermediateChoroplethMap['signs_of_mental_illness']==mental_illness_value]
            bar_chart_by_age = create_bar_chart_for_age_and_gender(filter_by_mental_illness)
            viz_states['bar_chart_mental'] = 1
            viz_states['gun_chart'] = 1
            return bar_chart_by_age
        elif viz_states['line_chart']==1:
            intermediateLineYearData = pd.read_json(intermediateLineYearData)
            mental_illness_value = mentalBarClick['points'][0]['x']
            filter_by_mental_illness = intermediateLineYearData[intermediateLineYearData['signs_of_mental_illness']==mental_illness_value]
            bar_chart_by_age = create_bar_chart_for_age_and_gender(filter_by_mental_illness)
            viz_states['bar_chart_mental'] = 1
            viz_states['gun_chart'] = 1
            return bar_chart_by_age
        else:
            mental_illness_value = mentalBarClick['points'][0]['x']
            filter_by_mental_illness = df[df['signs_of_mental_illness']==mental_illness_value]
            bar_chart_by_age = create_bar_chart_for_age_and_gender(filter_by_mental_illness)
            viz_states['bar_chart_mental'] = 1
            viz_states['gun_chart'] = 1
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
        viz_states['bar_chart_mental']==0
        return create_bar_chart_for_mental_illness(df)
    if viz_states['bar_chart_mental']==1:
        return dash.no_update
    triggered_element = dash.callback_context.triggered[0]['prop_id'].split('.')[0]
    if triggered_element == 'gun-line-chart':
        if viz_states['gun_chart']==1:
            return dash.no_update
        startDate = gunClick['xaxis.range[0]']
        endDate = gunClick['xaxis.range[1]']
        filter_by_date = df[(df['date']>=startDate) & (df['date']<=endDate)]
        bar_chart_by_mental_illness = create_bar_chart_for_mental_illness(filter_by_date)
        return bar_chart_by_mental_illness
    if triggered_element == 'choropleth-map':
        if viz_states['bar_chart_race']==1:
            intermediateBarRace = pd.read_json(intermediateBarChartRace)
            filter_by_location = intermediateBarRace[intermediateBarRace['state']==mapClick['points'][0]['location']]
            bar_chart_by_mental_illness = create_bar_chart_for_mental_illness(filter_by_location)
            viz_states['choropleth_map'] = 1
            return bar_chart_by_mental_illness
        elif viz_states['line_chart']==1:
            intermediateLineYearData = pd.read_json(intermediateLineYearData)
            filter_by_location = intermediateLineYearData[intermediateLineYearData['state']==mapClick['points'][0]['location']]
            bar_chart_by_mental_illness = create_bar_chart_for_mental_illness(filter_by_location)
            viz_states['choropleth_map'] = 1
            return bar_chart_by_mental_illness
        elif viz_states['bar_chart_age']==1:
            intermediateBarChartAge = pd.read_json(intermediateBarChartAge)
            filter_by_location = intermediateBarChartAge[intermediateBarChartAge['state']==mapClick['points'][0]['location']]
            bar_chart_by_mental_illness = create_bar_chart_for_mental_illness(filter_by_location)
            viz_states['choropleth_map'] = 1
            return bar_chart_by_mental_illness
        else:
            filter_by_location = df[df['state']==mapClick['points'][0]['location']]
            bar_chart_by_mental_illness = create_bar_chart_for_mental_illness(filter_by_location)
            viz_states['choropleth_map'] = 1
            return bar_chart_by_mental_illness

    if triggered_element =='bar-chart-race':
        if viz_states['choropleth_map']==1:
            intermediateChoroplethMap = pd.read_json(intermediateChoroplethMap)
            race = raceBarChartClick['points'][0]['x']
            filter_by_race = intermediateChoroplethMap[intermediateChoroplethMap['race']==race]
            bar_chart_by_mental_illness = create_bar_chart_for_mental_illness(filter_by_race)
            viz_states['bar_chart_race'] = 1
            return bar_chart_by_mental_illness
        elif viz_states['line_chart']==1:
            intermediateLineYearData = pd.read_json(intermediateLineYearData)
            race = raceBarChartClick['points'][0]['x']
            filter_by_race = intermediateLineYearData[intermediateLineYearData['race']==race]
            bar_chart_by_mental_illness = create_bar_chart_for_mental_illness(filter_by_race)
            viz_states['bar_chart_race'] = 1
            return bar_chart_by_mental_illness
        elif viz_states['bar_chart_mental']==1:
            intermediateBarChartMental = pd.read_json(intermediateBarChartMental)
            race = raceBarChartClick['points'][0]['x']
            filter_by_race = intermediateBarChartMental[intermediateBarChartMental['race']==race]
            bar_chart_by_mental_illness = create_bar_chart_for_mental_illness(filter_by_race)
            viz_states['bar_chart_race'] = 1
            return bar_chart_by_mental_illness
        else:
            race = raceBarChartClick['points'][0]['x']
            filter_by_race = df[df['race']==race]
            bar_chart_by_mental_illness = create_bar_chart_for_mental_illness(filter_by_race)
            viz_states['bar_chart_race'] = 1
            return bar_chart_by_mental_illness

    if triggered_element == 'line-chart':
        if viz_states['choropleth_map']==1:
            intermediateChoroplethMap = pd.read_json(intermediateChoroplethMap)
            startDate = lineChartClick['xaxis.range[0]']
            endDate = lineChartClick['xaxis.range[1]']
            filter_by_date = intermediateChoroplethMap[(intermediateChoroplethMap['date']>=startDate) & (intermediateChoroplethMap['date']<=endDate)]
            bar_chart_by_mental_illness = create_bar_chart_for_mental_illness(filter_by_date)
            viz_states['line_chart'] = 1
            viz_states['gun_chart'] = 1
            return bar_chart_by_mental_illness
        elif viz_states['bar_chart_race']==1:
            intermediateBarChartRace = pd.read_json(intermediateBarChartRace)
            startDate = lineChartClick['xaxis.range[0]']
            endDate = lineChartClick['xaxis.range[1]']
            filter_by_date = intermediateBarChartRace[(intermediateBarChartRace['date']>=startDate) & (intermediateBarChartRace['date']<=endDate)]
            bar_chart_by_mental_illness = create_bar_chart_for_mental_illness(filter_by_date)
            viz_states['line_chart'] = 1
            viz_states['gun_chart'] = 1
            return bar_chart_by_mental_illness
        elif viz_states['bar_chart_mental']==1:
            intermediateBarChartMental = pd.read_json(intermediateBarChartMental)
            startDate = lineChartClick['xaxis.range[0]']
            endDate = lineChartClick['xaxis.range[1]']
            filter_by_date = intermediateBarChartMental[(intermediateBarChartMental['date']>=startDate) & (intermediateBarChartMental['date']<=endDate)]
            bar_chart_by_mental_illness = create_bar_chart_for_mental_illness(filter_by_date)
            viz_states['line_chart'] = 1
            viz_states['gun_chart'] = 1
            return bar_chart_by_mental_illness
        else:
            startDate = lineChartClick['xaxis.range[0]']
            endDate = lineChartClick['xaxis.range[1]']
            filter_by_date = df[(df['date']>=startDate) & (df['date']<=endDate)]
            bar_chart_by_mental_illness = create_bar_chart_for_mental_illness(filter_by_date)
            viz_states['line_chart'] = 1
            viz_states['gun_chart'] = 1
            return bar_chart_by_mental_illness

    if triggered_element == 'bar-chart-age':
        if viz_states['bar_chart_race']==1:
            intermediateBarChartRace = pd.read_json(intermediateBarChartRace)
            gender, age= get_age_and_gender(ageBarClick)
            filter_by_age_gender = intermediateBarChartRace[(intermediateBarChartRace['gender']==gender) & (intermediateBarChartRace['age_bins']==age)]
            bar_chart_by_mental_illness = create_bar_chart_for_mental_illness(filter_by_age_gender)
            viz_states['bar_chart_age'] = 1
            return bar_chart_by_mental_illness
        elif viz_states['choropleth_map']==1:
            intermediateChoroplethMap = pd.read_json(intermediateChoroplethMap)
            gender, age= get_age_and_gender(ageBarClick)
            filter_by_age_gender = intermediateChoroplethMap[(intermediateChoroplethMap['gender']==gender) & (intermediateChoroplethMap['age_bins']==age)]
            bar_chart_by_mental_illness = create_bar_chart_for_mental_illness(filter_by_age_gender)
            viz_states['bar_chart_age'] = 1
            return bar_chart_by_mental_illness
        elif viz_states['line_chart']==1:
            intermediateLineYearData = pd.read_json(intermediateLineYearData)
            gender, age= get_age_and_gender(ageBarClick)
            filter_by_age_gender = intermediateLineYearData[(intermediateLineYearData['gender']==gender) & (intermediateLineYearData['age_bins']==age)]
            bar_chart_by_mental_illness = create_bar_chart_for_mental_illness(filter_by_age_gender)
            viz_states['bar_chart_age'] = 1
            return bar_chart_by_mental_illness
        else:
            gender, age= get_age_and_gender(ageBarClick)
            filter_by_age_gender = df[(df['gender']==gender) & (df['age_bins']==age)]
            bar_chart_by_mental_illness = create_bar_chart_for_mental_illness(filter_by_age_gender)
            viz_states['bar_chart_age'] = 1
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
        viz_states['radar_chart_weapons']==0
        return create_radar_chart_for_weapons(df)
    if viz_states['radar_chart_weapons']==1:
        return dash.no_update
    triggered_element = dash.callback_context.triggered[0]['prop_id'].split('.')[0]
    if triggered_element == 'gun-line-chart':
        if viz_states['gun_chart']==1:
            return dash.no_update
        startDate = gunClick['xaxis.range[0]']
        endDate = gunClick['xaxis.range[1]']
        filter_by_date = df[(df['date']>=startDate) & (df['date']<=endDate)]
        radar_chart_for_weapons = create_radar_chart_for_weapons(filter_by_date)
        return radar_chart_for_weapons
    if triggered_element == 'choropleth-map':
        if viz_states['bar_chart_race']==1:
            intermediateBarRace = pd.read_json(intermediateBarChartRace)
            filter_by_location = intermediateBarRace[intermediateBarRace['state']==mapClick['points'][0]['location']]
            radar_chart_for_weapons = create_radar_chart_for_weapons(filter_by_location)
            viz_states['choropleth_map'] = 1
            return radar_chart_for_weapons
        elif viz_states['line_chart']==1:
            intermediateLineYearData = pd.read_json(intermediateLineYearData)
            filter_by_location = intermediateLineYearData[intermediateLineYearData['state']==mapClick['points'][0]['location']]
            radar_chart_for_weapons = create_radar_chart_for_weapons(filter_by_location)
            viz_states['choropleth_map'] = 1
            return radar_chart_for_weapons
        elif viz_states['bar_chart_age']==1:
            intermediateBarChartAge = pd.read_json(intermediateBarChartAge)
            filter_by_location = intermediateBarChartAge[intermediateBarChartAge['state']==mapClick['points'][0]['location']]
            radar_chart_for_weapons = create_radar_chart_for_weapons(filter_by_location)
            viz_states['choropleth_map'] = 1
            return radar_chart_for_weapons
        elif viz_states['bar_chart_mental']==1:
            intermediateBarChartMental = pd.read_json(intermediateBarChartMental)
            filter_by_location = intermediateBarChartMental[intermediateBarChartMental['state']==mapClick['points'][0]['location']]
            radar_chart_for_weapons = create_radar_chart_for_weapons(filter_by_location)
            viz_states['choropleth_map'] = 1
            return radar_chart_for_weapons
        else:
            filter_by_location = df[df['state']==mapClick['points'][0]['location']]
            radar_chart_for_weapons = create_radar_chart_for_weapons(filter_by_location)
            viz_states['choropleth_map'] = 1
            return radar_chart_for_weapons

    if triggered_element =='bar-chart-race':
        if viz_states['choropleth_map']==1:
            intermediateChoroplethMap = pd.read_json(intermediateChoroplethMap)
            race = raceBarChartClick['points'][0]['x']
            filter_by_race = intermediateChoroplethMap[intermediateChoroplethMap['race']==race]
            radar_chart_for_weapons = create_radar_chart_for_weapons(filter_by_race)
            viz_states['bar_chart_race'] = 1
            return radar_chart_for_weapons
        elif viz_states['line_chart']==1:
            intermediateLineYearData = pd.read_json(intermediateLineYearData)
            race = raceBarChartClick['points'][0]['x']
            filter_by_race = intermediateLineYearData[intermediateLineYearData['race']==race]
            radar_chart_for_weapons = create_radar_chart_for_weapons(filter_by_race)
            viz_states['bar_chart_race'] = 1
            return radar_chart_for_weapons
        elif viz_states['bar_chart_mental']==1:
            intermediateBarChartMental = pd.read_json(intermediateBarChartMental)
            race = raceBarChartClick['points'][0]['x']
            filter_by_race = intermediateBarChartMental[intermediateBarChartMental['race']==race]
            radar_chart_for_weapons = create_radar_chart_for_weapons(filter_by_race)
            viz_states['bar_chart_race'] = 1
            return radar_chart_for_weapons
        elif viz_states['bar_chart_age']==1:
            intermediateBarChartAge = pd.read_json(intermediateBarChartAge)
            race = raceBarChartClick['points'][0]['x']
            filter_by_race = intermediateBarChartAge[intermediateBarChartAge['race']==race]
            radar_chart_for_weapons = create_radar_chart_for_weapons(filter_by_race)
            viz_states['bar_chart_race'] = 1
            return radar_chart_for_weapons
        else:
            race = raceBarChartClick['points'][0]['x']
            filter_by_race = df[df['race']==race]
            radar_chart_for_weapons = create_radar_chart_for_weapons(filter_by_race)
            viz_states['bar_chart_race'] = 1
            return radar_chart_for_weapons

    if triggered_element == 'line-chart':
        if viz_states['choropleth_map']==1:
            intermediateChoroplethMap = pd.read_json(intermediateChoroplethMap)
            startDate = lineChartClick['xaxis.range[0]']
            endDate = lineChartClick['xaxis.range[1]']
            filter_by_date = intermediateChoroplethMap[(intermediateChoroplethMap['date']>=startDate) & (intermediateChoroplethMap['date']<=endDate)]
            radar_chart_for_weapons = create_radar_chart_for_weapons(filter_by_date)
            viz_states['line_chart'] = 1
            viz_states['gun_chart'] = 1
            return radar_chart_for_weapons
        elif viz_states['bar_chart_race']==1:
            intermediateBarChartRace = pd.read_json(intermediateBarChartRace)
            startDate = lineChartClick['xaxis.range[0]']
            endDate = lineChartClick['xaxis.range[1]']
            filter_by_date = intermediateBarChartRace[(intermediateBarChartRace['date']>=startDate) & (intermediateBarChartRace['date']<=endDate)]
            radar_chart_for_weapons = create_radar_chart_for_weapons(filter_by_date)
            viz_states['line_chart'] = 1
            viz_states['gun_chart'] = 1
            return radar_chart_for_weapons
        elif viz_states['bar_chart_mental']==1:
            intermediateBarChartMental = pd.read_json(intermediateBarChartMental)
            startDate = lineChartClick['xaxis.range[0]']
            endDate = lineChartClick['xaxis.range[1]']
            filter_by_date = intermediateBarChartMental[(intermediateBarChartMental['date']>=startDate) & (intermediateBarChartMental['date']<=endDate)]
            radar_chart_for_weapons = create_radar_chart_for_weapons(filter_by_date)
            viz_states['line_chart'] = 1
            viz_states['gun_chart'] = 1
            return radar_chart_for_weapons
        elif viz_states['bar_chart_age']==1:
            intermediateBarChartAge = pd.read_json(intermediateBarChartAge)
            startDate = lineChartClick['xaxis.range[0]']
            endDate = lineChartClick['xaxis.range[1]']
            filter_by_date = intermediateBarChartAge[(intermediateBarChartAge['date']>=startDate) & (intermediateBarChartAge['date']<=endDate)]
            radar_chart_for_weapons = create_radar_chart_for_weapons(filter_by_date)
            viz_states['line_chart'] = 1
            viz_states['gun_chart'] = 1
            return radar_chart_for_weapons
        else:
            startDate = lineChartClick['xaxis.range[0]']
            endDate = lineChartClick['xaxis.range[1]']
            filter_by_date = df[(df['date']>=startDate) & (df['date']<=endDate)]
            radar_chart_for_weapons = create_radar_chart_for_weapons(filter_by_date)
            viz_states['line_chart'] = 1
            viz_states['gun_chart'] = 1
            return radar_chart_for_weapons

    if triggered_element == 'bar-chart-age':
        if viz_states['bar_chart_race']==1:
            intermediateBarChartRace = pd.read_json(intermediateBarChartRace)
            gender, age= get_age_and_gender(ageBarClick)
            filter_by_age_gender = intermediateBarChartRace[(intermediateBarChartRace['gender']==gender) & (intermediateBarChartRace['age_bins']==age)]
            radar_chart_for_weapons = create_radar_chart_for_weapons(filter_by_age_gender)
            viz_states['bar_chart_age'] = 1
            return radar_chart_for_weapons
        elif viz_states['choropleth_map']==1:
            intermediateChoroplethMap = pd.read_json(intermediateChoroplethMap)
            gender, age= get_age_and_gender(ageBarClick)
            filter_by_age_gender = intermediateChoroplethMap[(intermediateChoroplethMap['gender']==gender) & (intermediateChoroplethMap['age_bins']==age)]
            radar_chart_for_weapons = create_radar_chart_for_weapons(filter_by_age_gender)
            viz_states['bar_chart_age'] = 1
            return radar_chart_for_weapons
        elif viz_states['line_chart']==1:
            intermediateLineYearData = pd.read_json(intermediateLineYearData)
            gender, age= get_age_and_gender(ageBarClick)
            filter_by_age_gender = intermediateLineYearData[(intermediateLineYearData['gender']==gender) & (intermediateLineYearData['age_bins']==age)]
            radar_chart_for_weapons = create_radar_chart_for_weapons(filter_by_age_gender)
            viz_states['bar_chart_age'] = 1
            return radar_chart_for_weapons
        elif viz_states['bar_chart_mental']==1:
            intermediateBarChartMental = pd.read_json(intermediateBarChartMental)
            gender, age= get_age_and_gender(ageBarClick)
            filter_by_age_gender = intermediateBarChartMental[(intermediateBarChartMental['gender']==gender) & (intermediateBarChartMental['age_bins']==age)]
            radar_chart_for_weapons = create_radar_chart_for_weapons(filter_by_age_gender)
            viz_states['bar_chart_age'] = 1
            return radar_chart_for_weapons
        else:
            gender, age= get_age_and_gender(ageBarClick)
            filter_by_age_gender = df[(df['gender']==gender) & (df['age_bins']==age)]
            radar_chart_for_weapons = create_radar_chart_for_weapons(filter_by_age_gender)
            viz_states['bar_chart_age'] = 1
            return radar_chart_for_weapons

    if triggered_element == 'mental-illness-bar':
        if viz_states['bar_chart_race']==1:
            intermediateBarChartRace = pd.read_json(intermediateBarChartRace)
            mental_illness_value = mentalBarClick['points'][0]['x']
            filter_by_mental_illness = intermediateBarChartRace[intermediateBarChartRace['signs_of_mental_illness']==mental_illness_value]
            radar_chart_for_weapons = create_radar_chart_for_weapons(filter_by_mental_illness)
            viz_states['bar_chart_mental'] = 1
            return radar_chart_for_weapons
        elif viz_states['choropleth_map']==1:
            intermediateChoroplethMap = pd.read_json(intermediateChoroplethMap)
            mental_illness_value = mentalBarClick['points'][0]['x']
            filter_by_mental_illness = intermediateChoroplethMap[intermediateChoroplethMap['signs_of_mental_illness']==mental_illness_value]
            radar_chart_for_weapons = create_radar_chart_for_weapons(filter_by_mental_illness)
            viz_states['bar_chart_mental'] = 1
            return radar_chart_for_weapons
        elif viz_states['line_chart']==1:
            intermediateLineYearData = pd.read_json(intermediateLineYearData)
            mental_illness_value = mentalBarClick['points'][0]['x']
            filter_by_mental_illness = intermediateLineYearData[intermediateLineYearData['signs_of_mental_illness']==mental_illness_value]
            radar_chart_for_weapons = create_radar_chart_for_weapons(filter_by_mental_illness)
            viz_states['bar_chart_mental'] = 1
            return radar_chart_for_weapons
        elif viz_states['bar_chart_mental']==1:
            intermediateBarChartMental = pd.read_json(intermediateBarChartMental)
            mental_illness_value = mentalBarClick['points'][0]['x']
            filter_by_mental_illness = intermediateBarChartMental[intermediateBarChartMental['signs_of_mental_illness']==mental_illness_value]
            radar_chart_for_weapons = create_radar_chart_for_weapons(filter_by_mental_illness)
            viz_states['bar_chart_mental'] = 1
            return radar_chart_for_weapons
        elif viz_states['bar_chart_age']==1:
            intermediateBarChartAge = pd.read_json(intermediateBarChartAge)
            mental_illness_value = mentalBarClick['points'][0]['x']
            filter_by_mental_illness = intermediateBarChartAge[intermediateBarChartAge['signs_of_mental_illness']==mental_illness_value]
            radar_chart_for_weapons = create_radar_chart_for_weapons(filter_by_mental_illness)
            viz_states['bar_chart_mental'] = 1
            return radar_chart_for_weapons
        else:
            mental_illness_value = mentalBarClick['points'][0]['x']
            filter_by_mental_illness = df[df['signs_of_mental_illness']==mental_illness_value]
            radar_chart_for_weapons = create_radar_chart_for_weapons(filter_by_mental_illness)
            viz_states['bar_chart_mental'] = 1
            return radar_chart_for_weapons

#update sankey diagram
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
        return create_sankey_diagram(df)
    triggered_element = dash.callback_context.triggered[0]['prop_id'].split('.')[0]
    if triggered_element == 'gun-line-chart':
        if viz_states['gun_chart']==1:
            return dash.no_update
        startDate = gunClick['xaxis.range[0]']
        endDate = gunClick['xaxis.range[1]']
        filter_by_date = df[(df['date']>=startDate) & (df['date']<=endDate)]
        sankey_diagram = create_sankey_diagram(filter_by_date)
        return sankey_diagram
    if triggered_element =='bar-chart-race':
        if viz_states['bar_chart_age']==1:
            intermediateBarChartAge = pd.read_json(intermediateBarChartAge)
            race = raceBarChartClick['points'][0]['x']
            filter_by_race = intermediateBarChartAge[intermediateBarChartAge['race']==race]
            sankey_diagram = create_sankey_diagram(filter_by_race)
            viz_states['bar_chart_race'] = 1
            return sankey_diagram
        elif viz_states['choropleth_map']==1:
            intermediateChoroplethMap = pd.read_json(intermediateChoroplethMap)
            race = raceBarChartClick['points'][0]['x']
            filter_by_race = intermediateChoroplethMap[intermediateChoroplethMap['race']==race]
            sankey_diagram = create_sankey_diagram(filter_by_race)
            viz_states['bar_chart_race'] = 1
            return sankey_diagram
        elif viz_states['line_chart']==1:
            intermediateLineYearData = pd.read_json(intermediateLineYearData)
            race = raceBarChartClick['points'][0]['x']
            filter_by_race = intermediateLineYearData[intermediateLineYearData['race']==race]
            sankey_diagram = create_sankey_diagram(filter_by_race)
            viz_states['bar_chart_race'] = 1
            return sankey_diagram
        elif viz_states['bar_chart_mental']==1:
            intermediateBarChartMental = pd.read_json(intermediateBarChartMental)
            race = raceBarChartClick['points'][0]['x']
            filter_by_race = intermediateBarChartMental[intermediateBarChartMental['race']==race]
            sankey_diagram = create_sankey_diagram(filter_by_race)
            viz_states['bar_chart_race'] = 1
            return sankey_diagram
        elif viz_states['bar_chart_age']==1:
            intermediateBarChartAge = pd.read_json(intermediateBarChartAge)
            race = raceBarChartClick['points'][0]['x']
            filter_by_race = intermediateBarChartAge[intermediateBarChartAge['race']==race]
            sankey_diagram = create_sankey_diagram(filter_by_race)
            viz_states['bar_chart_race'] = 1
            return sankey_diagram
        else:
            race = raceBarChartClick['points'][0]['x']
            filter_by_race = df[df['race']==race]
            sankey_diagram = create_sankey_diagram(filter_by_race)
            viz_states['bar_chart_race'] = 1
            return sankey_diagram

    elif triggered_element =='bar-chart-age':
        if viz_states['bar_chart_race']==1 and viz_states['bar_chart_mental']==1:
            intermediateBarChartRace = pd.read_json(intermediateBarChartRace)
            intermediateBarChartMental = pd.read_json(intermediateBarChartMental)
            if len(intermediateBarChartRace)>len(intermediateBarChartMental):
                race = intermediateBarChartRace['race'].unique()[0]
                intermediate_df = intermediateBarChartMental[intermediateBarChartMental['race']==race]
            else:
                mental_illness_value = mentalBarClick['points'][0]['x']
                intermediate_df = intermediateBarChartRace[intermediateBarChartRace['signs_of_mental_illness']==mental_illness_value]
            gender, age= get_age_and_gender(ageBarClick)
            filter_by_age_gender = intermediate_df[(intermediate_df['gender']==gender) & (intermediate_df['age_bins']==age)]
            sankey_diagram = create_sankey_diagram(filter_by_age_gender)
            viz_states['bar_chart_age'] = 1
            return sankey_diagram
        if viz_states['bar_chart_race']==1 and viz_states['choropleth-map']==1:
            intermediateBarChartRace = pd.read_json(intermediateBarChartRace)
            intermediateChoroplethMap = pd.read_json(intermediateChoroplethMap)
            if len(intermediateBarChartRace)>len(intermediateChoroplethMap):
                race = intermediateBarChartRace['race'].unique()[0]
                intermediate_df = intermediateChoroplethMap[intermediateChoroplethMap['race']==race]
            else:
                state = mapClick['points'][0]['location']]
                intermediate_df = intermediateBarChartRace[intermediateBarChartRace['state']==state]
            gender, age= get_age_and_gender(ageBarClick)
            filter_by_age_gender = intermediate_df[(intermediate_df['gender']==gender) & (intermediate_df['age_bins']==age)]
            sankey_diagram = create_sankey_diagram(filter_by_age_gender)
            viz_states['bar_chart_age'] = 1
            return sankey_diagram
        elif viz_states['bar_chart_race']==1:
            intermediateBarChartRace = pd.read_json(intermediateBarChartRace)
            gender, age= get_age_and_gender(ageBarClick)
            filter_by_age_gender = intermediateBarChartRace[(intermediateBarChartRace['gender']==gender) & (intermediateBarChartRace['age_bins']==age)]
            sankey_diagram = create_sankey_diagram(filter_by_age_gender)
            viz_states['bar_chart_age'] = 1
            return sankey_diagram
        elif viz_states['choropleth_map']==1:
            intermediateChoroplethMap = pd.read_json(intermediateChoroplethMap)
            gender, age= get_age_and_gender(ageBarClick)
            filter_by_age_gender = intermediateChoroplethMap[(intermediateChoroplethMap['gender']==gender) & (intermediateChoroplethMap['age_bins']==age)]
            sankey_diagram = create_sankey_diagram(filter_by_age_gender)
            viz_states['bar_chart_age'] = 1
            return sankey_diagram
        elif viz_states['line_chart']==1:
            intermediateLineYearData = pd.read_json(intermediateLineYearData)
            gender, age= get_age_and_gender(ageBarClick)
            filter_by_age_gender = intermediateLineYearData[(intermediateLineYearData['gender']==gender) & (intermediateLineYearData['age_bins']==age)]
            sankey_diagram = create_sankey_diagram(filter_by_age_gender)
            viz_states['bar_chart_age'] = 1
            return sankey_diagram
        elif viz_states['bar_chart_mental']==1:
            intermediateBarChartMental = pd.read_json(intermediateBarChartMental)
            gender, age= get_age_and_gender(ageBarClick)
            filter_by_age_gender = intermediateBarChartMental[(intermediateBarChartMental['gender']==gender) & (intermediateBarChartMental['age_bins']==age)]
            sankey_diagram = create_sankey_diagram(filter_by_age_gender)
            viz_states['bar_chart_age'] = 1
            return sankey_diagram
        else:
            gender, age= get_age_and_gender(ageBarClick)
            filter_by_age_gender = df[(df['gender']==gender) & (df['age_bins']==age)]
            sankey_diagram = create_sankey_diagram(filter_by_age_gender)
            viz_states['bar_chart_age'] = 1
            return sankey_diagram

    elif triggered_element =='line-chart':
        if viz_states['bar_chart_race']==1 and viz_states['bar_chart_age']==1:
            intermediateBarChartRace = pd.read_json(intermediateBarChartRace)
            intermediateBarChartAge = pd.read_json(intermediateBarChartAge)
            if len(intermediateBarChartRace)>len(intermediateBarChartAge):
                race = intermediateBarChartRace['race'].unique()[0]
                intermediate_df = intermediateBarChartAge[intermediateBarChartAge['race']==race]
            else:
                age = intermediateBarChartAge['age_bins'].unique()[0]
                gender = intermediateBarChartAge['gender'].unique()[0]
                intermediate_df = intermediateBarChartRace[(intermediateBarChartRace['age_bins']==age) & (intermediateBarChartRace['gender']==gender)]
            startDate = lineChartClick['xaxis.range[0]']
            endDate = lineChartClick['xaxis.range[1]']
            filter_by_date = intermediate_df[(intermediate_df['date']>=startDate) & (intermediate_df['date']<=endDate)]
            sankey_diagram = create_sankey_diagram(filter_by_date)
            viz_states['line_chart'] = 1
            viz_states['gun_chart'] = 1
            return sankey_diagram
        if viz_states['bar_chart_race']==1:
            intermediateBarChartRace = pd.read_json(intermediateBarChartRace)
            startDate = lineChartClick['xaxis.range[0]']
            endDate = lineChartClick['xaxis.range[1]']
            filter_by_date = intermediateBarChartRace[(intermediateBarChartRace['date']>=startDate) & (intermediateBarChartRace['date']<=endDate)]
            sankey_diagram = create_sankey_diagram(filter_by_date)
            viz_states['line_chart'] = 1
            viz_states['gun_chart'] = 1
            return sankey_diagram
        if viz_states['bar_chart_age']==1:
            intermediateBarChartAge = pd.read_json(intermediateBarChartAge)
            startDate = lineChartClick['xaxis.range[0]']
            endDate = lineChartClick['xaxis.range[1]']
            filter_by_date = intermediateBarChartAge[(intermediateBarChartAge['date']>=startDate) & (intermediateBarChartAge['date']<=endDate)]
            sankey_diagram = create_sankey_diagram(filter_by_date)
            viz_states['line_chart'] = 1
            viz_states['gun_chart'] = 1
            return sankey_diagram
        if viz_states['bar_chart_mental']==1:
            intermediateBarChartMental = pd.read_json(intermediateBarChartMental)
            startDate = lineChartClick['xaxis.range[0]']
            endDate = lineChartClick['xaxis.range[1]']
            filter_by_date = intermediateBarChartMental[(intermediateBarChartMental['date']>=startDate) & (intermediateBarChartMental['date']<=endDate)]
            sankey_diagram = create_sankey_diagram(filter_by_date)
            viz_states['line_chart'] = 1
            viz_states['gun_chart'] = 1
            return sankey_diagram
        else:
            startDate = lineChartClick['xaxis.range[0]']
            endDate = lineChartClick['xaxis.range[1]']
            filter_by_date = df[(df['date']>=startDate) & (df['date']<=endDate)]
            sankey_diagram = create_sankey_diagram(filter_by_date)
            viz_states['line_chart'] = 1
            viz_states['gun_chart'] = 1
            return sankey_diagram

    elif triggered_element == 'choropleth-map':
        if viz_states['bar_chart_race']==1 and viz_states['bar_chart_age']==1:
            intermediateBarChartRace = pd.read_json(intermediateBarChartRace)
            intermediateBarChartAge = pd.read_json(intermediateBarChartAge)
            if len(intermediateBarChartRace)>len(intermediateBarChartAge):
                race = intermediateBarChartRace['race'].unique()[0]
                intermediate_df = intermediateBarChartAge[intermediateBarChartAge['race']==race]
            else:
                age = intermediateBarChartAge['age_bins'].unique()[0]
                gender = intermediateBarChartAge['gender'].unique()[0]
                intermediate_df = intermediateBarChartRace[(intermediateBarChartRace['age_bins']==age) & (intermediateBarChartRace['gender']==gender)]
            filter_by_location = intermediate_df[intermediate_df['state']==mapClick['points'][0]['location']]
            sankey_diagram = create_sankey_diagram(filter_by_location)
            viz_states['choropleth_map'] = 1
            return sankey_diagram
        if viz_states['bar_chart_race']==1:
            intermediateBarChartRace = pd.read_json(intermediateBarChartRace)
            filter_by_location = intermediateBarChartRace[intermediateBarChartRace['state']==mapClick['points'][0]['location']]
            sankey_diagram = create_sankey_diagram(filter_by_location)
            viz_states['choropleth_map'] = 1
            return sankey_diagram
        if viz_states['bar_chart_age']==1:
            intermediateBarChartAge = pd.read_json(intermediateBarChartAge)
            filter_by_location = intermediateBarChartAge[intermediateBarChartAge['state']==mapClick['points'][0]['location']]
            sankey_diagram = create_sankey_diagram(filter_by_location)
            viz_states['choropleth_map'] = 1
            return sankey_diagram
        if viz_states['bar_chart_mental']==1:
            intermediateBarChartMental = pd.read_json(intermediateBarChartMental)
            filter_by_location = intermediateBarChartMental[intermediateBarChartMental['state']==mapClick['points'][0]['location']]
            sankey_diagram = create_sankey_diagram(filter_by_location)
            viz_states['choropleth_map'] = 1
            return sankey_diagram
        else:
            filter_by_location = df[df['state']==mapClick['points'][0]['location']]
            sankey_diagram = create_sankey_diagram(filter_by_location)
            viz_states['choropleth_map'] = 1
            return sankey_diagram

    elif triggered_element =='mental-illness-bar':
        if viz_states['bar_chart_race']==1 and viz_states['bar_chart_age']==1:
            intermediateBarChartRace = pd.read_json(intermediateBarChartRace)
            intermediateBarChartAge = pd.read_json(intermediateBarChartAge)
            if len(intermediateBarChartRace)>len(intermediateBarChartAge):
                race = intermediateBarChartRace['race'].unique()[0]
                intermediate_df = intermediateBarChartAge[intermediateBarChartAge['race']==race]
            else:
                age = intermediateBarChartAge['age_bins'].unique()[0]
                gender = intermediateBarChartAge['gender'].unique()[0]
                intermediate_df = intermediateBarChartRace[(intermediateBarChartRace['age_bins']==age) & (intermediateBarChartRace['gender']==gender)]
            mental_illness_value = mentalBarClick['points'][0]['x']
            filter_by_mental_illness = intermediate_df[intermediate_df['signs_of_mental_illness']==mental_illness_value]
            sankey_diagram = create_sankey_diagram(filter_by_mental_illness)
            viz_states['bar_chart_mental'] = 1
            return sankey_diagram
        if viz_states['bar_chart_race']==1:
            intermediateBarChartRace = pd.read_json(intermediateBarChartRace)
            mental_illness_value = mentalBarClick['points'][0]['x']
            filter_by_mental_illness = intermediateBarChartRace[intermediateBarChartRace['signs_of_mental_illness']==mental_illness_value]
            sankey_diagram = create_sankey_diagram(filter_by_mental_illness)
            viz_states['bar_chart_mental'] = 1
            return sankey_diagram
        if viz_states['bar_chart_age']==1:
            intermediateBarChartAge = pd.read_json(intermediateBarChartAge)
            mental_illness_value = mentalBarClick['points'][0]['x']
            filter_by_mental_illness = intermediateBarChartAge[intermediateBarChartAge['signs_of_mental_illness']==mental_illness_value]
            sankey_diagram = create_sankey_diagram(filter_by_mental_illness)
            viz_states['bar_chart_mental'] = 1
            return sankey_diagram
        if viz_states['choropleth_map']==1:
            intermediateChoroplethMap = pd.read_json(intermediateChoroplethMap)
            mental_illness_value = mentalBarClick['points'][0]['x']
            filter_by_mental_illness = intermediateChoroplethMap[intermediateChoroplethMap['signs_of_mental_illness']==mental_illness_value]
            sankey_diagram = create_sankey_diagram(filter_by_mental_illness)
            viz_states['bar_chart_mental'] = 1
            return sankey_diagram
        else:
            mental_illness_value = mentalBarClick['points'][0]['x']
            filter_by_mental_illness = df[df['signs_of_mental_illness']==mental_illness_value]
            sankey_diagram = create_sankey_diagram(filter_by_mental_illness)
            viz_states['bar_chart_mental'] = 1
            return sankey_diagram

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

#update indicator graph
@app.callback(
    Output('indicator-graph','figure'),
    [Input('line-chart','relayoutData'),
     Input('bar-chart-race', 'clickData'),
     Input('bar-chart-age', 'clickData'),
     Input('choropleth-map','clickData'),
     Input('mental-illness-bar', 'clickData'),
     Input('reset_button','n_clicks')], prevent_initial_call=True)
def update_indicator_graph(lineChartClick, raceBarChartClick, ageBarClick, mapClick, mentalBarClick, n_clicks):

    changed_id = [p['prop_id'] for p in dash.callback_context.triggered][0].split('.')[0]
    if changed_id=='reset_button':
        return indicator_graph(len(df))
    triggered_element = dash.callback_context.triggered[0]['prop_id'].split('.')[0]
    if triggered_element=='line-chart':
        startDate = lineChartClick['xaxis.range[0]']
        endDate = lineChartClick['xaxis.range[1]']
        filter_by_date = df[(df['date']>=startDate) & (df['date']<=endDate)]
        updated_indicator_graph = indicator_graph(len(filter_by_date))
        return updated_indicator_graph
    elif triggered_element =='bar-chart-race':
        race = raceBarChartClick['points'][0]['x']
        filter_by_race = df[df['race']==race]
        updated_indicator_graph = indicator_graph(len(filter_by_race))
        return updated_indicator_graph
    elif triggered_element =='bar-chart-age':
        gender, age = get_age_and_gender(ageBarClick)
        filter_by_age_gender = df[(df['gender']==gender) & (df['age_bins']==age)]
        updated_indicator_graph = indicator_graph(len(filter_by_age_gender))
        return updated_indicator_graph
    elif triggered_element == 'choropleth-map':
        filter_by_location = df[df['state']==mapClick['points'][0]['location']]
        updated_indicator_graph = indicator_graph(len(filter_by_location))
        return updated_indicator_graph
    elif triggered_element == 'mental-illness-bar':
        mental_illness_value = mentalBarClick['points'][0]['x']
        filter_by_mental_illness = df[df['signs_of_mental_illness']==mental_illness_value]
        updated_indicator_graph = indicator_graph(len(filter_by_mental_illness))
        return updated_indicator_graph



#-----------------------------------------------------------------------------------------------------------------------------------
#intermediate data update callbacks
@app.callback(
    Output('intermediate-value-bar-chart-race','children'),
    [Input('bar-chart-race','clickData'),
     Input('reset_button','n_clicks')],prevent_initial_call=True)
def update_df_line_bar_chart_race(raceBarChartClick, n_clicks):
    changed_id = [p['prop_id'] for p in dash.callback_context.triggered][0].split('.')[0]
    if changed_id=='reset_button':
        return None
    race = raceBarChartClick['points'][0]['x']
    filter_by_race = df[df['race']==race]
    return filter_by_race.to_json()

@app.callback(
    Output('intermediate-value-line-chart-year','children'),
    [Input('line-chart','relayoutData'),
     Input('reset_button','n_clicks')], prevent_initial_call=True)
def update_df_line_bar_chart_race(lineChartClick, n_clicks):
    changed_id = [p['prop_id'] for p in dash.callback_context.triggered][0].split('.')[0]
    if changed_id=='reset_button':
        return None
    startDate = lineChartClick['xaxis.range[0]']
    endDate = lineChartClick['xaxis.range[1]']
    filter_by_date = df[(df['date']>=startDate) & (df['date']<=endDate)]
    return filter_by_date.to_json()

@app.callback(
    Output('intermediate-value-choropleth-map','children'),
    [Input('choropleth-map','clickData'),
    Input('reset_button','n_clicks')], prevent_initial_call=True)
def update_df_choropleth_map(mapClick, n_clicks):
    changed_id = [p['prop_id'] for p in dash.callback_context.triggered][0].split('.')[0]
    if changed_id=='reset_button':
        return None
    filter_by_location = df[df['state']==mapClick['points'][0]['location']]
    return filter_by_location.to_json()

@app.callback(
    Output('intermediate-value-bar-chart-age','children'),
    [Input('bar-chart-age','clickData'),
     Input('reset_button','n_clicks')], prevent_initial_call=True)
def update_df_bar_chart_age(ageBarClick, n_clicks):
    changed_id = [p['prop_id'] for p in dash.callback_context.triggered][0].split('.')[0]
    if changed_id=='reset_button':
        return None
    gender, age = get_age_and_gender(ageBarClick)
    filter_by_age_gender = df[(df['gender']==gender) & (df['age_bins']==age)]
    return filter_by_age_gender.to_json()

@app.callback(
    Output('intermediate-value-bar-chart-mental','children'),
    [Input('mental-illness-bar','clickData'),
     Input('reset_button','n_clicks')], prevent_initial_call=True)
def update_df_bar_chart_mental_illness(mentalBarClick, n_clicks):
    changed_id = [p['prop_id'] for p in dash.callback_context.triggered][0].split('.')[0]
    if changed_id=='reset_button':
        return None
    mental_illness_value = mentalBarClick['points'][0]['x']
    filter_by_mental_illness = df[df['signs_of_mental_illness']==mental_illness_value]
    return filter_by_mental_illness.to_json()

@app.callback(
    Output('reset-viz-states','children'),
    Input('reset_button','n_clicks'), prevent_initial_call=True)
def update_df_radar_chart_weapons(n_clicks):
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



#-----------------------------------------------------------------------------------------------------------------------------------


if __name__ == '__main__':
    app.run_server(debug=True)
    #app.run_server(debug=False)
