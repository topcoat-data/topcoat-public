from turtle import color
from pandas.core.frame import DataFrame
import altair as alt

from common.plugin.visualization import BooleanOption, SelectOption, InputOption, NumericOption, ColorOption, ColorPaletteOption, VisualizationConfig, register
import pandas as pd
default_colors=['#636EFA', '#EF553B', '#00CC96', '#AB63FA', '#FFA15A', '#19D3F3', '#FF6692', '#B6E880', '#FF97FF', '#FECB52']

def render(source: DataFrame, config: VisualizationConfig):
    df = source.melt(config.dimensions[0].id_or_name,var_name='measures', value_name='y')
    main_chart = alt.Chart(df).mark_bar().encode(
        x='y',
        y=config.dimensions[0].id_or_name,
        row="measures",
        color='measures:N'
    ).properties(
        height=200,
        width=100
    )
    #source[config.measures[0].id_or_name+'_label'] =[config.measures[0].id_or_name]*len(source)
    #main_chart = alt.Chart(source).mark_bar(opacity=1,color=default_colors[0], cornerRadius=5).encode(
    #    alt.X(config.dimensions[0].id_or_name, axis=alt.Axis(grid=True, title='Animal')),
    #    alt.Y(config.measures[0].id_or_name, axis=alt.Axis(grid=True)),color=config.measures[0].id_or_name+'_label')
    #i=0
    #for measure in config.measures[1:]:
    #    source[measure.id_or_name+'_label'] =[measure.id_or_name]*len(source)
    #    i+=1
    #    main_chart = main_chart + alt.Chart(source).mark_bar(opacity=1,color=default_colors[i], cornerRadius=5).encode(alt.X(config.dimensions[0].id_or_name, axis=alt.Axis(grid=True, title='Animal')), alt.Y(measure.id_or_name, axis=alt.Axis(grid=True)),color=measure.id_or_name+'_label')
    return main_chart


register(
    key=__name__,
    options={
        'bar_corner_radius': NumericOption(
            attachment='visualization',
            default='0',
            min=0,
            max=999,
            label='Bar Corner Radius',
            description='Defines the roundness of corners of bars',
            section='Polygon'
        ),
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
            section='Axes.Y'
        ),
        'yAxisMin': InputOption(
            attachment='visualization',
            default=None,
            label='Y Axis Min',
            description='Sets the minimum value for the axis. If not specified, 0 will be used. If there are negative values, the lowest value will determine the axis min',
            section='Axes.Y'
        ),
        'showYAxis': BooleanOption(
            attachment='visualization',
            default=True,
            label='Show Y Axes',
            description='Determines if the axis line should display',
            section='Axes.Y'
        ),
        'showYGridLines': BooleanOption(
            attachment='measure',
            default=False,
            label='Show Y Grid Lines',
            description='Determines if grid lines should appear within the visualization frame. Grid lines extend from ticks.',
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
        'seriesChartType': SelectOption(
            attachment='measure',
            default='bar_chart',
            label='Series Chart Type',
            description='Allows you to include a different type of visualization within a bar chart, such as line chart',
            values=[
                { 'bar_chart' : 'bar_chart'},
                { 'line_chart' : 'line_chart'}
            ],
            section='General'
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
        'barSpacing': NumericOption(
            attachment='visualization',
            default='0.5',
            min=0,
            max=1,
            label='Bar Spacing',
            description='Defines the space between columns in a stacked bar chart or groups of columns in a grouped bar chart. Accepted values range from 0-1, with 0 meaning no spacing and 1.0 meaning max spacing.',
            section='Polygon'
        ),

        'seriesPositioning': SelectOption(
            attachment='visualization',
            default='auto',
            label='Series Positioning',
            description='Defines whether the data shows data grouped/overlayed to show a comparison, stacked, or stacked representing the total relative to the sum',
            values=[
                { 'stack' : 'stack'},
                { 'group' : 'group'},
                { 'overlay' : 'overlay'},
                { 'stack_percentage' : 'stack_percentage'}
            ],
            section='General'
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
                { ' plot' : ' plot'},
                { ' disconnect' : ' disconnect'}
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
            description='If seriesChartType is set to line_chart, defines the shape for the data points.',
            values=[
                { 'circle' : 'circle'},
                { 'square' : 'square'},
                { 'diamond' : ' diamond'},
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

