import warnings
warnings.simplefilter('ignore') # filter some warning messages

import datetime
import numpy as np
import pandas as pd
import xarray as xr

import matplotlib.pyplot as plt
import cartopy.crs as ccrs
from cartopy.mpl.gridliner import LONGITUDE_FORMATTER, LATITUDE_FORMATTER

from pathlib import Path
import configparser
from lxml import objectify

# to obtain rich information from PO.DAAC Drive, import and create an instance of Drive
from podaac import drive as podaacdrive
import podaac.podaac as podaac


##############################################################################

def get_podaac_datasetid(dresult):
    dresult_xml = objectify.fromstring(dresult)
    # But note that there can be multiple entry instances, so list handlingwould be needed, generically
    # Actually, the "podaac:datasetId" element would probably be more correct than "id"
    dataset_id = dresult_xml.entry.id.text
    return dataset_id

##############################################################################

basepath = Path('/home/douglasnehme/Dropbox/profissional/ohw_2019/ohw19')

# Create an instance of the Podaac class
p = podaac.Podaac()


with open(basepath / 'podaac.ini', 'r') as f:
    config = configparser.ConfigParser()
    config.read_file(f)
    d = podaacdrive.Drive(None, 
                          config['drive']['urs_username'], 
                          config['drive']['urs_password'])


start_time='2019-08-20T00:00:00Z'
end_time='2019-08-27T23:59:59Z'


dresult = p.dataset_search(keyword='mur', start_time=start_time, end_time=end_time)
dataset_id = get_podaac_datasetid(dresult)

gresult = p.granule_search(dataset_id=dataset_id,
                           start_time=start_time,
                           end_time=end_time,
                           items_per_page='50')


urls = d.mine_drive_urls_from_granule_search(granule_search_response=gresult)

urls_mur = [w.replace('-tools.jpl.nasa.gov/drive/files/', '-opendap.jpl.nasa.gov/opendap/') 
            for w in urls]


ds_sst_mur = xr.open_dataset(sorted(urls_mur)[-1])



dresult_ostia = p.dataset_search(keyword='ostia', start_time=start_time, end_time=end_time)

dataset_id_ostia = get_podaac_datasetid(dresult_ostia)

gresult_ostia = p.granule_search(dataset_id=dataset_id_ostia,
                                 start_time=start_time,
                                 end_time=end_time,
                                 items_per_page='50')
urls = d.mine_drive_urls_from_granule_search(granule_search_response=gresult_ostia)
urls_ostia = [w.replace('-tools.jpl.nasa.gov/drive/files/', '-opendap.jpl.nasa.gov/opendap/') 
              for w in urls]

ds_sst_ostia = xr.open_dataset(sorted(urls_ostia)[-1])