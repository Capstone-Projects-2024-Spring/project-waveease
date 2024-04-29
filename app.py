import platform
import subprocess
import tkinter as tk
import oldversion.camera as ca
import oldversion.utile as utile
import gesture.mouse_simulator as ms
import officialVersion.gesture_recognition as gs
import oldversion.cleanup as cleanup
import tkinter.messagebox as messagebox
import tkinter.ttk as ttk
import configparser
from playsound import playsound

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

recognitior = gs.GestureRecognition()


def start_mouse_simulation():
    ms.start_recognition()
    messagebox.showinfo("message", "simulation closed!")


def show_tutorial():
    tutorial_window = tk.Toplevel(root)
    tutorial_window.title("Tutorial")
    tutorial_window.geometry("600x400")
    tutorial_window.configure(bg="#f0f0f0")

    scrollbar = tk.Scrollbar(tutorial_window)
    scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

    text_widget = tk.Text(tutorial_window, wrap=tk.WORD, yscrollcommand=scrollbar.set,
                          font=("Helvetica", 14), bg="#ffffff", fg="#333333")
    text_widget.pack(expand=True, fill='both', padx=20, pady=20)

    tutorial_text = """
    1. Move the mouse: Extend your right hand palm to move (note that it is the right hand).
    2. Left mouse button: Keep your fingers upward, use your index finger and thumb to touch; keep the other fingers upward, this is the left click.
    3. Right mouse button: Similarly, use your middle finger and thumb to touch.
    4. Drag, hold the left button: Make a fist, then extend your thumb to trigger the drag mode, moving with the thumb as the coordinate. Switch to using your palm to engage the drag mode.
    """
    text_widget.insert(tk.END, tutorial_text)
    text_widget.config(state='disabled')

    scrollbar.config(command=text_widget.yview)


def start_gesture_recognition():
    recognitior.start()
    messagebox.showinfo("message", "recognition closed!")


config = configparser.ConfigParser()


def load_settings():  # load from config file
    try:
        config.read('officialVersion/config.ini')
        settings["hotkey"] = config.get('hotkey', 'value')
        settings["hotkey2"] = config.get('hotkey2', 'value')
        settings["hotkey3"] = config.get('hotkey3', 'value')
        settings["hotkey4"] = config.get('hotkey4', 'value')
        settings["hotkey5"] = config.get('hotkey5', 'value')
    except Exception as e:
        messagebox.showerror('config file not exist, will load from preset file', f'fail {str(e)}')


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


def load_preset(preset, hotkey_entry_var):
    config2 = configparser.ConfigParser()
    config2.read('officialVersion/preset.ini')
    try:
        hotkey_entry_var[0].set(config2.get(preset, 'h1'))
        hotkey_entry_var[1].set(config2.get(preset, 'h2'))
        hotkey_entry_var[2].set(config2.get(preset, 'h3'))
        hotkey_entry_var[3].set(config2.get(preset, 'h4'))
        hotkey_entry_var[4].set(config2.get(preset, 'h5'))
    except Exception as e:
        messagebox.showerror('Error to load preset file', f'fail {str(e)}')

def save_preset(preset, hotkey):
    config2 = configparser.ConfigParser()
    config2.read('officialVersion/preset.ini')
    config2[preset.get()] = {
        'preset': preset.get(),
        'h1': hotkey[0].get(),
        'h2': hotkey[1].get(),
        'h3': hotkey[2].get(),
        'h4': hotkey[3].get(),
        'h5': hotkey[4].get()
    }
    with open('officialVersion/preset.ini', 'w') as configfile:
        config2.write(configfile)
    messagebox.showinfo(preset.get(), 'New preset saved')


