import pyautogui
import win32gui
import time
import get_location

click_battle = {'name':"battle button",'location':(0.15,0.78)}
click_confirm_battle = {'name':"confirm battle button",'location':(0.46,0.70)}
click_target = {'name':"target",'location':(0.22,0.32)}
click_cards = [{'name':"card 1",'location':(0.29,0.92)},{'name':"card 2",'location':(0.46,0.92)},{'name':"card 3",'location':(0.64,0.92)},{'name':"card 4",'location':(0.84,0.92)}]
click_end_battle = {'name':"end battle button",'location':(0.50,0.88)}

def fight_battle():
    
    click_battle['location'] = get_location.get_location_pixels(click_battle['location'])
    click_confirm_battle['location'] = get_location.get_location_pixels(click_confirm_battle['location'])
    click_target['location'] = get_location.get_location_pixels(click_target['location'])
    for click_card in click_cards:
        click_card['location'] = get_location.get_location_pixels(click_card['location'])
    click_end_battle['location'] = get_location.get_location_pixels(click_end_battle['location'])
    
    while True:
        pyautogui.click(click_battle['location'])
        time.sleep(1)
        pyautogui.click(click_confirm_battle['location'])
        for click_card in click_cards:
            pyautogui.click(click_card['location'])
            pyautogui.click(click_target['location'])
        pyautogui.click(click_end_battle['location'])
        time.sleep(5)

fight_battle()
