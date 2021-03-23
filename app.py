import pandas as pd
import plotly.express as px  # (version 4.7.0)
import plotly.graph_objects as go

import dash  # (version 1.12.0) pip install dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output

app = dash.Dash(__name__)

#--------------------------------------------------  ---------------------------------------------------------------------------------

df = pd.read_json('police-killings-integrated-dataset-2021-03-20.json.gz')

viz_states = {'pie_chart':0, 'choropleth_map':0, 'line_chart':0, 'stacked_bar_chart':0}

colors = {
    'background': '#111111',
    'text': '#030303F'
}

#Pie chart
def create_pie_chart(df):
    df_group_by_race = df.groupby('race')['name'].agg('count').reset_index().rename(columns={'name':'count'})
    pie_chart = go.Figure(data=[go.Pie(labels=df_group_by_race['race'], values=df_group_by_race['count'], title='Ethnicity Versus Killings', textinfo='label+percent',
                             insidetextorientation='radial')])
    return pie_chart

#Choropleth map
def create_choropleth_map(df):
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
    return choropleth_map

#stacked bar chart
def create_stacked_bar_chart(df):
    df_group_by_age_gender = df.groupby(['age_bins','gender'])['name'].agg('count').reset_index().rename(columns={'name':'count'})
    stacked_bar = px.bar(df_group_by_age_gender, x="age_bins", y="count", color="gender",
            hover_data=['count'], barmode = 'stack', custom_data=['gender'])
    return stacked_bar


#line chart
def create_line_chart(df):
    df_group_by_date = df.groupby('date')['name'].agg('count').reset_index().rename(columns={'name':'count'})
    line_chart = px.line(df_group_by_date, x='date', y="count")
    return line_chart

#Sankey Diagram
def generateSankey(df,cat_cols=[],value_cols='',title='Sankey Diagram'):
    colorPalette = ['#4B8BBE','#306998','#FFE873','#FFD43B','#646464']
    labelList = []
    colorNumList = []
    for catCol in cat_cols:
        labelListTemp =  list(set(df[catCol].values))
        colorNumList.append(len(labelListTemp))
        labelList = labelList + labelListTemp

    # remove duplicates from labelList
    labelList = list(dict.fromkeys(labelList))

    # define colors based on number of levels
    colorList = []
    for idx, colorNum in enumerate(colorNumList):
        colorList = colorList + [colorPalette[idx]]*colorNum

    # transform df into a source-target pair
    for i in range(len(cat_cols)-1):
        if i==0:
            sourceTargetDf = df[[cat_cols[i],cat_cols[i+1],value_cols]]
            sourceTargetDf.columns = ['source','target','count']
        else:
            tempDf = df[[cat_cols[i],cat_cols[i+1],value_cols]]
            tempDf.columns = ['source','target','count']
            sourceTargetDf = pd.concat([sourceTargetDf,tempDf])
        sourceTargetDf = sourceTargetDf.groupby(['source','target']).agg({'count':'sum'}).reset_index()

    # add index for source-target pair
    sourceTargetDf['sourceID'] = sourceTargetDf['source'].apply(lambda x: labelList.index(x))
    sourceTargetDf['targetID'] = sourceTargetDf['target'].apply(lambda x: labelList.index(x))

    # creating the sankey diagram
    fig = go.Figure(data=[go.Sankey(
        node = dict(
          pad = 15,
          thickness = 20,
          line = dict(
            color = "black",
            width = 0.5
          ),
          label = labelList,
          color = colorList
        ),
        link = dict(
          source = sourceTargetDf['sourceID'],
          target = sourceTargetDf['targetID'],
          value = sourceTargetDf['count']
        ),

    )])
    fig.update_layout(
            title = title
            )
    return fig


def create_sankey_diagram(df):
    df_grouped_sankey = df.groupby(['race','age_bins','gender','signs_of_mental_illness'])['name'].agg('count').reset_index().rename(columns={'name':'count'})
    sankey_diagram = generateSankey(df_grouped_sankey,
                               ['race','age_bins','gender','signs_of_mental_illness'],
                               value_cols='count',
                               title='Police Killings in the US')
    return sankey_diagram

def get_age_and_gender(stackBarClick):
    gender_id = stackBarClick['points'][0]['curveNumber']
    if gender_id==0:
        gender='Female'
    else:
        gender='Male'

    age = stackBarClick['points'][0]['x']
    return gender, age

#-----------------------------------------------------------------------------------------------------------------------------------

app.layout = html.Div([

    html.H1("Police Killings in the US", style={
            'textAlign': 'center',
            'color': colors['text']
        }),
    dcc.Loading(dcc.Graph(
                id='line-chart',
                figure=create_line_chart(df)
    )),

    html.Div([
            dcc.Graph(
                    id='choropleth-map',
                    figure=create_choropleth_map(df),
                    #config={#'responsive': True,
                    #                'doubleClick':'reset'},
            ),

            dcc.Graph(
                    id='sankey-diagram',
                    figure=create_sankey_diagram(df)
            )
    ], style={'columnCount': 2}),

    html.Div([
            dcc.Graph(
                    id='pie-chart-interaction',
                    figure=create_pie_chart(df),
                    config={#'responsive': True,
                                'doubleClick':'reset'},
            ),

            dcc.Graph(
                    id='stacked-bar-chart',
                    figure=create_stacked_bar_chart(df),
            ),
    ], style={'columnCount': 2}),


])