def open_settings():
    load_settings()

    # here to open the setting page
    settings_window = tk.Toplevel(root)
    settings_window.title("Setting")
    # settings_window.geometry("300x250")

    # Camera and music app
    avaible_camera = ca.find_available_cameras()
    camera_options = avaible_camera
    music_app_options = ["App music 1", "Spotify 2"]

    selected_camera = tk.StringVar()
    selected_music_app = tk.StringVar()
    hotkey_entry_var = [tk.StringVar(), tk.StringVar(), tk.StringVar(), tk.StringVar(), tk.StringVar()]
    preset = tk.StringVar()

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

    tk.Button(settings_window, text="Open App", command=launch_app).grid(row=2, column=0, pady=10, padx=10, sticky="ew",
                                                                         columnspan=2)

    tk.Label(settings_window, text="👆Set hotkey 1:").grid(row=3, column=0, pady=10, padx=10, sticky="w")
    hotkey_entry = tk.Entry(settings_window, textvariable=hotkey_entry_var[0])
    hotkey_entry.grid(row=3, column=1, padx=10, sticky="ew")

    tk.Label(settings_window, text="👇Set hotkey 2:").grid(row=4, column=0, pady=10, padx=10, sticky="w")
    tk.Entry(settings_window, textvariable=hotkey_entry_var[1]).grid(row=4, column=1, padx=10, sticky="ew")

    tk.Label(settings_window, text="🤙Set hotkey 3:").grid(row=5, column=0, pady=10, padx=10, sticky="w")
    tk.Entry(settings_window, textvariable=hotkey_entry_var[2]).grid(row=5, column=1, padx=10, sticky="ew")

    tk.Label(settings_window, text="💅Set hotkey 4:").grid(row=6, column=0, pady=10, padx=10, sticky="w")
    tk.Entry(settings_window, textvariable=hotkey_entry_var[3]).grid(row=6, column=1, padx=10, sticky="ew")

    tk.Label(settings_window, text="✋Set hotkey 5:").grid(row=7, column=0, pady=10, padx=10, sticky="w")
    tk.Entry(settings_window, textvariable=hotkey_entry_var[4]).grid(row=7, column=1, padx=10, sticky="ew")

    tk.Label(settings_window, text="🤘Preset Settings").grid(row=8, column=0, pady=10, padx=10, sticky="ew",
                                                            columnspan=2, rowspan=2)
    tk.Button(settings_window, text="Default", command=lambda: load_preset('default', hotkey_entry_var)).grid(row=10,
                                                                                                              column=0,
                                                                                                              pady=10,
                                                                                                              padx=10,
                                                                                                              sticky="ew")
    tk.Button(settings_window, text="PowerPoint", command=lambda: load_preset('powerpoint', hotkey_entry_var)).grid(
        row=10, column=1, pady=10, padx=10, sticky="ew")
    tk.Entry(settings_window, textvariable=preset).grid(row=11, column=0, padx=10, sticky="ew", columnspan=2)
    tk.Button(settings_window, text="Load", command=lambda: load_preset(preset.get(), hotkey_entry_var)).grid(row=12,
                                                                                                              column=0,
                                                                                                              pady=10,
                                                                                                              padx=10,
                                                                                                              sticky="ew")
    tk.Button(settings_window, text="Save New", command=lambda: save_preset(preset, hotkey_entry_var)).grid(row=12,
                                                                                                            column=1,
                                                                                                            pady=10,
                                                                                                            padx=10,
                                                                                                            sticky="ew")

    tk.Label(settings_window, text="‧₊˚ ☁️⋅♡𓂃 ࣪ ִֶָ☾. ⋆｡°•☁️.").grid(row=13, column=0, pady=10, padx=10, sticky="ew",
                                                                     columnspan=2)

    # Create save and back button
    save_button = tk.Button(settings_window, text="Save",
                            command=lambda: save_settings(selected_camera, selected_music_app, hotkey_entry_var))
    save_button.grid(row=14, column=0, pady=10, padx=10, sticky="ew")

    back_button = tk.Button(settings_window, text="Back", command=settings_window.destroy)
    back_button.grid(row=14, column=1, pady=10, padx=10, sticky="ew")

    settings_window.grid_columnconfigure(1, weight=1)


def exit_app():
    cleanup.cleanup()
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
# root.geometry("500x500")  # initial size
root.resizable(False, False)
# root.minsize(500, 300)
root.configure(background="#87CEEB")

# layout
# root.grid_columnconfigure([1, 2], weight=1, minsize=70)
# root.grid_columnconfigure(1, weight=1, minsize=70)

# root.grid_rowconfigure(0, weight=1, minsize=50)
# root.grid_rowconfigure(1, weight=1, minsize=10)
# root.grid_rowconfigure([2,3], weight=1, minsize=10) ## does not work for Mac
root.attributes('-alpha', 1.0)

# Add a label
# label = tk.Label(root, text=r"""\
# __          __         _                                       _              __          __                  ______                        
# \ \        / /        | |                                     | |             \ \        / /                 |  ____|                       
#  \ \  /\  / /    ___  | |   ___    ___    _ __ ___     ___    | |_    ___      \ \  /\  / /    __ _  __   __ | |__      __ _   ___    ___   
#   \ \/  \/ /    / _ \ | |  / __|  / _ \  | '_ ` _ \   / _ \   | __|  / _ \      \ \/  \/ /    / _` | \ \ / / |  __|    / _` | / __|  / _ \  
#    \  /\  /    |  __/ | | | (__  | (_) | | | | | | | |  __/   | |_  | (_) |      \  /\  /    | (_| |  \ V /  | |____  | (_| | \__ \ |  __/  
#     \/  \/      \___| |_|  \___|  \___/  |_| |_| |_|  \___|    \__|  \___/        \/  \/      \__,_|   \_/   |______|  \__,_| |___/  \___|""", background='#c3c3c3')
label = tk.Label(root, text=r""" ༄ Welcome to WavEase ༄ """, background='#87CEEB', fg="white")
label.configure(font=("Comic Sans MS", 28, "bold"))
label.grid(row=0, column=1, sticky="nsew", padx=20, pady=10, columnspan=2)

# tree graphic
frameCnt = 120
frames = [tk.PhotoImage(file='.assets/tree-01.gif', format='gif -index %i' % (i)) for i in range(frameCnt)]


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

tutorial_button = tk.Button(root, text="Show Tutorial",
                            command=show_tutorial,
                            background='#87CEEB', fg="white")
tutorial_button.grid(row=2, column=3, padx=8, pady=8, ipadx=30, ipady=5, sticky='ew')

settings_button = tk.Button(root, text="Settings",
                            command=open_settings,
                            background='#87CEEB', fg="white")
settings_button.grid(row=3, column=1, padx=8, pady=8, ipadx=30, ipady=5, sticky='ew')

exit_button = tk.Button(root, text="Exit",
                        command=exit_app,
                        background='#87CEEB', fg="white")
exit_button.grid(row=3, column=2, padx=8, pady=8, ipadx=30, ipady=5, sticky='ew')

playsound('.assets/bird_audio.wav')
# start the evert loop
root.mainloop()
