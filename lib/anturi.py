class Sensor:
    def __init__(self, id: str, current_time : str):

        self.id = id

        self.temp : float = 0
        self.error_state : bool = False
        self.time_stamp : str = current_time
    
    def error_state_handle(self, error : bool):
        self.error_state = error;

    def set_temp(self, value: float):
        self.temp = round(value, 1)
