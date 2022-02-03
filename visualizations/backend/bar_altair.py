from pandas.core.frame import DataFrame
import altair as alt

from common.plugin.visualization import BooleanOption, InputOption, SelectOption, VisualizationConfig, register


def render(source: DataFrame, config: VisualizationConfig):

    chart = alt.Chart(source).mark_bar().encode(
        x='animal',
        y='lifespan'
    )
    print(chart)
    return chart


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
