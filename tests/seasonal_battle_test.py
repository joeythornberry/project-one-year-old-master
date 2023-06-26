from shared import locations
from battle import fight_seasonal_battles

import queue
import time
import threading

#fights one battle. start it on the seasonal screen.

locations.coerce_window_size()
time.sleep(5)
locations.load_location_pixels()


end_battle_queue = queue.Queue()
emote_queue = queue.Queue()
emote_thread = threading.Thread(target = fight_seasonal_battles.emote_timer,args = (emote_queue,end_battle_queue ))
end_battle_queue.put("STOP_BATTLING")
emote_thread.start()
fight_seasonal_battles.fight_battles(end_battle_queue,emote_queue)
