import pandas as pd
import plotly.express as px
import plotly.graph_objects as go

def get_age_and_gender(stackBarClick):
    gender_id = stackBarClick['points'][0]['curveNumber']
    if gender_id==0:
        gender='Female'
    else:
        gender='Male'

    age = stackBarClick['points'][0]['x']
    return gender, age

def indicator_graph(number):
    indicator_figure = go.Figure(go.Indicator(
    mode = "gauge+number",
    value = number,
    number = {'prefix': ""},
    visible=True))
    indicator_figure.update_traces(gauge={'bordercolor':'black', 'borderwidth':10,
                                          'bar':{'color':'#0091D5'},
                                          'axis':{'range':[0,6570],
                                          'tickmode':'auto'}})
    indicator_figure.update_layout(font={'size':5,'color':'black'})
    return indicator_figure

#Choropleth map
def create_choropleth_map(df):
    df_group_by_state = df.groupby('state')['name'].agg('count').reset_index().rename(columns={'name':'count'})
    choropleth_map = go.Figure(data=go.Choropleth(
        locations=df_group_by_state['state'],
        z = df_group_by_state['count'],
        locationmode = 'USA-states',
        colorscale = 'Portland',
        colorbar_title = "Number of Deaths"
    ))
    choropleth_map.update_layout(
        #title_text = 'Police Shooting Deaths by US States',
        geo_scope='usa',
        clickmode='event+select',
        margin={"r":0,"t":0,"l":0,"b":0}
    )
    choropleth_map.update_layout(plot_bgcolor="#d1dade",margin=dict(t=0,l=80,b=0,r=40),
                            font_family="Georgia",
                            title_font_family="Georgia",font_size=20)
    return choropleth_map

def create_line_chart(df):
    df_group_by_date = df.groupby('date')['name'].agg('count').reset_index().rename(columns={'name':'count'})
    line_chart = go.Figure(data=go.Scatter(x=df_group_by_date['date'], y=df_group_by_date['count'], mode='lines',
                            line={'color':'#AC3E31'}))
    line_chart.update_layout(showlegend=False,plot_bgcolor="#d1dade",margin=dict(t=0,l=80,b=0,r=40),
                            xaxis_title='Year',
                            yaxis_title='Number of Killings',
                            font_family="Georgia",
                            title_font_family="Georgia",font_size=22)
    return line_chart

def create_line_chart_gun_data(df_gun):
    gun_data_line_chart = go.Figure(data=go.Scatter(x=df_gun['date'], y=df_gun['totals'], line={'color':'#AC3E31'}))
    gun_data_line_chart.update_layout(showlegend=False,plot_bgcolor="#d1dade",margin=dict(t=0,l=80,b=0,r=40),
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
    pie_chart.update_layout(showlegend=False, plot_bgcolor="#d1dade",margin=dict(t=0,l=80,b=0,r=40),
                            font_family="Georgia",
                            title_font_family="Georgia",font_size=22)
    pie_chart.update_layout(margin=dict(t=0, b=0, l=0, r=0))
    return pie_chart

#stacked bar chart
def create_stacked_bar_chart(df):
    df_group_by_age_gender = df.groupby(['age_bins','gender'])['name'].agg('count').reset_index().rename(columns={'name':'count'})
    stacked_bar = px.bar(df_group_by_age_gender, x="age_bins", y="count", color="gender",
            hover_data=['count'], barmode = 'stack', custom_data=['gender'])
    stacked_bar.update_layout(clickmode='event+select',
                              margin={"r":0,"t":0,"l":0,"b":0})
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


def blank_fig(height):
    """
    Build blank figure with the requested height
    """
    return {
        "data": [],
        "layout": {
            "height": height,
            "xaxis": {"visible": False},
            "yaxis": {"visible": False},
        },
    }
