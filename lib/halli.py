from pydantic import BaseModel
from typing import Dict, List
from lib.anturi import *

class Factory:
    def __init__(self, zones : dict):
        self.zones = zones;
        
    def add_zone(self, newZone : str) -> bool:
        if newZone not in self.zones:
            self.zones[newZone] = {}
            return True
        return False

    

    def add_sensor(self, zone : str, sensor : object) -> int:

        #Tarkistetaan onko haluttu lohko olemassa
        if zone not in self.zones:
            return 1

        # Tarkistetaan onko anturi jo jossain lohkossa
        for _, sensors in self.zones.items():
            if sensor.id in sensors:
                return 2
                
        self.zones[zone][sensor.id] = sensor 
        return 0
        
    def move_sensor(self, sensor_id : str, old_zone : str, new_zone : str) -> int:
            sensor_temp = None

            if old_zone not in self.zones:
                return 1
            if new_zone not in self.zones:
                return 2
            
            if sensor_id not in self.zones[old_zone]:
                return 3
            elif sensor_id in self.zones[old_zone]:
                sensor_temp = self.zones[old_zone][sensor_id]
                del self.zones[old_zone][sensor_id]
                self.zones[new_zone][sensor_id] = sensor_temp
                return 0
            

    #Muunnetaan data vastaamaan tehtävänannossa määriteltyä formaattia
    def parse_sensor_data(self, zones : Dict) -> Dict:

        return_model = {}

        for zone, sensors in zones.items():
            new_model = {}
            for sensor_id, sensor_data in sensors.items():
                new_model[sensor_id] = SensorAllModel(id=sensor_data.id, error_state=sensor_data.error_state)
            return_model[zone] = new_model
        return return_model
        



