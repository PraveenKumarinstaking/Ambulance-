from flask import Flask, render_template_string, request, jsonify
from flask_cors import CORS
import numpy as np
import math
import random
from environment import AmbulanceRoutingEnv

app = Flask(__name__)
CORS(app)  # Critical for cross-origin evaluation pings
env = AmbulanceRoutingEnv()

# Mock Hospital Locations
HOSPITALS = [
    {"id": "central", "name": "Central Hospital", "coords": [51.505, -0.09]},
    {"id": "westside", "name": "Westside Clinic", "coords": [51.515, -0.12]},
    {"id": "north", "name": "North General", "coords": [51.525, -0.08]},
    {"id": "south", "name": "South Medical", "coords": [51.495, -0.10]}
]

HTML_TEMPLATE = """
<!DOCTYPE html>
<html>
<head>
    <title>Ambulance Routing</title>
    <link rel="stylesheet" href="https://unpkg.com/leaflet@1.9.4/dist/leaflet.css" />
    <script src="https://unpkg.com/leaflet@1.9.4/dist/leaflet.js"></script>
    <style>
        body { font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, Helvetica, Arial, sans-serif; margin: 0; display: flex; height: 100vh; background: #f5f5f5; }
        #sidebar { width: 380px; padding: 25px; background: white; z-index: 1000; box-shadow: 4px 0 15px rgba(0,0,0,0.08); display: flex; flex-direction: column; }
        #map { flex: 1; }
        h1 { color: #d32f2f; margin-top: 0; font-size: 24px; display: flex; align-items: center; gap: 10px; }
        .card { background: #fff; border: 1px solid #eee; padding: 20px; border-radius: 12px; margin-bottom: 20px; box-shadow: 0 2px 4px rgba(0,0,0,0.04); }
        .label { font-size: 12px; color: #666; text-transform: uppercase; letter-spacing: 0.5px; margin-bottom: 5px; }
        .value { font-size: 18px; font-weight: 600; color: #333; margin-bottom: 15px; }
        select { width: 100%; padding: 12px; border-radius: 8px; border: 1px solid #ddd; font-size: 14px; margin-bottom: 15px; }
        button { width: 100%; padding: 14px; background: #d32f2f; color: white; border: none; border-radius: 8px; font-weight: 600; cursor: pointer; transition: background 0.2s; }
        button:hover { background: #b71c1c; }
        button.secondary { background: #1976d2; margin-top: 10px; }
        button.secondary:hover { background: #1565c0; }
        #status-area { margin-top: auto; }
    </style>
</head>
<body>
    <div id="sidebar">
        <h1>🚑 Ambulance Router</h1>
        <div class="card">
            <div class="label">Patient Condition</div>
            <select id="condition-selector">
                <option value="random">Random</option>
                <option value="normal">Normal</option>
                <option value="critical">Critical</option>
            </select>
            <button onclick="resetEnv()">Initialize Environment</button>
        </div>
        
        <div id="status-area" style="display:none">
            <div class="card">
                <div class="label">Nearest Hospital</div>
                <div id="target" class="value">-</div>
                <div class="label">Traffic Level</div>
                <div id="traffic" class="value">-</div>
                <div class="label">Patient Condition</div>
                <div id="condition" class="value">-</div>
            </div>
            <div class="card">
                <div class="label">Select Route</div>
                <button class="secondary" onclick="stepEnv(0)">Take Main Highway</button>
                <button class="secondary" onclick="stepEnv(1)">Take City Shortcut</button>
            </div>
        </div>
    </div>
    <div id="map"></div>
    <script>
        const map = L.map('map').setView([51.505, -0.09], 13);
        L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png', {
            attribution: '&copy; OpenStreetMap contributors'
        }).addTo(map);
        
        let ambMarker, targetMarker;

        async function resetEnv() {
            const cond = document.getElementById('condition-selector').value;
            const res = await fetch(`/reset?condition=${cond}`, { method: 'POST' });
            const data = await res.json();
            
            document.getElementById('target').innerText = data.target_name;
            document.getElementById('traffic').innerText = data.traffic;
            document.getElementById('condition').innerText = data.info.condition;
            document.getElementById('status-area').style.display = 'block';
            
            if (ambMarker) map.removeLayer(ambMarker);
            if (targetMarker) map.removeLayer(targetMarker);
            
            ambMarker = L.marker([data.lat, data.lng]).addTo(map).bindPopup("Ambulance").openPopup();
            targetMarker = L.marker(data.target_coords).addTo(map).bindPopup(data.target_name);
            
            const group = new L.featureGroup([ambMarker, targetMarker]);
            map.fitBounds(group.getBounds().pad(0.2));
        }

        async function stepEnv(action) {
            const res = await fetch('/step', {
                method: 'POST',
                headers: {'Content-Type': 'application/json'},
                body: JSON.stringify({action})
            });
            const data = await res.json();
            alert(`Step Complete! Reward: ${data.reward.toFixed(2)}\nSuccess: ${data.done ? 'Yes' : 'No'}`);
            if (data.done) location.reload();
        }
    </script>
</body>
</html>
"""

