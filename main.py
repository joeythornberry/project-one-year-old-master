from battle import battle_navigation
from battle import fight_clan_battles
from battle import fight_seasonal_battles
from battle import fight_battles
from shared import locations
import time

locations.coerce_window_size()
time.sleep(3)
locations.load_location_pixels()
battle_navigation.get_to_clan_screen()
fight_battles.fight_battles_until_timer(fight_clan_battles.start_clan_battle,fight_clan_battles.timer)
battle_navigation.get_to_home_screen()
