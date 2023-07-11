import tkinter as tk
import json
import logging

logging.basicConfig(level=logging.INFO)

window = tk.Tk()
window.title("Simple GUI")

logging.info("loading control data")
try:
    with open('user_data.json','r') as user_data:
        json_data = user_data.read()
    logging.info("data loaded successfully")
except:
    logging.info("error opening file: resetting to default. sorry you lost all your data!")
    blank_json_user_data = '{"api_key": null, "users": [{"id_state": "n/a", "id_entry": null, "clan_state": 0, "clan_entry": null, "seasonal_state": 0, "seasonal_entry": null}, {"id_state": "n/a", "id_entry": null, "clan_state": 0, "clan_entry": null, "seasonal_state": 0, "seasonal_entry": null}, {"id_state": "n/a", "id_entry": null, "clan_state": 0, "clan_entry": null, "seasonal_state": 0, "seasonal_entry": null}, {"id_state": "n/a", "id_entry": null, "clan_state": 0, "clan_entry": null, "seasonal_state": 0, "seasonal_entry": null}, {"id_state": "n/a", "id_entry": null, "clan_state": 0, "clan_entry": null, "seasonal_state": 0, "seasonal_entry": null}, {"id_state": "n/a", "id_entry": null, "clan_state": 0, "clan_entry": null, "seasonal_state": 0, "seasonal_entry": null}, {"id_state": "n/a", "id_entry": null, "clan_state": 0, "clan_entry": null, "seasonal_state": 0, "seasonal_entry": null}, {"id_state": "n/a", "id_entry": null, "clan_state": 0, "clan_entry": null, "seasonal_state": 0, "seasonal_entry": null}, {"id_state": "n/a", "id_entry": null, "clan_state": 0, "clan_entry": null, "seasonal_state": 0, "seasonal_entry": null}]}'

    logging.info("writing default settings to file")
    with open('user_data.json','w') as user_data:
        json_data = json.loads(blank_json_user_data)
        json.dump(json_data,user_data,indent=None)
    
    logging.info("loading new data")
    with open('user_data.json','r') as user_data:
        json_data = user_data.read()
    
data = json.loads(json_data)
    
logging.info("loading control data into GUI")
for user in data["users"]:
    label = tk.Label(window,text="user id:")
    label.pack()
    user["id_state"] = tk.StringVar(value=user["id_state"])
    user["id_entry"] = tk.Entry(window,textvariable=user["id_state"])
    user["id_entry"].pack()

    user["clan_state"] = tk.IntVar(value=user["clan_state"])
    user["clan_entry"] = tk.Checkbutton(window,text="fight clan battles",variable=user["clan_state"])
    user["clan_entry"].pack()
    
    user["seasonal_state"] = tk.IntVar(value=user["seasonal_state"])
    user["seasonal_entry"] = tk.Checkbutton(window,text="fight seasonal battles",variable=user["seasonal_state"])
    user["seasonal_entry"].pack()

def submit():
    for user in data["users"]:
        user["id_state"] = user["id_state"].get()
        user["id_entry"] = None
        
        user["clan_state"] = user["clan_state"].get()
        user["clan_entry"] = None
        
        user["seasonal_state"] = user["seasonal_state"].get()
        user["seasonal_entry"] = None

    with open('user_data.json','w') as user_data:
        json.dump(data,user_data)
        
        window.destroy()
    
submit_button = tk.Button(window, text="Fight Battles", command=submit)
submit_button.pack()

window.mainloop()
