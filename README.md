# 🚑 Emergency Ambulance Routing RL Project

A Reinforcement Learning (RL) powered simulation for optimizing emergency ambulance routes. This project demonstrates a Gymnasium-compatible environment where an agent identifies the fastest route to a hospital based on real-time traffic, patient criticality, and distance.

---

## 📂 Project Structure

```text
Emergency Ambulance Routing/
├── environment.py       # Core Gymnasium RL Environment
├── app_flask.py         # Advanced Web UI with Map (Flask + Leaflet.js)
├── demo.py              # CLI-based Environment Demo
├── requirements.txt     # Project Dependencies
├── README.md            # Project Documentation
├── Dockerfile           # Containerization Configuration
├── .gitignore           # Git Exclusion Rules
└── docx                 # Original project prompt
```

---

## 🚀 Key Features

### 1. Reinforcement Learning Environment
Built using the **Gymnasium** API, the environment simulates a single-step decision process:
- **Observation Space**: 
    - `traffic_level`: Low (0), Medium (1), High (2)
    - `distance`: 1.0 to 20.0 km
    - `patient_condition`: Normal (0), Critical (1)
- **Action Space**:
    - `0`: Take Highway (High speed, traffic-prone)
    - `1`: Take Shortcut (Low speed, stable)
    - `2`: Wait (Penalty)
- **Reward Logic**: 
    - Heavy penalties for delays in **Critical** cases.
    - Efficiency bonuses for **Normal** patient transit.

### 2. Interactive Map Visualization
The Flask web interface (`app_flask.py`) uses **Leaflet.js** to provide:
- **Live Location Tracking**: View the ambulance position on a real map of London.
- **Nearest Hospital Search**: Automatically identifies the closest of 4 nearby hospitals.
- **Visual Status**: Color-coded markers and status pills for easy scenario identification.

### 3. Patient Condition Control
Users can manually toggle the patient's state between **Normal** and **Critical** to test how the agent's strategy shifts from efficiency to urgency.

---

## 🛠️ Installation & Setup

### 1. Install Dependencies
Ensure you have Python 3.10+ installed:
```bash
pip install -r requirements.txt
```

### 2. Run the Simulation

#### **Web Interface (Recommended)**
Provides map visualization and interactive controls:
```bash
python app_flask.py
```
*Access at: `http://127.0.0.1:5000`*

#### **Terminal Demo**
Quick CLI run to verify RL logic:
```bash
python demo.py
```

---

## 🌐 Deployment
The project is ready for deployment via:
- **Docker**: Build and run the `Dockerfile` for containerized hosting.
- **Hugging Face Spaces**: Optimized for hosting as a Python/Gradio or Flask space.

---

## 📜 Repository
This project is hosted at:
[https://github.com/PraveenKumarinstaking/Ambulance-](https://github.com/PraveenKumarinstaking/Ambulance-)
