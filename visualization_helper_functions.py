import pandas as pd
import plotly.express as px
import plotly.graph_objects as go

def trigger_bar_chart_race(df):
    race = raceBarChartClick['points'][0]['x']
    filter_by_race = df[df['race']==race]
    choropleth_map = create_choropleth_map(filter_by_race)
    return choropleth_map

def trigger_line_chart_year(df):
    startDate = lineChartClick['xaxis.range[0]']
    endDate = lineChartClick['xaxis.range[1]']
    filter_by_date = intermediateBarChartRace[(intermediateBarChartRace['date']>=startDate) & (intermediateBarChartRace['date']<=endDate)]
    choropleth_map = create_choropleth_map(filter_by_date)
    return choropleth_map

def get_age_and_gender(stackBarClick):
    gender_id = stackBarClick['points'][0]['curveNumber']
    if gender_id==0:
        gender='Male'
    else:
        gender='Female'

    age = stackBarClick['points'][0]['x']
    return gender, age

def indicator_graph(number):
    indicator_figure = go.Figure(go.Indicator(
    mode = "number",
    value = number,
    number = {'prefix': ""},
    visible=True))
    indicator_figure.update_traces(gauge={'bordercolor':'black', 'borderwidth':10,
                                          'bar':{'color':'#0091D5'},
                                          'axis':{'range':[0,6571],
                                          'tickmode':'auto'}})
    indicator_figure.update_layout(font={'size':5,'color':'black'})
    return indicator_figure

def top_5_by_race(df):
    df_group_by_race = df.groupby('race')['name'].agg('count').reset_index().rename(columns={'name':'count'})
    top_5_by_race_bar = px.bar(df_group_by_race, x="race", y="count", title="Top 5 By Race", color='race')
    top_5_by_race_bar.update_layout(clickmode='event+select',
                              margin={"r":0,"t":0,"l":0,"b":0})
    return top_5_by_race_bar

#Choropleth map
def create_choropleth_map(df):
    df_group_by_state = df.groupby('state')['name'].agg('count').reset_index().rename(columns={'name':'count'})
    choropleth_map = go.Figure(data=go.Choropleth(
        locations=df_group_by_state['state'],
        z = df_group_by_state['count'],
        locationmode = 'USA-states',
        colorscale = 'Greens',
        colorbar_title = "Number of Deaths"
    ))
    choropleth_map.update_layout(
        #title_text = 'Police Shooting Deaths by US States',
        width=1700, height=700,
        geo_scope='usa',
        clickmode='event+select',
        margin={"r":0,"t":0,"l":0,"b":0}
    )
    choropleth_map.update_layout(plot_bgcolor="#d1dade",margin=dict(t=0,l=80,b=0,r=40),
                            font_family="Georgia",
                            title_font_family="Georgia",font_size=25, dragmode=False)
    return choropleth_map

def create_line_chart(df):
    df_group_by_date = df.groupby('date')['name'].agg('count').reset_index().rename(columns={'name':'count'})
    line_chart = go.Figure(data=go.Scatter(x=df_group_by_date['date'], y=df_group_by_date['count'],
                            mode='lines+markers', fill='tozeroy',
                            line={'color':'#30425e'}))
    line_chart.update_layout(showlegend=False,plot_bgcolor="#d1dade",margin=dict(t=0,l=80,b=0,r=40),
                            xaxis_title='Year', height=700, width=2600,
                            yaxis_title='Number of Killings',
                            font_family="Georgia",
                            title_font_family="Georgia",font_size=25)
    return line_chart

def create_line_chart_gun_data(df_gun):
    gun_data_line_chart = go.Figure(data=go.Scatter(x=df_gun['date'], y=df_gun['totals'], fill='tozeroy',  mode='lines+markers', line={'color':'#AC3E31'}))
    gun_data_line_chart.update_layout(showlegend=False,plot_bgcolor="#d1dade",margin=dict(t=50,l=200,b=0,r=40),
                            xaxis_title='Year',
                            yaxis_title='Number of Gun Purchase',
                            font_family="Georgia",
                            title_font_family="Georgia",font_size=22)
    return gun_data_line_chart

#Pie chart
def create_pie_chart(df):
    df_group_by_race = df.groupby('race')['name'].agg('count').reset_index().rename(columns={'name':'count'})
    pie_chart = go.Figure(data=[go.Pie(labels=df_group_by_race['race'], values=df_group_by_race['count'],
                         textinfo='label+percent', insidetextorientation='radial'
                         )])
    colors = ['gold', 'mediumturquoise', 'darkorange', 'lightgreen']
    pie_chart.update_traces(marker=dict(colors=colors))
    pie_chart.update_layout(showlegend=False, plot_bgcolor="#d1dade",margin=dict(t=0,l=0,b=0,r=40),
                            font_family="Georgia",
                            title_font_family="Georgia",font_size=22)
    pie_chart.update_layout(margin=dict(t=0, b=0, l=0, r=0))
    return pie_chart

