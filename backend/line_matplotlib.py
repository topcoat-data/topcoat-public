import matplotlib
from pandas.core.frame import DataFrame

import matplotlib.pyplot as plt
import numpy as np

from common.plugin.visualization import BooleanOption, InputOption, SelectOption, VisualizationConfig


def render(source: DataFrame, config: VisualizationConfig):

    df = source.set_index(['animal'])
    ax = df.plot()
    plt.subplots_adjust(left=0.1, top=1, right=1)

    return ax.figure


register(
    key=__name__,
    options={
    },
    render=render
)
