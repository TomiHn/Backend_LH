class Factory:
    def __init__(self, zones : list):
        self.zones = zones;

    #Lohkon lisäys, lohko on dict, jossa key on lohkon nimi ja valuena lista lohkoon kuuluvista antureista
    def add_zone(self, newZone : dict):
        self.zones.append(newZone)
    

    #Anturin lisäys lohkoon
    def add_sensor_to_zone(self, sensor: object, zone: str):
        # Tarkistetaan ettei anturi ole jo jossain lohkossa
        for zone_dict in self.zones:
            if sensor in [sensor for sublist in zone_dict.values() for sensor in sublist]:
                print("Sensor already in a zone")
                return;    
        for zone_key in self.zones:
            if zone in zone_key:
                zone_key[zone].append(sensor)
                return
        
        print("Zone not found")