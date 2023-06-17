import threading
import queue

import pyautogui
import win32gui
import time
import get_location

import requests
import json

import logging

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

STOP_BATTLING = "STOP_BATTLING"

developer_key = "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzUxMiIsImtpZCI6IjI4YTMxOGY3LTAwMDAtYTFlYi03ZmExLTJjNzQzM2M2Y2NhNSJ9.eyJpc3MiOiJzdXBlcmNlbGwiLCJhdWQiOiJzdXBlcmNlbGw6Z2FtZWFwaSIsImp0aSI6IjdjYmYwNjdiLTZmN2UtNDVjOC05NjI0LTEzYzdjMjlmYTJiZCIsImlhdCI6MTY4NTExODE5MSwic3ViIjoiZGV2ZWxvcGVyLzMwZmI2M2JmLWRlNjQtZDEwZS1kMGM1LWMyNzBkNmYyYTJkMiIsInNjb3BlcyI6WyJyb3lhbGUiXSwibGltaXRzIjpbeyJ0aWVyIjoiZGV2ZWxvcGVyL3NpbHZlciIsInR5cGUiOiJ0aHJvdHRsaW5nIn0seyJjaWRycyI6WyI3NC4xMTAuMTQ5LjE4NCJdLCJ0eXBlIjoiY2xpZW50In1dfQ.ZDebhTIIn48zsbqUYmGUJxKUJwbthhawog9n6PznTKONOzKbj-1957pbXRuSLlFhQlfi0QEg34UN4BBJGXTbeQ"
player_id_after_hashtag = "UR08UPU0J"

#click_battle = {'name':"battle button",'location':(0.15,0.78)}
#click_confirm_battle = {'name':"confirm battle button",'location':(0.46,0.70)}
click_target = {'name':"target",'location':(0.22,0.32)}
click_cards = [{'name':"card 1",'location':(0.29,0.92)},{'name':"card 2",'location':(0.46,0.92)},{'name':"card 3",'location':(0.64,0.92)},{'name':"card 4",'location':(0.84,0.92)}]
#click_end_battle = {'name':"end battle button",'location':(0.50,0.88)}

def fight_battles(end_battle_queue):
    
    #click_battle['location'] = get_location.get_location_pixels(click_battle['location'])
    #click_confirm_battle['location'] = get_location.get_location_pixels(click_confirm_battle['location'])
    click_target['location'] = get_location.get_location_pixels(click_target['location'])
    for click_card in click_cards:
        click_card['location'] = get_location.get_location_pixels(click_card['location'])
    #click_end_battle['location'] = get_location.get_location_pixels(click_end_battle['location'])
    
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

def timer(end_battle_queue):
    last_battle_time = None
    while True:
        logging.info("checking time of last completed battle")
        battle_log=requests.get("https://api.clashroyale.com/v1/players/%23"+player_id_after_hashtag+"/battlelog", headers={"Accept":"application/json", "authorization": "Bearer "+developer_key})
        battle_log = json.dumps(battle_log.json())
        battle_log = json.loads(battle_log) 

        if last_battle_time == None:
            last_battle_time = battle_log[0]["battleTime"]
        elif battle_log[0]["battleTime"] != last_battle_time:
            logging.info("stopping battle")

            #sleep so we always start a new battle after end conditions are met (otherwise sometimes it does and sometimes it doesn't, as it's impossible to ensure that the api updates fast enough to stop a new battle, but sometimes it will)
            time.sleep(10)
            end_battle_queue.put(STOP_BATTLING)   
            break

        time.sleep(30)
        
end_battle_queue = queue.Queue()
timer_thread = threading.Thread(target = timer, args = (end_battle_queue, ))
timer_thread.start()
fight_battles(end_battle_queue)
