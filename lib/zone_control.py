from lib.anturi import Sensor
from lib.halli import Factory

sensor1 = Sensor("SF-1")
sensor2 = Sensor("SF-2")
sensor3 = Sensor("SF-3")


halli = Factory([])
lohko1 = {"Lohko1" : []}
lohko2 = {"Lohko2" : []}
lohko3 = {"Lohko3" : []}

halli.add_zone(lohko1)
halli.add_zone(lohko2)
halli.add_zone(lohko3)


halli.add_sensor_to_zone(sensor1, "Lohko1")
halli.add_sensor_to_zone(sensor1, "Lohko1")
halli.add_sensor_to_zone(sensor2, "Lohko2")
halli.add_sensor_to_zone(sensor3, "Lohko3")