def get_distance(p1, p2):
    return math.sqrt((p1[0]-p2[0])**2 + (p1[1]-p2[1])**2)

@app.route('/', methods=['GET', 'POST'])
def index():
    return render_template_string(HTML_TEMPLATE, hospitals=HOSPITALS)

@app.route('/reset', methods=['GET', 'POST'])
def reset():
    # Robust handling for POST JSON or GET params (Required for OpenEnv)
    data = request.get_json(silent=True) or {}
    cond_param = data.get('condition', request.args.get('condition', 'random'))
    seed = data.get('seed', request.args.get('seed'))
    if seed is not None: seed = int(seed)
    
    state, info_orig = env.reset(seed=seed)
    
    # Override condition based on param
    if cond_param == 'normal': env.state[2] = 0
    elif cond_param == 'critical': env.state[2] = 1
    
    # Location logic for UI visualization
    base_coords = HOSPITALS[0]['coords']
    distance = float(env.state[1])
    angle = random.uniform(0, 2 * math.pi)
    lat_offset = (distance / 111.0) * math.cos(angle)
    lng_offset = (distance / (111.0 * math.cos(math.radians(base_coords[0])))) * math.sin(angle)
    amb_lat, amb_lng = base_coords[0] + lat_offset, base_coords[1] + lng_offset
    nearest_h = min(HOSPITALS, key=lambda h: get_distance([amb_lat, amb_lng], h['coords']))
    
    traffic_map = {0: "Low", 1: "Medium", 2: "High"}
    condition_map = {0: "Normal", 1: "Critical"}
    
    app.current_amb_pos = (amb_lat, amb_lng)
    
    return jsonify({
        "observation": env.state.tolist(),
        "info": {
            "traffic": traffic_map.get(int(env.state[0])),
            "condition": condition_map.get(int(env.state[2])),
            "target_name": nearest_h['name']
        },
        "traffic": traffic_map.get(int(env.state[0])),
        "target_name": nearest_h['name'],
        "target_coords": nearest_h['coords'],
        "lat": amb_lat, "lng": amb_lng
    })

@app.route('/state', methods=['GET', 'POST'])
def state():
    if env.state is None:
        return jsonify({"error": "Environment not initialized"}), 400
    
    traffic_map = {0: "Low", 1: "Medium", 2: "High"}
    condition_map = {0: "Normal", 1: "Critical"}
    
    return jsonify({
        "observation": env.state.tolist(),
        "info": {
            "traffic": traffic_map.get(int(env.state[0])),
            "condition": condition_map.get(int(env.state[2]))
        }
    })

@app.route('/step', methods=['GET', 'POST'])
def step():
    data = request.get_json(silent=True) or {}
    action = data.get('action', 0)
    state, reward, done, truncated, info = env.step(action)
    
    return jsonify({
        "observation": state.tolist(),
        "reward": float(reward),
        "done": done,
        "truncated": truncated,
        "info": info
    })

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=7860)
