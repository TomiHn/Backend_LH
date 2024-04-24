from pydantic import BaseModel, RootModel, Field
from typing import Dict, List

class Sensor:
    def __init__(self, id: str, current_time : str):

        self.id = id

        self.error_state : bool = False
        self.temperature_readings = []

        self.time = current_time
    def error_state_handle(self, error : bool):
        self.error_state = error;

    def set_temp(self, value: float, time : str):
        self.time = time
        self.temperature_readings.insert(0, f"{self.time}: {round(value, 1)}")


#Mallit
#Paljon malleja koska dataa pitää vääntää eri muotoihin
#Yleismalli
class SensorModel(BaseModel):
    id : str
    error_state: bool
    temperature_readings: List[str] = Field(...)

    #Saadaan palautettua vain tietty määrä mittatuloksia
    def get_temperature_readings(self, num : int) -> List[str]:
        return self.temperature_readings[:num]
    
#Malli kaikkien palautus metodiin
class SensorAllModel(BaseModel):
        id : str
        error_state: bool

#Malli yhden palautukseen
class SensorSingleModel(BaseModel):
    id: str
    error_state: bool
    temperature_readings: List[str]

    #BaseModel luokan config asetus, tällä saadaan luettua esim SQL dataa FastApiin
    class Config:
        from_attributes = True

class SensorRootModel(RootModel):
    root: Dict[str, Dict[str, SensorAllModel]]

