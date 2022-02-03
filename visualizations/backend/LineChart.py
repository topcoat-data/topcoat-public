from pandas.core.frame import DataFrame
from common.plugin.visualization import BooleanOption, SelectOption, InputOption, NumericOption, ColorOption, ColorPaletteOption, VisualizationConfig, register
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
    fig = make_subplots(specs=[[{"secondary_y": True}]])
    show_main_y_grid=False
    orientation=config.options['orientation']
    orientation = 'v' if orientation == "vertical" else 'h'
    # options for dimension
    dim_name = config.dimensions[0].options['seriesName'] if 'seriesName' in config.dimensions[0].options else ""
    dimension = source[config.dimensions[0].id_or_name]
    colors = fill_series(default_colors,len(source))
    seriesColors=[]
    if 'seriesColors' in config.options:
        seriesColors = config.options['seriesColors']
        if seriesColors:
            seriesColors = fill_series(seriesColors,len(source))
        else:
            seriesColors=colors
    showYGridLines=config.options['showYGridLines']
    showY2GridLines=config.options['showY2GridLines']
    i=0
    for measure in config.measures:
        plotOnSecondaryAxis=measure.options['plotOnSecondaryAxis']
        seriesName = measure.options['seriesName'] if "seriesName" in measure.options else measure.id_or_name
        print(type(source[config.dimensions[0].id_or_name]))
        measure_series = source[measure.id_or_name]
        x = dimension if orientation == "v" else measure_series
        y = measure_series if orientation == "v" else dimension
        if len(seriesColors)==0:
            seriesColor = colors[i] if  measure.options['seriesColor'] == "auto" else  measure.options['seriesColor']
        else:
            seriesColor = seriesColors[i]
        connectgaps = measure.options['plotNulls'] == "connect" or measure.options['plotNulls'] == "plot"
        lineAreaFill = 'tozeroy' if orientation=="v" and measure.options['lineAreaFill'] else 'tozerox'if orientation=="h" and measure.options['lineAreaFill'] else "none"
        fillcolor = colors[i] if measure.options['lineAreaFillColor'] == "auto" else measure.options['lineAreaFillColor']
        marker_color = seriesColor if measure.options['pointColor'] == "auto" else measure.options['pointColor']
        lineColor = seriesColor if measure.options['lineColor'] == "auto" else measure.options['lineColor']
        line= dict(
        shape = measure.options['lineShape'],
        width = float(measure.options['lineSize']),
        smoothing = float(measure.options['splineAmount']),
        color = lineColor
        )
        if measure.options['pointShape'] == "no_point":
            #in case user choose no point the marker should set be 0 to not be shown
            marker=dict(
                size = 0
            )
        else:
            # setting shape, size, and color of marker here
            marker=dict(
                symbol = measure.options['pointShape'],
                size = float(measure.options['pointSize']),
                color = marker_color
            )
            # to set marker style there are 2 option 1) Filled 2) Outlined
            if measure.options['pointStyle'] == 'outlined':
                #if the choice is outlined it should set the marker's borders color and size and set marker's background to white
                marker["color"] = 'white'
                marker['line']=dict(
                    width=3,
                    color = marker_color
                )

        line_trace = go.Scatter(x=x, y=y,line=line,name=seriesName,connectgaps=connectgaps,fill=lineAreaFill,fillcolor=fillcolor,marker=marker)
        fig.add_trace(line_trace,secondary_y=plotOnSecondaryAxis)

        i+=1

        if plotOnSecondaryAxis:
            # set range(min,max) on secondary y axis configurations
            y2AxisMax = config.options['y2AxisMax']
            y2AxisMin = config.options['y2AxisMin']
            y2_range=[y2AxisMin,y2AxisMax]
            # set secondary y axis scale type configuration
            y2AxisScaleType = config.options['y2AxisScaleType']
            y2AxisScaleType = "-" if y2AxisScaleType == "auto" else "date" if y2AxisScaleType == "datetime" else "category" if y2AxisScaleType == "ordinal" else "linear"
            # set visibility of secondary y axis tick text configuration
            y2AxisShowTickText = config.options['y2AxisShowTickText']
            # set secondary y axis tick text angle configuration
            y2AxisTickTextAngle = config.options['y2AxisTickTextAngle']
            y2_tick_angle = 0 if y2AxisTickTextAngle == "horizontal" else -45 if y2AxisTickTextAngle == "angled" else -90
            # set y2 axis tick interval configuration
            y2AxisTickTextInterval = config.options['y2AxisTickTextInterval']
            # set secondary y axis tick format configuration
            y2AxisTickFormat = config.options['y2AxisTickFormat']
            # set y axis label configuration
            y2AxisTitle = config.options['y2AxisTitle']
            fig.update_yaxes(
                range=y2_range,
                type=y2AxisScaleType,
                showticklabels=y2AxisShowTickText,
                tickangle=y2_tick_angle,
                dtick=y2AxisTickTextInterval,
                title=y2AxisTitle,
                tickformat=y2AxisTickFormat,
                secondary_y= True
            )

    margin = {
        'l': 60,
        'r': 60,
        'b': 60,
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
            x=0.01
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
            x=1.2
        )
    # set grid line color configuration
    gridLineColor = config.options['gridLineColor']
    print(gridLineColor)
    #if the color in hexa format convert it to rgb else set the color by its name
    try:
        rgb= hex_to_rgb(gridLineColor)
        gridcolor= 'rgb'+str(rgb)
    except Exception as e:
        print(str(e))
        gridcolor= gridLineColor
    # set visibility of x axis configuration
    showXAxis = config.options['showXAxis']
    # set show x axis grid line configuration
    showXGridLines = config.options["showXGridLines"]
    # set range (min,max) for x axis configuration
    xAxisMax = config.options["xAxisMax"]
    xAxisMin = config.options["xAxisMin"]
    x_range=[xAxisMin,xAxisMax]
    # set x axis scale type configuration
    xAxisScaleType= config.options['xAxisScaleType']
    xAxisScaleType = "-" if xAxisScaleType == "auto"  else "date" if xAxisScaleType == "datetime" else "category" if xAxisScaleType == "ordinal" else "linear"
    # set show x axis tick text configuration
    xAxisShowTickText = config.options['xAxisShowTickText']
    # set x axis tick text angle configuration
    xAxisTickTextAngle = config.options['xAxisTickTextAngle']
    x_tick_angle = 0 if xAxisTickTextAngle == "horizontal" else -45 if xAxisTickTextAngle == "angled" else -90
    # set x axis tick interval configuration
    xAxisTickTextInterval = config.options['xAxisTickTextInterval']
    # set x axis tick format configuration
    xAxisTickFormat = config.options['xAxisTickFormat']
    # set x axis label configuration
    xAxisTitle = config.options['xAxisTitle'] if config.options['xAxisTitle'] and config.options['xAxisTitle'] != ""  else "" if  orientation == "h" else dim_name
    print("xAxisTitle = "+xAxisTitle)
    # set range(min,max) for y axis configuration
    yAxisMax = config.options["yAxisMax"]
    yAxisMin = config.options["yAxisMin"]
    y_range = [yAxisMin,yAxisMax]
    # set visibility of y axis configuration
    showYAxis = config.options['showYAxis']
    # set y axis scale type configuration
    yAxisScaleType = config.options['yAxisScaleType']
    yAxisScaleType = "-" if yAxisScaleType == "auto" else "date" if yAxisScaleType == "datetime" else "category" if yAxisScaleType == "ordinal" else "linear"
    # set visibility of y axis tick text configuration
    yAxisShowTickText = config.options['yAxisShowTickText']
    # set visibility of y axis tick text configuration
    yAxisShowTickText = config.options['yAxisShowTickText']
    # set y axis tick text angle configuration
    yAxisTickTextAngle = config.options['yAxisTickTextAngle']
    y_tick_angle = 0 if yAxisTickTextAngle == "horizontal" else -45 if yAxisTickTextAngle == "angled" else -90
    # set y axis tick interval configuration
    yAxisTickTextInterval = config.options['yAxisTickTextInterval']
    # set y axis tick format configuration
    yAxisTickFormat = config.options['yAxisTickFormat']
    # set y axis label configuration
    yAxisTitle = config.options['yAxisTitle']
    yAxisTitle = config.options['yAxisTitle'] if config.options['yAxisTitle'] and config.options['yAxisTitle'] != ""  else "" if  config.options['yAxisTitle'] == "" and orientation == "v" else dim_name
    if config.options['fontFamily'] != "auto":
        fig.update_layout(font_family=config.options['fontFamily'])
    if config.options['fontColor'] != "auto":
        fig.update_layout(font_color='rgb'+str(hex_to_rgb(config.options['fontColor'])))
    fig.update_layout(
        title=config.options['title'],
        margin = margin,
        plot_bgcolor = 'rgba(0,0,0,0)',
        xaxis_visible = showXAxis,
        xaxis_showticklabels = showXAxis,
        yaxis_visible = showYAxis,
        showlegend=showlegend,
        legend=legend,
        yaxis_showticklabels = showYAxis
    )
    fig.update_xaxes(
        gridwidth = 1,
        gridcolor = gridcolor,
        showgrid = showXGridLines,
        range = x_range,
        type = xAxisScaleType,
        showticklabels = xAxisShowTickText,
        tickangle = x_tick_angle,
        dtick = xAxisTickTextInterval,
        tickformat=xAxisTickFormat,
        title = xAxisTitle,
    )
    fig.update_yaxes(
        gridwidth = 1,
        gridcolor = gridcolor,
        range = y_range,
        type = yAxisScaleType,
        showticklabels = yAxisShowTickText,
        tickangle = y_tick_angle,
        dtick = yAxisTickTextInterval,
        tickformat=yAxisTickFormat,
        title = yAxisTitle,
        showgrid=showYGridLines,
        secondary_y = False
    )
    fig.update_yaxes(
        visible=True,
        showgrid=showY2GridLines,
        gridcolor = gridcolor,
        secondary_y = True
    )

    return fig


