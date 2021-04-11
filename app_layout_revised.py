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

viz_states = {'bar_chart_race':0, 'choropleth_map':0, 'line_chart':0, 'bar_chart_age':0, 'bar_chart_mental':0, 'radar_chart_weapons':0, 'gun_chart':0}

app.layout = html.Div([

#title
    html.Div([
        html.Div([
            html.H1(children='IAT 814: Police Killings in the United States',
                    style = {'textAlign' : 'center',
                             'color': 'white',
                             'font-family': 'Georgia',
                             'font-size': '10px',
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

#line chart per year+information box+indicator graph
    html.Div([
        html.Div([
                html.H3('Police Killings by Year',
                        style={
                                'textAlign':'center',
                                'color': 'black',
                                'font-family': 'Georgia',
                                'font-size': '10px',
                                'margin-bottom':'10px',
                                'font-weight': 'bold',
                                'line-height': '1',
                                }),
                dcc.Loading(dcc.Graph(
                        id='line-chart',
                        figure=create_line_chart(df)
                ))], style={'flex':'20%',
                            'height':'60%',
                            'margin-right':'20px',
                            'border': 'solid white',
                            'border-color': 'white',
                            'border-width': ' 5px 5px 5px 5px',
                            'box-shadow': 'rgb(38, 57, 77) 0px 20px 30px -10px',
                            'padding':'20px', 'background-color':'#c8d7e3'}
                , className='line-chart-block'),

        html.Div([
            html.P('Police brutality is the use of excessive or unnecessary force by personnel affiliated with law enforcement duties when dealing with suspects and civilians.\
                   Police violence is a leading cause of death for young men in the United States.\
                   This dashboard can be used to explore the possible causes for Police Killings in the United States.',
                   style={'padding-top':'60px'}),
            html.Br(),

            html.P(html.Strong(html.Center('ALL LIVES MATTER')),style={'font-size': '20px'})
        ], style={'float':'left','flex':'10%','height':'60%',
                 'text-align':'center',
                 'background-color':'#c8d7e3',
                 'box-shadow': 'rgb(38, 57, 77) 0px 20px 30px -10px',
                  'font-family': 'Georgia',
                  'font-size': '10px',
                  'padding':'20px',
                  'border': 'solid white',
                  'border-color': 'white',
                  'border-width': '5px 5px 5px 5px',
                  }),
        html.Div([
            html.H1(children='Total Number of Police Killings',style={'font-size': '10px'}),
            html.Div(dcc.Loading(
                        dcc.Graph(
                                id="indicator-graph",
                                figure=indicator_graph(len(df)),
                                )),
                    style={'border': 'solid white',
                    'border-color': 'white',
                    'border_radius':'50%'}),
            html.Button('RESET ALL',id='reset_button', n_clicks=0,
                        style={'background-color': '#DADADA', 'height':'60%',
                                'border':'none',
                                'padding': '15px 32px',
                                'box-shadow': 'rgb(38, 57, 77) 0px 20px 30px -10px',
                                #'display':'inline-block',
                                'width':'90px',
                                'height':'70px',
                                'margin-top':'70px',
                                'text-align': 'center',
                                'text-decoration': 'none',
                                'display': 'inline-block',
                                'font-size': '20px'}),
            ],
            style={'flex':'10%',
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

    #gun purchase per year+ choropleth map
        html.Div([
            html.Div([
                html.H3('Purchase of Gun By Year',
                        style={
                                'textAlign':'center',
                                'color': 'black',
                                'font-family': 'Georgia',
                                'font-size': '20px',
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


], style={})

#-----------------------------------------------------------------------------------------------------------------------------------


if __name__ == '__main__':
    app.run_server(debug=True)
    #app.run_server(debug=False)
