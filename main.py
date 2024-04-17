
# TARPEET #
# - Anturien koodit
# - Mitä lähettää? : Pelkkä lämpötila
# - Virhetila?
#     - Tieto palvelimelle
#     - Ei lämpötilan lähetystä

# - Käyttöliittymä
#     - Anturien lisäys
#     - Tilamuutos?
#     - Lohkon vaihto
#     - Poistaa mittaustulos
#     - Näyttää anturien tiedot
#         - Tunniste
#         - Tila
#         - Viimeisin mitta-arvo ja aikaleima
#         - 10 uusinta
#         - Aikojen sorttaus
#     - Virhetilasta ajankohta

# - JSON formaatissa
# - Raportti



from lib.anturi import Sensor
from lib.halli import Factory
from lib.zone_control import *

from fastapi import FastAPI

import sys

app = FastAPI()




@app.get("/zones")
def get_zones():
    return halli.zones



@app.get("/sensor")
def get_sensor(sensor_id : str):
    for zone in halli.zones:
        for sensors in zone.values():
            for sensor in sensors:
                return sensor


