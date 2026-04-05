import gymnasium as gym
from environment import AmbulanceRoutingEnv
import numpy as np

def run_demo():
    # Initialize the environment
    env = AmbulanceRoutingEnv()
    
    # Reset the environment
    state, _ = env.reset(seed=42)
    
    # State mapping
    traffic_map = {0: "Low", 1: "Medium", 2: "High"}
    condition_map = {0: "Normal", 1: "Critical"}
    
    print("-----------------------------------------")
    print("Emergency Ambulance Routing Demo")
    print("-----------------------------------------")
    print(f"Initial State:")
    print(f"  Traffic Level:      {traffic_map[int(state[0])]}")
    print(f"  Distance:           {state[1]:.2f} km")
    print(f"  Patient Condition: {condition_map[int(state[2])]}")
    print("-----------------------------------------")
    
    # Agent Logic: Simple Rule-Based Policy
    # If critical, take shortcut if highway is high traffic
    if state[2] == 1:  # Critical
        if state[0] == 2:  # High Traffic
            action = 1  # Shortcut
        else:
            action = 0  # Highway
    else:
        # If normal, take highway unless high traffic
        if state[0] == 2:
            action = 1
        else:
            action = 0
            
    action_map = {0: "Take Highway", 1: "Take Shortcut", 2: "Wait"}
    
    # Step the environment
    next_state, reward, done, truncated, info = env.step(action)
    
    print(f"Chosen Action: {action_map[action]}")
    print(f"Resulting Reward: {reward:.2f}")
    print(f"Estimated Time: {info['time_taken']:.2f} minutes")
    print(f"Done Status: {done}")
    print("-----------------------------------------")

if __name__ == "__main__":
    run_demo()
