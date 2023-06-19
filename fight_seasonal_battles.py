import threading
import queue

import pyautogui
import win32gui
import time
import get_location

import private
import requests
import json

import logging

logging.basicConfig(level=logging.INFO, format='%(message)s')

STOP_BATTLING = "STOP_BATTLING"

NUMBER_OF_TOWERS = 3
TOKENS_FOR_DESTROYING_TOWER = 100
TOKENS_FOR_REMAINING_TOWER = 50
ELIXIR_SPENT_EVERY_SECOND = 0.357
TOKENS_FOR_SPENDING_ELIXIR = 1
UNDERESTIMATE_FOR_SAFETY = 0.95

click_battle = {'name':"battle button",'location':(0.15,0.78)}
#click_confirm_battle = {'name':"confirm battle button",'location':(0.46,0.70)}
click_target = {'name':"target",'location':(0.22,0.32)}
click_cards = [{'name':"card 1",'location':(0.29,0.92)},{'name':"card 2",'location':(0.46,0.92)},{'name':"card 3",'location':(0.64,0.92)},{'name':"card 4",'location':(0.84,0.92)}]
#click_end_battle = {'name':"end battle button",'location':(0.50,0.88)}

def start_battle():
            click_battle_location = None
            while click_battle_location == None:
                time.sleep(1)
                click_battle_location = pyautogui.locateCenterOnScreen('seasonal_battle.png',grayscale = True, confidence = 0.9)
            pyautogui.click(click_battle_location)
            
            click_confirm_battle_location = None
            while click_confirm_battle_location == None:
                time.sleep(1)
                click_confirm_battle_location = pyautogui.locateCenterOnScreen('confirm_seasonal_battle.png',grayscale = True, confidence = 0.9)
            pyautogui.click(click_confirm_battle_location)



def fight_battles(end_battle_queue):
    
    #click_battle['location'] = get_location.get_location_pixels(click_battle['location'])
    #click_confirm_battle['location'] = get_location.get_location_pixels(click_confirm_battle['location'])
    click_target['location'] = get_location.get_location_pixels(click_target['location'])
    for click_card in click_cards:
        click_card['location'] = get_location.get_location_pixels(click_card['location'])
    #click_end_battle['location'] = get_location.get_location_pixels(click_end_battle['location'])
    
    start_battle()

    while True:
        
        for click_card in click_cards:
            pyautogui.click(click_card['location'])
            pyautogui.click(click_target['location'])
            time.sleep(1)
        logging.info("fighting")

        click_end_battle = pyautogui.locateCenterOnScreen('end_of_battle_ok.png',grayscale = True, confidence = 0.9)
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
