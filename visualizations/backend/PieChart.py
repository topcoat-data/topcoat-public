from pandas.core.frame import DataFrame
from common.plugin.visualization import BooleanOption, SelectOption, InputOption, NumericOption, ColorOption, ColorPaletteOption, VisualizationConfig, register
import pandas as pd
import math
from plotly.subplots import make_subplots
import plotly.graph_objects as go

default_colors=['#636EFA', '#EF553B', '#00CC96', '#AB63FA', '#FFA15A', '#19D3F3', '#FF6692', '#B6E880', '#FF97FF', '#FECB52']



def fill_series(series, needed_length):
    grp_count = needed_length // len(series)
    reminder = needed_length % len(series)
    needed_series=[]
    for _ in range(grp_count):
        needed_series = needed_series + series
    needed_series = needed_series + series[:reminder]
    return needed_series


def hex_to_rgb(value):
        """Convert Colors from Hexadecimal to RGB"""
        value = value.lstrip('#')
        lv = len(value)
        return tuple(int(value[i:i + lv // 3], 16) for i in range(0, lv, lv // 3))

def is_float(value):
    try:
        float(value)
        return True
    except ValueError:
        return False

def render(source: DataFrame, config: VisualizationConfig):
    colors = fill_series(default_colors,len(source))
    seriesColors=[]
    if 'seriesColors' in config.options:
        seriesColors = config.options['seriesColors']
        if seriesColors:
            seriesColors = fill_series(seriesColors,len(source))
        else:
            seriesColors=colors
    rows = math.ceil(len(config.measures)/2)
    specs=[]
    pieChartType = config.options['pieChartType']
    for r in range(rows):
        row=[]
        for c in range(2):
            row.append({'type':'domain'})
        specs.append(row)
    fig = make_subplots(rows=rows, cols=2, specs=specs,subplot_titles = ['temp_subtitle' for _ in range(len(config.measures))])
    labels = source[config.dimensions[0].id_or_name]
    innerRadius = float(config.options['innerRadius'])
    data=[]
    r=1
    c=1
    m=0
    for measure in config.measures:
        values = source[measure.id_or_name]
        valueFormat = measure.options['valueFormat'] if "valueFormat" in measure.options else ""
        source[measure.id_or_name+"_percentage"] = (source[measure.id_or_name] / source[measure.id_or_name].sum()) * 100
        print(valueFormat)
        source[measure.id_or_name+"_percentage_formatted"] = source[measure.id_or_name+"_percentage"].apply(valueFormat.format) if valueFormat != "" and "%"  in valueFormat else source[measure.id_or_name].apply(valueFormat.format) if valueFormat != "" and "%"  not in valueFormat else  source[measure.id_or_name+"_percentage"].apply('{:.2f}%'.format)
        data_labels = source[config.dimensions[0].id_or_name] + " <br> "+ source[measure.id_or_name+"_percentage_formatted"]
        seriesName = measure.options['seriesName'] if "seriesName" in measure.options else measure.id_or_name
        print(fig.layout.annotations)
        fig.layout.annotations[m]['text'] = seriesName

        m+=1
        if pieChartType == "Full":
            series = go.Pie(
                labels=labels,
                values=values,
                text=data_labels,
                textinfo ="text",
                hoverinfo ="text",
                insidetextorientation='radial',
                name=seriesName,
                hole=innerRadius,
                marker={
                    'colors':seriesColors
                }
            )
        else:
            vals= pd.concat([pd.Series([values.sum()]), values])
            labs = pd.concat([pd.Series([" "]), labels])

            data_labels = pd.concat([pd.Series([" "]), data_labels])
            print(data_labels)
            colors = ['rgb(255, 255, 255)'] + default_colors
            series = go.Pie(
                labels=labs,
                values=vals,
                insidetextorientation='radial',
                name=seriesName,
                hole=innerRadius,
                domain={"x": [0, 0.48]},
                direction="clockwise",
                rotation= 90,
                text=data_labels,
                textinfo ="text",
                hoverinfo ="text",
                marker={
                    'colors': colors
                }
            )
        fig.add_trace(series,r, c)
        if c == 2:
            c=1
            r+=1
        else:
            c+=1

    margin = {
        'l': 20,
        'r': 20,
        'b': 20,
        't': 20
    }
    # set show legend configuration
    showlegend = config.options['showLegend']
    # set legend Position configuration
    legendPosition = config.options['legendPosition']
    legend={}
    if legendPosition == "left":
        legend=dict(
            yanchor="top",
            y=1,
            xanchor="left",
            x=-0.5
        )
    if legendPosition == "center":
        legend=dict(
            yanchor="top",
            y=1,
            xanchor="center",
            x=0.5
        )
    if legendPosition == "right":
        legend=dict(
            yanchor="top",
            y=1,
            xanchor="right",
            x=1.5
        )
    if config.options['fontFamily'] != "auto":
        fig.update_layout(font_family=config.options['fontFamily'])
    if config.options['fontColor'] != "auto":
        fig.update_layout(font_color='rgb'+str(hex_to_rgb(config.options['fontColor'])))
    fig.update_layout(
        title=config.options['title'],
        margin = margin,
        plot_bgcolor = 'rgba(0,0,0,0)',
        showlegend=showlegend,
        legend=legend
    )
    return fig

register(
    key=__name__,
    options={
        'seriesColors': ColorPaletteOption(
            attachment='visualization',
            default=None,
            label='Series Colors',
            description='Accepts an array of color values for the bars, lines or points. Colors will be used for each series in order. If the number of measures exceeds the number of colors available, the colors repeat from the beginning of the array. Individual series values can be overwritten.',
            section='Colors'
        ),
        'pieChartType': SelectOption(
            attachment='visualization',
            default='Full',
            label='Pie Chart Type',
            description='Show the pie chart as full or half circle.',
            values=[
                { 'Full' : 'Full'},
                { 'Half' : 'Half'}
            ],
            section='Polygon'
        ),
        'fontColor': ColorOption(
            attachment='visualization',
            default='auto',
            label='Font Color',
            description='Sets the font color for all text shown on the chart',
            section='Font'
        ),

        'fontFamily': SelectOption(
            attachment='visualization',
            default='auto',
            label='Font Family',
            description='Sets the font for all text shown on the chart',
            values=[
                { 'auto' : 'auto'},
                { 'Courier New' : 'Courier New'},
                {'Times New Roman':'Times New Roman'}
            ],
            section='Font'
        ),
        'valueFormat': InputOption(
            attachment='column',
            default='inherit',
            label='Value Format',
            description='Accepts python string formatting to set the series value format (such as dates, currency, percent, etc.)',
            section='Formatting'
        ),
        'innerRadius': NumericOption(
            attachment='visualization',
            default='0',
            min=-1,
            max=1,
            label='Inner Radius',
            description='Allows for the visualization as a donut chart. When set to 0, this will display as a pie chart. Accepts values 0-99, representing the percentage of the chart\'s total diameter that the center hole should consume.',
            section='Polygon'
        ),
        'seriesName': InputOption(
            attachment='column',
            default=None,
            label='Series Name',
            description='Accepts python string formatting to set the series name. For tables, this is the column name. For other charts, this impacts what can be shown on legend, label or hover.',
            section='Formatting'
        ),
        'title': InputOption(
            attachment='visualization',
            default=None,
            label='Title',
            description='Accepts any string value to use as the display title of the chart on a page',
            section='General'
        ),

        'legendPosition': SelectOption(
            attachment='visualization',
            default='center',
            label='Legend Position',
            description='If showLegend is set to true, defines where the legend displays along the base of the chart.',
            values=[
                { 'left' : 'left'},
                { 'center' : 'center'},
                { 'right' : 'right'}
            ],
            section='Legend'
        ),
        'showLegend': BooleanOption(
            attachment='visualization',
            default=False,
            label='Show Legend',
            description='When set to true, the legend is displayed with the visualization',
            section='Legend'
        )
    },
    render=render
)
