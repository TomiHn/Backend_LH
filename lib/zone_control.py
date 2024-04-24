from lib.anturi import Sensor
from lib.halli import Factory
from datetime import datetime

current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

sensor1 = Sensor("SF-1", current_time)
sensor2 = Sensor("SF-2", current_time)
sensor3 = Sensor("SF-3", current_time)
sensor4 = Sensor("SF-4", current_time)


sensor1.error_state_handle(True)


sensor1.set_temp(22.2, current_time)
sensor1.set_temp(23, current_time)
sensor1.set_temp(23, current_time)
sensor1.set_temp(23, current_time)
sensor1.set_temp(23, current_time)
sensor1.set_temp(23, current_time)
sensor1.set_temp(23, current_time)
sensor1.set_temp(23, current_time)
sensor1.set_temp(23, current_time)
sensor1.set_temp(23, current_time)
sensor1.set_temp(23, current_time)
sensor1.set_temp(23, current_time)
sensor1.set_temp(23, current_time)
sensor1.set_temp(23, current_time)
sensor1.set_temp(23, current_time)
sensor1.set_temp(23, current_time)
sensor1.set_temp(23, current_time)
sensor1.set_temp(23, current_time)
sensor1.set_temp(23, current_time)
sensor1.set_temp(23, current_time)
sensor1.set_temp(23, current_time)
sensor1.set_temp(23, current_time)

halli = Factory(zones = {})


halli.add_zone("lohko1")
halli.add_zone("lohko2")
halli.add_zone("lohko3")


halli.add_sensor("lohko1", sensor1)
halli.add_sensor("lohko2", sensor2)
halli.add_sensor("lohko3", sensor3)
halli.add_sensor("lohko3", sensor4)


