import win32gui
from win32api import GetSystemMetrics
import logging
from shared import private
from shared import emulators
import pyautogui

DEFAULT_NOX_HEIGHT = 1012
DEFAULT_NOX_WIDTH = 592
#592,1012 are default nox window size
def coerce_window_size_callback(handle,extras):
    if win32gui.GetWindowText(handle).startswith(private.emulator):
        starting_window_rect = win32gui.GetWindowRect(handle)
        window_rect = list(starting_window_rect)
        window_rect[1] = 0
        window_rect[3] = DEFAULT_NOX_HEIGHT
        window_rect[0] = 0
        window_rect[2] = DEFAULT_NOX_WIDTH
        #this is for if you don't want to disable ads on bluestacks (they change the size)
        """
        if private.emulator == emulators.BLUESTACKS:
            ad_width = round((window_rect[2]-window_rect[0])*(0.37 + 0.15))
            window_rect[2] += ad_width
        """    
        win32gui.MoveWindow(handle,window_rect[0],window_rect[1],window_rect[2],window_rect[3],True)

def coerce_window_size():
    win32gui.EnumWindows(coerce_window_size_callback,None)

locations = {"battle button":(0.15,0.78),"target":(0.23, 0.24),"card 1":(0.29,0.92),"card 2":(0.46,0.92),"card 3":(0.64,0.92),"card 4":(0.84,0.92),"seasonal button":(0.84,0.99),"get rid of popup":(0.93,0.49),"home button":(0.47,0.99),"clan button":(0.76,0.99),"emote button":(0.09, 0.83),"clan drag 1":(0.5,0.5),"clan drag 2":(0.5,0.7)}

def get_window_dimensions_callback(handle,extras):
    if win32gui.GetWindowText(handle).startswith(private.emulator):
        window_rect = list(win32gui.GetWindowRect(handle))
        logging.debug(window_rect)
        #this is for if you don't disable ads on bluestacks (they change the size)
        """
        if private.emulator == emulators.BLUESTACKS:
            ad_width = (window_rect[2]-window_rect[0])*(0.39)
            window_rect[0] += ad_width
        """    
        extras["window_rect"] = window_rect
        
def load_location_pixels():
    """given a tuple containing a location on the window (two numbers between 0 and 1, starting from top left), returns the actual pixel location as a tuple"""
    
    extras = {"window_rect": None}
    win32gui.EnumWindows(get_window_dimensions_callback,extras)
    
    if(extras["window_rect"] == None):
        raise Exception("window not found")
    
    window_rect = extras["window_rect"]
    
    window_size = (window_rect[2]-window_rect[0],window_rect[3]-window_rect[1])

    for location_key in locations.keys():
        location = locations[location_key]
        #location to pixel formula: window location (top left) + (window size * location)
        pixels = (round(window_rect[0]+location[0]*window_size[0]),round(window_rect[1]+window_size[1]*location[1]))
    
        if location[0]<0 or location[0]>1 or location[1]<0 or location[1]>1:
            raise Exception("location is not on window")

        if pixels[0]<0 or pixels[0]>GetSystemMetrics(0) or pixels[1]<0 or pixels[1]>GetSystemMetrics(1):
           raise Exception(f"{location} produces {pixels}, which is not on screen")

        locations[location_key] = pixels

