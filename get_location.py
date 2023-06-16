import win32gui
from win32api import GetSystemMetrics
import logging

logging.basicConfig(level=logging.DEBUG, format='%(levelname)s: %(message)s')

def get_window_dimensions_callback(handle,extras):
    if win32gui.GetWindowText(handle).startswith("Anaconda"):
        window_rect = win32gui.GetWindowRect(handle)
        logging.debug(window_rect)
        extras["window_rect"] = window_rect
        
def get_location_pixels(location):
    """given a tuple containing a location on the window (two numbers between 0 and 1, starting from top left), returns the actual pixel location as a tuple"""
    
    if location[0]<0 or location[0]>1 or location[1]<0 or location[1]>1:
        raise Exception("location is not on window")

    extras = {"window_rect": None}
    win32gui.EnumWindows(get_window_dimensions_callback,extras)
    
    if(extras["window_rect"] == None):
        raise Exception("window not found")
    
    window_rect = extras["window_rect"]
    
    window_size = (window_rect[2]-window_rect[0],window_rect[3]-window_rect[1])

    #location to pixel formula: window location (top left) + (window size * location)
    pixels = (window_rect[0]+location[0]*window_size[0],window_rect[1]+window_size[1]*location[1])
    
    if pixels[0]<0 or pixels[0]>GetSystemMetrics(0) or pixels[1]<0 or pixels[1]>GetSystemMetrics(1):
       raise Exception("location not on screen")

    return pixels
