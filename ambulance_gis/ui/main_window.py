"""
Ambulance GIS System - Main Window

The main application window with input controls for the simulation.
"""

import tkinter as tk
from tkinter import ttk, messagebox
import csv

from config import paths, ui_config
from ambulance_gis.utils.validators import (
    ValidationError,
    validate_location,
    validate_speed,
    validate_route,
)


def run() -> None:
    """Run the main application window."""
    window = tk.Tk()
    window.configure(background=ui_config.BACKGROUND_COLOR)

    def start() -> None:
        """
        Start the ambulance simulation.

        Reads source and destination locations from the UI, validates input,
        and launches the simulation with the specified parameters.
        """
        try:
            # Validate inputs
            validate_location(source.get(), "Source")
            validate_location(destination.get(), "Destination")
            validate_route(source.get(), destination.get())
            s = validate_speed(speed.get())

            # Parse coordinates from CSV
            sour = None
            dest = None

            with open(paths.POINTS_FILE, "r") as f:
                roads = csv.reader(f)
                next(roads)
                for row in roads:
                    if destination.get() == row[6]:
                        dest = (int(row[0]), int(row[1]))
                    if source.get() == row[6]:
                        sour = (int(row[0]), int(row[1]))

            if sour is None or dest is None:
                messagebox.showerror("Error", "Could not find coordinates for selected locations")
                return

            # Start the simulation
            from ambulance_gis.core.simulation import main_function
            main_function(sour, dest, s)

        except ValidationError as e:
            messagebox.showerror("Validation Error", e.message)
        except FileNotFoundError:
            messagebox.showerror("Error", f"Data file not found: {paths.POINTS_FILE}")
        except Exception as e:
            messagebox.showerror("Error", f"An unexpected error occurred: {str(e)}")

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

    lbl6 = tk.Label(window, text="Where are you?", fg='black', font=("Helvetica", 10), bg=ui_config.BACKGROUND_COLOR)
    lbl6.place(x=150, y=280)

    source = ttk.Combobox(window, values=ui_config.LOCATIONS)
    source.place(x=130, y=300)

    btn = tk.Button(window, text="Start Driving", fg='white', bg='black', command=start)
    btn.place(x=160, y=400)

    window.title(ui_config.WINDOW_TITLE)
    window.geometry(ui_config.WINDOW_SIZE)
    window.mainloop()


if __name__ == "__main__":
    run()
