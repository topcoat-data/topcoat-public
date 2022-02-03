from pandas.core.frame import DataFrame
import plotly.graph_objects as go

from common.plugin.visualization import BooleanOption, InputOption, SelectOption, VisualizationConfig, register


def render(source: DataFrame, config: VisualizationConfig):

    data = []
    for measure in config.measures:
        series = go.Bar(x=source[config.dimensions[0].id_or_name], y=source[measure.id_or_name])
        data.append(series)

    fig = go.Figure(
        data=data
    )

    margin = {
      'l': 60,
      'r': 60,
      'b': 60,
      't': 20
    }
    fig.update_layout(margin = margin, yaxis_gridcolor="lightgray", plot_bgcolor='rgba(0,0,0,0)')

    barmode = config.options['bar_mode']
    fig.update_layout(barmode=barmode)

    hide_axes = config.options['hide_axes']
    if hide_axes:
        fig.update_layout(xaxis_visible=False, xaxis_showticklabels=False,
                          yaxis_visible=False, yaxis_showticklabels=False)

    return fig


register(
    key=__name__,
    options={
        'hide_axes': BooleanOption(
            attachment='visualization',
            default=True,
            label='Hide Axes',
            description='Indictes whether to hide chart axes',
            section='Formatting'
        ),
        'bar_mode': SelectOption(
            attachment='visualization',
            default='stack',
            label='Bar Mode',
            description='Indictes the bar mode',
            values=[
                {'stack': 'Stacked bars'},
                {'group': 'Grouped bars'}
            ],
            section='Formatting'
        )
    },
    render=render
)
