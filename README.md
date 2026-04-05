---
title: Ambulance Routing
emoji: 🚑
colorFrom: red
colorTo: blue
sdk: docker
pinned: false
---

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

### Hugging Face Spaces (Recommended)

This project is optimized for deployment on [Hugging Face Spaces](https://huggingface.co/spaces) using Docker SDK.

**Steps to deploy:**

1. **Create a new Space** on [huggingface.co/new-space](https://huggingface.co/new-space).
2. Select **Docker** as the SDK.
3. Clone your Space repository:
   ```bash
   git clone https://huggingface.co/spaces/YOUR_USERNAME/YOUR_SPACE_NAME
   ```
4. Copy the project files into the Space directory:
   ```bash
   cp environment.py app_flask.py requirements.txt Dockerfile YOUR_SPACE_NAME/
   ```
5. Push to Hugging Face:
   ```bash
   cd YOUR_SPACE_NAME
   git add .
   git commit -m "Deploy Ambulance Routing App"
   git push
   ```
6. Your app will be live at:
   ```
   https://YOUR_USERNAME-YOUR_SPACE_NAME.hf.space
   ```

> **Note:** The app binds to port `7860` (Hugging Face default) and host `0.0.0.0`.

### Docker (Local)
```bash
docker build -t ambulance-routing .
docker run -p 7860:7860 ambulance-routing
```
*Access at: `http://localhost:7860`*

---

## 📜 Repository
This project is hosted at:
[https://github.com/PraveenKumarinstaking/Ambulance-](https://github.com/PraveenKumarinstaking/Ambulance-)
