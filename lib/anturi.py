class Sensor:
    def __init__(self, id: str, current_time : str):

        self.id = id

        self.error_state : bool = False
        self.temperature_readings = []
    
    def error_state_handle(self, error : bool):
        self.error_state = error;

    def set_temp(self, value: float, time : str):
        self.temperature_readings.insert(0, f"{time}: {round(value, 1)}")
