import urllib, json
import pandas as pd
import quandl
import Picklez
from io import BytesIO
from zipfile import ZipFile

def gatherQuandl():
    quandleAPIKey = Picklez.load_obj('quandleAPIKey')

    url = "https://www.quandl.com/api/v3/datatables/"+\
          "WIKI/PRICES.json?api_key=%s&qopts.export=true&api_key=%s" % quandleAPIKey
    response = urllib.urlopen(url)
    link = json.loads(response.read())


    url = urllib.urlopen(link['datatable_bulk_download']['file']['link'])
    with ZipFile(BytesIO(url.read())) as my_zip_file:
        for contained_file in my_zip_file.namelist():
            print contained_file
            quandlData = pd.read_csv(my_zip_file.open(contained_file))

    Picklez.save_obj(quandlData,'data/quandlData')
