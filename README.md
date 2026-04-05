---
title: Ambulance Routing
emoji: 🚑
colorFrom: red
colorTo: blue
sdk: docker
pinned: false
---

# 🚑 Emergency Ambulance Routing — OpenEnv Mini Environment

A single-step **OpenEnv / Gymnasium**-compatible RL environment where an agent selects the optimal ambulance route based on traffic, distance, and patient severity.

---

## 📦 Submission Files

| File | Description |
|---|---|
| `environment.py` | Core OpenEnv environment with `reset()` and `step()` |
| `demo.py` | Demo script — runs one episode and prints results |
| `requirements.txt` | Python dependencies |
| `README.md` | This documentation |
| **Hugging Face Space** | [https://huggingface.co/spaces/pvlove1432/Ambulance-Routing](https://huggingface.co/spaces/pvlove1432/Ambulance-Routing) |
| **GitHub Repository** | [https://github.com/PraveenKumarinstaking/Ambulance-](https://github.com/PraveenKumarinstaking/Ambulance-) |

---

## 🧠 Environment Interface

### Observation Space
A 3-element vector `[traffic_level, distance, patient_condition]`:

| Index | Field | Type | Range |
|---|---|---|---|
| 0 | `traffic_level` | Discrete | 0 = Low, 1 = Medium, 2 = High |
| 1 | `distance` | Continuous | 1.0 — 20.0 km |
| 2 | `patient_condition` | Discrete | 0 = Normal, 1 = Critical |

### Action Space
Discrete(3):

| Action | Meaning |
|---|---|
| 0 | Take Highway — fast but traffic-prone |
| 1 | Take Shortcut — slower but stable |
| 2 | Wait — always penalized |

### `reset(seed=None)`
- Randomly initializes `traffic_level`, `distance`, and `patient_condition`.
- Supports deterministic seeding via the `seed` parameter.
- Returns `(observation, info)`.

### `step(action)`
- Executes the chosen route action.
- Calculates travel time using `estimate_time()`.
- Returns `(observation, reward, done, truncated, info)`.
- Episode ends after **one decision** (`done = True`).

### Reward Logic (±10 increments)

| Condition | Reward |
|---|---|
| Fast response for Critical patient | **+10** |
| Delayed Critical response | **-10** |
| Severe Critical delay | **-20** |
| Efficient Normal route | **+10** |
| Slow Normal route | **-10** |
| Waiting (any case) | **-10** |
| Optimal Highway (low traffic) | **+10** |
| Smart Shortcut (high traffic) | **+10** |

### Tool-like Helper Functions
- `get_traffic_status()` — returns current traffic as a string
- `estimate_time(route)` — calculates estimated travel time in minutes
- `send_emergency_alert()` — simulates sending an alert for critical patients

---

## ▶️ How to Run

### 1. Install Dependencies
```bash
pip install -r requirements.txt
```

### 2. Run the Demo
```bash
python demo.py
```
**Output:**
```
-----------------------------------------
Emergency Ambulance Routing Demo
-----------------------------------------
Initial State:
  Traffic Level:      Medium
  Distance:           12.45 km
  Patient Condition:  Critical
-----------------------------------------
Chosen Action: Take Highway
Resulting Reward: -10.00
Estimated Time: 17.81 minutes
Done Status: True
-----------------------------------------
```

### 3. Run the Web Interface (Optional)
```bash
python app_flask.py
```
Open `http://localhost:7860` in your browser.

---

## 🛠️ Tech Stack
- **Python** — Programming language
- **Gymnasium / OpenEnv** — RL environment API
- **NumPy** — Numeric operations
- **Flask + Leaflet.js** — Web UI with map (optional)
- **Docker** — Containerization for Hugging Face Spaces
