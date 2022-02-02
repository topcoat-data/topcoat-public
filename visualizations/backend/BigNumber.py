from pandas.core.frame import DataFrame
from common.plugin.visualization import BooleanOption, SelectOption, InputOption, NumericOption, ColorOption, ColorPaletteOption, VisualizationConfig

def render(source: DataFrame, config: VisualizationConfig):
    return 'Test'

register(
    key=__name__,
    options={
        'comparison_format': InputOption(
            attachment='visualization',
            default=None,
            label='Comparison Format',
            description='Accepts python string formatting to set the comparison value format (such as dates, currency, percent, etc.)',
            section='Comparison'
        ),
        'comparison_label': InputOption(
            attachment='visualization',
            default='auto',
            label='Comparison Label',
            description='Accepts python string formatting to set the label next to the comparison number.',
            section='Comparison'
        ),
        'number_format': InputOption(
            attachment='visualization',
            default=None,
            label='Number Format',
            description='Accepts python string formatting to set the number value format (such as dates, currency, percent, etc.)',
            section='Formatting'
        ),
        'number_label': InputOption(
            attachment='visualization',
            default='auto',
            label='Number Label',
            description='Accepts python string formatting to set the label below the number.',
            section='Formatting'
        ),
        'positive_values_bad': BooleanOption(
            attachment='visualization',
            default=False,
            label='Positive Values Bad',
            description='If set to true, an increase relative to the comparison will be a upward-facing green arrow. If set to false, the increase will show a downward-facing red arrow.',
            section='Comparison'
        ),
        'show_comparison': BooleanOption(
            attachment='visualization',
            default=False,
            label='Show Comparison',
            description='Determines if the number should have an indicator showing a comparison',
            section='Comparison'
        ),

        'font_color': ColorOption(
            attachment='visualization',
            default='auto',
            label='Font Color',
            description='Sets the font color for all text shown on the chart',
            section='Font'
        ),

        'font_family': SelectOption(
            attachment='visualization',
            default='auto',
            label='Font Family',
            description='Sets the font for all text shown on the chart',
            values=[
                { '' : ''}
            ],
            section='Font'
        ),
        'title': InputOption(
            attachment='visualization',
            default=None,
            label='Title',
            description='Accepts any string value to use as the display title of the chart on a page',
            section='General'
        )
    },
    render=render
)
