
from math import ceil

import pandas as pd
import numpy as np
import requests
import os 

from dotenv import load_dotenv
load_dotenv()

user = os.getenv('dhm_user')
pwd = os.getenv('dhm_pwd')

dhm_url = f'https://services.datafordeler.dk/DHMTerraen/DHMKoter/1.0.0/GEOREST/HentKoter?format=json&username={user}&password={pwd}&georef=EPSG:4326&geop='

def to_url(coords):
    return '|'.join( [
        f"POINT({coords.iloc[i].lat} {coords.iloc[i].lng})"
        for i in range(len(coords))
    ] )

def request_altitudes(coords):
    n = ceil(len(coords) / 50)
    chunks = np.array_split(coords, n)
    altitudes = pd.DataFrame({'way_id': [], 'way_dist': [], 'altitude': []})
    i = 0
    for j, chunk in enumerate(chunks):
        print('chunk', j)
        url = dhm_url + to_url(chunk)
        res = requests.get(url).json()
        _altitudes = res['HentKoterRespons']['data']
        for alt in _altitudes:
            pos = coords.iloc[i]
            altitudes = altitudes.append( {
                'way_id': pos.way_id, 
                'way_dist': pos.way_dist, 
                'altitude': alt['kote']
            }, ignore_index=True )
            i += 1
    return altitudes