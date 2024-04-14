class Sensor:
    def __init__(self, id: str):

        self.id = id

        self.temp : float = 0
        self.error_state : bool = False
    
    def error_state_handle(self, error : bool):
        self.error_state = error;

    def set_temp(self, value: float):
        self.temp = round(value, 1)