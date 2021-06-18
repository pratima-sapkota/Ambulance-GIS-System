# Ambulance-GIS-System

## Simulation of a real-time system to find the best path to reach its destination.

The main objective of this simulation is to demonstrate how an emergency vehicle can be guided to take the best path to reach its destination based upon the distance and traffic congestion at each junction.

## Features

- Real-time traffic congestion visualization
- Dynamic path recalculation based on current conditions
- Interactive GUI for selecting source and destination
- Visual simulation of ambulance movement

## Requirements

- Python 3.8 or greater

## Installation

### Quick Install

Install all dependencies using the requirements file:

```bash
pip install -r requirements.txt
```

### Using pip with pyproject.toml

```bash
pip install -e .
```

### Individual Packages

1. **SimPy** - Discrete-event simulation
   ```bash
   pip install simpy>=4.1.1
   ```

2. **SymPy** - Symbolic mathematics
   ```bash
   pip install sympy>=1.12
   ```

3. **Matplotlib** - Visualization
   ```bash
   pip install matplotlib>=3.8.0
   ```

4. **NetworkX** - Graph representation
   ```bash
   pip install networkx>=3.2
   ```

## Running the Application

### Option 1: Direct execution
```bash
python main.py
```

### Option 2: Module execution
```bash
python -m ambulance_gis
```

### Option 3: If installed via pip
```bash
ambulance-gis
```

## Development Setup

1. Clone the repository:
   ```bash
   git clone https://github.com/Urmila-m/Ambulance-GIS-System.git
   cd Ambulance-GIS-System
   ```

2. Create a virtual environment:
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. Install development dependencies:
   ```bash
   pip install -r requirements-dev.txt
   ```

### Development Tools

- **Format code:**
  ```bash
  black ambulance_gis/
  isort ambulance_gis/
  ```

- **Check code style:**
  ```bash
  flake8 ambulance_gis/
  ```

- **Type checking:**
  ```bash
  mypy ambulance_gis/
  ```

- **Run tests:**
  ```bash
  pytest
  ```

## Project Structure

```
Ambulance-GIS-System/
├── ambulance_gis/           # Main package
│   ├── __init__.py
│   ├── __main__.py          # python -m ambulance_gis entry point
│   ├── core/                # Business logic
│   │   ├── ambulance.py     # Ambulance movement and pathfinding
│   │   ├── road_map.py      # Road network management
│   │   └── simulation.py    # Simulation environment
│   ├── ui/                  # User interface
│   │   └── main_window.py   # Main application window
│   ├── utils/               # Utilities
│   │   ├── geometry.py      # Distance calculations
│   │   ├── validators.py    # Input validation
│   │   └── logger.py        # Logging configuration
│   └── visualization/       # Visualization
│       └── map_renderer.py  # Map rendering
├── data/                    # Data files
│   ├── points.csv           # Node/intersection data
│   └── roads.csv            # Edge/road data
├── config.py                # Application configuration
├── main.py                  # Application launcher
├── requirements.txt         # Production dependencies
├── requirements-dev.txt     # Development dependencies
├── pyproject.toml           # Project metadata and tool config
└── README.md
```

## Screenshots

![image info](./ui.PNG)
![image info](./simulate_1.png)
![image_info](./simulate_2.png)
![image_info](./simulate_3.png)

## License

MIT License

## Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

#Health and Urban Population Management
