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

viz_states = {'pie_chart':0, 'choropleth_map':0, 'line_chart':0, 'stacked_bar_chart':0}

#-----------------------------------------------------------------------------------------------------------------------------------

app.layout = html.Div([

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
                'background-color' : '#488A99',
                'margin-left':'0px',
                'margin-right':'0px'}
    ),

    html.Div([
        html.Div([
            html.P('Police violence is a leading cause of death for young men in the United States. Over the life course, about 1 in every 1,000 black men can expect to be killed by police. Risk of being killed by police peaks between the ages of 20 y and 35 y for men and women and for all racial and ethnic groups. Black women and men and American Indian and Alaska Native women and men are significantly more likely than white women and men to be killed by police. Latino men are also more likely to be killed by police than are white men..')
        ], style={'float':'left','flex':'60%',
                 'text-align':'justify',
                 'background-color':'#c8d7e3',
                  'font-family': 'Helvetica Neue',
                  'font-size': '40px',
                  'padding':'20px',
                  'border': 'solid black',
                  'border-color': 'black',
                  'border-width': '5px 5px 0px 5px',
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
                    'border': 'solid black',
                    'border-color': 'black',
                    'border-width': ' 5px 5px 0px 0px',
                    'padding':'20px',
                    'margin-left': '0px',
                    'margin-right': '0px'}),

        html.Div([
            html.H1(children='Total Number of Police Killings'),
            html.Div(dcc.Loading(
                        dcc.Graph(
                                id="indicator-graph",
                                figure=indicator_graph(len(df)),
                                )),
                    style={'border': 'solid black',
                    'border-color': 'black',
                    'border_radus':'50%'}),
            html.Button('Reset All',id='reset_button',n_clicks=0,
                        style={'background-color': '#DADADA',
                                'border':'none',
                                'padding': '15px 32px',
                                'margin-top':'10px',
                                'text-align': 'center',
                                'text-decoration': 'none',
                                'display': 'inline-block',
                                'font-size': '30px'}),
            ],
            style={'flex':'40%',
                    'background-color': '#c8d7e3',
                    'text-align':'center',
                    'border': 'solid black',
                    'border-color': 'black',
                    'border-width': ' 5px 5px 0px 0px',
                    'padding':'20px'})
    ],
    className='information-bar',
    style={'display':'flex',
           'height':'50%',
           'margin-left': '0px',
           'margin-right': '0px',
           }
    ),


    html.Div([
            html.H3('Police Killings by Year',
                    style={
                            'textAlign':'center',
                            'color': 'black',
                            'font-family': 'Helvetica Neue',
                            'font-size': '32px','font-weight': 'bold',
                            'line-height': '1',
                            }),
            dcc.Loading(dcc.Graph(
                    id='line-chart',
                    figure=create_line_chart(df)
            ))

    ], className='line-chart-block', style={'background-color':'#c8d7e3',
                                            'border': 'solid black',
                                            'box-shadow': 'rgb(38, 57, 77) 0px 20px 30px -10px',
                                            'border-color': 'black',
                                            'border-width': ' 5px',
                                            'padding':'20px',
                                            'margin-left': '0px',
                                            'margin-right': '0px'}),
                                            #'margin-top':'80px',
                                            #'margin-bottom':'80px'

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
                                                    'margin-left':'0px','margin-right': '0px',
                                                    'border': 'solid black',
                                                    'border-color': 'black',
                                                    'border-width': ' 0px 5px 5px 5px',
                                                    'padding':'20px'}),

    html.Div([
        html.Div([
                html.H3('Police Killings by State',
                        style={
                                'textAlign' : 'center',
                                'color': 'black',
                                'font-family': 'Helvetica Neue',
                                'font-size': '30px','font-weight': 'bold',
                                'line-height': '1'}),
                dcc.Graph(
                id='choropleth-map',
                figure=create_choropleth_map(df),
                )], style={'flex':'50%',
                            'border': 'solid black',
                            'border-color': 'black',
                            'border-width': ' 0px 5px 5px 5px',
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
                            'border': 'solid black',
                            'border-color': 'black',
                            'border-width': '0px 5px 5px 0px',
                            'padding':'20px', 'background-color':'#c8d7e3'
                            }
                , className='sankey-block'),

    ],
    className='sankey-map',
    style={'display':'flex',
           'height':'80%',
           'margin-left': '0px',
           'margin-right': '0px',}
           #'margin-top':'80px',
           #'margin-bottom':'70px'}
    ),

    html.Div([
        html.Div([
                html.H3('Police Killings by Race',
                        style={
                                'textAlign' : 'center',
                                'color': 'black',
                                'font-family': 'Helvetica Neue',
                                'font-size': '30px','font-weight': 'bold',
                                'line-height': '1'}),
                dcc.Graph(
                        id='pie-chart-interaction',
                        figure=create_pie_chart(df),
                        style={'flex':'50%'}
                        #config={#'responsive': True,
                        #            'doubleClick':'reset'},
                )], style={'flex':'50%',
                            'border': 'solid black',
                            'border-color': 'black',
                            'border-width': '0px 5px 5px 5px',
                            'padding':'20px', 'background-color':'#c8d7e3'
                            }
                            #'border-radius': '15px'}

                , className='pie-block'),

        html.Div([
                html.H3('Police Killings by Age and Gender',
                        style={
                                'textAlign' : 'center',
                                'color': 'black',
                                'font-family': 'Helvetica Neue',
                                'font-size': '30px','font-weight': 'bold',
                                'line-height': '1'}),
                dcc.Graph(
                        id='stacked-bar-chart',
                        figure=create_stacked_bar_chart(df),
                        config={'doubleClick':'reset'},
                        style={'flex':'50%'}
                )], style={'flex':'50%',
                            'border': 'solid black',
                            'border-color': 'black',
                            'border-width': '0px 5px 5px 0px',
                            'padding':'20px', 'background-color':'#c8d7e3'
                            }
                            #'border-radius': '15px'}

                , className='stacked-bar-block'),

    ],
    className='bar-pie',
    style={'display':'flex',
           'height':'80%',
           'margin-left': '0px',
           'margin-right': '0px',
           #'margin-top':'20px',
           'margin-bottom':'70px'}
    ),
], style={})

