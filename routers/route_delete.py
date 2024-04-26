from lib.anturi import *
from lib.halli import *
from lib.alustus import *
from datetime import datetime

from fastapi import HTTPException, APIRouter

router_deletes = APIRouter()

current_time = datetime.now().strftime("%Y-%m-%d %H:%M")

@router_deletes.delete("/zones/delete")
def delete_temperature_reading(sensor_id : str, time_of_reading : str):
        
    try:
        start = datetime.strptime(time_of_reading, "%Y-%m-%d %H:%M")
    except ValueError:
        raise HTTPException(status_code=400, detail="Aikaleima väärässä formaatissa. Käytä: 'YYYY-MM-DD HH:MM'")

    sensor_to_modify = None
    # Tarkistetaan onko anturi jo jossain lohkossa
    for _, sensors in halli.zones.items():
        if sensor_id in sensors:
            sensor_to_modify = sensors[sensor_id]
            
    if len(sensor_to_modify.temperature_readings) == 0:
        return {"message": f"Anturilla [{sensor_id}] ei ole mittatuloksia!"}
    
    #Inhottava listafunktio joka hakee annetun aikavälin tulokset 
    sensor_to_modify.temperature_readings = [reading for reading in sensor_to_modify.temperature_readings if not reading.startswith(time_of_reading)] 


    return {"message": f"Mittatulokset aikaleimalla {time_of_reading} poistettu!"}