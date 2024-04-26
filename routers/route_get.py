
from lib.anturi import *
from lib.halli import *
from lib.alustus import *
from datetime import datetime

from fastapi import HTTPException, status, APIRouter
from fastapi.responses import StreamingResponse

router_gets = APIRouter()

current_time = datetime.now().strftime("%Y-%m-%d %H:%M")


@router_gets.get("/", summary="Näytetään kaikkien lohkojen sisältö raakana. (Auttaa debuggailussa)")
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



@router_gets.get("/zones/{zone}", summary="Haetaan halutusta lohkosta kaikki anturit", response_model=SensorRootModel)
def get_sensors_in_zone(zone : str):
    """
    Etsii halutun lohkon ja palauttaa kaikki sen sisältämät anturit määrätyssä formaatissa\n
    \n
    Parameters:
    - **zone (str)** => Lohko, jonka anturit halutaan nähdä. esim: lohko1
    """

    if zone not in halli.zones:
        raise HTTPException(status_code=404, detail=f"Lohkoa [{zone}] ei löytynyt!")

    _zone = halli.zones[zone]
    output_model = {}

    #Muovataan taas palautettava data sopimaan palautusmalliin
    for sensor_id, sensor in _zone.items():
        sensor_model = SensorModel(**sensor.__dict__)
        output_model[sensor_id] = SensorSingleModel(**sensor_model.dict(exclude={"temperature_readings"}), temperature_readings=sensor_model.get_temperature_readings(1))
    return {zone: output_model}
    
@router_gets.get("/sensor/{sensor_id}/readings", summary="Näytetään halutun anturin mittatulokset halutulta aikaväliltä")
def get_temp_readings(sensor_id : str , start_time : str, end_time : str):
    """
    Tällä methodilla saadaan näytettyä mittatulokset tietyltä aikaväliltä. Annetut ajat PITÄÄ OLLA formaatissa 'YYYY-MM-DD HH:MM'!\n
    \n
    Parameters:
    - **sensor_id (str)** => Halutun anturin tunniste. esim: SF-1
    - **start_time (str)** => Halutun aikavälin alku. esim: 2024-04-25 09:43
    - **end_time (str)** => Halutun aikavälin loppu. esim: 2024-04-25 10:10

    """
    #Muutetaan argumentit datetime arvoiksi vertailua varten
    try:
        start = datetime.strptime(start_time, "%Y-%m-%d %H:%M")
        end = datetime.strptime(end_time, "%Y-%m-%d %H:%M")
    except ValueError:
        raise HTTPException(status_code=400, detail="Ajat väärässä formaatissa. Käytä: 'YYYY-MM-DD HH:MM")

    #Etsitään anturi ja tehdään sille toimenpiteet
    sensor_found = False
    sensor_to_modify = None
    for _, sensors in halli.zones.items():
        if sensor_id in sensors:
            sensor_to_modify = sensors[sensor_id]
            sensor_found = True
    if not sensor_found:
        raise HTTPException(status_code=404, detail=f"Anturia: [{sensor_id}] ei löytynyt!")
    
    #Filteröidään tulokset aikavälille
    filtered = []
    for reading in sensor_to_modify.temperature_readings:
        reading_time_str, reading_value = reading.split(": ")
        reading_time = datetime.strptime(reading_time_str, "%Y-%m-%d %H:%M")
        if start <= reading_time <= end:
            filtered.append(reading)

    if len(filtered) == 0:
        return {f"{sensor_id}": {"message": "Ei tuloksia halutulta aikaväliltä"}}
    return {f"{sensor_id}": filtered}

@router_gets.get("/zone/errors", summary="Anturien haku virhetilan perusteella")
def get_sensors_by_state(state : bool) -> Dict:
        """
        Methodi jolla voidaan filtteröidä anturit niiden virhetilan perusteella.\n
        Parameters:
        - **state (bool)** => Virhetila. True = virhetilassa / False = normaalitilassa
        """
        
        #Luodaan uusi malli palautusta varten
        return_data = {}
        for _id, sensors in halli.zones.items():
            return_data[_id] = {}
            for sensor_id, sensor in sensors.items():
                if sensor.error_state == state:
                    return_data[_id][sensor_id] = SensorAllModel(id=sensor_id, error_state=state).dict()
        return return_data

