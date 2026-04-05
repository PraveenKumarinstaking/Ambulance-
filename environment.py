import gymnasium as gym
from gymnasium import spaces
import numpy as np

class AmbulanceRoutingEnv(gym.Env):
    """
    Emergency Ambulance Routing environment where an agent selects the best route 
    based on traffic, distance, and patient severity.
    """
    def __init__(self):
        super(AmbulanceRoutingEnv, self).__init__()

        # Action space: 0: take_highway, 1: take_shortcut, 2: wait
        self.action_space = spaces.Discrete(3)

        # Observation space: 
        # 0: traffic_level (0: low, 1: medium, 2: high)
        # 1: distance_to_hospital (1.0 to 20.0 km)
        # 2: patient_condition (0: normal, 1: critical)
        self.observation_space = spaces.Box(
            low=np.array([0, 1.0, 0]), 
            high=np.array([2, 50.0, 1]), 
            dtype=np.float32
        )

        self.state = None

    def reset(self, seed=None, options=None):
        super().reset(seed=seed)
        
        # Randomly initialize state
        traffic_level = self.np_random.integers(0, 3)
        distance = self.np_random.uniform(1.0, 20.0)
        patient_condition = self.np_random.integers(0, 2)

        self.state = np.array([traffic_level, distance, patient_condition], dtype=np.float32)
        
        return self.state, {}

    def step(self, action):
        traffic_level, distance, patient_condition = self.state
        
        # Tool-like functions simulation
        time_taken = self.estimate_time(action, traffic_level, distance)
        
        # Base reward logic
        reward = 0
        
        # Critical patient logic
        if patient_condition == 1:  # Critical
            if time_taken < 5.0:
                reward += 20  # Fast response bonus
            elif time_taken > 15.0:
                reward -= 50  # Strong delay penalty
            else:
                reward -= (time_taken - 5.0) * 2
        else:  # Normal
            reward += (10.0 - time_taken)  # Reward efficiency

        # Action specific rewards/penalties
        if action == 2:  # Wait
            reward -= 30  # Always penalized for waiting in emergency
            
        # Send emergency alert simulation
        if patient_condition == 1:
            self.send_emergency_alert()

        done = True  # Single-step episode
        truncated = False
        
        return self.state, reward, done, truncated, {"time_taken": time_taken}

    def estimate_time(self, action, traffic, distance):
        """Simulates time estimation based on route and conditions."""
        base_speed = 40.0  # km/h
        
        if action == 0:  # Highway
            speed = base_speed * 1.5
            if traffic == 1: speed *= 0.7  # Medium traffic
            elif traffic == 2: speed *= 0.4  # High traffic
        elif action == 1:  # Shortcut
            speed = base_speed * 0.8
            if traffic == 1: speed *= 0.9
            elif traffic == 2: speed *= 0.8
        else:  # Wait
            return 999.0  # Massive delay
            
        time_hours = distance / speed
        return time_hours * 60.0  # Output in minutes

    def get_traffic_status(self):
        """Mock helper for traffic status."""
        levels = ["low", "medium", "high"]
        return levels[int(self.state[0])]

    def send_emergency_alert(self):
        """Mock helper for sending emergency alerts."""
        pass

    def render(self):
        print(f"Current State: Traffic={self.get_traffic_status()}, Distance={self.state[1]:.2f}km, Patient={'Critical' if self.state[2] == 1 else 'Normal'}")
