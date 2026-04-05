# Emergency Ambulance Routing RL Environment

This project implements a single-step Reinforcement Learning (RL) environment where an agent selects the best route for an ambulance based on traffic conditions, distance to the hospital, and patient severity.

## Goal
The goal is to minimize patient transit time and maximize rewards by choosing the most efficient route.

## Tech Stack
- **Python**
- **Gymnasium**: RL framework
- **NumPy**: Numeric operations
- **Gradio**: Interactive UI

## Installation

```bash
pip install -r requirements.txt
```

## Usage

### Run Demo
Execute the demo script to see the environment in action:
```bash
python demo.py
```

### Run Web UI (Alternative)
If Gradio has issues, use the Flask version:
```bash
python app_flask.py
```
Open your browser at `http://127.0.0.1:5000`.

## Environment Details
- **Observation Space**: `[traffic_level, distance, patient_condition]`
- **Action Space**:
  - `0`: Take Highway
  - `1`: Take Shortcut
  - `2`: Wait
- **Rewards**: Calculated based on patient condition and time taken.
