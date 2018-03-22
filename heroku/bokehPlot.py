from bokeh.layouts import gridplot
from bokeh.plotting import figure, show, output_file
from bokeh.embed import components
from bokeh.io import output_notebook
from bokeh.palettes import Category10

import numpy as np
import pandas as pd
import Picklez

# output_notebook()

qdf = Picklez.load_obj('data/quandlData2017')
qdf['date'] = qdf['date'].apply(lambda x: pd.to_datetime(x))
qdf = qdf.set_index('date')

def generate_bokeh_plot(qdf,tickers,data_types):
    p1 = figure(title="WIKI/PRICES", toolbar_location="right",background_fill_color="#E8DDCB", x_axis_type="datetime",
                logo=None, tools="pan,wheel_zoom,box_zoom,reset,save")

    for m, ticker in enumerate(tickers):
        for n, data_type in enumerate(data_types):
            idxs=qdf['ticker']==ticker
            p1.line(qdf.index[idxs],  qdf[idxs][data_type],
                    color=Category10[10][n+(n+1)*m], line_width=2, alpha=0.7,
                    legend=ticker+':'+data_type)

    p1.legend.location = "top_left"
    p1.legend.background_fill_color = "darkgrey"
    p1.xaxis.axis_label = 'time'
    p1.yaxis.axis_label = ''

    return p1
