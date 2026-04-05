from flask import Flask, render_template_string, request, jsonify
import numpy as np
import math
import random
from environment import AmbulanceRoutingEnv

app = Flask(__name__)
env = AmbulanceRoutingEnv()

# Mock Hospital Locations (London Area)
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
    <title>Advanced Ambulance Routing</title>
    <link rel="stylesheet" href="https://unpkg.com/leaflet@1.9.4/dist/leaflet.css" />
    <script src="https://unpkg.com/leaflet@1.9.4/dist/leaflet.js"></script>
    <style>
        body { font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif; margin: 0; display: flex; height: 100vh; background: #f4f4f9; }
        #sidebar { width: 400px; padding: 20px; box-shadow: 2px 0 5px rgba(0,0,0,0.1); background: white; z-index: 1000; overflow-y: auto; }
        #map { flex: 1; }
        .card { background: #fff; padding: 15px; border-radius: 8px; margin-bottom: 20px; border: 1px solid #eee; }
        h1 { color: #d32f2f; margin-top: 0; font-size: 1.5em; }
        .status-pill { display: inline-block; padding: 4px 12px; border-radius: 15px; font-size: 0.85em; font-weight: bold; }
        .critical { background: #ffebee; color: #d32f2f; border: 1px solid #ffcdd2; }
        .normal { background: #e8f5e9; color: #2e7d32; border: 1px solid #c8e6c9; }
        button { background: #d32f2f; color: white; border: none; padding: 12px; border-radius: 6px; cursor: pointer; width: 100%; margin-bottom: 10px; font-size: 1em; transition: background 0.3s; }
        button:hover { background: #b71c1c; }
        .result-box { margin-top: 20px; padding: 15px; border-radius: 8px; background: #fdfdfd; border: 1px solid #ddd; }
        .control-group { margin-bottom: 15px; }
        label { font-weight: bold; display: block; margin-bottom: 5px; color: #333; }
        select { width: 100%; padding: 8px; border-radius: 4px; border: 1px solid #ccc; margin-bottom: 10px; }
    </style>
</head>
<body>
    <div id="sidebar">
        <h1>🚑 Ambulance Routing</h1>
        
        <div class="card">
            <div class="control-group">
                <label>Set Patient Condition:</label>
                <select id="condition-selector">
                    <option value="random">Random (Auto)</option>
                    <option value="normal">Normal Case</option>
                    <option value="critical">Critical Emergency</option>
                </select>
            </div>
            <button onclick="resetEnv()">Start New Emergency</button>
            
            <div id="state-info" style="display:none; margin-top:15px;">
                <p><strong>Target:</strong> <span id="target-hospital">-</span></p>
                <p><strong>Traffic:</strong> <span id="traffic-val">-</span></p>
                <p><strong>Distance:</strong> <span id="distance-val">-</span> km</p>
                <p><strong>Condition:</strong> <span id="condition-pill" class="status-pill">-</span></p>
                <hr>
                <button onclick="stepEnv(0)">Take Highway</button>
                <button onclick="stepEnv(1)">Take Shortcut</button>
                <button onclick="stepEnv(2)">Wait</button>
            </div>
        </div>

        <div id="result-display" class="result-box" style="display:none;">
            <h3>Outcome Result</h3>
            <div id="result-content"></div>
        </div>
    </div>
    <div id="map"></div>

    <script>
        const hospitals = {{ hospitals|tojson }};
        const map = L.map('map').setView([51.505, -0.09], 13);
        L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png').addTo(map);

        const hospitalIcon = L.icon({
            iconUrl: 'https://raw.githubusercontent.com/pointhi/leaflet-color-markers/master/img/marker-icon-2x-red.png',
            shadowUrl: 'https://cdnjs.cloudflare.com/ajax/libs/leaflet/0.7.7/images/marker-shadow.png',
            iconSize: [25, 41], iconAnchor: [12, 41], popupAnchor: [1, -34], shadowSize: [41, 41]
        });

        const ambulanceIcon = L.icon({
            iconUrl: 'https://raw.githubusercontent.com/pointhi/leaflet-color-markers/master/img/marker-icon-2x-blue.png',
            shadowUrl: 'https://cdnjs.cloudflare.com/ajax/libs/leaflet/0.7.7/images/marker-shadow.png',
            iconSize: [25, 41], iconAnchor: [12, 41], popupAnchor: [1, -34], shadowSize: [41, 41]
        });

        hospitals.forEach(h => L.marker(h.coords, {icon: hospitalIcon}).addTo(map).bindPopup(h.name));
        
        let ambulanceMarker = null;
        let routeLine = null;
        let currentTargetCoords = null;

        async function resetEnv() {
            const cond = document.getElementById('condition-selector').value;
            const resp = await fetch(`/reset?condition=${cond}`);
            const data = await resp.json();
            
            currentTargetCoords = data.target_coords;
            document.getElementById('state-info').style.display = 'block';
            document.getElementById('result-display').style.display = 'none';
            document.getElementById('traffic-val').innerText = data.traffic;
            document.getElementById('distance-val').innerText = data.distance;
            document.getElementById('target-hospital').innerText = data.target_name;
            
            const pill = document.getElementById('condition-pill');
            pill.innerText = data.condition;
            pill.className = 'status-pill ' + (data.condition === 'Critical' ? 'critical' : 'normal');

            if (ambulanceMarker) map.removeLayer(ambulanceMarker);
            if (routeLine) map.removeLayer(routeLine);
            
            ambulanceMarker = L.marker([data.lat, data.lng], {icon: ambulanceIcon}).addTo(map)
                .bindPopup('Ambulance Location').openPopup();
            
            map.fitBounds(L.latLngBounds([ambulanceMarker.getLatLng(), currentTargetCoords]), {padding: [50, 50]});
        }

        async function stepEnv(action) {
            const resp = await fetch('/step', {
                method: 'POST',
                headers: {'Content-Type': 'application/json'},
                body: JSON.stringify({action: action})
            });
            const data = await resp.json();
            
            if (routeLine) map.removeLayer(routeLine);
            routeLine = L.polyline([[data.start_lat, data.start_lng], currentTargetCoords], {
                color: action === 2 ? 'gray' : (action === 0 ? 'blue' : 'green'), 
                weight: 5, dashArray: '10, 10'
            }).addTo(map);

            document.getElementById('result-display').style.display = 'block';
            document.getElementById('result-content').innerHTML = `
                <p><strong>Action:</strong> ${data.action_name}</p>
                <p><strong>Reward:</strong> ${data.reward}</p>
                <p><strong>Time:</strong> ${data.time_taken.toFixed(2)} mins</p>
            `;
        }
    </script>
</body>
</html>
"""

def get_distance(p1, p2):
    return math.sqrt((p1[0]-p2[0])**2 + (p1[1]-p2[1])**2)

@app.route('/')
def index():
    return render_template_string(HTML_TEMPLATE, hospitals=HOSPITALS)

@app.route('/reset')
def reset():
    # Pass condition if provided
    cond_param = request.args.get('condition', 'random')
    
    # Gym Reset
    state, _ = env.reset()
    
    # Override condition if specified
    if cond_param == 'normal':
        env.state[2] = 0
    elif cond_param == 'critical':
        env.state[2] = 1
    
    traffic_map = {0: "Low", 1: "Medium", 2: "High"}
    condition_map = {0: "Normal", 1: "Critical"}
    
    # Location Logic
    base_coords = HOSPITALS[0]['coords']
    distance = float(env.state[1])
    angle = random.uniform(0, 2 * math.pi)
    lat_offset = (distance / 111.0) * math.cos(angle)
    lng_offset = (distance / (111.0 * math.cos(math.radians(base_coords[0])))) * math.sin(angle)
    
    amb_lat = base_coords[0] + lat_offset
    amb_lng = base_coords[1] + lng_offset

    nearest_h = min(HOSPITALS, key=lambda h: get_distance([amb_lat, amb_lng], h['coords']))
    dist_to_nearest = get_distance([amb_lat, amb_lng], nearest_h['coords']) * 111.0
    
    app.current_amb_pos = (amb_lat, amb_lng)
    app.current_target = nearest_h

    return jsonify({
        "traffic": traffic_map[int(env.state[0])],
        "distance": f"{dist_to_nearest:.2f}",
        "condition": condition_map[int(env.state[2])],
        "lat": amb_lat,
        "lng": amb_lng,
        "target_name": nearest_h['name'],
        "target_coords": nearest_h['coords']
    })

@app.route('/step', methods=['POST'])
def step():
    data = request.json
    action = data.get('action', 0)
    state, reward, done, truncated, info = env.step(action)
    action_map = {0: "Take Highway", 1: "Take Shortcut", 2: "Wait"}
    start_pos = getattr(app, 'current_amb_pos', HOSPITALS[0]['coords'])
    return jsonify({
        "action_name": action_map[action], "reward": f"{reward:.2f}",
        "time_taken": info['time_taken'], "start_lat": start_pos[0], "start_lng": start_pos[1]
    })

if __name__ == '__main__':
    app.run(debug=True, port=5000)
