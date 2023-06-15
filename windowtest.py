import pyautogui
import win32gui
import time

def callback(hwnd, extra):
    rect = win32gui.GetWindowRect(hwnd)
    x = rect[0]
    y = rect[1]
    w = rect[2] - x
    h = rect[3] - y
    #print("Window %s:" % win32gui.GetWindowText(hwnd))
    title=win32gui.GetWindowText(hwnd)
    if title.startswith("NoxPlayer"):
        print("\tLocation: (%d, %d)" % (x, y))
        print("\t    Size: (%d, %d)" % (w, h))
        print("a")

        i = 20
        while i > 1:
            i -= 1
            pyautogui.click(x+w*.317, y+h*0.889)
            time.sleep(1)
            pyautogui.click(x+w*.217, y+h*0.328)
            time.sleep(1)
            pyautogui.click(x+w*.483, y+h*0.889)
            time.sleep(1)
            pyautogui.click(x+w*.217, y+h*0.328)
            time.sleep(1)
            pyautogui.click(x+w*.65, y+h*0.889)
            time.sleep(1)
            pyautogui.click(x+w*.217, y+h*0.328)
            time.sleep(1)
            pyautogui.click(x+w*.217, y+h*0.889)
            time.sleep(1)
            pyautogui.click(x+w*.720, y+h*0.328)
            time.sleep(1)

408, 366

def main():
    win32gui.EnumWindows(callback, None)

if __name__ == '__main__':
    main()