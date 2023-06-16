import pyautogui
import win32gui
import logging

logging.basicConfig(level=logging.DEBUG, format='%(asctime)s - %(levelname)s - %(message)s')

DECIMAL_POINTS = 2

def mouse_location_relative_to_window_callback(handle,extras):
  if win32gui.GetWindowText(handle).startswith(extras['name']):
      
    screen_dimensions = win32gui.GetWindowRect(handle)
    window_rect = win32gui.GetWindowRect(handle)
    window_size = (window_rect[2]-window_rect[0],window_rect[3]-window_rect[1])
    logging.debug(window_rect)
    
    position = pyautogui.position()
    logging.debug(position)
    
    position_relative_to_window = (position[0]-window_rect[0],position[1]-window_rect[1])
    logging.debug(position_relative_to_window)
    
    if position_relative_to_window[0] > 0 and position_relative_to_window[0] < window_size[0] and position_relative_to_window[1] > 0 and position_relative_to_window[1] < window_size[1]:
      extras['location_relative_to_window'] = (round(position_relative_to_window[0]/window_size[0],DECIMAL_POINTS),round(position_relative_to_window[1]/window_size[1],DECIMAL_POINTS))


def get_location_relative_to_window():
  extras = {'name':"NoxPlayer",'location_relative_to_window':None} 
  win32gui.EnumWindows(mouse_location_relative_to_window_callback,extras)
  return extras['location_relative_to_window']

print(get_location_relative_to_window())