#-----------------------------------------------------------------------------------------------------------------------------------

#update indicator graph
@app.callback(
    Output('indicator-graph','figure'),
    [Input('line-chart','relayoutData'),
     Input('pie-chart-interaction', 'clickData'),
     Input('stacked-bar-chart', 'clickData'),
     Input('choropleth-map','clickData'),
     Input('reset_button','n_clicks')], prevent_initial_call=True)
def update_indicator_graph(lineChartClick, pieClick, stackBarClick, mapClick, n_clicks):
    triggered_element = dash.callback_context.triggered[0]['prop_id'].split('.')[0]
    changed_id = [p['prop_id'] for p in dash.callback_context.triggered][0].split('.')[0]
    if changed_id=='reset_button':
        return indicator_graph(len(df))
    if triggered_element=='line-chart':
        startDate = lineChartClick['xaxis.range[0]']
        endDate = lineChartClick['xaxis.range[1]']
        filter_by_date = df[(df['date']>=startDate) & (df['date']<=endDate)]
        #df = filter_by_date
        updated_indicator_graph = indicator_graph(len(filter_by_date))
        return updated_indicator_graph
    elif triggered_element =='pie-chart-interaction':
        filter_by_race = df[df['race']==str(pieClick['points'][0]['label'])]
        updated_indicator_graph = indicator_graph(len(filter_by_race))
        return updated_indicator_graph
    elif triggered_element =='stacked-bar-chart':
        gender, age= get_age_and_gender(stackBarClick)
        filter_by_age_gender = df[(df['gender']==gender) & (df['age_bins']==age)]
        updated_indicator_graph = indicator_graph(len(filter_by_age_gender))
        return updated_indicator_graph
    elif triggered_element == 'choropleth-map':
        filter_by_location = df[df['state']==mapClick['points'][0]['location']]
        updated_indicator_graph = indicator_graph(len(filter_by_location))
        #df = filter_by_location
        return updated_indicator_graph

