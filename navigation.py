import get_location
import pyautogui
import time

click_seasonal_button = {'name':"seasonal button", 'location':(0.84,0.99)}


click_off_popup = {'name':"get rid of popup",'location':(0.93,0.49)}

def get_to_seasonal_screen():
    click_seasonal_button['location'] = get_location.get_location_pixels(click_seasonal_button['location'])
    pyautogui.click(click_seasonal_button['location'])
    time.sleep(0.5)
    pyautogui.click(click_seasonal_button['location'])

click_home_button = {'name':"home_button",'location':(0.47,0.99)}


def get_to_home_screen():
    click_home_button['location'] = get_location.get_location_pixels(click_home_button['location'])
    pyautogui.click(click_home_button['location'])
    click_off_popup['location'] = get_location.get_location_pixels(click_off_popup['location'])
    pyautogui.click(click_off_popup['location'])


