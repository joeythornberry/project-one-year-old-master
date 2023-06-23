from shared import locations
import pyautogui
import time

def get_to_seasonal_screen():
    pyautogui.click(locations.locations["seasonal button"])
    time.sleep(0.5)
    pyautogui.click(locations.locations["seasonal button"])

def get_to_home_screen():
    pyautogui.click(locations.locations["home button"])
    time.sleep(0.5)
    pyautogui.click(locations.locations["get rid of popup"])

def get_to_clan_screen():
    pyautogui.click(locations.locations["clan button"])
    time.sleep(0.5)
    
