import threading
import time
import pyautogui

def foo():
    for i in range(10):
        print("fooofooooo")
        pyautogui.moveTo(700,100)
        time.sleep(1)
foo_thread = threading.Thread(target = foo)
foo_thread.start()
for i in range(10):
    print("pnenll")
    pyautogui.moveTo(700,500)
    time.sleep(1)
