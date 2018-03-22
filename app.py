from bokehPlot import *
from flask import Flask, render_template, request, redirect, flash

app = Flask(__name__)

@app.route('/')
@app.route('/index')
def index():
    tickers = np.unique(qdf['ticker'])
    data_types = [key for key in qdf.keys()]
    data_types.pop( data_types.index('ticker') )

    # Determine the number of tickers to plot
    nplot = request.args.get("nplot")
    init_config = True
    if nplot == None:
        nplot = 1
    else:
        nplot = int(nplot)
        init_config = False

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
    script, div = components(generate_bokeh_plot(qdf,tickers2Plot,data2Plot))

    return render_template("index.html", nPlotMax=5, nplot=nplot, tickers=tickers, data_types=data_types,
                                        tickers2Plot=tickers2Plot, data2Plot=data2Plot, script=script, div=div)


if __name__ == '__main__':
  app.run(port=33507)
