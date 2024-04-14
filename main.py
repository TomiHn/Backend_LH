
# TARPEET #
# - Anturien koodit
# - Mitä lähettää? : Pelkkä lämpötila
# - Virhetila?
#     - Tieto palvelimelle
#     - Ei lämpötilan lähetystä

# - Käyttöliittymä
#     - Anturien lisäys
#     - Tilamuutos?
#     - Lohkon vaihto
#     - Poistaa mittaustulos
#     - Näyttää anturien tiedot
#         - Tunniste
#         - Tila
#         - Viimeisin mitta-arvo ja aikaleima
#         - 10 uusinta
#         - Aikojen sorttaus
#     - Virhetilasta ajankohta

# - JSON formaatissa
# - Raportti

from lib.anturi import Sensor
from lib.halli import Factory
from lib.zone_control import *

sensor1.set_temp(22.22)
