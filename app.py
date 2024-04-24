import platform
import subprocess
import tkinter as tk
from oldversion import utile as utile
import gesture.mouse_simulator as ms
import officialVersion.gesture_recognition as gs
from oldversion import camera as ca
from oldversion.cleanup import cleanup
from tkinter import messagebox, ttk
import configparser
#from playsound import playsound

import time
import os

settings = {
    "selected_camera": "",
    "selected_music_app": "",
    "hotkey": "",
    "hotkey2": "",
    "hotkey3": "",
    "hotkey4": "",
    "hotkey5": "",
}

hotkey_entry = tk.Entry

def start_mouse_simulation():
    ms.start_recognition()
    messagebox.showinfo("message", "simulation closed!")


def start_gesture_recognition():
    gs.start()
    messagebox.showinfo("message", "recognition closed!")

config = configparser.ConfigParser()

def load_settings(): #load from config file
    try:
        config.read('officialVersion/config.ini')
        settings["hotkey"] = config.get('hotkey', 'value')
        settings["hotkey2"] = config.get('hotkey2', 'value')
        settings["hotkey3"] = config.get('hotkey3', 'value')
        settings["hotkey4"] = config.get('hotkey4', 'value')
        settings["hotkey5"] = config.get('hotkey5', 'value')
    except Exception as e:
        messagebox.showerror('Error loading config, try saving settings first', f'fail {str(e)}')

load_settings()

def save_settings(selected_camera, selected_music_app, hotkey):
    # Update the global setting
    settings["selected_camera"] = selected_camera.get()
    settings["selected_music_app"] = selected_music_app.get()
    settings["hotkey"] = hotkey[0].get()
    settings["hotkey2"] = hotkey[1].get()
    settings["hotkey3"] = hotkey[2].get()
    settings["hotkey4"] = hotkey[3].get()
    settings["hotkey5"] = hotkey[4].get()

    config['hotkey'] = {'value': hotkey[0].get()}
    config['hotkey2'] = {'value': hotkey[1].get()}
    config['hotkey3'] = {'value': hotkey[2].get()}
    config['hotkey4'] = {'value': hotkey[3].get()}
    config['hotkey5'] = {'value': hotkey[4].get()}
    with open('officialVersion/config.ini', 'w') as configfile:
        config.write(configfile)
    messagebox.showinfo('Saved', 'Saved to file')

    messagebox.showinfo("Save Setting", "Configuration saved！")


def open_settings():
    
    # here to open the setting page
    settings_window = tk.Toplevel(root)
    settings_window.title("Setting")
    #settings_window.geometry("300x250")


    # Camera and music app
    avaible_camera = ca.find_available_cameras()
    camera_options = avaible_camera
    music_app_options = ["App music 1", "Spotify 2"]

    selected_camera = tk.StringVar()
    selected_music_app = tk.StringVar()
    hotkey_entry_var = [tk.StringVar(), tk.StringVar(), tk.StringVar(), tk.StringVar(), tk.StringVar()]

    # Rollback to previous saved setting
    selected_camera.set(camera_options[0] if camera_options else "No available Camera ")
    selected_music_app.set(settings["selected_music_app"] if settings["selected_music_app"] else music_app_options[0])
    hotkey_entry_var[0].set(settings["hotkey"])
    hotkey_entry_var[1].set(settings["hotkey2"])
    hotkey_entry_var[2].set(settings["hotkey3"])
    hotkey_entry_var[3].set(settings["hotkey4"])
    hotkey_entry_var[4].set(settings["hotkey5"])

    # Create UI
    tk.Label(settings_window, text="Select Camera:").grid(row=0, column=0, pady=10, padx=10, sticky="w")
    camera_menu = ttk.Combobox(settings_window, textvariable=selected_camera, values=camera_options)
    camera_menu.grid(row=0, column=1, padx=10, sticky="ew")

    tk.Label(settings_window, text="Select music app:").grid(row=1, column=0, pady=10, padx=10, sticky="w")
    music_app_menu = ttk.Combobox(settings_window, textvariable=selected_music_app, values=music_app_options)
    music_app_menu.grid(row=1, column=1, padx=10, sticky="ew")

    tk.Button(settings_window, text="Open App", command=launch_app ).grid(row=2, column=0, pady=10, padx=10, sticky="ew", columnspan=2)

    tk.Label(settings_window, text="Set hotkey 1:").grid(row=3, column=0, pady=10, padx=10, sticky="w")
    hotkey_entry = tk.Entry(settings_window, textvariable=hotkey_entry_var[0])
    hotkey_entry.grid(row=3, column=1, padx=10, sticky="ew")

    tk.Label(settings_window, text="Set hotkey 2:").grid(row=4, column=0, pady=10, padx=10, sticky="w")
    tk.Entry(settings_window, textvariable=hotkey_entry_var[1]).grid(row=4, column=1, padx=10, sticky="ew")

    tk.Label(settings_window, text="Set hotkey 3:").grid(row=5, column=0, pady=10, padx=10, sticky="w")
    tk.Entry(settings_window, textvariable=hotkey_entry_var[2]).grid(row=5, column=1, padx=10, sticky="ew")

    tk.Label(settings_window, text="Set hotkey 4:").grid(row=6, column=0, pady=10, padx=10, sticky="w")
    tk.Entry(settings_window, textvariable=hotkey_entry_var[3]).grid(row=6, column=1, padx=10, sticky="ew")

    tk.Label(settings_window, text="Set hotkey 5:").grid(row=7, column=0, pady=10, padx=10, sticky="w")
    tk.Entry(settings_window, textvariable=hotkey_entry_var[4]).grid(row=7, column=1, padx=10, sticky="ew")

    # Create save and back button
    save_button = tk.Button(settings_window, text="Save",
                            command=lambda: save_settings(selected_camera, selected_music_app, hotkey_entry_var))
    save_button.grid(row=8, column=0, pady=10, padx=10, sticky="ew")

    back_button = tk.Button(settings_window, text="Back", command=settings_window.destroy)
    back_button.grid(row=8, column=1, pady=10, padx=10, sticky="ew")

    settings_window.grid_columnconfigure(1, weight=1)


