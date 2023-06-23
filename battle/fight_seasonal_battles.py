import threading
import queue

import pyautogui
import win32gui
import time
from shared import locations

from shared import private
import requests
import json

import logging

logging.basicConfig(level=logging.INFO, format='%(message)s')

IMAGE_PATH = "shared/images/"

STOP_BATTLING = "STOP_BATTLING"

NUMBER_OF_TOWERS = 3
TOKENS_FOR_DESTROYING_TOWER = 100
TOKENS_FOR_REMAINING_TOWER = 50
ELIXIR_SPENT_EVERY_SECOND = 0.357
TOKENS_FOR_SPENDING_ELIXIR = 1
UNDERESTIMATE_FOR_SAFETY = 0.95

def start_battle():
            click_battle_location = None
            while click_battle_location == None:
                time.sleep(1)
                click_battle_location = pyautogui.locateCenterOnScreen(IMAGE_PATH+'seasonal_battle.png',grayscale = True, confidence = 0.9)
            pyautogui.click(click_battle_location)
            
            click_confirm_battle_location = None
            while click_confirm_battle_location == None:
                time.sleep(1)
                click_confirm_battle_location = pyautogui.locateCenterOnScreen(IMAGE_PATH+'confirm_seasonal_battle.png',grayscale = True, confidence = 0.9)
            pyautogui.click(click_confirm_battle_location)



def fight_battles(end_battle_queue):
    
    start_battle()

    while True:
        
        for i in range(3):
            pyautogui.click(locations.locations["card "+str(i+1)])
            pyautogui.click(locations.locations["target"])
            time.sleep(1)
        logging.info("fighting")

        click_end_battle = pyautogui.locateCenterOnScreen(IMAGE_PATH+'end_of_battle_ok.png',grayscale = True, confidence = 0.9)
        if click_end_battle != None:
            pyautogui.click(click_end_battle)

            try:
                if end_battle_queue.get_nowait() == STOP_BATTLING:
                    break
            except:
                pass

            start_battle()

def timer(end_battle_queue):

    seasonal_tokens_needed = 1000
    start_time = time.time()

    last_battle_time = None
    while True:
        logging.info("checking time of last completed battle")
        battle_log=requests.get("https://api.clashroyale.com/v1/players/%23"+private.player_id_after_hashtag+"/battlelog", headers={"Accept":"application/json", "authorization": "Bearer "+private.developer_key})
        battle_log = json.dumps(battle_log.json())
        battle_log = json.loads(battle_log) 

        if last_battle_time == None:
            last_battle_time = battle_log[0]["battleTime"]
        elif battle_log[0]["battleTime"] != last_battle_time:
            
            last_battle_time = battle_log[0]["battleTime"]

            crowns = battle_log[0]["team"][0]["crowns"]
            opponent_crowns = battle_log[0]["opponent"][0]["crowns"]
            time_of_battle = time.time() - start_time

            tokens_for_destroying_towers = crowns*TOKENS_FOR_DESTROYING_TOWER
            tokens_for_remaining_towers = (NUMBER_OF_TOWERS-opponent_crowns)*TOKENS_FOR_REMAINING_TOWER
            tokens_for_spending_elixir = time_of_battle*ELIXIR_SPENT_EVERY_SECOND*TOKENS_FOR_SPENDING_ELIXIR
            tokens_gained = round((tokens_for_destroying_towers+tokens_for_remaining_towers+tokens_for_spending_elixir)*UNDERESTIMATE_FOR_SAFETY)

            
            seasonal_tokens_needed -= tokens_gained
            logging.info(f"estimated {tokens_gained} tokens gained: {seasonal_tokens_needed} left")

            if seasonal_tokens_needed <= 0:
                #sleep so we always start a new battle after end conditions are met (otherwise sometimes it does and sometimes it doesn't, as it's impossible to ensure that the api updates fast enough to stop a new battle, but sometimes it will)
                time.sleep(10)
                end_battle_queue.put(STOP_BATTLING)   
                break

        time.sleep(30)
        
def fight_seasonal_battles():
    end_battle_queue = queue.Queue()
    timer_thread = threading.Thread(target = timer, args = (end_battle_queue, ))
    timer_thread.start()
    fight_battles(end_battle_queue)

