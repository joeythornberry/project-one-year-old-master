from battle import battle_navigation
from battle import fight_seasonal_battles
from shared import locations
import time

locations.coerce_window_size()
time.sleep(3)
locations.load_location_pixels()
battle_navigation.get_to_seasonal_screen()
fight_seasonal_battles.fight_seasonal_battles()
battle_navigation.get_to_home_screen()
