import gymnasium as gym
from gymnasium import spaces
import numpy as np

class AmbulanceRoutingEnv(gym.Env):
    def __init__(self):
        super(AmbulanceRoutingEnv, self).__init__()
        self.action_space = spaces.Discrete(3)
        self.observation_space = spaces.Box(
            low=np.array([0, 1.0, 0]), 
            high=np.array([2, 50.0, 1]), 
            dtype=np.float32
        )
        self.state = None

    def reset(self, seed=None, options=None):
        super().reset(seed=seed)
        traffic_level = self.np_random.integers(0, 3)
        distance = self.np_random.uniform(1.0, 20.0)
        patient_condition = self.np_random.integers(0, 2)
        self.state = np.array([traffic_level, distance, patient_condition], dtype=np.float32)
        return self.state, {}

    def step(self, action):
        traffic_level, distance, patient_condition = self.state
        time_taken = self.estimate_time(action, traffic_level, distance)
        
        reward = 0
        breakdown = []
        
        if patient_condition == 1:
            if time_taken < 5.0:
                reward += 10
                breakdown.append(("Fast Critical Response", "+10"))
            elif time_taken < 15.0:
                reward -= 10
                breakdown.append(("Delayed Critical Response", "-10"))
            else:
                reward -= 20
                breakdown.append(("Severe Critical Delay", "-20"))
        else:
            if time_taken < 10.0:
                reward += 10
                breakdown.append(("Efficient Normal Route", "+10"))
            else:
                reward -= 10
                breakdown.append(("Slow Normal Route", "-10"))

        if action == 2:
            reward -= 10
            breakdown.append(("Waiting Penalty", "-10"))
        elif action == 0 and traffic_level == 0:
            reward += 10
            breakdown.append(("Optimal Highway Choice", "+10"))
        elif action == 1 and traffic_level == 2:
            reward += 10
            breakdown.append(("Smart Shortcut Choice", "+10"))
            
        if patient_condition == 1:
            self.send_emergency_alert()

        done = True
        truncated = False
        return self.state, reward, done, truncated, {"time_taken": time_taken, "breakdown": breakdown}

    def estimate_time(self, action, traffic, distance):
        base_speed = 40.0
        if action == 0:
            speed = base_speed * 1.5
            if traffic == 1: speed *= 0.7
            elif traffic == 2: speed *= 0.4
        elif action == 1:
            speed = base_speed * 0.8
            if traffic == 1: speed *= 0.9
            elif traffic == 2: speed *= 0.8
        else:
            return 999.0
        return (distance / speed) * 60.0

    def get_traffic_status(self):
        return ["low", "medium", "high"][int(self.state[0])]

    def send_emergency_alert(self):
        pass

    def render(self):
        print(f"State: Traffic={self.get_traffic_status()}, Distance={self.state[1]:.2f}km, Patient={'Critical' if self.state[2] == 1 else 'Normal'}")