#update line hcart for gun purchase
@app.callback(
    Output('gun-line-chart', 'figure'),
    [Input('line-chart','relayoutData'),
     Input('reset_button','n_clicks')], prevent_initial_call=True)
def update_gun_data_line_chart(lineChartClick, n_clicks):
    triggered_element = dash.callback_context.triggered[0]['prop_id'].split('.')[0]
    changed_id = [p['prop_id'] for p in dash.callback_context.triggered][0].split('.')[0]
    if changed_id=='reset_button':
        return create_line_chart_gun_data(gun_data)
    if triggered_element=='line-chart':
        startDate = lineChartClick['xaxis.range[0]']
        endDate = lineChartClick['xaxis.range[1]']
        filter_gun_data_by_date = gun_data[(gun_data['date']>=startDate) & (gun_data['date']<=endDate)]
        gun_data_line_chart = create_line_chart_gun_data(filter_gun_data_by_date)
        return gun_data_line_chart

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


#update choropleth map
@app.callback(
    Output('choropleth-map', 'figure'),
    [Input('pie-chart-interaction', 'clickData'),
    Input('stacked-bar-chart', 'clickData'),
    Input('line-chart','relayoutData'),
    Input('reset_button','n_clicks')], prevent_initial_call=True)
def update_choropleth_map(pieClick, stackBarClick, lineChartClick, n_clicks):
    changed_id = [p['prop_id'] for p in dash.callback_context.triggered][0].split('.')[0]
    if changed_id=='reset_button':
        viz_states['choropleth_map'] = 0
        return create_choropleth_map(df)
    if viz_states['choropleth_map']==1:
        return dash.no_update
    triggered_element = dash.callback_context.triggered[0]['prop_id'].split('.')[0]
    if triggered_element =='pie-chart-interaction':
        filter_by_race = df[df['race']==str(pieClick['points'][0]['label'])]
        choropleth_map = create_choropleth_map(filter_by_race)
        viz_states['pie_chart'] = 1
        return choropleth_map
    elif triggered_element =='stacked-bar-chart':
        gender, age= get_age_and_gender(stackBarClick)
        filter_by_age_gender = df[(df['gender']==gender) & (df['age_bins']==age)]
        choropleth_map = create_choropleth_map(filter_by_age_gender)
        viz_states['stacked_bar_chart'] = 1
        return choropleth_map
    elif triggered_element =='line-chart':
        startDate = lineChartClick['xaxis.range[0]']
        endDate = lineChartClick['xaxis.range[1]']
        filter_by_date = df[(df['date']>=startDate) & (df['date']<=endDate)]
        choropleth_map = create_choropleth_map(filter_by_date)
        viz_states['line_chart'] = 1
        return choropleth_map

#update pie chart
@app.callback(
    Output('pie-chart-interaction', 'figure'),
    [Input('choropleth-map', 'clickData'),
     Input('stacked-bar-chart', 'clickData'),
     Input('line-chart','relayoutData'),
     Input('reset_button','n_clicks')], prevent_initial_call=True)
def update_pie_chart(mapClick, stackBarClick, lineChartClick, n_clicks):
    changed_id = [p['prop_id'] for p in dash.callback_context.triggered][0].split('.')[0]
    if changed_id=='reset_button':
        viz_states['pie_chart'] = 0
        return create_pie_chart(df)
    if viz_states['pie_chart']==1:
        return dash.no_update
    triggered_element = dash.callback_context.triggered[0]['prop_id'].split('.')[0]
    if triggered_element == 'choropleth-map':
        filter_by_location = df[df['state']==mapClick['points'][0]['location']]
        pie_chart = create_pie_chart(filter_by_location)
        viz_states['choropleth_map'] = 1
        return pie_chart
    if triggered_element =='stacked-bar-chart':
        gender, age= get_age_and_gender(stackBarClick)
        filter_by_age_gender = df[(df['gender']==gender) & (df['age_bins']==age)]
        pie_chart = create_pie_chart(filter_by_age_gender)
        viz_states['stacked_bar_chart'] = 1
        return pie_chart
    if triggered_element =='line-chart':
        startDate = lineChartClick['xaxis.range[0]']
        endDate = lineChartClick['xaxis.range[1]']
        filter_by_date = df[(df['date']>=startDate) & (df['date']<=endDate)]
        pie_chart = create_pie_chart(filter_by_date)
        viz_states['line_chart'] = 1
        return pie_chart


