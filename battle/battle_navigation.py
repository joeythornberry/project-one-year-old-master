from shared import locations
import pyautogui
import time

IMAGE_PATH = "shared/images/"

def clickx():
    x = pyautogui.locateCenterOnScreen(IMAGE_PATH+'x.png',grayscale = True, confidence = 0.8) 
    if x != None:
        pyautogui.click(x)

def get_to_seasonal_screen():
    pyautogui.click(locations.locations["seasonal button"])
    time.sleep(0.5)
    pyautogui.click(locations.locations["seasonal button"])

def get_to_home_screen():
    pyautogui.click(locations.locations["home button"])
    time.sleep(0.5)
    clickx()
    

def get_to_clan_screen():
    pyautogui.click(locations.locations["clan button"])
    time.sleep(0.5)
    clickx()
