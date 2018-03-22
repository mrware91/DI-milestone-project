from bokeh.layouts import gridplot
from bokeh.plotting import figure, show, output_file
from bokeh.embed import components
from bokeh.io import output_notebook
from bokeh.palettes import Category10

import pandas as pd
import Picklez

import quandl
import os

# Grab tickers and plotable datatypes from quandl
quandl.ApiConfig.api_key = os.environ['quandlAPIKey']
tickers = quandl.get_table('WIKI/PRICES', date = { 'gte': '2017-01-01', 'lte': '2017-01-03' },
                         paginate=True, qopts={'columns': ['ticker']})['ticker'].unique()

sampleData = quandl.get('WIKI/AAPL', start_date="2001-12-31", end_date="2005-12-31")

data_types = [key for key in sampleData.keys()]
df_columns = list(data_types)
df_columns.append('ticker')

# Generate quandl data
def generateQuandlData(pTickers, start_date="2001-12-31",end_date="2005-12-31"):
    allData = pd.DataFrame(columns = df_columns)
    for ticker in pTickers:
        data = quandl.get('WIKI/%s' % (ticker), start_date=start_date, end_date=end_date)
        data['ticker'] = ticker
        allData = allData.append(data)

    return allData

def generate_bokeh_plot(pTickers,pDataTypes, start_date="2001-12-31",end_date="2005-12-31"):
    uTickers = list(set(pTickers))
    qdf = generateQuandlData(uTickers, start_date, end_date)

    p1 = figure(title="WIKI/PRICES", toolbar_location="right",background_fill_color="#E8DDCB", x_axis_type="datetime",
                logo=None, tools="pan,wheel_zoom,box_zoom,reset,save")

    for m, ticker in enumerate(uTickers):
        for n, data_type in enumerate(pDataTypes):
            idxs=qdf['ticker']==ticker
            p1.line(qdf.index[idxs],  qdf[idxs][data_type],
                    color=Category10[10][n+(n+1)*m], line_width=2, alpha=0.7,
                    legend=ticker+':'+data_type)

    p1.legend.location = "top_left"
    p1.legend.background_fill_color = "darkgrey"
    p1.xaxis.axis_label = 'time'
    p1.yaxis.axis_label = ''

    return p1
