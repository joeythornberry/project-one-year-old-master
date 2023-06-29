import pyautogui
import win32gui
import time
from shared import locations

from shared import private
import requests
import json

import logging

import threading
import queue

logging.basicConfig(level=logging.INFO, format='%(message)s')

IMAGE_PATH = "shared/images/"

STOP_BATTLING = "STOP_BATTLING"
EMOTE = "EMOTE"

NUMBER_OF_TOWERS = 3
TOKENS_FOR_DESTROYING_TOWER = 100
TOKENS_FOR_REMAINING_TOWER = 50
ELIXIR_SPENT_EVERY_SECOND = 0.357
TOKENS_FOR_SPENDING_ELIXIR = 1
UNDERESTIMATE_FOR_SAFETY = 0.95

def start_clan_battle():
    print("starting battle")
    pyautogui.moveTo(locations.locations["clan drag 1"])
    pyautogui.dragTo(locations.locations["clan drag 2"][0],locations.locations["clan drag 2"][1],0.5)
    battle_button = None
    while battle_button == None:
        time.sleep(1)
        battle_button = pyautogui.locateCenterOnScreen("shared/images/clan_battle.png",confidence = 0.8)
    pyautogui.click(battle_button)
        
    confirm_battle_button = None
    while confirm_battle_button == None:
        time.sleep(1)
        confirm_battle_button = pyautogui.locateCenterOnScreen("shared/images/confirm_clan_battle.png",confidence = 0.8)
    pyautogui.click(confirm_battle_button)

def fight_battles(end_battle_queue,emote_queue):
    
    start_clan_battle()

    while True:
        
        for i in range(4):
            pyautogui.click(locations.locations["card "+str(i+1)])
            pyautogui.click(locations.locations["target"])
            time.sleep(1)
        logging.info("fighting")

        logging.info("looking for emote request")
        try:
            if emote_queue.get_nowait() == EMOTE:
                emote()
        except:
            pass

        click_end_battle = pyautogui.locateCenterOnScreen(IMAGE_PATH+'end_of_battle_ok.png',grayscale = True, confidence = 0.8)
        if click_end_battle != None:
            pyautogui.click(click_end_battle)
            try:
                if end_battle_queue.get_nowait() == STOP_BATTLING:
                    break
            except:
                pass

            start_clan_battle()

def timer(end_battle_queue):

    counter = 0
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
            counter += 1
            if counter >= 3:
                #sleep so we always start a new battle after end conditions are met (otherwise sometimes it does and sometimes it doesn't, as it's impossible to ensure that the api updates fast enough to stop a new battle, but sometimes it will)
                time.sleep(10)
                end_battle_queue.put(STOP_BATTLING)   
                break

        time.sleep(30)

def emote_timer(emote_queue,end_battle_queue):
    while True:
        time.sleep(10)
        emote_queue.put(EMOTE)
        try:
            if end_battle_queue.get_nowait() == STOP_BATTLING:
                break
        except:
            pass
    
        
def fight_clan_battles():
    end_battle_queue = queue.Queue()
    emote_queue = queue.Queue()
    timer_thread = threading.Thread(target = timer, args = (end_battle_queue, ))
    emote_thread = threading.Thread(target = emote_timer, args = (emote_queue,end_battle_queue, ))
    timer_thread.start()
    emote_thread.start()
    fight_battles(end_battle_queue,emote_queue)

def emote():

    pyautogui.click(locations.locations["emote button"])
    time.sleep(.2)
    cry_button = None
    attempts = 0
    while cry_button == None and attempts < 4:
        time.sleep(.2)
        cry_button = pyautogui.locateCenterOnScreen(IMAGE_PATH+'cry.png',grayscale = True, confidence = 0.6)
        attempts += 1
    if cry_button != None:    
        pyautogui.click(cry_button)
        logging.info("emoting woo")



