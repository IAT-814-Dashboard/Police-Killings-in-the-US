import pandas as pd
import plotly.express as px
import plotly.graph_objects as go

import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output
from visualization_helper_functions import *
import dash_bootstrap_components as dbc

app = dash.Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP])

df = pd.read_json('data/police-killings-integrated-dataset-2021-03-20.json.gz')
gun_data = pd.read_csv('data/gun-data-by-year.csv')

viz_states = {'bar_chart_race':0, 'choropleth_map':0, 'line_chart':0, 'bar_chart_age':0, 'bar_chart_mental':0}

#-----------------------------------------------------------------------------------------------------------------------------------

app.layout = html.Div([

#title
    html.Div([
        html.Div([
            html.H1(children='IAT 814: Police Killings in the United States',
                    style = {'textAlign' : 'center',
                             'color': 'white',
                             'font-family': 'Helvetica Neue',
                             'font-size': '40px','font-weight': 'bold', 'letter-spacing': '-1px',
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
                'margin-top': '75px',
                'margin-left': '35px',
                'margin-right': '35px',}
    ),

#information bar+indicator graph
    html.Div([
        html.Div([
            html.P('Police violence is a leading cause of death for young men in the United States. Over the life course, about 1 in every 1,000 black men can expect to be killed by police. Risk of being killed by police peaks between the ages of 20 y and 35 y for men and women and for all racial and ethnic groups. Black women and men and American Indian and Alaska Native women and men are significantly more likely than white women and men to be killed by police. Latino men are also more likely to be killed by police than are white men..')
        ], style={'float':'left','flex':'60%',
                 'text-align':'justify',
                 'background-color':'#c8d7e3',
                 'box-shadow': 'rgb(38, 57, 77) 0px 20px 30px -10px',
                  'font-family': 'Helvetica Neue',
                  'font-size': '40px',
                  'padding':'20px',
                  'border': 'solid white',
                  'border-color': 'white',
                  'border-width': '5px 5px 5px 5px',
                  }),
        html.Div([
            html.H3('Top 5 By Race',
                    style={
                            'textAlign':'center',
                            'color': 'black',
                            'font-family': 'Helvetica Neue',
                            'font-size': '32px','font-weight': 'bold',
                            'line-height': '1',
                            }),
            dcc.Loading(dcc.Graph(
                                id='top-5-race',
                                figure=top_5_by_race(df)
            ))
        ], style={'flex':'40%',
                    'background-color':'#c8d7e3',
                    'box-shadow': 'rgb(38, 57, 77) 0px 20px 30px -10px',
                    'border': 'solid white',
                    'border-color': 'white',
                    'border-width': ' 5px 5px 5px 5px',
                    'padding':'20px',
                    'margin-left': '20px',
                    'margin-right': '20px',}),
        html.Div([
            html.H1(children='Total Number of Police Killings'),
            html.Div(dcc.Loading(
                        dcc.Graph(
                                id="indicator-graph",
                                figure=indicator_graph(len(df)),
                                )),
                    style={'border': 'solid white',
                    'border-color': 'white',
                    'border_radius':'50%'}),
            html.Button('Reset All',id='reset_button',n_clicks=0,
                        style={'background-color': '#DADADA',
                                'border':'none',
                                'padding': '15px 32px',
                                'box-shadow': 'rgb(38, 57, 77) 0px 20px 30px -10px',
                                'margin-top':'10px',
                                'text-align': 'center',
                                'text-decoration': 'none',
                                'display': 'inline-block',
                                'font-size': '30px'}),
            ],
            style={'flex':'40%',
                    'background-color': '#c8d7e3',
                    'text-align':'center',
                    'border': 'solid white',
                    'box-shadow': 'rgb(38, 57, 77) 0px 20px 30px -10px',
                    'border-color': 'white',
                    'border-width': ' 5px 5px 5px 5px',
                    'padding':'20px'})
    ],
    className='information-bar',
    style={'display':'flex',
           'height':'50%',
           'margin-top':'30px',
           'margin-left': '35px',
           'margin-right': '35px',
           }
    ),


#bar chart per year+ choropleth map
    html.Div([
        html.Div([
                html.H3('Police Killings by Year',
                        style={
                                'textAlign':'center',
                                'color': 'black',
                                'font-family': 'Helvetica Neue',
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
                html.H3('Police Killings by State',
                        style={
                                'textAlign' : 'center',
                                'color': 'black',
                                'font-family': 'Helvetica Neue',
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
                            'font-family': 'Helvetica Neue',
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
                            'font-family': 'Helvetica Neue',
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
                            'font-family': 'Helvetica Neue',
                            'font-weight': 'bold',
                            'line-height': '1'}),
            dcc.Graph(
                    id='mental-illness-bar',
                    figure=create_bar_char_for_mental_illness(df),
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
className='bar-pie',
style={'display':'flex',
       'height':'100%',
       'margin-top':'30px',
       'margin-left': '35px',
       'margin-right': '35px',
       'margin-bottom':'70px'}
),


#radar chart
    html.Div([
        html.Div([
                html.H3('Police Killings by Weapons',
                        style={
                                'textAlign' : 'center',
                                'color': 'black',
                                'font-family': 'Helvetica Neue',
                                'font-size': '30px','font-weight': 'bold',
                                'line-height': '1'}),
                dcc.Graph(
                id='radar-chart-weapons',
                figure=create_radar_chart_for_weapons(df),
                )], style={'flex':'50%',
                            'margin-right':'20px',
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
                                'font-family': 'Helvetica Neue',
                                'font-size': '30px','font-weight': 'bold',
                                'line-height': '1'}),
                dcc.Graph(
                        id='sankey-diagram',
                        figure=create_sankey_diagram(df),
                        config={'editable':True},

                )], style={'flex':'50%',
                            'border': 'solid white',
                            'border-color': 'white',
                            'border-width': '5px 5px 5px 0px',
                            'box-shadow': 'rgb(38, 57, 77) 0px 20px 30px -10px',
                            'padding':'20px', 'background-color':'#c8d7e3'
                            }
                , className='sankey-block'),

    ],
    className='sankey-map',
    style={'display':'flex',
           'height':'100%',
           'margin-top':'30px',
           'margin-left': '35px',
           'margin-right': '35px',}
    ),


#purchase of gun by year
    html.Div([
            html.H3('Purchase of Gun By Year',
                    style={
                            'textAlign' : 'center',
                            'color': 'black',
                            'font-family': 'Helvetica Neue',
                            'font-size': '30px','font-weight': 'bold',
                            'line-height': '1'}),
            dcc.Loading(dcc.Graph(
                    id='gun-line-chart',
                    figure=create_line_chart_gun_data(gun_data)
            )),
    ], className='gun-data-line-chart-block',style={'background-color':'#c8d7e3',
                                                    'margin-top':'30px',
                                                    'margin-left': '35px',
                                                    'margin-right': '35px',
                                                    'border': 'solid white',
                                                    'border-color': 'white',
                                                    'border-width': ' 5px 5px 5px 5px',
                                                    'box-shadow': 'rgb(38, 57, 77) 0px 20px 30px -10px',
                                                    'padding':'20px'}),

    html.Div(id='intermediate-value-line-chart-year', style={'display': 'none'}),
    html.Div(id='intermediate-value-bar-chart-race', style={'display': 'none'}),
    html.Div(id='intermediate-value-choropleth-map', style={'display': 'none'}),
    html.Div(id='intermediate-value-bar-chart-age', style={'display': 'none'}),
    html.Div(id='intermediate-value-bar-chart-mental', style={'display': 'none'}),
    html.Div(id='intermediate-value-radar-chart-weapons', style={'display': 'none'})



], style={})

#-----------------------------------------------------------------------------------------------------------------------------------


#update choropleth map
@app.callback(
    Output('choropleth-map', 'figure'),
    [Input('bar-chart-race', 'clickData'),
    Input('bar-chart-age', 'clickData'),
    Input('line-chart','relayoutData'),
    Input('mental-illness-bar', 'clickData'),
    Input('intermediate-value-bar-chart-mental','children'),
    Input('intermediate-value-line-chart-year','children'),
    Input('intermediate-value-bar-chart-race','children'),
    Input('intermediate-value-bar-chart-age','children'),
    Input('reset_button','n_clicks')], prevent_initial_call=True)
def update_choropleth_map(raceBarChartClick, ageBarClick, lineChartClick, mentalBarClick, intermediateBarChartMental, intermediateLineYearData, intermediateBarChartRace, intermediateBarChartAge, n_clicks):
    if viz_states['choropleth_map']==1:
        return dash.no_update
    triggered_element = dash.callback_context.triggered[0]['prop_id'].split('.')[0]
    if triggered_element =='line-chart':
        if viz_states['bar_chart_race']==1:
            intermediateBarChartRace = pd.read_json(intermediateBarChartRace)
            startDate = lineChartClick['xaxis.range[0]']
            endDate = lineChartClick['xaxis.range[1]']
            filter_by_date = intermediateBarChartRace[(intermediateBarChartRace['date']>=startDate) & (intermediateBarChartRace['date']<=endDate)]
            choropleth_map = create_choropleth_map(filter_by_date)
            viz_states['line_chart'] = 1
            return choropleth_map
        elif viz_states['bar_chart_age']==1:
            intermediateBarChartAge = pd.read_json(intermediateBarChartAge)
            startDate = lineChartClick['xaxis.range[0]']
            endDate = lineChartClick['xaxis.range[1]']
            filter_by_date = intermediateBarChartAge[(intermediateBarChartAge['date']>=startDate) & (intermediateBarChartAge['date']<=endDate)]
            choropleth_map = create_choropleth_map(filter_by_date)
            viz_states['line_chart'] = 1
            return choropleth_map
        elif viz_states['bar_chart_mental']==1:
            intermediateBarChartMental = pd.read_json(intermediateBarChartMental)
            startDate = lineChartClick['xaxis.range[0]']
            endDate = lineChartClick['xaxis.range[1]']
            filter_by_date = intermediateBarChartMental[(intermediateBarChartMental['date']>=startDate) & (intermediateBarChartMental['date']<=endDate)]
            choropleth_map = create_choropleth_map(filter_by_date)
            viz_states['line_chart'] = 1
            return choropleth_map
        else:
            startDate = lineChartClick['xaxis.range[0]']
            endDate = lineChartClick['xaxis.range[1]']
            filter_by_date = df[(df['date']>=startDate) & (df['date']<=endDate)]
            choropleth_map = create_choropleth_map(filter_by_date)
            viz_states['line_chart'] = 1
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
     Input('intermediate-value-bar-chart-mental','children'),
     Input('intermediate-value-bar-chart-age','children'),
     Input('intermediate-value-choropleth-map','children'),
     Input('intermediate-value-line-chart-year','children'),
     Input('reset_button','n_clicks')], prevent_initial_call=True)
def update_bar_chart_race(mapClick, ageBarClick, lineChartClick, mentalBarClick, intermediateBarChartMental, intermediateBarChartAge, intermediateChoroplethMap, intermediateLineYearData, n_clicks):
    if viz_states['bar_chart_race']==1:
        return dash.no_update
    triggered_element = dash.callback_context.triggered[0]['prop_id'].split('.')[0]
    if triggered_element =='line-chart':
        if viz_states['choropleth_map']==1:
            intermediateChoroplethData = pd.read_json(intermediateChoroplethMap)
            startDate = lineChartClick['xaxis.range[0]']
            endDate = lineChartClick['xaxis.range[1]']
            filter_by_date = intermediateChoroplethData[(intermediateChoroplethData['date']>=startDate) & (intermediateChoroplethData['date']<=endDate)]
            bar_chart_race = create_bar_char_for_race(filter_by_date)
            viz_states['line_chart'] = 1
            return bar_chart_race
        elif viz_states['bar_chart_age']==1:
            intermediateBarChartAge = pd.read_json(intermediateBarChartAge)
            startDate = lineChartClick['xaxis.range[0]']
            endDate = lineChartClick['xaxis.range[1]']
            filter_by_date = intermediateBarChartAge[(intermediateBarChartAge['date']>=startDate) & (intermediateBarChartAge['date']<=endDate)]
            bar_chart_race = create_bar_char_for_race(filter_by_date)
            viz_states['line_chart'] = 1
            return bar_chart_race
        elif viz_states['bar_chart_mental']==1:
            intermediateBarChartMental = pd.read_json(intermediateBarChartMental)
            startDate = lineChartClick['xaxis.range[0]']
            endDate = lineChartClick['xaxis.range[1]']
            filter_by_date = intermediateBarChartMental[(intermediateBarChartMental['date']>=startDate) & (intermediateBarChartMental['date']<=endDate)]
            bar_chart_race = create_bar_char_for_race(filter_by_date)
            viz_states['line_chart'] = 1
            return bar_chart_race
        else:
            startDate = lineChartClick['xaxis.range[0]']
            endDate = lineChartClick['xaxis.range[1]']
            filter_by_date = df[(df['date']>=startDate) & (df['date']<=endDate)]
            bar_chart_race = create_bar_char_for_race(filter_by_date)
            viz_states['line_chart'] = 1
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
     Input('intermediate-value-bar-chart-mental','children'),
     Input('intermediate-value-bar-chart-age','children'),
     Input('intermediate-value-bar-chart-race','children'),
     Input('intermediate-value-choropleth-map','children'),
     Input('reset_button','n_clicks')], prevent_initial_call=True)
def update_line_chart(mapClick, raceBarChartClick, ageBarClick, mentalBarClick, intermediateBarChartMental, intermediateBarChartAge, intermediateBarChartRace, intermediateChoroplethMap, n_clicks):
    triggered_element = dash.callback_context.triggered[0]['prop_id'].split('.')[0]
    if viz_states['line_chart']==1:
        return dash.no_update
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
            filter_by_location = intermediateBarRace[intermediateBarRace['state']==mapClick['points'][0]['location']]
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
     Input('intermediate-value-bar-chart-mental','children'),
     Input('intermediate-value-line-chart-year','children'),
     Input('intermediate-value-bar-chart-race','children'),
     Input('intermediate-value-choropleth-map','children'),
     Input('reset_button','n_clicks')], prevent_initial_call=True)
def update_bar_chart_age_and_gender(mapClick, raceBarChartClick, lineChartClick, mentalBarClick, intermediateBarChartMental, intermediateLineYearData, intermediateBarChartRace, intermediateChoroplethMap, n_clicks):
    if viz_states['bar_chart_age']==1:
        return dash.no_update
    triggered_element = dash.callback_context.triggered[0]['prop_id'].split('.')[0]
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
            return bar_chart_by_age
        elif viz_states['bar_chart_race']==1:
            intermediateBarChartRace = pd.read_json(intermediateBarChartRace)
            startDate = lineChartClick['xaxis.range[0]']
            endDate = lineChartClick['xaxis.range[1]']
            filter_by_date = intermediateBarChartRace[(intermediateBarChartRace['date']>=startDate) & (intermediateBarChartRace['date']<=endDate)]
            bar_chart_by_age = create_bar_chart_for_age_and_gender(filter_by_date)
            viz_states['line_chart'] = 1
            return bar_chart_by_age
        elif viz_states['bar_chart_mental']==1:
            intermediateBarChartMental = pd.read_json(intermediateBarChartMental)
            startDate = lineChartClick['xaxis.range[0]']
            endDate = lineChartClick['xaxis.range[1]']
            filter_by_date = intermediateBarChartMental[(intermediateBarChartMental['date']>=startDate) & (intermediateBarChartMental['date']<=endDate)]
            bar_chart_by_age = create_bar_chart_for_age_and_gender(filter_by_date)
            viz_states['line_chart'] = 1
            return bar_chart_by_age
        else:
            startDate = lineChartClick['xaxis.range[0]']
            endDate = lineChartClick['xaxis.range[1]']
            filter_by_date = df[(df['date']>=startDate) & (df['date']<=endDate)]
            bar_chart_by_age = create_bar_chart_for_age_and_gender(filter_by_date)
            viz_states['line_chart'] = 1
            return bar_chart_by_age

    if triggered_element == 'mental-illness-bar':
        if viz_states['bar_chart_race']==1:
            intermediateBarChartRace = pd.read_json(intermediateBarChartRace)
            mental_illness_value = mentalBarClick['points'][0]['x']
            filter_by_mental_illness = intermediateBarChartRace[intermediateBarChartRace['signs_of_mental_illness']==mental_illness_value]
            bar_chart_by_age = create_bar_chart_for_age_and_gender(filter_by_mental_illness)
            viz_states['bar_chart_mental'] = 1
            return bar_chart_by_age
        elif viz_states['choropleth_map']==1:
            intermediateChoroplethMap = pd.read_json(intermediateChoroplethMap)
            mental_illness_value = mentalBarClick['points'][0]['x']
            filter_by_mental_illness = intermediateChoroplethMap[intermediateChoroplethMap['signs_of_mental_illness']==mental_illness_value]
            bar_chart_by_age = create_bar_chart_for_age_and_gender(filter_by_mental_illness)
            viz_states['bar_chart_mental'] = 1
            return bar_chart_by_age
        elif viz_states['line_chart']==1:
            intermediateLineYearData = pd.read_json(intermediateLineYearData)
            mental_illness_value = mentalBarClick['points'][0]['x']
            filter_by_mental_illness = intermediateLineYearData[intermediateLineYearData['signs_of_mental_illness']==mental_illness_value]
            bar_chart_by_age = create_bar_chart_for_age_and_gender(filter_by_mental_illness)
            viz_states['bar_chart_mental'] = 1
            return bar_chart_by_age
        else:
            mental_illness_value = mentalBarClick['points'][0]['x']
            filter_by_mental_illness = df[df['signs_of_mental_illness']==mental_illness_value]
            bar_chart_by_age = create_bar_chart_for_age_and_gender(filter_by_mental_illness)
            viz_states['bar_chart_mental'] = 1
            return bar_chart_by_age

#update mental illness bar chart
@app.callback(
    Output('mental-illness-bar', 'figure'),
    [Input('choropleth-map', 'clickData'),
     Input('bar-chart-race', 'clickData'),
     Input('line-chart','relayoutData'),
     Input('bar-chart-age', 'clickData'),
     Input('intermediate-value-bar-chart-age','children'),
     Input('intermediate-value-line-chart-year','children'),
     Input('intermediate-value-bar-chart-race','children'),
     Input('intermediate-value-choropleth-map','children'),
     Input('reset_button','n_clicks')], prevent_initial_call=True)
def update_bar_chart_mental_illness(mapClick, raceBarChartClick, lineChartClick, ageBarClick, intermediateBarChartAge, intermediateLineYearData, intermediateBarChartRace, intermediateChoroplethMap, n_clicks):
    if viz_states['bar_chart_mental']==1:
        return dash.no_update
    triggered_element = dash.callback_context.triggered[0]['prop_id'].split('.')[0]
    if triggered_element == 'choropleth-map':
        if viz_states['bar_chart_race']==1:
            intermediateBarRace = pd.read_json(intermediateBarChartRace)
            filter_by_location = intermediateBarRace[intermediateBarRace['state']==mapClick['points'][0]['location']]
            bar_chart_by_mental_illness = create_bar_char_for_mental_illness(filter_by_location)
            viz_states['choropleth_map'] = 1
            return bar_chart_by_mental_illness
        elif viz_states['line_chart']==1:
            intermediateLineYearData = pd.read_json(intermediateLineYearData)
            filter_by_location = intermediateLineYearData[intermediateLineYearData['state']==mapClick['points'][0]['location']]
            bar_chart_by_mental_illness = create_bar_char_for_mental_illness(filter_by_location)
            viz_states['choropleth_map'] = 1
            return bar_chart_by_mental_illness
        elif viz_states['bar_chart_age']==1:
            intermediateBarChartAge = pd.read_json(intermediateBarChartAge)
            filter_by_location = intermediateBarChartAge[intermediateBarChartAge['state']==mapClick['points'][0]['location']]
            bar_chart_by_mental_illness = create_bar_char_for_mental_illness(filter_by_location)
            viz_states['choropleth_map'] = 1
            return bar_chart_by_mental_illness
        else:
            filter_by_location = df[df['state']==mapClick['points'][0]['location']]
            bar_chart_by_mental_illness = create_bar_char_for_mental_illness(filter_by_location)
            viz_states['choropleth_map'] = 1
            return bar_chart_by_mental_illness

    if triggered_element =='bar-chart-race':
        if viz_states['choropleth_map']==1:
            intermediateChoroplethMap = pd.read_json(intermediateChoroplethMap)
            race = raceBarChartClick['points'][0]['x']
            filter_by_race = intermediateChoroplethMap[intermediateChoroplethMap['race']==race]
            bar_chart_by_mental_illness = create_bar_char_for_mental_illness(filter_by_race)
            viz_states['bar_chart_race'] = 1
            return bar_chart_by_mental_illness
        elif viz_states['line_chart']==1:
            intermediateLineYearData = pd.read_json(intermediateLineYearData)
            race = raceBarChartClick['points'][0]['x']
            filter_by_race = intermediateLineYearData[intermediateLineYearData['race']==race]
            bar_chart_by_mental_illness = create_bar_char_for_mental_illness(filter_by_race)
            viz_states['bar_chart_race'] = 1
            return bar_chart_by_mental_illness
        elif viz_states['bar_chart_mental']==1:
            intermediateBarChartMental = pd.read_json(intermediateBarChartMental)
            race = raceBarChartClick['points'][0]['x']
            filter_by_race = intermediateBarChartMental[intermediateBarChartMental['race']==race]
            bar_chart_by_mental_illness = create_bar_char_for_mental_illness(filter_by_race)
            viz_states['bar_chart_race'] = 1
            return bar_chart_by_mental_illness
        else:
            race = raceBarChartClick['points'][0]['x']
            filter_by_race = df[df['race']==race]
            bar_chart_by_mental_illness = create_bar_char_for_mental_illness(filter_by_race)
            viz_states['bar_chart_race'] = 1
            return bar_chart_by_mental_illness

    if triggered_element == 'line-chart':
        if viz_states['choropleth_map']==1:
            intermediateChoroplethMap = pd.read_json(intermediateChoroplethMap)
            startDate = lineChartClick['xaxis.range[0]']
            endDate = lineChartClick['xaxis.range[1]']
            filter_by_date = intermediateChoroplethMap[(intermediateChoroplethMap['date']>=startDate) & (intermediateChoroplethMap['date']<=endDate)]
            bar_chart_by_mental_illness = create_bar_char_for_mental_illness(filter_by_date)
            viz_states['line_chart'] = 1
            return bar_chart_by_mental_illness
        elif viz_states['bar_chart_race']==1:
            intermediateBarChartRace = pd.read_json(intermediateBarChartRace)
            startDate = lineChartClick['xaxis.range[0]']
            endDate = lineChartClick['xaxis.range[1]']
            filter_by_date = intermediateBarChartRace[(intermediateBarChartRace['date']>=startDate) & (intermediateBarChartRace['date']<=endDate)]
            bar_chart_by_mental_illness = create_bar_char_for_mental_illness(filter_by_date)
            viz_states['line_chart'] = 1
            return bar_chart_by_mental_illness
        elif viz_states['bar_chart_mental']==1:
            intermediateBarChartMental = pd.read_json(intermediateBarChartMental)
            startDate = lineChartClick['xaxis.range[0]']
            endDate = lineChartClick['xaxis.range[1]']
            filter_by_date = intermediateBarChartMental[(intermediateBarChartMental['date']>=startDate) & (intermediateBarChartMental['date']<=endDate)]
            bar_chart_by_mental_illness = create_bar_char_for_mental_illness(filter_by_date)
            viz_states['line_chart'] = 1
            return bar_chart_by_mental_illness
        else:
            startDate = lineChartClick['xaxis.range[0]']
            endDate = lineChartClick['xaxis.range[1]']
            filter_by_date = df[(df['date']>=startDate) & (df['date']<=endDate)]
            bar_chart_by_mental_illness = create_bar_char_for_mental_illness(filter_by_date)
            viz_states['line_chart'] = 1
            return bar_chart_by_mental_illness

    if triggered_element == 'bar-chart-age':
        if viz_states['bar_chart_race']==1:
            intermediateBarChartRace = pd.read_json(intermediateBarChartRace)
            gender, age= get_age_and_gender(ageBarClick)
            filter_by_age_gender = intermediateBarChartRace[(intermediateBarChartRace['gender']==gender) & (intermediateBarChartRace['age_bins']==age)]
            bar_chart_by_mental_illness = create_bar_char_for_mental_illness(filter_by_age_gender)
            viz_states['bar_chart_age'] = 1
            return bar_chart_by_mental_illness
        elif viz_states['choropleth_map']==1:
            intermediateChoroplethMap = pd.read_json(intermediateChoroplethMap)
            gender, age= get_age_and_gender(ageBarClick)
            filter_by_age_gender = intermediateChoroplethMap[(intermediateChoroplethMap['gender']==gender) & (intermediateChoroplethMap['age_bins']==age)]
            bar_chart_by_mental_illness = create_bar_char_for_mental_illness(filter_by_age_gender)
            viz_states['bar_chart_age'] = 1
            return bar_chart_by_mental_illness
        elif viz_states['line_chart']==1:
            intermediateLineYearData = pd.read_json(intermediateLineYearData)
            gender, age= get_age_and_gender(ageBarClick)
            filter_by_age_gender = intermediateLineYearData[(intermediateLineYearData['gender']==gender) & (intermediateLineYearData['age_bins']==age)]
            bar_chart_by_mental_illness = create_bar_char_for_mental_illness(filter_by_age_gender)
            viz_states['bar_chart_age'] = 1
            return bar_chart_by_mental_illness
        else:
            gender, age= get_age_and_gender(ageBarClick)
            filter_by_age_gender = df[(df['gender']==gender) & (df['age_bins']==age)]
            bar_chart_by_mental_illness = create_bar_char_for_mental_illness(filter_by_age_gender)
            viz_states['bar_chart_age'] = 1
            return bar_chart_by_mental_illness



#update sankey diagram
@app.callback(
    Output('sankey-diagram', 'figure'),
    [Input('pie-chart-interaction', 'clickData'),
    Input('stacked-bar-chart', 'clickData'),
    Input('line-chart','relayoutData'),
    Input('choropleth-map','clickData'),
    Input('reset_button','n_clicks')], prevent_initial_call=True)
def update_sankey_diagram(pieClick, stackBarClick, lineChartClick, mapClick, n_clicks):
    changed_id = [p['prop_id'] for p in dash.callback_context.triggered][0].split('.')[0]
    if changed_id=='reset_button':
        return create_sankey_diagram(df)
    triggered_element = dash.callback_context.triggered[0]['prop_id'].split('.')[0]
    if triggered_element =='pie-chart-interaction':
        filter_by_race = df[df['race']==str(pieClick['points'][0]['label'])]
        sankey_diagram = create_sankey_diagram(filter_by_race)
        viz_states['pie_chart'] = 1
        return sankey_diagram
    elif triggered_element =='stacked-bar-chart':
        gender, age= get_age_and_gender(stackBarClick)
        filter_by_age_gender = df[(df['gender']==gender) & (df['age_bins']==age)]
        sankey_diagram = create_sankey_diagram(filter_by_age_gender)
        viz_states['stacked_bar_chart'] = 1
        return sankey_diagram
    elif triggered_element =='line-chart':
        startDate = lineChartClick['xaxis.range[0]']
        endDate = lineChartClick['xaxis.range[1]']
        filter_by_date = df[(df['date']>=startDate) & (df['date']<=endDate)]
        sankey_diagram = create_sankey_diagram(filter_by_date)
        viz_states['line_chart'] = 1
        return sankey_diagram
    elif triggered_element == 'choropleth-map':
        filter_by_location = df[df['state']==mapClick['points'][0]['location']]
        sankey_diagram = create_sankey_diagram(filter_by_location)
        viz_states['choropleth_map'] = 1
        return sankey_diagram

#-----------------------------------------------------------------------------------------------------------------------------------
#intermediate data update callbacks

@app.callback(
    Output('intermediate-value-bar-chart-race','children'),
    Input('bar-chart-race','clickData'), prevent_initial_call=True)
def update_df_line_bar_chart_race(raceBarChartClick):
    race = raceBarChartClick['points'][0]['x']
    filter_by_race = df[df['race']==race]
    return filter_by_race.to_json()

@app.callback(
    Output('intermediate-value-line-chart-year','children'),
    Input('line-chart','relayoutData'), prevent_initial_call=True)
def update_df_line_bar_chart_race(lineChartClick):
    startDate = lineChartClick['xaxis.range[0]']
    endDate = lineChartClick['xaxis.range[1]']
    filter_by_date = df[(df['date']>=startDate) & (df['date']<=endDate)]
    return filter_by_date.to_json()

@app.callback(
    Output('intermediate-value-choropleth-map','children'),
    Input('choropleth-map','clickData'), prevent_initial_call=True)
def update_df_choropleth_map(mapClick):
    filter_by_location = df[df['state']==mapClick['points'][0]['location']]
    return filter_by_location.to_json()

@app.callback(
    Output('intermediate-value-bar-chart-age','children'),
    Input('bar-chart-age','clickData'), prevent_initial_call=True)
def update_df_bar_chart_age(ageBarClick):
    gender, age = get_age_and_gender(ageBarClick)
    filter_by_age_gender = df[(df['gender']==gender) & (df['age_bins']==age)]
    return filter_by_age_gender.to_json()


@app.callback(
    Output('intermediate-value-bar-chart-mental','children'),
    Input('mental-illness-bar','clickData'), prevent_initial_call=True)
def update_df_bar_chart_mental_illness(mentalBarClick):
    mental_illness_value = mentalBarClick['points'][0]['x']
    filter_by_mental_illness = df[df['signs_of_mental_illness']==mental_illness_value]
    return filter_by_mental_illness.to_json()

@app.callback(
    Output('intermediate-value-radar-chart-weapons','children'),
    Input('radar-chart-weapons','relayoutData'), prevent_initial_call=True)
def update_df_radar_chart_weapons(radarClick):
    print(radarClick)
    return filter_by_mental_illness.to_json()

#-----------------------------------------------------------------------------------------------------------------------------------


if __name__ == '__main__':
    app.run_server(debug=True)
    #app.run_server(debug=False)
