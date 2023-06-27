import pyautogui
import time
from shared import locations

def start_battle():
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
