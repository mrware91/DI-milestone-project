from bokehPlot import *
from flask import Flask, render_template, request, redirect, flash
from flask_cors import CORS
import quandl
import os
from datetime import datetime

plot_start=None
plot_end=None

# Define and start Flask server
app = Flask(__name__)
CORS(app)

@app.route('/')
@app.route('/index')
def index():
    # Determine the number of tickers to plot
    nplot = request.args.get("nplot")
    init_config = True
    if nplot == None:
        nplot = 1
    else:
        nplot = int(nplot)
        init_config = False

    # Determine start and end date
    start_date = request.args.get("start_date")
    end_date = request.args.get("end_date")
    bad_date = False

    if start_date is None:
        start_date='2017-01-01'
    if end_date is None:
        end_date = '2018-01-01'

    try:
        if datetime.strptime(end_date, '%Y-%m-%d')<datetime.strptime(start_date, '%Y-%m-%d'):
            plot_start='2017-01-01'
            plot_end  = '2018-01-01'
            bad_date  = True
        else:
            plot_start = start_date
            plot_end = end_date
    except Exception:
        plot_start='2017-01-01'
        plot_end  = '2018-01-01'
        bad_date  = True




    # Determine which tickers to plot
    tickers2Plot = []
    if init_config:
        tickers2Plot.append(tickers[0])
    else:
        for n in xrange(nplot):
            val = request.args.get("ticker[%d]"%n)
            if val is None:
                tickers2Plot.append(tickers[0])
            else:
                tickers2Plot.append(val)
    print tickers2Plot

    # Determine which data types to plot
    data2Plot = []
    if init_config:
        data2Plot.append(data_types[0])
    else:
        for dt in data_types:
            if bool(request.args.get(dt)):
                data2Plot.append(dt)

    # Generate the plot
    script, div = components(generate_bokeh_plot(tickers2Plot,data2Plot, plot_start, plot_end))

    return render_template("index.html", nPlotMax=5, nplot=nplot, tickers=tickers, data_types=data_types,
                                        tickers2Plot=tickers2Plot, data2Plot=data2Plot, script=script, div=div,
                                        start_date=start_date, end_date=end_date,
                                        plot_start=plot_start, plot_end=plot_end,
                                        bad_date=bad_date)


if __name__ == '__main__':
  app.run(port=33507)
