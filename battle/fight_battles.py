import pyautogui
import time
import queue
import threading
import logging

from shared import locations

EMOTE = "EMOTE"
STOP_BATTLING = "STOP_BATTLING"

IMAGE_PATH = "shared/images/"

def fight_battles(end_battle_queue,emote_queue,start_new_battle):
    
    start_new_battle()

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

            start_new_battle()

def emote_timer(emote_queue,end_battle_queue):
    while True:
        time.sleep(10)
        emote_queue.put(EMOTE)
        try:
            if end_battle_queue.get_nowait() == STOP_BATTLING:
                break
        except:
            pass
    
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


def fight_battles_until_timer(start_new_battle,timer):
    end_battle_queue = queue.Queue()
    emote_queue = queue.Queue()
    timer_thread = threading.Thread(target = timer, args = (end_battle_queue, ))
    emote_thread = threading.Thread(target = emote_timer, args = (emote_queue,end_battle_queue, ))
    timer_thread.start()
    emote_thread.start()
    fight_battles(end_battle_queue,emote_queue,start_new_battle)
