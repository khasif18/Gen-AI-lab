# Smart Home Intelligent Temperature Agent

## Problem Statement
Design and implement a simple intelligent agent that monitors room temperature and automatically controls an air conditioner (AC) to maintain a comfortable temperature. 

## Features
- **Interactive Web UI**: Built as a modern Smart Home dashboard.
- **Goal-Based Agent Logic**: Agent uses upper and lower bounds to decide actions, applying hysteresis to avoid rapid toggling.
- **Live Environmental Simulation**: Temperature fluctuates realistically based on AC state and randomized noise.
- **Real-Time Data Visualizations**: Chart.js integration for Temp vs Time and AC Status vs Time.
- **Explainable AI**: The UI explicitly reveals the agent's Perception, Goal, Decision, and Action.
- **Controls**: Change simulation speed, pause, or reset the experiment.

## Technologies Used
- HTML5
- CSS3 (Vanilla)
- JavaScript (ES6 Classes)
- [Chart.js](https://www.chartjs.org/) for real-time graphs

## How to Run
The simplest way to run this experiment:
1. Double-click the `index.html` file to open it in any modern web browser.
2. No backend server or complex environment is required. (If some browsers block local Chart.js CDN fetching due to strict local CORS, serve it via python using `python -m http.server 8000` inside this directory and visit `http://localhost:8000`).

## How the Intelligent Agent Works
The agent follows this logical pipeline:
1. **Perception**: Agent retrieves the current room temperature from the `RoomEnvironment`.
2. **Goal Evaluation**: The agent's goal is maintaining a comfortable 20°C - 24°C range. 
3. **Decision**:
   - If Temp >= 25°C, turn AC **ON**.
   - If Temp <= 23°C, turn AC **OFF**.
   - If between 23°C and 25°C, **MAINTAIN** current state (Hysteresis logic).
4. **Action**: Agent sends an actuator command to alter the environment (turning the AC ON/OFF).
5. **Feedback Loop**: The environment updates its internal state based on the action, and the agent repeats the loop.

## Expected Behavior
When starting, the room defaults to 29°C (hot). The agent perceives this, determines it is above the 25°C threshold, and immediately turns the AC ON. You will see the room temperature begin to drop on the chart and data table.
Once the temperature hits 23.0°C, the agent turns the AC OFF. The room will naturally warm up again. The process cycles indefinitely, maintaining the room in a comfortable equilibrium.
