
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
from datetime import datetime

from fastapi import FastAPI, HTTPException, status


current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

app = FastAPI()




@app.get("/zones")
def get_zones():
    return halli.zones



@app.get("/sensor/{sensor_id}")
def get_sensor(sensor_id : str):
    for _, sensors in halli.zones.items():
        if sensor_id in sensors:
            return sensors[sensor_id]
    return None

@app.post("/zones", status_code=status.HTTP_201_CREATED)
def add_one_sensor(sensor_id, zone : str):
    sensor_new = Sensor(sensor_id, current_time)
    halli.add_sensor(zone, sensor_new)
            



