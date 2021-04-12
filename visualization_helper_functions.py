import pandas as pd
import plotly.express as px
import plotly.graph_objects as go

def get_age_and_gender(stackBarClick):
    gender_id = stackBarClick['points'][0]['curveNumber']
    if gender_id==0:
        gender='Male'
    else:
        gender='Female'

    age = stackBarClick['points'][0]['x']
    return gender, age

def indicator_graph(number):
    indicator_figure = go.Figure(go.Indicator(mode = "number",
                                              value = number,
                                              number = {'prefix': ""},
                                              visible=True))
    indicator_figure.update_traces(gauge={'bordercolor':'black', 'borderwidth':10,
                                          'bar':{'color':'#0091D5'},
                                          'axis':{'range':[0,6571],
                                          'tickmode':'auto'}})
    indicator_figure.update_layout(font={'size':10,'color':'black'},
                                    width=500,height=300,
                                    paper_bgcolor='rgba(0,0,0,0)',
                                    plot_bgcolor='rgba(0,0,0,0)')
    return indicator_figure

#Choropleth map
def create_choropleth_map(df):
    df_group_by_state = df.groupby('state')['name'].agg('count').reset_index().rename(columns={'name':'count'})
    choropleth_map = go.Figure(data=go.Choropleth(
        locations = df_group_by_state['state'],
        z = df_group_by_state['count'],
        #text = df_group_by_state['text'],
        locationmode = 'USA-states',
        colorscale = 'Greens',
        colorbar_title = "Number of Deaths"
    ))
    choropleth_map.update_layout(
        #title_text = 'Police Shooting Deaths by US States',
        width=1700, height=700,
        geo_scope='usa',
        clickmode='event+select',
        margin={"r":0,"t":0,"l":0,"b":0},
        hoverlabel = dict(font=dict(size=25)),
    )
    choropleth_map.update_layout(plot_bgcolor="#d1dade",
                                margin=dict(t=0,l=80,b=0,r=40),
                                font_family="Georgia",
                                title_font_family="Georgia",
                                font_size=25,
                                dragmode=False,
                                paper_bgcolor='rgba(0,0,0,0)',
                                #plot_bgcolor='rgba(0,0,0,0)'
                                )
    return choropleth_map

def create_line_chart(df):
    df_group_by_date = df.groupby('date')['name'].agg('count').reset_index().rename(columns={'name':'count'})
    line_chart = go.Figure(data=go.Scatter(x=df_group_by_date['date'], y=df_group_by_date['count'],
                            mode='lines+markers', fill='tozeroy',
                            line={'color':'#30425e'}))
    line_chart.update_xaxes(showspikes=True, spikecolor="green", spikesnap="cursor", spikemode="across")
    line_chart.update_yaxes(showspikes=True, spikecolor="orange", spikethickness=2)
    line_chart.update_layout(showlegend=False,plot_bgcolor="#d1dade",
                            paper_bgcolor='rgba(0,0,0,0)',
                            #plot_bgcolor='rgba(0,0,0,0)',
                            margin=dict(t=0,l=80,b=0,r=40),
                            xaxis_title='Year', height=700, width=2600,
                            yaxis_title='Number of Killings',
                            font_family="Georgia",
                            title_font_family="Georgia",font_size=25,
                            hovermode='x unified')
    return line_chart

def create_line_chart_gun_data(df_gun):
    gun_data_line_chart = go.Figure(data=go.Scatter(x=df_gun['date'], y=df_gun['totals'],
                                                    fill='tozeroy',
                                                    mode='lines+markers',
                                                    line={'color':'#30425e'}))
    gun_data_line_chart.update_layout(showlegend=False,plot_bgcolor="#d1dade",
                                      paper_bgcolor='rgba(0,0,0,0)',
                                      #plot_bgcolor='rgba(0,0,0,0)',
                                      margin=dict(t=0,l=80,b=0,r=40),
                                      xaxis_title='Year', height=700, width=2600,
                                      yaxis_title='Number of Gun Purchase',
                                      font_family="Georgia", hovermode='x unified',
                                      title_font_family="Georgia",font_size=22)
    return gun_data_line_chart

