
from lib.anturi import *
from lib.halli import *
from lib.zone_control import *
from datetime import datetime

from fastapi import HTTPException, status, APIRouter

router_gets = APIRouter()

current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")


@router_gets.get("/zones", summary="Näytetään kaikkien lohkojen sisältö raakana. (Auttaa debuggailussa)")
def get_zones():
    return halli.zones
    

#Palautetaan anturit tehtävänannon formaatissa
@router_gets.get("/zones/parsed_sensors", response_model=SensorRootModel, summary="Näytetään kaikki anturit tehtävänannon formaatissa")
def get_sensors_parsed():
    return_data = halli.parse_sensor_data(halli.zones)
    return SensorRootModel(root=return_data)



@router_gets.get("/sensor/{sensor_id}", summary="Palauttaa yhden anturin tiedot halutussa formaatissa")
def get_sensor(sensor_id : str):
    """
    Etsii ja palauttaa halutun anturin tiedot anturin tunnisteella\n
    \n
    Parameters:
    - **sensor_id (str)** => Halutun anturin tunniste. esim: SF-1
    """
    for _, sensors in halli.zones.items():
        if sensor_id not in sensors:
            raise HTTPException(status_code=404, detail=f"Anturia: [{sensor_id}] ei löytynyt!")
        else:
            #Jos anturi löytyy, tehdään sille juttuja
            sensor = sensors[sensor_id]
            #Muutetaan data yleismallin mukaiseksi
            sensor_model = SensorModel(**sensor.__dict__)
            #Karsitaan edellämainitusta datasta ylimääräiset ja muokataan se tehtävänannon mukaiseksi
            return {_: SensorSingleModel(**sensor_model.dict(exclude={"temperature_readings"}), temperature_readings=sensor_model.get_temperature_readings(10))}



@router_gets.get("/zones/{zone}", summary="Haetaan halutusta lohkosta kaikki anturit")
def get_sensors_in_zone(zone : str):
    """
    Etsii halutun lohkon ja palauttaa kaikki sen sisältämät anturit määrätyssä formaatissa\n
    \n
    Parameters:
    - **zone (str)** => Lohko, jonka anturit halutaan nähdä. esim: lohko1
    """
    _zone = halli.zones[zone]
    output_model = {}

    #Muovataan taas palautettava data sopimaan palautusmalliin
    for sensor_id, sensor in _zone.items():
        sensor_model = SensorModel(**sensor.__dict__)
        output_model[sensor_id] = SensorSingleModel(**sensor_model.dict(exclude={"temperature_readings"}), temperature_readings=sensor_model.get_temperature_readings(1))
    return {zone: output_model}
    