#-----------------------------------------------------------------------------------------------------------------------------------

@app.callback(
    Output('sankey-diagram', 'figure'),
    [Input('pie-chart-interaction', 'clickData'),
    Input('stacked-bar-chart', 'clickData'),
    Input('line-chart','relayoutData'),
    Input('choropleth-map','clickData')], prevent_initial_call=True)
def update_sankey_diagram(pieClick, stackBarClick, lineChartClick, mapClick):

    triggered_element = dash.callback_context.triggered[0]['prop_id'].split('.')[0]
    if triggered_element =='pie-chart-interaction':
        filter_by_race = df[df['race']==str(pieClick['points'][0]['label'])]
        sankey_diagram = create_sankey_diagram(filter_by_race)
        viz_states['pie_chart'] = 1

    elif triggered_element =='stacked-bar-chart':
        gender, age= get_age_and_gender(stackBarClick)
        filter_by_age_gender = df[(df['gender']==gender) & (df['age_bins']==age)]
        sankey_diagram = create_sankey_diagram(filter_by_age_gender)
        viz_states['stacked_bar_chart'] = 1
    elif triggered_element =='line-chart':
        startDate = lineChartClick['xaxis.range[0]']
        endDate = lineChartClick['xaxis.range[1]']
        filter_by_date = df[(df['date']>=startDate) & (df['date']<=endDate)]
        sankey_diagram = create_sankey_diagram(filter_by_date)
        viz_states['line_chart'] = 1
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
    Input('line-chart','relayoutData')], prevent_initial_call=True)
def update_choropleth_map(pieClick, stackBarClick, lineChartClick):
    if viz_states['choropleth_map']==1:
        return dash.no_update
    triggered_element = dash.callback_context.triggered[0]['prop_id'].split('.')[0]
    if triggered_element =='pie-chart-interaction':
        filter_by_race = df[df['race']==str(pieClick['points'][0]['label'])]
        choropleth_map = create_choropleth_map(filter_by_race)
        viz_states['pie_chart'] = 1
    elif triggered_element =='stacked-bar-chart':
        gender, age= get_age_and_gender(stackBarClick)
        filter_by_age_gender = df[(df['gender']==gender) & (df['age_bins']==age)]
        choropleth_map = create_choropleth_map(filter_by_age_gender)
        viz_states['stacked_bar_chart'] = 1
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
     Input('line-chart','relayoutData')], prevent_initial_call=True)
def update_pie_chart(mapClick, stackBarClick, lineChartClick):
    if viz_states['pie_chart']==1:
        return dash.no_update
    triggered_element = dash.callback_context.triggered[0]['prop_id'].split('.')[0]
    if triggered_element == 'choropleth-map':
        filter_by_location = df[df['state']==mapClick['points'][0]['location']]
        pie_chart = create_pie_chart(filter_by_location)
        viz_states['choropleth_map'] = 1
    if triggered_element =='stacked-bar-chart':
        gender, age= get_age_and_gender(stackBarClick)
        filter_by_age_gender = df[(df['gender']==gender) & (df['age_bins']==age)]
        pie_chart = create_pie_chart(filter_by_age_gender)
        viz_states['stacked_bar_chart'] = 1
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
     Input('line-chart','relayoutData')], prevent_initial_call=True)
def update_stacked_bar_chart(mapClick, pieClick, lineChartClick):
    if viz_states['stacked_bar_chart']==1:
        return dash.no_update
    triggered_element = dash.callback_context.triggered[0]['prop_id'].split('.')[0]
    if triggered_element == 'choropleth-map':
        filter_by_location = df[df['state']==mapClick['points'][0]['location']]
        stacked_bar = create_stacked_bar_chart(filter_by_location)
        viz_states['choropleth_map'] = 1
    if triggered_element =='pie-chart-interaction':
        filter_by_race = df[df['race']==str(pieClick['points'][0]['label'])]
        stacked_bar = create_stacked_bar_chart(filter_by_race)
        viz_states['pie_chart'] = 1
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
     Input('stacked-bar-chart','clickData')], prevent_initial_call=True)
def update_line_chart(mapClick, pieClick, stackBarClick):
    if viz_states['line_chart']==1:
        return dash.no_update
    triggered_element = dash.callback_context.triggered[0]['prop_id'].split('.')[0]
    if triggered_element == 'choropleth-map':
        filter_by_location = df[df['state']==mapClick['points'][0]['location']]
        line_chart = create_line_chart(filter_by_location)
        viz_states['choropleth_map'] = 1
    if triggered_element =='pie-chart-interaction':
        filter_by_race = df[df['race']==str(pieClick['points'][0]['label'])]
        line_chart = create_line_chart(filter_by_race)
        viz_states['pie_chart'] = 1
    if triggered_element =='stacked-bar-chart':
        gender, age= get_age_and_gender(stackBarClick)
        filter_by_age_gender = df[(df['gender']==gender) & (df['age_bins']==age)]
        line_chart = create_line_chart(filter_by_age_gender)
        viz_states['stacked_bar_chart'] = 1
    return line_chart

#-----------------------------------------------------------------------------------------------------------------------------------

if __name__ == '__main__':
    #app.run_server(debug=True)
    app.run_server(debug=True)
