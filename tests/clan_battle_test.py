from shared import locations
from battle import fight_clan_battles
import time

locations.coerce_window_size()
time.sleep(3)
locations.load_location_pixels()

fight_clan_battles.start_battle()
