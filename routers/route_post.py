
from lib.anturi import *
from lib.halli import *
from lib.alustus import *
from datetime import datetime

from fastapi import HTTPException, status, APIRouter

router_posts = APIRouter()

current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")


@router_posts.post("/zones/addZone", status_code=status.HTTP_201_CREATED, summary="Uuden lohkon lisäys methodi")
def add_zone(zone : str):
    """
    Lisää halutun uuden lohkon hallin lohkoihin, lohkoon voi lisäyksen jälkeen siirtää tai lisätä antureita\n
    \n
    Parameters:
    - **zone (str)** => Haluttu uusi lohko, ei saa olla lohko joka on jo olemassa
    """

    if not halli.add_zone(zone):
        raise HTTPException(status_code=409, detail=f"Lohko: {zone} on jo olemassa!")
    halli.add_zone(zone)
    return {"message": f"Lohko: {zone} lisätty"}

@router_posts.post("/zones", status_code=status.HTTP_201_CREATED, summary="Anturin lisäys tiettyyn lohkoon")
def add_one_sensor(sensor_id, zone : str):
    """
    Lisää anturin tiettyyn lohkoon, kaikilla antureilla pitää olla uniikki tunniste ja lohkon pitää olla olemassa\n
    \n
    Parameters:
    - **sensor_id (str)** => Lisättävän anturin haluttu tunniste. esim: SF-5
    - **zone (str)** => Lohko mihin anturi halutaan lisätä. esim: lohko1
    """

    sensor_new = Sensor(sensor_id, current_time)
    add_result = halli.add_sensor(zone, sensor_new)

    #add_sensor methodi palauttaa numeron riippuen siitä mitä tapahtuu
    if  add_result == 0: # Lisäys onnistui
        return f"Anturi: [{sensor_id}] lisätty lohkoon [{zone}]."
    elif add_result == 1: # Lohkoa ei löytynyt
        raise HTTPException(status_code=404, detail=f"Lohkoa [{zone}] ei löytynyt!")
    elif add_result == 2: # Anturia ei löytynyt
        raise HTTPException(status_code=409, detail=f"Anturi [{sensor_id}] on jo olemassa!")
            

@router_posts.post("/zones/move_sensor", status_code=status.HTTP_201_CREATED, summary="Anturin siirto lohkosta toiseen")
def move_sensor_route(sensor_id : str, old_zone : str, new_zone : str):
    """
    Anturi ja molemmat lohkot pitää olla olemassa jotta methodi toimii\n
    \n
    Parameters: 
    - **sensor_id (str)** => Siirrettävän anturin tunniste. esim: SF-1 
    - **old_zone (str)** => Siirrettävän anturin alkuperäinen lohko. esim: lohko1
    - **new_zone (str)** => Lohko mihin anturi halutaan siirtää. esim: lohko2

    """

    move_result = halli.move_sensor(sensor_id, old_zone, new_zone)

    #move_sensor methodi palauttaa numeron riippuen siitä mitä tapahtuu
    if move_result == 0: # Siirto onnistui
        return {"message": f"Anturi [{sensor_id}] siirretty lohkosta [{old_zone}] lohkoon [{new_zone}]."}
    elif move_result == 1: # Vanhaa lohkoa ei löytynyt
        raise HTTPException(status_code=404, detail=f"Vanhaa lohkoa [{old_zone}] ei löytynyt!")
    elif move_result == 2: # Uutta lohkoa ei läytynyt
        raise HTTPException(status_code=404, detail=f"Uutta lohkoa [{new_zone}] ei löytynyt!")
    elif move_result == 3: # Anturia ei löytynyt
        raise HTTPException(status_code=404, detail=f"Anturia [{sensor_id}] ei löytynyt lohkosta [{old_zone}]!")


@router_posts.post("/sensor/{sensor_id}/error", status_code=status.HTTP_201_CREATED, summary="Tietyn anturin virhetilan muutos")
def change_sensor_status(sensor_id : str, error_status: bool):
        
        """
        Methodi anturin tilan hallintaan, tämä tieto pitäisi tulla anturilta enkä keksinyt parempaa tapaa hallinnoida tilaa tehtävän kontekstissa\n
        \n
        Parameters:
        - **sensor_id (str)** => Halutun anturin tunniste. esim: SF-1
        - **error_status (bool)** => Halutaanko virhetila päälle vai ei, True = päällä / False = pois päältä
        """

        #Tarkistetaan löytyykö anturi
        sensor_found = False
        for _, sensors in halli.zones.items():
            if sensor_id in sensors:
                #Aika pitää päivittää nykyiseen aikaan
                current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                sensors[sensor_id].error_state_handle(error_status, current_time)
                sensor_found = True
                break
        if not sensor_found:
                raise HTTPException(status_code=404, detail=f"Anturia: [{sensor_id}] ei löytynyt!")
        return {"message": f"Anturi [{sensor_id}]:n virhetila on nyt [{error_status}]"}

@router_posts.post("/sensor/{sensor_id}/temperature", summary="Lähettää haluttuun anturiin uuden lämpötilamittauksen")
def send_temp_reading(sensor_id : str, temp : float):
            """
            Tällä metodilla pystytään simuloimaan lämpötilan mittausta. Jokainen methodin suoritus "ottaa" halutulla anturilla uuden mittatuloksen.\n
            \n
            Parameters:
            - **sensor_id (str)** => Tunniste anturille jolla halutaan simuloida mittaus. esim: SF-1
            - **temp (float)** => Haluttu lämpötila arvo. esim: 25.45 
            """

            current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            
            sensor_found = False

            for _, sensors in halli.zones.items():
                if sensor_id in sensors:
                    if sensors[sensor_id].error_state: #Estetään lämpötilan päivitys jos anuri on virhetilassa
                        raise HTTPException(status_code=406, detail=f"Anturi [{sensor_id}] on virhetilassa!")
                    sensor_found = True
                    break
            if not sensor_found:
                raise HTTPException(status_code=404, detail=f"Anturia: [{sensor_id}] ei löytynyt!")
            return {"message": f"Anturin [{sensor_id}] lämpötila on [{temp}], aikaleimalla [{current_time}]"}

