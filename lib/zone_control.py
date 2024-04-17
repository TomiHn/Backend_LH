from lib.anturi import Sensor
from lib.halli import Factory
from datetime import datetime

current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

sensor1 = Sensor("SF-1", current_time)
sensor2 = Sensor("SF-2", current_time)
sensor3 = Sensor("SF-3", current_time)

sensor1.error_state_handle(True)

halli = Factory([])
lohko1 = {"Lohko1" : []}
lohko2 = {"Lohko2" : []}
lohko3 = {"Lohko3" : []}

halli.add_zone(lohko1)
halli.add_zone(lohko2)
halli.add_zone(lohko3)


halli.add_sensor_to_zone(sensor1, "Lohko1")
halli.add_sensor_to_zone(sensor2, "Lohko2")
halli.add_sensor_to_zone(sensor3, "Lohko3")
