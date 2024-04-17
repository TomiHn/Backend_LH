class Factory:
    def __init__(self, zones : dict):
        self.zones = zones;
        
    def add_zone(self, newZone : dict):
        if newZone not in self.zones:
            self.zones[newZone] = {}

    

    def add_sensor(self, zone, sensor : object):

        # Tarkistetaan onko anturi jo jossain lohkossa
        for sensors in self.zones.items():
            if sensor in sensors:
                return f"Sensor {sensor.id} already exists!"
                
        self.zones[zone][sensor.id] = sensor 
        
