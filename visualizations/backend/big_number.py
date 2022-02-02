from pandas.core.frame import DataFrame

from common.plugin.visualization import BooleanOption, InputOption, SelectOption, VisualizationConfig


def render(source: DataFrame, config: VisualizationConfig):
    col_name = config.measures[0].id_or_name

    big_number_template = '''
        <div style="width: 200px; border: 1px solid lightgray; padding: 10px; margin: 10px; border-radius: 5px; background: #eeeeee;">
            <div style="font-size: 16px;">{}</div>
            <div style="font-size: 40px; font-weight: bold;">{}</div>
        </div>
    '''
    html = big_number_template.format(col_name.capitalize(),source[col_name][0] )
    return html


register(
    key=__name__,
    options={
    },
    render=render
)