def exit_app():
    cleanup()
    root.destroy()
    exit(0)


def launch_app():
    spotify_path = utile.find_spotify_path()
    if spotify_path:
        print(f"Launching Spotify from: {spotify_path}")
        if platform.system() == "Darwin":  # macOS
            subprocess.Popen(["open", spotify_path])
        else:
            subprocess.Popen([spotify_path])
    else:
        print("Spotify installation not found.")


# Create the main windows
root = tk.Tk()
root.title("WavEase!")
#root.geometry("500x500")  # initial size
root.resizable(False, False)
#root.minsize(500, 300)
root.configure(background="#87CEEB")

# layout
#root.grid_columnconfigure([1, 2], weight=1, minsize=70)
# root.grid_columnconfigure(1, weight=1, minsize=70)

#root.grid_rowconfigure(0, weight=1, minsize=50)
#root.grid_rowconfigure(1, weight=1, minsize=10)
#root.grid_rowconfigure([2,3], weight=1, minsize=10) ## does not work for Mac
root.attributes('-alpha', 1.0) 

# Add a label
#label = tk.Label(root, text=r"""\
# __          __         _                                       _              __          __                  ______                        
# \ \        / /        | |                                     | |             \ \        / /                 |  ____|                       
#  \ \  /\  / /    ___  | |   ___    ___    _ __ ___     ___    | |_    ___      \ \  /\  / /    __ _  __   __ | |__      __ _   ___    ___   
#   \ \/  \/ /    / _ \ | |  / __|  / _ \  | '_ ` _ \   / _ \   | __|  / _ \      \ \/  \/ /    / _` | \ \ / / |  __|    / _` | / __|  / _ \  
#    \  /\  /    |  __/ | | | (__  | (_) | | | | | | | |  __/   | |_  | (_) |      \  /\  /    | (_| |  \ V /  | |____  | (_| | \__ \ |  __/  
#     \/  \/      \___| |_|  \___|  \___/  |_| |_| |_|  \___|    \__|  \___/        \/  \/      \__,_|   \_/   |______|  \__,_| |___/  \___|""", background='#c3c3c3')
label = tk.Label(root, text= r""" ༄ Welcome to WavEase ༄ """, background='#87CEEB', fg="white")
label.configure(font = ("Comic Sans MS", 28, "bold"))
label.grid(row=0, column=1, sticky="nsew", padx=20, pady=10, columnspan=2)

#tree graphic
frameCnt = 120
frames = [tk.PhotoImage(file='.assets/tree-01.gif',format = 'gif -index %i' %(i)) for i in range(frameCnt)]

def update(ind):

    frame = frames[ind]
    ind += 1
    if ind == frameCnt:
        ind = 0
    tree.configure(image=frame)
    root.after(100, update, ind)
tree = tk.Label(root, background='#87CEEB')
tree.grid(row=1, column=1, sticky="nsew", columnspan=2)
root.after(0, update, 0)

# Add Button
start_button = tk.Button(root, text="Start Recognition", 
                         command=start_gesture_recognition,
                         background='#87CEEB', fg="white")
start_button.grid(row=2, column=1, padx=8, pady=8, ipadx=30, ipady=5, sticky='ew')

mouse_button = tk.Button(root, text="Start Mouse Simulation", 
                         command=start_mouse_simulation,
                         background='#87CEEB', fg="white")
mouse_button.grid(row=2, column=2, padx=8, pady=8, ipadx=30, ipady=5, sticky='ew')

settings_button = tk.Button(root, text="Settings",
                             command=open_settings,
                             background='#87CEEB', fg="white")
settings_button.grid(row=3, column=1, padx=8, pady=8, ipadx=30, ipady=5, sticky='ew')

exit_button = tk.Button(root, text="Exit", 
                         command=exit_app,
                         background='#87CEEB', fg="white")
exit_button.grid(row=3, column=2, padx=8, pady=8, ipadx=30, ipady=5, sticky='ew')

#playsound('.assets/bird_audio.wav')
# start the evert loop
root.mainloop()
