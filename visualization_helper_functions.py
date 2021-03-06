import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from assets.state_mapping import state_mapping

FONT_COLOR='white'
LINE_COLOR='#f2c029'

def get_country_list_for_dropdown(df):
    country_mapping = {}
    list_of_countries = []
    for key, value in state_mapping.items():
        country_mapping['label'] = value
        country_mapping['value'] = key
        list_of_countries.append(country_mapping.copy())
    return list_of_countries

def get_age_and_gender(stackBarClick):
    gender_id = stackBarClick['points'][0]['curveNumber']
    if gender_id==0:
        gender='Male'
    else:
        gender='Female'
    age = stackBarClick['points'][0]['x']
    return gender, age

#Choropleth map
def create_choropleth_map(df):
    df_group_by_state = df.groupby('state')['name'].agg('count').reset_index().rename(columns={'name':'count'})
    choropleth_map = go.Figure(data=go.Choropleth(locations = df_group_by_state['state'],
                                                  z = df_group_by_state['count'],
                                                  locationmode = 'USA-states',
                                                  colorscale = 'Greens',
                                                  colorbar_title = "Number of Deaths"))
    choropleth_map.update_layout(width=1600,
                                 height=700,
                                 geo_scope='usa',
                                 clickmode='event+select',
                                 margin={"r":0,"t":0,"l":0,"b":0},
                                 hoverlabel = dict(font=dict(size=25)))
    choropleth_map.update_layout(geo=dict(bgcolor= 'rgba(0,0,0,0)'),
                                 plot_bgcolor="#1c2b3b",
                                 margin=dict(t=0,l=80,b=0,r=40),
                                 font_family="Proxima Nova",
                                 title_font_family="Proxima Nova",
                                 font_size=35,
                                 font_color=FONT_COLOR,
                                 dragmode=False,
                                 paper_bgcolor='rgba(0,0,0,0)',
                                 )
    return choropleth_map

def create_line_chart(df):
    df_group_by_date = df.groupby('date')['name'].agg('count').reset_index().rename(columns={'name':'count'})
    line_chart = go.Figure(data=go.Scatter(x=df_group_by_date['date'],
                                           y=df_group_by_date['count'],
                                           mode='lines+markers',
                                           line={'color':LINE_COLOR}))
    line_chart.update_xaxes(showspikes=True,
                            showgrid=False,
                            spikecolor="green",
                            spikesnap="cursor",
                            spikemode="across")
    line_chart.update_yaxes(showspikes=True,
                            spikecolor="orange",
                            spikethickness=2)
    line_chart.update_layout(showlegend=False,
                             plot_bgcolor="#1c2b3b",
                             paper_bgcolor='rgba(0,0,0,0)',
                             margin=dict(t=0,l=80,b=0,r=40),
                             xaxis_title='Year', height=700, width=2600,
                             yaxis_title='Number of Killings',
                             font_family="Proxima Nova",
                             font_color=FONT_COLOR,
                             title_font_family="Proxima Nova",
                             font_size=35,
                             hoverlabel = dict(font=dict(size=30)),
                             )
    return line_chart

def create_line_chart_gun_data(df_gun):
    gun_data_line_chart = go.Figure(data=go.Scatter(x=df_gun['date'],
                                                    y=df_gun['totals'],
                                                    #fill='tozeroy',
                                                    mode='lines+markers',
                                                    line={'color':LINE_COLOR}))
    gun_data_line_chart.update_xaxes(showspikes=True,
                                     showgrid=False,
                                     spikecolor="green",
                                     spikesnap="cursor",
                                     spikemode="across")
    gun_data_line_chart.update_yaxes(showspikes=True,
                                     spikecolor="orange",
                                     spikethickness=2)
    gun_data_line_chart.update_layout(showlegend=False,plot_bgcolor="#1c2b3b",
                                      paper_bgcolor='rgba(0,0,0,0)',
                                      margin=dict(t=0,l=80,b=0,r=40),
                                      xaxis_title='Year',
                                      height=700,
                                      width=2600,
                                      yaxis_title='Number of Gun Purchase',
                                      font_family="Proxima Nova",
                                      font_color=FONT_COLOR,
                                      hoverlabel = dict(font=dict(size=30)),
                                      title_font_family="Proxima Nova",
                                      font_size=35)
    return gun_data_line_chart

def create_bar_chart_for_mental_illness(df):
    df_group_by_mental_illness = df.groupby('signs_of_mental_illness')['name'].agg('count').reset_index().rename(columns={'name':'count'})
    mental_illness_bar = px.bar(df_group_by_mental_illness,
                                x="signs_of_mental_illness",
                                y="count",
                                hover_data=['count'],
                                width=1300,
                                height=800,
                                color_discrete_sequence =['#f2c029','#f2c029'],
                                )
    mental_illness_bar.update_layout(clickmode='event+select',
                                     paper_bgcolor='rgba(0,0,0,0)',
                                     showlegend=False,
                                     plot_bgcolor="#1c2b3b",
                                     margin=dict(t=50,l=200,b=80,r=40),
                                     xaxis_title='Signs of Mental Illness',
                                     yaxis_title='Number of Killings',
                                     font_family="Proxima Nova",
                                     title_font_family="Proxima Nova",
                                     hoverlabel = dict(font=dict(size=30)),
                                     font_size=35,
                                     font_color=FONT_COLOR,
                                     xaxis_tickangle=-45)

    return mental_illness_bar