def create_bar_char_for_mental_illness(df):
    df_group_by_mental_illness = df.groupby('signs_of_mental_illness')['name'].agg('count').reset_index().rename(columns={'name':'count'})
    mental_illness_bar = px.bar(df_group_by_mental_illness, x="signs_of_mental_illness", y="count",
                            color='signs_of_mental_illness',
                            hover_data=['count'],
                            width=1400,
                            height=800,
                            orientation='v'
                            )
    mental_illness_bar.update_layout(clickmode='event+select',
                                 plot_bgcolor="#d1dade",
                                 margin=dict(t=50,l=200,b=80,r=40),
                                 xaxis_title='Signs of Mental Illness',
                                 yaxis_title='Number of Killings',
                                 font_family="Georgia",
                                 title_font_family="Georgia",
                                 font_size=25,
                                 xaxis_tickangle=-45)

    return mental_illness_bar


def create_radar_chart_for_weapons(df):
    df_group_by_weapon = df.groupby('armed')['name'].agg('count').reset_index().rename(columns={'name':'count'})
    df_group_by_weapon = df_group_by_weapon[df_group_by_weapon['count']>20]
    radar_chart_by_weapon = go.Figure(data=go.Scatterpolar(r=df_group_by_weapon['count'],
                                                        theta=df_group_by_weapon['armed'],
                                                        fill='toself'))

    radar_chart_by_weapon.update_layout(width=1400, height=900, font_size=30,
                                        polar=dict(radialaxis=dict(visible=True)),
                                        showlegend=False)
    return radar_chart_by_weapon

def create_bar_char_for_race(df):
    df_group_by_race = df.groupby('race')['name'].agg('count').reset_index().rename(columns={'name':'count'})
    race_bar_chart = px.bar(df_group_by_race, x="race", y="count", color='race',
                        hover_data=['count'],
                        width =1400, height=800,
                        #color_discrete_map={'Male':'#153a8a','Female':'#bf680b'},
                        category_orders ={'gender':['Male','Female']})
    race_bar_chart.update_layout(clickmode='event+select',)
    race_bar_chart.update_layout(showlegend=True, plot_bgcolor="#d1dade",
                            margin=dict(t=50,l=200,b=80,r=40), hovermode='closest',
                            xaxis={'categoryorder':'total descending'},
                            xaxis_title='Race',
                            yaxis_title='Number of Killings',
                            font_family="Georgia",
                            title_font_family="Georgia",font_size=25, xaxis_tickangle=-45)
    return race_bar_chart

#stacked bar chart
def create_bar_chart_for_age_and_gender(df):
    df_group_by_age_gender = df.groupby(['age_bins','gender'])['name'].agg('count').reset_index().rename(columns={'name':'count'})
    stacked_bar = px.bar(df_group_by_age_gender, x="age_bins", y="count", color='gender',
                        hover_data=['count'],
                        barmode = 'group',
                        width=1400, height=800,
                        color_discrete_map={'Male':'#153a8a','Female':'#bf680b'},
                        category_orders ={'gender':['Male','Female']})
    stacked_bar.update_layout(clickmode='event+select', margin={"r":0,"t":0,"l":0,"b":0}),
    stacked_bar.update_layout(showlegend=True,plot_bgcolor="#d1dade",margin=dict(t=50,l=200,b=0,r=40),
                              xaxis_title='Age and Gender',
                              yaxis_title='Number of Killings',
                              font_family="Georgia",
                              title_font_family="Georgia",font_size=25,
                              xaxis_tickangle=-45)
    return stacked_bar

#Sankey Diagram
def generateSankey(df,cat_cols=[],value_cols='',title='Sankey Diagram'):
    colorPalette = ['#be584b','#6dad23','#FFE873','#5e49eb','#646464']
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

    fig.update_layout(plot_bgcolor="#d1dade",margin=dict(t=0,l=80,b=20,r=40),
                            font_family="Georgia",
                            title_font_family="Georgia",font_size=20)
    return fig

def create_sankey_diagram(df):
    df_grouped_sankey = df.groupby(['race','age_bins','gender','signs_of_mental_illness'])['name'].agg('count').reset_index().rename(columns={'name':'count'})
    sankey_diagram = generateSankey(df_grouped_sankey,
                               ['race','age_bins','gender','signs_of_mental_illness'],
                               value_cols='count',
                               )

    return sankey_diagram
