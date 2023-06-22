import navigation
import fight_seasonal_battles
import locations

locations.load_location_pixels()
navigation.get_to_seasonal_screen()
fight_seasonal_battles.fight_seasonal_battles()
navigation.get_to_home_screen()