def group_into_others(count,armed):
    if count<25:
        return 'Others'
    else:
        return armed

def create_bar_chart_for_weapons(df):
    df_group_by_weapon = df.groupby('armed')['name'].agg('count').reset_index().rename(columns={'name':'count'})
    df_group_by_weapon['armed'] = df_group_by_weapon[['count','armed']].apply(lambda x: group_into_others(*x), axis=1)
    df_group_by_weapon = df_group_by_weapon.groupby('armed')['armed','count'].agg('sum').reset_index()
    weapon_bar = px.bar(df_group_by_weapon,
                        y="armed",
                        x="count",
                        hover_data=['count'],
                        width=1400,
                        height=1000,
                        color_discrete_sequence =['#f2c029','#f2c029'],
                        )
    weapon_bar.update_layout(clickmode='event+select',
                             paper_bgcolor='rgba(0,0,0,0)',
                             showlegend=False,
                             plot_bgcolor="#1c2b3b",
                             margin=dict(t=50,l=200,b=80,r=40),
                             xaxis_title='Signs of Mental Illness',
                             yaxis_title='Number of Killings',
                             font_family="Proxima Nova",
                             title_font_family="Proxima Nova",
                             yaxis={'categoryorder':'total ascending'},
                             hoverlabel = dict(font=dict(size=30)),
                             font_size=35,
                             font_color=FONT_COLOR,
                             )

    return weapon_bar


def create_bar_chart_for_threat_level(df):
    df_group_by_threat_level = df.groupby('threat_level')['name'].agg('count').reset_index().rename(columns={'name':'count'})
    threat_level_bar_chart = px.bar(df_group_by_threat_level,
                                    x="threat_level",
                                    y="count", #color=''
                                    hover_data=['count'],
                                    width =1400,
                                    height=1000,
                                    color_discrete_sequence =['#f2c029','#f2c029','#f2c029'])
    threat_level_bar_chart.update_layout(showlegend=True,
                                         plot_bgcolor="#1c2b3b",
                                         clickmode='event+select',
                                         paper_bgcolor='rgba(0,0,0,0)',
                                         margin=dict(t=50,l=200,b=80,r=40),
                                         hoverlabel = dict(font=dict(size=30)),
                                         xaxis={'categoryorder':'total descending'},
                                         xaxis_title='Threat Level',
                                         yaxis_title='Number of Killings',
                                         font_family="Proxima Nova",
                                         font_color=FONT_COLOR,
                                         title_font_family="Proxima Nova",
                                         font_size=35,
                                         xaxis_tickangle=-45)
    return threat_level_bar_chart

def create_bar_chart_for_fleeing(df):
    df_group_by_fleeing = df.groupby('flee')['name'].agg('count').reset_index().rename(columns={'name':'count'})
    fleeing_bar_chart = px.bar(df_group_by_fleeing,
                               x="flee",
                               y="count",
                               hover_data=['count'],
                               width =1250,
                               height=1000,
                               color_discrete_sequence = ['#f2c029','#f2c029','#f2c029','#f2c029'])
    fleeing_bar_chart.update_layout(showlegend=True,
                                    plot_bgcolor="#1c2b3b",
                                    clickmode='event+select',
                                    paper_bgcolor='rgba(0,0,0,0)',
                                    margin=dict(t=50,l=200,b=80,r=40),
                                    hoverlabel = dict(font=dict(size=30)),
                                    xaxis={'categoryorder':'total descending'},
                                    xaxis_title='Type of Fleeing',
                                    yaxis_title='Number of Killings',
                                    font_family="Proxima Nova",
                                    font_color=FONT_COLOR,
                                    title_font_family="Proxima Nova",
                                    font_size=35,
                                    xaxis_tickangle=-45)
    return fleeing_bar_chart


def create_bar_chart_for_race(df):
    df_group_by_race = df.groupby('race')['name'].agg('count').reset_index().rename(columns={'name':'count'})
    race_bar_chart = px.bar(df_group_by_race,
                            x="race",
                            y="count",
                            hover_data=['count'],
                            color_discrete_sequence =['#f2c029','#f2c029','#f2c029','#f2c029','#f2c029','#f2c029'],
                            width =1400, height=800,
                            )

    race_bar_chart.update_layout(showlegend=True,
                                 plot_bgcolor="#1c2b3b",
                                 paper_bgcolor='rgba(0,0,0,0)',
                                 clickmode='event+select',
                                 margin=dict(t=50,l=200,b=80,r=40),
                                 xaxis={'categoryorder':'total descending'},
                                 xaxis_title='Race',
                                 yaxis_title='Number of Killings',
                                 font_family="Proxima Nova",
                                 font_color=FONT_COLOR,
                                 title_font_family="Proxima Nova",
                                 hoverlabel = dict(font=dict(size=30)),
                                 font_size=35,
                                 xaxis_tickangle=-45)
    return race_bar_chart

