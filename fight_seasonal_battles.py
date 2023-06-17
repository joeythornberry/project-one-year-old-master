import threading
import queue

import pyautogui
import win32gui
import time
import get_location

STOP_BATTLING = "STOP_BATTLING"

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
        print("fighting",flush=True)
        
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
    for i in range(10):
        print("foo " + str(i),flush=True)
        time.sleep(1)
    end_battle_queue.put(STOP_BATTLING)    
        
end_battle_queue = queue.Queue()
timer_thread = threading.Thread(target = timer, args = (end_battle_queue, ))
timer_thread.start()
fight_battles(end_battle_queue)
