# Laboratory Experiment: Goal-Based Intelligent Agent for Smart Home Temperature Control

## 1. AIM
To design and implement a web-based simulation of a goal-based intelligent agent that monitors and regulates room temperature within a predefined comfortable range by controlling an Air Conditioner (AC).

---

## 2. OBJECTIVE
1. To understand the fundamental concepts of an Intelligent Agent, Environment, Perception, and Action.
2. To simulate an environment where temperature fluctuates and an agent perceives these continuous changes.
3. To implement decision-making logic using upper and lower threshold values (hysteresis) to achieve a desired goal state.
4. To evaluate the agent's performance in real-time through an interactive web-based visual dashboard.

---

## 3. THEORY
- **Intelligent Agent:** An autonomous entity that observes through sensors and acts upon an environment using actuators to achieve specific goals.
- **Agent Environment:** The external space or system with which the agent interacts. Here, it is a simulated room with fluctuating temperature.
- **Perception:** The input the agent receives from the environment (current room temperature).
- **Goal:** The desired state the agent strives to maintain (temperature between 20°C and 24°C).
- **Action:** The output of the agent based on its decision logic (Turning the AC ON or OFF).
- **Goal-based Agent:** Unlike simple reflex agents that only use condition-action rules for the current percept, a goal-based agent considers whether its actions will help attain its goal. 

---

## 4. CASE STUDY
**Scenario:** A smart home temperature control system.  
**Objective:** Maintain a comfortable temperature range of **20°C – 24°C**.  
The agent receives the current room temperature from the simulated environment. Because rapid switching of the AC unit can cause wear and tear, we use **hysteresis** logic:
- If temperature >= 25°C → Turn AC **ON**
- If temperature <= 23°C → Turn AC **OFF**
- If temperature is between 23°C and 25°C → **Maintain** the previous AC state

---

## 5. SYSTEM DESIGN
The system follows a standard agent-environment interaction loop:
`Environment → Perception → Agent → Goal Evaluation → Decision → Action → Feedback`

**Components:**
- **Environment:** Represents the physical room and updates the temperature based on time and the AC state.
- **Perception/Sensor:** Retrieves the temperature and provides it to the Agent.
- **Intelligent Agent:** The logical unit that compares the perceived state to the goal.
- **Actuator:** The physical (simulated) AC unit.

---

## 6. ALGORITHM
1. Start the program simulation.
2. Initialize the room temperature to a hot starting state (e.g., 29°C).
3. Define the optimal temperature range.
4. Initialize the AC status to OFF.
5. In each simulation step:
   1. The agent reads the current room temperature.
   2. The agent compares the temperature to its thresholds.
   3. If Temp >= 25°C, decide Action = ON.
   4. If Temp <= 23°C, decide Action = OFF.
   5. If 23°C < Temp < 25°C, decide Action = Maintain State.
6. The agent performs the action (updates AC state).
7. The environment reacts: If AC is ON, temperature drops. If OFF, temperature rises.
8. Record the data, update the UI and live charts.
9. Repeat continuously until paused or reset.

---

## 7. PSEUDOCODE
```text
CLASS RoomEnvironment:
    temperature = 29.0
    METHOD updateTemperature(acState):
        IF acState == ON:
            temperature = temperature - cooling_factor
        ELSE:
            temperature = temperature + heating_factor

CLASS TemperatureAgent:
    acState = OFF
    METHOD perceive(environment):
        RETURN environment.temperature
    
    METHOD decide(temperature):
        IF temperature >= 25:
            acState = ON
        ELSE IF temperature <= 23:
            acState = OFF
        ELSE:
            KEEP acState
            
    METHOD act():
        RETURN acState

LOOP Continuously:
    current_temp = agent.perceive(room)
    agent.decide(current_temp)
    current_ac = agent.act()
    room.updateTemperature(current_ac)
    UI.update(current_temp, current_ac)
```

---

## 8. IMPLEMENTATION
The project is implemented entirely as a frontend web application:
- **HTML (`index.html`):** Structures the smart home dashboard layout, cards, control buttons, and table.
- **CSS (`style.css`):** Provides a modern, responsive design with dynamic room color changes based on temperature.
- **JavaScript (`script.js`):** Contains the Object-Oriented implementations of the `RoomEnvironment` and `TemperatureAgent`. It handles the simulation loop (`setInterval`), updates the DOM (Agent reasoning box, dynamic UI), and interfaces with **Chart.js** to draw the live temperature and AC status graphs.

---

## 9. SOURCE CODE
The complete source code consists of `index.html`, `style.css`, and `script.js` located in the `smart-home-agent/` project directory. The codebase relies solely on standard Web APIs and Chart.js from a CDN.

---

## 10. OUTPUT
**Dashboard Characteristics:**
- **Visual Room:** The background color of the room visual shifts from warm red/orange to cool blue/green based on the temperature. An airflow animation appears when the AC is ON.
- **Agent Reasoning:** The logic block clearly prints: "Temperature exceeds upper threshold. Turning AC ON."
- **Live Charts:** 
  - *Temperature Graph:* Shows a fluctuating sine-wave-like curve bouncing between 23°C and 25°C. The target range is highlighted with dashed lines.
  - *AC Status Graph:* Shows a step chart instantly switching from 0 (OFF) to 1 (ON) in correlation with the peaks and troughs of the temperature graph.
- **Event Table:** Continually adds rows detailing Step, Temp, Status, and Action.

---

## 11. RESULT
The goal-based intelligent agent was successfully designed and simulated via a web application. It demonstrated robust monitoring of the simulated room temperature and actively controlled the AC actuator to strictly maintain the room temperature within the predetermined comfortable bounds.

---

## 12. CONCLUSION
The experiment effectively demonstrated the functioning of a goal-based intelligent agent with a real-time web UI. Through the interactive dashboard, it is clearly visible how an agent perceives its environment, evaluates its current state against a goal, makes deterministic decisions incorporating hysteresis, and feeds those actions back into the environment. The visual feedback loop validates that intelligent agents interact continuously with their environment to achieve and maintain a steady goal state.

---

## 13. APPLICATIONS
1. **Smart Homes:** Intelligent thermostat devices (like Google Nest) controlling localized climate.
2. **HVAC Automation:** Heating, Ventilation, and Air Conditioning automation in large commercial buildings to optimize energy.
3. **Energy Management:** Automated systems aimed at reducing power consumption by preventing unnecessary cyclic toggling.
4. **IoT Automation:** Industrial environmental control systems where maintaining strict parameters (like in server rooms or greenhouses) is critical.