def create_bar_chart_for_mental_illness(df):
    df_group_by_mental_illness = df.groupby('signs_of_mental_illness')['name'].agg('count').reset_index().rename(columns={'name':'count'})
    mental_illness_bar = px.bar(df_group_by_mental_illness, x="signs_of_mental_illness", y="count",
                            color='signs_of_mental_illness',
                            hover_data=['count'],
                            width=1400,
                            height=800,
                            orientation='v'
                            )
    mental_illness_bar.update_layout(clickmode='event+select',
                                 paper_bgcolor='rgba(0,0,0,0)',
                                 #plot_bgcolor='rgba(0,0,0,0)',
                                 plot_bgcolor="#d1dade",
                                 margin=dict(t=50,l=200,b=80,r=40),
                                 xaxis_title='Signs of Mental Illness',
                                 yaxis_title='Number of Killings',
                                 font_family="Georgia",
                                 title_font_family="Georgia",
                                 font_size=25,
                                 hovermode='x unified',
                                 xaxis_tickangle=-45)

    return mental_illness_bar


def create_radar_chart_for_weapons(df):
    df_group_by_weapon = df.groupby('armed')['name'].agg('count').reset_index().rename(columns={'name':'count'})
    df_group_by_weapon = df_group_by_weapon[df_group_by_weapon['count']>20]
    radar_chart_by_weapon = go.Figure(data=go.Scatterpolar(r=df_group_by_weapon['count'],
                                                        theta=df_group_by_weapon['armed'],
                                                        fill='toself'))

    radar_chart_by_weapon.update_layout(width=1400, height=900, font_size=30,
                                        paper_bgcolor='rgba(0,0,0,0)',
                                        #plot_bgcolor='rgba(0,0,0,0)',
                                        margin=dict(t=50,l=200,b=80,r=40), hovermode='x unified',
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
                            paper_bgcolor='rgba(0,0,0,0)',
                            #plot_bgcolor='rgba(0,0,0,0)',
                            margin=dict(t=50,l=200,b=80,r=40),
                            xaxis={'categoryorder':'total descending'},
                            xaxis_title='Race', hovermode='x unified',
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
    stacked_bar.update_layout(showlegend=True,plot_bgcolor="#d1dade",
                              paper_bgcolor='rgba(0,0,0,0)',
                              #plot_bgcolor='rgba(0,0,0,0)',
                              margin=dict(t=50,l=200,b=0,r=40),
                              xaxis_title='Age and Gender',
                              yaxis_title='Number of Killings',
                              font_family="Georgia",
                              hoverlabel = dict(font=dict(size=40)),
                              title_font_family="Georgia",font_size=25,
                              xaxis_tickangle=-45)
    return stacked_bar

#Sankey Diagram
def generateSankey(df,cat_cols=[],value_cols='',title='Sankey Diagram'):
    colorPalette = ['#be584b','#6dad23','#FFE873','#5e49eb','#646464','#2a6147']
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
            color = "green",
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
    fig.update_traces(customdata=['Race','Age','Gender','Threat Level','Fleeing'])

    fig.update_layout(title_text='Race\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t \
                                  Age \t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t \
                                  Gender\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t \
                                  Threat Level\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t \
                                  Fleeing',
                      width=2800, height=900,
                      plot_bgcolor="#d1dade",
                      hoverlabel = dict(font=dict(size=20)),
                      margin=dict(t=70,l=100,b=20,r=100),
                      #paper_bgcolor='rgba(0,0,0,0)',
                      #plot_bgcolor='rgba(0,0,0,0)',
                      font_family="Georgia",
                      title_font_family="Georgia",font_size=28)
    return fig

def create_sankey_diagram(df):
    df_grouped_sankey = df.groupby(['race','age_bins','gender','signs_of_mental_illness','threat_level','flee'])['name'].agg('count').reset_index().rename(columns={'name':'count'})
    sankey_diagram = generateSankey(df_grouped_sankey,
                               ['race','age_bins','gender','signs_of_mental_illness','threat_level','flee'],
                               value_cols='count',
                               )

    return sankey_diagram