#update stacked bar chart
@app.callback(
    Output('stacked-bar-chart', 'figure'),
    [Input('choropleth-map', 'clickData'),
     Input('pie-chart-interaction', 'clickData'),
     Input('line-chart','relayoutData'),
     Input('reset_button','n_clicks')], prevent_initial_call=True)
def update_stacked_bar_chart(mapClick, pieClick, lineChartClick, n_clicks):
    changed_id = [p['prop_id'] for p in dash.callback_context.triggered][0].split('.')[0]
    if changed_id=='reset_button':
        viz_states['stacked_bar_chart'] = 0
        return create_stacked_bar_chart(df)
    if viz_states['stacked_bar_chart']==1:
        return dash.no_update
    triggered_element = dash.callback_context.triggered[0]['prop_id'].split('.')[0]
    if triggered_element == 'choropleth-map':
        filter_by_location = df[df['state']==mapClick['points'][0]['location']]
        stacked_bar = create_stacked_bar_chart(filter_by_location)
        viz_states['choropleth_map'] = 1
        return stacked_bar
    if triggered_element =='pie-chart-interaction':
        filter_by_race = df[df['race']==str(pieClick['points'][0]['label'])]
        stacked_bar = create_stacked_bar_chart(filter_by_race)
        viz_states['pie_chart'] = 1
        return stacked_bar
    if triggered_element == 'line-chart':
        startDate = lineChartClick['xaxis.range[0]']
        endDate = lineChartClick['xaxis.range[1]']
        filter_by_date = df[(df['date']>=startDate) & (df['date']<=endDate)]
        stacked_bar = create_stacked_bar_chart(filter_by_date)
        viz_states['stacked_bar_chart'] = 1
        return stacked_bar


#update line chart
@app.callback(
    Output('line-chart', 'figure'),
    [Input('choropleth-map', 'clickData'),
     Input('pie-chart-interaction', 'clickData'),
     Input('stacked-bar-chart','clickData'),
     Input('reset_button','n_clicks')], prevent_initial_call=True)
def update_line_chart(mapClick, pieClick, stackBarClick, n_clicks):
    changed_id = [p['prop_id'] for p in dash.callback_context.triggered][0].split('.')[0]
    if changed_id=='reset_button':
        viz_states['line_chart'] = 0
        return create_line_chart(df)
    if viz_states['line_chart']==1:
        return dash.no_update
    triggered_element = dash.callback_context.triggered[0]['prop_id'].split('.')[0]
    if triggered_element == 'choropleth-map':
        filter_by_location = df[df['state']==mapClick['points'][0]['location']]
        line_chart = create_line_chart(filter_by_location)
        viz_states['choropleth_map'] = 1
        return line_chart
    if triggered_element =='pie-chart-interaction':
        filter_by_race = df[df['race']==str(pieClick['points'][0]['label'])]
        line_chart = create_line_chart(filter_by_race)
        viz_states['pie_chart'] = 1
        return line_chart
    if triggered_element =='stacked-bar-chart':
        gender, age= get_age_and_gender(stackBarClick)
        filter_by_age_gender = df[(df['gender']==gender) & (df['age_bins']==age)]
        line_chart = create_line_chart(filter_by_age_gender)
        viz_states['stacked_bar_chart'] = 1
        return line_chart

#-----------------------------------------------------------------------------------------------------------------------------------

if __name__ == '__main__':
    app.run_server(debug=True)
    #app.run_server(debug=False)
