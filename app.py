import gradio as gr
import gymnasium as gym
from environment import AmbulanceRoutingEnv
import numpy as np

# Initialize the environment
env = AmbulanceRoutingEnv()

def run_step(action_idx):
    # For Gradio, we'll reset and step in one go to show the result of an action
    state, _ = env.reset()
    
    traffic_map = {0: "Low", 1: "Medium", 2: "High"}
    condition_map = {0: "Normal", 1: "Critical"}
    action_map = {0: "Take Highway", 1: "Take Shortcut", 2: "Wait"}
    
    # Capture initial state for display
    initial_traffic = traffic_map[int(state[0])]
    initial_distance = f"{state[1]:.2f} km"
    initial_condition = condition_map[int(state[2])]
    
    # Step the environment
    next_state, reward, done, truncated, info = env.step(action_idx)
    
    result = {
        "Initial Traffic": initial_traffic,
        "Initial Distance": initial_distance,
        "Initial Condition": initial_condition,
        "Chosen Action": action_map[action_idx],
        "Resulting Reward": f"{reward:.2f}",
        "Estimated Time": f"{info['time_taken']:.2f} minutes",
    }
    
    return result

with gr.Blocks(title="Emergency Ambulance Routing") as demo:
    gr.Markdown("# 🚑 Emergency Ambulance Routing RL Environment")
    gr.Markdown("Select an action to see the outcome in a simulated emergency scenario.")
    
    with gr.Row():
        with gr.Column():
            action_radio = gr.Radio(
                choices=[("Take Highway", 0), ("Take Shortcut", 1), ("Wait", 2)],
                label="Action Selection",
                value=0
            )
            submit_btn = gr.Button("Route Ambulance")
        
        with gr.Column():
            output = gr.JSON(label="Simulation Result")
            
    submit_btn.click(fn=run_step, inputs=action_radio, outputs=output)

if __name__ == "__main__":
    demo.launch()
