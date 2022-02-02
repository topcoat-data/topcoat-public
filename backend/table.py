from pandas.core.frame import DataFrame
from common.plugin.visualization import BooleanOption, SelectOption, InputOption, NumericOption, ColorOption, ColorPaletteOption, VisualizationConfig

def render(source: DataFrame, config: VisualizationConfig):
    return 'Test'

register(
    key=__name__,
    options={
        'download_csv': BooleanOption(
            attachment='visualization',
            default=False,
            label='Download CSV',
            description='When set to true, a button will become available allowing users to download data to a CSV',
            section='Interactivity'
        ),
        'searchable': BooleanOption(
            attachment='visualization',
            default=False,
            label='Searchable',
            description='When set to true, a text search box will become available allowing users to search for results',
            section='Interactivity'
        ),
        'series_html': InputOption(
            attachment='column',
            default=None,
            label='Series Custom HTML',
            description='Accepts HTML + vue.js to inform the HTML visualization for a series value',
            section='Formatting'
        ),
        'series_width': InputOption(
            attachment='column',
            default=None,
            label='Series Width',
            description='Accepts either a number of pixels or total percentage of the table width this series should consume',
            section='Formatting'
        ),
        'show_row_numbers': BooleanOption(
            attachment='visualization',
            default=False,
            label='Show Row Numbers',
            description='When set to true, row numbers will display to the left of all columns',
            section='Data Extensions'
        ),
        'show_total_column': BooleanOption(
            attachment='visualization',
            default=False,
            label='Show Total Column',
            description='When set to true, there will be a total column available that sums all numerical values in each row',
            section='Data Extensions'
        ),
        'show_total_row': BooleanOption(
            attachment='visualization',
            default=False,
            label='Show Total Row',
            description='When set to true, there will be a total row available that sums all numerical values in each column',
            section='Data Extensions'
        ),

        'font_color': ColorOption(
            attachment='visualization',
            default='auto',
            label='Font Color',
            description='Sets the font color for all text shown on the chart',
            section='Font'
        ),
        'sortable': BooleanOption(
            attachment='visualization',
            default=False,
            label='Sortable',
            description='When set to true, users will be able to sort columns by clicking on the column header',
            section='Interactivity'
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
        'value_format': InputOption(
            attachment='column',
            default='inherit',
            label='Value Format',
            description='Accepts python string formatting to set the series value format (such as dates, currency, percent, etc.)',
            section='Formatting'
        ),
        'series_name': InputOption(
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
        )
    },
    render=render
)