#stacked bar chart
def create_bar_chart_for_age_and_gender(df):
    df_group_by_age_gender = df.groupby(['age_bins','gender'])['name'].agg('count').reset_index().rename(columns={'name':'count'})
    bar_age_gender = px.bar(df_group_by_age_gender,
                            x="age_bins",
                            y="count",
                            color='gender',
                            hover_data=['count'],
                            barmode = 'group',
                            width=1400,
                            height=800,
                            color_discrete_map={'Male':'#398EEA','Female':'#ff96cc'},
                            category_orders ={'gender':['Male','Female']})
    bar_age_gender.update_layout(showlegend=True,plot_bgcolor="#1c2b3b",
                                 paper_bgcolor='rgba(0,0,0,0)',
                                 clickmode='event+select',
                                 margin=dict(t=50,l=200,b=0,r=40),
                                 xaxis_title='Age and Gender',
                                 yaxis_title='Number of Killings',
                                 font_family="Pro   xima Nova",
                                 font_color=FONT_COLOR,
                                 hoverlabel = dict(font=dict(size=30)),
                                 title_font_family="Proxima Nova",
                                 font_size=35,
                                 xaxis_tickangle=-45)
    return bar_age_gender



#Sankey Diagram
def generateSankey(df,startDate, endDate, gunStartDate, gunEndDate, state, race, gender, age, mental_illness_value, threat_value, flee_value, arms_value, cat_cols=[], value_cols='',title='Sankey Diagram'):
    colorPalette = ['#f2c029','#b8816a','#b8816a','#108f83','#be584b','#db8746']
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
    sankey = go.Figure(data=[go.Sankey(
        node = dict(
          pad = 20,
          thickness = 22,
          line = dict(
            color = "green",
            width = 0.8
          ),
          label = labelList,
          color = colorList
        ),
        link = dict(
          source = sourceTargetDf['sourceID'],
          target = sourceTargetDf['targetID'],
          value = sourceTargetDf['count'],
          color='#6a889c'
        ),
        textfont=dict(color='red',size=42)
    )])
    sankey.update_traces(customdata=['Race','Age','Gender','Threat Level','Fleeing'])
    sankey.update_layout(title_text='<b>Race\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\
                                  Age \t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t \
                                  Gender\t\t\t\t\t\t\t\t\t\t\t\t\t\t \
                                  Signs of Mental Illness \t\t\t\t\
                                  Threat Level\t\t\t\t\t\t\t \
                                  Fleeing<b>',
                         title_pad=dict(t=0,l=0,b=60,r=0),
                         width=4250,
                         height=1000,
                         plot_bgcolor="#1c2b3b",
                         hoverlabel = dict(font=dict(size=30)),
                         margin=dict(t=70,l=100,b=20,r=100),
                         paper_bgcolor='rgba(0,0,0,0)',
                         font_family="Proxima Nova",
                         font_color='white',
                         title_font_family="Proxima Nova",
                         font_size=32)
    return sankey


def create_parallel_coordinate(df):
    df_pc = df.groupby(['state','race','age_bins','gender','signs_of_mental_illness','flee','threat_level'])['name'].agg('count').reset_index().rename(columns={'name':'count'})
    fig = go.Figure(go.Parcats(
    dimensions=[
        {'label': 'Race',
         'values': df_pc['race']},
        {'label': 'Gender',
         'values': df_pc['gender']},
        {'label': 'Flee',
         'values': df_pc['flee']},
        {'label': 'Age',
         'values': df_pc['age_bins']},
        {'label': 'Signs of Mental Illness',
         'values': df_pc['signs_of_mental_illness']},
        {'label': 'Threat Level',
         'values': df_pc['threat_level']}],
    line={'color': df_pc['state'].astype('category').cat.codes, 'colorscale': 'greens'},
    tickfont={'size': 45, 'family': 'Proxima Nova'},
    #labelfont={'color':'#c73732', 'size':30},
    hoveron='category',
    hoverinfo='count+probability',
))
    fig.update_layout(width=4200,
                      height=2000,
                      font_size=45,
                      margin=dict(t=70,l=100,b=20,r=100),
                      font_family="Proxima Nova",
                      font_color='white',
                      title_font_family="Proxima Nova",
                      hoverlabel = dict(font=dict(size=80)),
                      paper_bgcolor='rgba(0,0,0,0)',)

    return fig
