"""
Ambulance GIS System - Main Entry Point

A desktop application for simulating ambulance navigation through a road network,
finding optimal paths based on distance and traffic congestion.
"""

import tkinter as tk
from tkinter import ttk
import csv

from config import paths, ui_config

window = tk.Tk()
window.configure(background=ui_config.BACKGROUND_COLOR)


def start() -> None:
    """
    Start the ambulance simulation.

    Reads source and destination locations from the UI, validates input,
    and launches the simulation with the specified parameters.
    """
    if (destination.get() == "" and source.get() == "") or (destination.get() == source.get()):
        print("empty/invalid inputs")

    with open(paths.POINTS_FILE, "r") as f:
        roads = csv.reader(f)
        next(roads)
        for row in roads:
            if destination.get() == row[6]:
                dest = (int(row[0]), int(row[1]))
            if source.get() == row[6]:
                sour = (int(row[0]), int(row[1]))
        s = int(speed.get())

    # calling the main funtion in main.py ... we have to make main_function in main.py
    import simulate as sim
    sim.main_function(sour, dest, s)


var = tk.StringVar()
var.set("Pulchowk")


lbl = tk.Label(window, text=ui_config.WINDOW_TITLE, fg='black', font=("Helvetica", 20),
               bg=ui_config.BACKGROUND_COLOR)
lbl.place(x=70, y=20)

lbl1 = tk.Label(window, text=">> Enter your location speed and destination", fg='black', font=("Helvetica", 8),
             bg=ui_config.BACKGROUND_COLOR)
lbl1.place(x=80, y=100)
lbl2 = tk.Label(window, text=">> See Realtime Traffic at different places", fg='black', font=("Helvetica", 8),
             bg=ui_config.BACKGROUND_COLOR)
lbl2.place(x=80, y=120)
lbl3 = tk.Label(window, text=">> Get the best path suggested in the map", fg='black', font=("Helvetica", 8),
             bg=ui_config.BACKGROUND_COLOR)
lbl3.place(x=80, y=140)

lbl4 = tk.Label(window, text="Destination", fg='black', font=("Helvetica", 10), bg=ui_config.BACKGROUND_COLOR)
lbl4.place(x=160, y=180)

destination = ttk.Combobox(window, values=ui_config.LOCATIONS)
destination.place(x=130, y=200)

lbl5 = tk.Label(window, text="Speed", fg='black', font=("Helvetica", 10), bg=ui_config.BACKGROUND_COLOR)
lbl5.place(x=160, y=230)
speed = tk.Entry()
speed.place(x=140, y=250)

lbl5 = tk.Label(window, text="Where are you?", fg='black', font=("Helvetica", 10), bg=ui_config.BACKGROUND_COLOR)
lbl5.place(x=150, y=280)

source = ttk.Combobox(window, values=ui_config.LOCATIONS)
source.place(x=130, y=300)

btn = tk.Button(window, text="Start Driving", fg='white', bg='black', command=start)
btn.place(x=160, y=400)

window.title(ui_config.WINDOW_TITLE)
window.geometry(ui_config.WINDOW_SIZE)
window.mainloop()