register(
    key=__name__,
    options={

        'gridLineColor': ColorOption(
            attachment='visualization',
            default='grey',
            label='Grid Line Color',
            description='If grid lines are displayed, set the grid line color',
            section='Axes'
        ),
        'plotOnSecondaryAxis': BooleanOption(
            attachment='measure',
            default=False,
            label='Plot on Secondary Axis',
            description='If set to true, the data from this series will be populated on the right axis',
            section='Axes'
        ),
        'showXAxis': BooleanOption(
            attachment='visualization',
            default=True,
            label='Show X Axes',
            description='Determines if the axis line should display',
            section='Axes.X'
        ),
        'showXGridLines': BooleanOption(
            attachment='visualization',
            default=False,
            label='Show X Grid Lines',
            description='Determines if grid lines should appear within the visualization frame. Grid lines extend from ticks.',
            section='Axes.X'
        ),
        'xAxisMax': InputOption(
            attachment='visualization',
            default=None,
            label='X Axis Max',
            description='Sets the maxium value for the axis. If not specified, the maximum value will determine the axis max. Date values are also accepted',
            section='Axes.X'
        ),
        'xAxisMin': InputOption(
            attachment='visualization',
            default=None,
            label='X Axis Min',
            description='Sets the minimum value for the axis. If not specified, 0 will be used. If there are negative values, the lowest value will determine the axis min. Date values are also accepted',
            section='Axes.X'
        ),

        'xAxisScaleType': SelectOption(
            attachment='visualization',
            default='auto',
            label='X Axis Scale Type',
            description='Determines the scale of the axis. If not specified, this is auto-detected based on the data',
            values=[
                { 'auto' : 'auto'},
                { 'datetime' : 'datetime'},
                { 'ordinal' : 'ordinal'},
                { 'numeric' : 'numeric'}
            ],
            section='Axes.X'
        ),
        'xAxisShowTickText': BooleanOption(
            attachment='visualization',
            default=True,
            label='X Axis Show Tick Marks',
            description='Determines if tick text should display on axis',
            section='Axes.X'
        ),

        'xAxisTickTextAngle': SelectOption(
            attachment='visualization',
            default='horizontal',
            label='X Axis Tick Texk Angle',
            description='Defines the orientation of the text along ticks on the axis',
            values=[
                { 'horizontal' : 'horizontal'},
                { 'angled' : 'angled'},
                { 'vertical' : 'vertical'}
            ],
            section='Axes.X'
        ),
        'xAxisTickTextInterval': InputOption(
            attachment='visualization',
            default=None,
            label='X Axis Tick Text Interval',
            description='For numerical or datetime values, this defines the interval for tick text along the axis. Gridlines will come from these intervals. If the axis scale is datetime, defines the interval for text along ticks in python date formatting',
            section='Axes.X'
        ),
        'xAxisTickFormat': InputOption(
            attachment='visualization',
            default='',
            label='Ticks Format',
            description='Accepts string d3 formatting to set x axis ticks format (such as dates, currency, percent, etc.) for dates formatting please view: https://github.com/d3/d3-time-format/tree/v2.2.3#locale_format , for numbers formating please review: https://github.com/d3/d3-format/tree/v1.4.5#d3-format',
            section='Axes.X'
        ),
        'xAxisTitle': InputOption(
            attachment='visualization',
            default=None,
            label='X Axis Label',
            description='Defines the title for the axis. If not set, no title will show.',
            section='Axes.X'
        ),
        'yAxisMax': InputOption(
            attachment='visualization',
            default=None,
            label='Y Axis Max',
            description='Sets the maxium value for the axis. If not specified, the maximum value will determine the axis max',
            section='Axes.X'
        ),
        'showYAxis': BooleanOption(
            attachment='visualization',
            default=True,
            label='Show Y Axes',
            description='Determines if the axis line should display',
            section='Axes.Y'
        ),
        'showYGridLines': BooleanOption(
            attachment='visualization',
            default=False,
            label='Show Y Grid Lines',
            description='Determines if grid lines should appear within the visualization frame. Grid lines extend from ticks.',
            section='Axes.Y'
        ),
        'yAxisMin': InputOption(
            attachment='visualization',
            default=None,
            label='Y Axis Min',
            description='Sets the minimum value for the axis. If not specified, 0 will be used. If there are negative values, the lowest value will determine the axis min',
            section='Axes.Y'
        ),

        'yAxisScaleType': SelectOption(
            attachment='visualization',
            default='auto',
            label='Y Axis Scale Type',
            description='Determines the scale of the axis',
            values=[
                { 'auto' : 'auto'},
                { 'datetime' : 'datetime'},
                { 'ordinal' : 'ordinal'},
                { 'numeric' : 'numeric'}
            ],
            section='Axes.Y'
        ),
        'yAxisShowTickText': BooleanOption(
            attachment='visualization',
            default=True,
            label='Y Axis Show Tick Marks',
            description='Determines if tick text should display on axis',
            section='Axes.Y'
        ),

        'yAxisTickTextAngle': SelectOption(
            attachment='visualization',
            default='horizontal',
            label='Y Axis Tick Text Angle',
            description='This defines the interval for tick text along the axis. Gridlines will come from these intervals.',
            values=[
                { 'horizontal' : 'horizontal'},
                { 'angled' : 'angled'},
                { 'vertical' : 'vertical'}
            ],
            section='Axes.Y'
        ),
        'yAxisTickTextInterval': InputOption(
            attachment='visualization',
            default=None,
            label='Y Axis Tick Text Interval',
            description='If the y axis scale is ordinal, defines the interval for text along ticks',
            section='Axes.Y'
        ),
        'yAxisTickFormat': InputOption(
            attachment='visualization',
            default='',
            label='Ticks Format',
            description='Accepts string d3 formatting to set y axis ticks format (such as dates, currency, percent, etc.) for dates formatting please view: https://github.com/d3/d3-time-format/tree/v2.2.3#locale_format , for numbers formating please review: https://github.com/d3/d3-format/tree/v1.4.5#d3-format',
            section='Axes.Y'
        ),
        'yAxisTitle': InputOption(
            attachment='visualization',
            default=None,
            label='Y Axis Label',
            description='Defines the title for the axis. If not set, no title will show.',
            section='Axes.Y'
        ),
        'y2AxisMax': InputOption(
            attachment='visualization',
            default=None,
            label='Y2 Axis Max',
            description='Sets the maxium value for the axis. If not specified, the maximum value will determine the axis max',
            section='Axes.Y2'
        ),
        'y2AxisMin': InputOption(
            attachment='visualization',
            default=None,
            label='Y2 Axis Min',
            description='Sets the minimum value for the axis. If not specified, 0 will be used. If there are negative values, the lowest value will determine the axis min',
            section='Axes.Y2'
        ),
        'showY2GridLines': BooleanOption(
            attachment='visualization',
            default=False,
            label='Show Secondary Y Grid Lines',
            description='Determines if grid lines should appear within the visualization frame. Grid lines extend from ticks.',
            section='Axes.Y2'
        ),
        'y2AxisScaleType': SelectOption(
            attachment='visualization',
            default='auto',
            label='Y2 Axis Scale Type',
            description='Determines the scale of the axis',
            values=[
                { 'auto' : 'auto'},
                { 'datetime' : 'datetime'},
                { 'ordinal' : 'ordinal'},
                { 'numeric' : 'numeric'}
            ],
            section='Axes.Y2'
        ),
        'y2AxisShowTickText': BooleanOption(
            attachment='visualization',
            default=True,
            label='Y2 Axis Show Tick Marks',
            description='Determines if tick text should display on axis',
            section='Axes.Y2'
        ),

        'y2AxisTickTextAngle': SelectOption(
            attachment='visualization',
            default='horizontal',
            label='Y2 Axis Tick Text Angle',
            description='This defines the interval for tick text along the axis. Gridlines will come from these intervals.',
            values=[
                { 'horizontal' : 'horizontal'},
                { 'angled' : 'angled'},
                { 'vertical' : 'vertical'}
            ],
            section='Axes.Y2'
        ),
        'y2AxisTickTextInterval': InputOption(
            attachment='visualization',
            default=None,
            label='Y2 Axis Tick Text Interval',
            description='If the y axis scale is ordinal, defines the interval for text along ticks',
            section='Axes.Y2'
        ),
        'y2AxisTickFormat': InputOption(
            attachment='visualization',
            default='',
            label='Ticks Format',
            description='Accepts string d3 formatting to set secondary y axis ticks format (such as dates, currency, percent, etc.) for dates formatting please view: https://github.com/d3/d3-time-format/tree/v2.2.3#locale_format , for numbers formating please review: https://github.com/d3/d3-format/tree/v1.4.5#d3-format',
            section='Axes.Y2'
        ),
        'y2AxisTitle': InputOption(
            attachment='visualization',
            default=None,
            label='Y2 Axis Label',
            description='Defines the title for the axis. If not set, no title will show.',
            section='Axes.Y2'
        ),

        'seriesColor': ColorOption(
            attachment='measure',
            default='auto',
            label='Series color',
            description='Defines the color value for the series',
            section='Colors'
        ),

        'seriesColors': ColorPaletteOption(
            attachment='visualization',
            default=None,
            label='Series Colors',
            description='Accepts an array of color values for the bars, lines or points. Colors will be used for each series in order. If the number of measures exceeds the number of colors available, the colors repeat from the beginning of the array. Individual series values can be overwritten.',
            section='Colors'
        ),

        'lineColor': ColorOption(
            attachment='measure',
            default='auto',
            label='Line Color',
            description='Defines the line color',
            section='Colors'
        ),

        'lineAreaFillColor': ColorOption(
            attachment='measure',
            default='auto',
            label='Line Area Fill Color',
            description='Defines the fill color',
            section='Fill'
        ),
        'lineAreaFill': BooleanOption(
            attachment='measure',
            default=False,
            label='Line Area Fill Type',
            description='If set to true, the area within the line will be filled. If set to false, there will be no area shading.',
            section='Fill'
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
                {'auto':'auto'},
                { 'Courier New' : 'Courier New'},
                {'Times New Roman':'Times New Roman'}
            ],
            section='Font'
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

        'orientation': SelectOption(
            attachment='visualization',
            default='vertical',
            label='Orientation',
            description='Defines the direction of the bars or lines as vertical or horizontal',
            values=[
                { 'vertical' : 'vertical'},
                { 'horizontal' : 'horizontal'}
            ],
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
        ),
        'lineSize': NumericOption(
            attachment='measure',
            default='2',
            min=0,
            max=10,
            label='Line Size',
            description='Defines the width of the line. If set to zero, no line will be displayed.',
            section='Line'
        ),

        'plotNulls': SelectOption(
            attachment='measure',
            default='plot',
            label='Plot Nulls',
            description='If lineSize is not set to zero, this setting determines how to handle null values. When "connect" is select, the line contiues to next point when there is a null value. When "plot" is selected", null values are plotted on the zero line and the line connects through them. When "disconnect" is selected, the line does not connect across the null values.',
            values=[
                { 'connect' : 'connect'},
                { 'plot' : 'plot'},
                { 'disconnect' : 'disconnect'}
            ],
            section='Line'
        ),
        'splineAmount': NumericOption(
            attachment='measure',
            default='1',
            min=0,
            max=1.3,
            label='Spline Amount',
            description='Defines the amount of curve in the line',
            section='Line'
        ),

        'lineShape': SelectOption(
            attachment='measure',
            default='linear',
            label='Line Shape',
            description='Determines the shape of the line between points. Linear forms straight lines and spline forms curved lines. The remaining values correspond to step function shapes.',
            values=[
                { 'linear' : 'linear'},
                { 'spline' : 'spline'},
                { 'hv' : 'hv'},
                { 'vh' : 'vh'},
                { 'hvh' : 'hvh'},
                { 'vhv' : 'vhv'}
            ],
            section='Line'
        ),

        'pointColor': ColorOption(
            attachment='measure',
            default='auto',
            label='Point Color',
            description='Defines the the point color',
            section='Point'
        ),
        'pointSize': NumericOption(
            attachment='measure',
            default='2',
            min=0,
            max=10,
            label='Point Size',
            description='Defines the point size. If set to zero, no point will be displayed.',
            section='Point'
        ),

        'pointShape': SelectOption(
            attachment='measure',
            default='circle',
            label='Series Point Shape',
            description='If series_chart_type is set to line_chart, defines the shape for the data points.',
            values=[
                { 'circle' : 'circle'},
                { 'square' : 'square'},
                { 'diamond' : 'diamond'},
                { 'triangle-down' : 'triangle-down'},
                { 'triangle-up' : 'triangle-up'},
                { 'no_point' : 'no_point'}
            ],
            section='Point'
        ),

        'pointStyle': SelectOption(
            attachment='measure',
            default='filled',
            label='Series Point Style',
            description='Defines the style for the data point shape.',
            values=[
                { 'filled' : 'filled'},
                { 'outlined' : 'outlined'}
            ],
            section='Point'
        )
    },
    render=render
)
