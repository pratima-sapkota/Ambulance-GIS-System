"""
Ambulance GIS System - Main Window

The main application window with input controls for the simulation.
Uses grid layout and ttk themed widgets for a modern look.
"""

import tkinter as tk
from tkinter import ttk, messagebox
import csv
from typing import Optional, Tuple

from config import paths, ui_config
from ambulance_gis.utils.validators import (
    ValidationError,
    validate_location,
    validate_speed,
    validate_route,
)


class MainWindow:
    """
    Main application window for the Ambulance GIS System.

    Uses ttk themed widgets and grid layout for a modern,
    responsive interface.

    Attributes:
        window: The root Tk window.
        source: Combobox for source location selection.
        destination: Combobox for destination location selection.
        speed: Entry for speed input.
    """

    def __init__(self) -> None:
        """Initialize the main window."""
        self.window = tk.Tk()
        self.window.title(ui_config.WINDOW_TITLE)
        self.window.geometry(ui_config.WINDOW_SIZE)
        self.window.configure(background=ui_config.BACKGROUND_COLOR)

        # Configure ttk style
        self._setup_style()

        # Configure grid weights for responsiveness
        self.window.columnconfigure(0, weight=1)
        self.window.columnconfigure(1, weight=2)

        # Build the UI
        self._create_widgets()

    def _setup_style(self) -> None:
        """Configure ttk styling for a modern look."""
        style = ttk.Style()
        style.theme_use('clam')

        # Configure common styles
        style.configure(
            'TLabel',
            background=ui_config.BACKGROUND_COLOR,
            font=('Helvetica', 10)
        )
        style.configure(
            'Title.TLabel',
            background=ui_config.BACKGROUND_COLOR,
            font=('Helvetica', 20, 'bold')
        )
        style.configure(
            'Info.TLabel',
            background=ui_config.BACKGROUND_COLOR,
            font=('Helvetica', 9)
        )
        style.configure(
            'TButton',
            font=('Helvetica', 10),
            padding=10
        )
        style.configure(
            'TCombobox',
            padding=5
        )
        style.configure(
            'TEntry',
            padding=5
        )

    def _create_widgets(self) -> None:
        """Create and layout all widgets."""
        # Title
        title_label = ttk.Label(
            self.window,
            text=ui_config.WINDOW_TITLE,
            style='Title.TLabel'
        )
        title_label.grid(row=0, column=0, columnspan=2, pady=(20, 10))

        # Info section
        info_frame = ttk.Frame(self.window)
        info_frame.grid(row=1, column=0, columnspan=2, pady=(0, 20), padx=20, sticky='w')

        info_texts = [
            ">> Enter your location, speed and destination",
            ">> See realtime traffic at different places",
            ">> Get the best path suggested in the map",
        ]

        for i, text in enumerate(info_texts):
            info_label = ttk.Label(info_frame, text=text, style='Info.TLabel')
            info_label.grid(row=i, column=0, sticky='w', pady=2)

        # Form section - using a frame for better organization
        form_frame = ttk.Frame(self.window)
        form_frame.grid(row=2, column=0, columnspan=2, pady=10, padx=40)
        form_frame.columnconfigure(1, weight=1)

        # Source (Where are you?)
        source_label = ttk.Label(form_frame, text="Source:")
        source_label.grid(row=0, column=0, sticky='e', padx=(0, 10), pady=10)

        self.source = ttk.Combobox(
            form_frame,
            values=ui_config.LOCATIONS,
            state='readonly',
            width=20
        )
        self.source.grid(row=0, column=1, sticky='w', pady=10)

        # Destination
        dest_label = ttk.Label(form_frame, text="Destination:")
        dest_label.grid(row=1, column=0, sticky='e', padx=(0, 10), pady=10)

        self.destination = ttk.Combobox(
            form_frame,
            values=ui_config.LOCATIONS,
            state='readonly',
            width=20
        )
        self.destination.grid(row=1, column=1, sticky='w', pady=10)

        # Speed
        speed_label = ttk.Label(form_frame, text="Speed:")
        speed_label.grid(row=2, column=0, sticky='e', padx=(0, 10), pady=10)

        self.speed = ttk.Entry(form_frame, width=23)
        self.speed.grid(row=2, column=1, sticky='w', pady=10)

        # Speed hint
        speed_hint = ttk.Label(
            form_frame,
            text="(1-200 units)",
            style='Info.TLabel'
        )
        speed_hint.grid(row=2, column=2, sticky='w', padx=(5, 0))

        # Start button
        button_frame = ttk.Frame(self.window)
        button_frame.grid(row=3, column=0, columnspan=2, pady=30)

        start_button = ttk.Button(
            button_frame,
            text="Start Driving",
            command=self._on_start_click
        )
        start_button.grid(row=0, column=0)

    def _get_coordinates(self, location_name: str) -> Optional[Tuple[int, int]]:
        """
        Get coordinates for a location name from the CSV file.

        Args:
            location_name: Name of the location to look up.

        Returns:
            Tuple of (x, y) coordinates or None if not found.
        """
        try:
            with open(paths.POINTS_FILE, "r") as f:
                reader = csv.reader(f)
                next(reader)  # Skip header
                for row in reader:
                    if row[6] == location_name:
                        return (int(row[0]), int(row[1]))
        except (FileNotFoundError, IndexError, ValueError):
            pass
        return None

    def _on_start_click(self) -> None:
        """Handle the Start Driving button click."""
        try:
            # Validate inputs
            validate_location(self.source.get(), "Source")
            validate_location(self.destination.get(), "Destination")
            validate_route(self.source.get(), self.destination.get())
            speed_value = validate_speed(self.speed.get())

            # Get coordinates
            source_coords = self._get_coordinates(self.source.get())
            dest_coords = self._get_coordinates(self.destination.get())

            if source_coords is None or dest_coords is None:
                messagebox.showerror(
                    "Error",
                    "Could not find coordinates for selected locations"
                )
                return

            # Start the simulation
            from ambulance_gis.core.simulation import main_function
            main_function(source_coords, dest_coords, speed_value)

        except ValidationError as e:
            messagebox.showerror("Validation Error", e.message)
        except FileNotFoundError:
            messagebox.showerror("Error", f"Data file not found: {paths.POINTS_FILE}")
        except Exception as e:
            messagebox.showerror("Error", f"An unexpected error occurred: {str(e)}")

    def run(self) -> None:
        """Start the main event loop."""
        self.window.mainloop()


def run() -> None:
    """Run the main application window."""
    app = MainWindow()
    app.run()


if __name__ == "__main__":
    run()
