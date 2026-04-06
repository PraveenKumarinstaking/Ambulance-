import os
import json
import requests
from openai import OpenAI

# Environment Variables
API_BASE_URL = os.getenv("API_BASE_URL", "http://localhost:7860")
MODEL_NAME = os.getenv("MODEL_NAME", "gpt-4o")
HF_TOKEN = os.getenv("HF_TOKEN", "")

# Flask App URL (local development or Space URL)
APP_URL = "http://localhost:7860"

def get_state():
    resp = requests.get(f"{APP_URL}/state")
    return resp.json()

def reset_env(condition="random"):
    resp = requests.post(f"{APP_URL}/reset", json={"condition": condition})
    return resp.json()

def step_env(action):
    resp = requests.post(f"{APP_URL}/step", json={"action": action})
    return resp.json()

def run_inference():
    client = OpenAI(base_url=f"{API_BASE_URL}/v1", api_key=HF_TOKEN)
    
    print("[START]")
    
    # Initialize Environment
    state_data = reset_env(condition="random")
    
    # Simple Loop for one step (can be extended)
    for i in range(1):
        prompt = f"""
        You are an ambulance routing system.
        Current Situation:
        - Traffic Level: {state_data['traffic']}
        - Distance to Hospital: {state_data['distance']} km
        - Patient Condition: {state_data['condition']}
        
        Choose an action:
        0: Take Highway
        1: Take Shortcut
        2: Wait
        
        Respond with ONLY the action number.
        """
        
        response = client.chat.completions.create(
            model=MODEL_NAME,
            messages=[{"role": "user", "content": prompt}],
            max_tokens=1
        )
        
        action = int(response.choices[0].message.content.strip())
        
        # Execute Step
        step_data = step_env(action)
        
        # Log Step [STEP] -> {"step": current_step, "action": action, "reward": reward, "done": done, "obs": observation}
        # Based on OpenEnv requirements for structured logging
        log_entry = {
            "step": i + 1,
            "action": action,
            "reward": float(step_data['reward']),
            "done": True,
            "obs": state_data['traffic']
        }
        print(f"[STEP] {json.dumps(log_entry)}")
    
    print("[END]")

if __name__ == "__main__":
    run_inference()
