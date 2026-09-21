import os
import random
import numpy as np
import matplotlib.pyplot as plt
from docx import Document
from docx.shared import Inches, Pt
from docx.enum.text import WD_ALIGN_PARAGRAPH

def run_simulation_and_plot():
    # Simulation Code
    class RoomEnvironment:
        def __init__(self, initial_temperature):
            self.current_temperature = initial_temperature

        def get_temperature(self):
            return self.current_temperature

        def update_temperature(self, ac_status):
            variation = random.uniform(-0.2, 0.2)
            if ac_status == 1: # AC is ON
                self.current_temperature -= (0.5 + variation)
            else: # AC is OFF
                self.current_temperature += (0.4 + variation)

    class TemperatureAgent:
        def __init__(self, lower_threshold, upper_threshold):
            self.ac_status = 0 # 0 for OFF, 1 for ON
            self.lower_threshold = lower_threshold
            self.upper_threshold = upper_threshold

        def perceive(self, environment):
            return environment.get_temperature()

        def decide(self, temperature):
            if temperature >= self.upper_threshold:
                self.ac_status = 1
                return "Turning AC ON"
            elif temperature <= self.lower_threshold:
                self.ac_status = 0
                return "Turning AC OFF"
            else:
                return "Maintaining AC " + ("ON" if self.ac_status == 1 else "OFF")

        def act(self):
            return self.ac_status

    # Initialize simulation
    random.seed(42)
    room = RoomEnvironment(initial_temperature=22.0)
    agent = TemperatureAgent(lower_threshold=23.0, upper_threshold=25.0)

    time_steps = 30
    history_temp = []
    history_ac = []
    
    print("Simulation Output:\n")

    for step in range(1, time_steps + 1):
        temp = agent.perceive(room)
        action_desc = agent.decide(temp)
        ac_state = agent.act()
        
        history_temp.append(temp)
        history_ac.append(ac_state)
        
        print(f"Step {step:2d} | Temperature: {temp:.2f}°C | AC: {'ON' if ac_state == 1 else 'OFF':3s} | Action: {action_desc}")
        
        room.update_temperature(ac_state)

    # Visualization
    steps = np.arange(1, time_steps + 1)
    
    # Plot 1: Temperature over time
    plt.figure(figsize=(10, 5))
    plt.plot(steps, history_temp, marker='o', linestyle='-', color='b', label='Room Temperature')
    plt.axhline(y=25.0, color='r', linestyle='--', label='Upper Threshold (25°C)')
    plt.axhline(y=23.0, color='g', linestyle='--', label='Lower Threshold (23°C)')
    plt.fill_between(steps, 23.0, 25.0, color='green', alpha=0.1, label='Comfortable Range')
    plt.xlabel('Time Step')
    plt.ylabel('Temperature (°C)')
    plt.title('Room Temperature Control Over Time')
    plt.legend()
    plt.grid(True)
    plt.tight_layout()
    plt.savefig('temperature_plot.png')
    plt.close()

    # Plot 2: AC Status over time
    plt.figure(figsize=(10, 3))
    plt.step(steps, history_ac, where='mid', color='orange', linewidth=2)
    plt.yticks([0, 1], ['OFF (0)', 'ON (1)'])
    plt.xlabel('Time Step')
    plt.ylabel('AC Status')
    plt.title('Air Conditioner Status Over Time')
    plt.grid(axis='x')
    plt.tight_layout()
    plt.savefig('ac_status_plot.png')
    plt.close()

    return history_temp, history_ac

def generate_word_document(history_temp, history_ac):
    doc = Document()
    
    # Title
    title = doc.add_heading('Laboratory Experiment Report', 0)
    title.alignment = WD_ALIGN_PARAGRAPH.CENTER
    doc.add_heading('Goal-Based Intelligent Agent for Smart Home Temperature Control', level=1).alignment = WD_ALIGN_PARAGRAPH.CENTER
    
    # 1. AIM
    doc.add_heading('1. AIM', level=2)
    doc.add_paragraph('To design and implement a goal-based intelligent agent in Python that monitors and regulates room temperature within a predefined comfortable range by controlling an Air Conditioner (AC).')
    
    # 2. OBJECTIVE
    doc.add_heading('2. OBJECTIVE', level=2)
    doc.add_paragraph('1. To understand the concept of a goal-based intelligent agent and its interaction with an environment.')
    doc.add_paragraph('2. To simulate an environment where temperature fluctuates and an agent perceives these changes.')
    doc.add_paragraph('3. To implement decision-making logic using upper and lower threshold values (hysteresis) to achieve a desired goal.')
    doc.add_paragraph('4. To evaluate and visualize the performance of the intelligent agent over discrete time steps.')
    
    # 3. THEORY
    doc.add_heading('3. THEORY', level=2)
    p = doc.add_paragraph()
    p.add_run('Intelligent Agent: ').bold = True
    p.add_run('An autonomous entity that observes through sensors and acts upon an environment using actuators to achieve specific goals.\n')
    p.add_run('Agent Environment: ').bold = True
    p.add_run('The external space or system with which the agent interacts. In this experiment, it is a simulated room with fluctuating temperature.\n')
    p.add_run('Perception & Action: ').bold = True
    p.add_run('The agent receives data (temperature) as perception, processes it, and outputs an action (turning the AC ON or OFF).\n')
    p.add_run('Goal-based Agent: ').bold = True
    p.add_run('An agent that acts to achieve a specific goal state. Rather than simple condition-action rules, it considers whether its actions will help attain the goal.\n\n')
    p.add_run('The interaction follows this conceptual model:\n')
    p.add_run('Environment → Perception → Agent → Decision → Action → Environment\n\n')
    p.add_run('In the smart home scenario, the agent\'s sole goal is to maintain the room temperature within a predefined comfortable range, modifying the environment through its actions.')

    # 4. CASE STUDY
    doc.add_heading('4. CASE STUDY', level=2)
    doc.add_paragraph('Scenario: A smart home temperature control system.\n'
                      'Comfortable temperature range: 20°C – 24°C.\n'
                      'The agent receives the current room temperature from the simulated environment.')
    doc.add_paragraph('Decision Rules:')
    doc.add_paragraph('• If temperature >= 25°C → Turn AC ON', style='List Bullet')
    doc.add_paragraph('• If temperature <= 23°C → Turn AC OFF', style='List Bullet')
    doc.add_paragraph('• If temperature is between 23°C and 25°C → Maintain the previous AC state', style='List Bullet')
    doc.add_paragraph('This range introduces hysteresis, which prevents the AC from rapidly switching ON and OFF when the temperature hovers exactly at the threshold, ensuring energy efficiency and component longevity.')

    # 5. SYSTEM DESIGN
    doc.add_heading('5. SYSTEM DESIGN', level=2)
    p2 = doc.add_paragraph()
    p2.add_run('Environment: ').bold = True
    p2.add_run('Represents the room and maintains the current temperature.\n')
    p2.add_run('Sensor / Perception: ').bold = True
    p2.add_run('Provides the current room temperature to the agent.\n')
    p2.add_run('Intelligent Agent: ').bold = True
    p2.add_run('Analyzes the temperature and decides the required action.\n')
    p2.add_run('Actuator: ').bold = True
    p2.add_run('Represents the air conditioner.\n')
    p2.add_run('Goal: ').bold = True
    p2.add_run('Maintain a comfortable room temperature.')
    
    doc.add_paragraph('Flow Diagram:')
    doc.add_paragraph('Room Environment\n↓\nTemperature Sensor\n↓\nIntelligent Agent\n↓\nGoal Evaluation\n↓\nDecision\n↓\nAC ON / AC OFF\n↓\nRoom Temperature Changes\n↓\nFeedback')
    
    # 6. ALGORITHM
    doc.add_heading('6. ALGORITHM', level=2)
    algo = [
        "Start the program.",
        "Initialize the room temperature.",
        "Define the comfortable temperature range.",
        "Initialize AC status.",
        "Read the current room temperature.",
        "Compare the temperature with the desired range.",
        "Turn AC ON if the temperature reaches the upper threshold.",
        "Turn AC OFF if the temperature reaches the lower threshold.",
        "Maintain the previous AC state between the thresholds.",
        "Update the room temperature based on the AC state.",
        "Repeat the process for a fixed number of time steps.",
        "Record temperature and AC status.",
        "Plot the temperature variation.",
        "Display the result.",
        "Stop."
    ]
    for i, step in enumerate(algo, 1):
        doc.add_paragraph(f"{i}. {step}")

    # 7. PSEUDOCODE
    doc.add_heading('7. PSEUDOCODE', level=2)
    pseudocode = """
CLASS RoomEnvironment:
    INIT temperature
    METHOD get_temperature():
        RETURN temperature
    METHOD update_temperature(ac_status):
        IF ac_status == ON:
            temperature = temperature - decrement_value
        ELSE:
            temperature = temperature + increment_value

CLASS TemperatureAgent:
    INIT lower_threshold, upper_threshold, ac_status = OFF
    METHOD perceive(environment):
        RETURN environment.get_temperature()
    METHOD decide(temperature):
        IF temperature >= upper_threshold:
            ac_status = ON
        ELSE IF temperature <= lower_threshold:
            ac_status = OFF
        ELSE:
            KEEP ac_status
    METHOD act():
        RETURN ac_status

LOOP for N time steps:
    current_temp = agent.perceive(room)
    agent.decide(current_temp)
    current_ac = agent.act()
    room.update_temperature(current_ac)
    RECORD current_temp, current_ac
"""
    doc.add_paragraph(pseudocode, style='No Spacing')

    # 8. IMPLEMENTATION
    doc.add_heading('8. IMPLEMENTATION', level=2)
    doc.add_paragraph('The experiment is implemented in Python using the Object-Oriented Programming paradigm. It simulates the RoomEnvironment and TemperatureAgent components utilizing standard Python logic along with NumPy and Matplotlib for data processing and visualization.')

    # 9. SIMULATION & 10. DATA COLLECTION
    doc.add_heading('9. SIMULATION & 10. DATA COLLECTION', level=2)
    doc.add_paragraph('The simulation runs for 30 time steps. At each step, the temperature and AC status are recorded in arrays for visualization and tabular display.')
    
    # Add a table for all 30 steps to keep it complete
    table = doc.add_table(rows=1, cols=3)
    table.style = 'Table Grid'
    hdr_cells = table.rows[0].cells
    hdr_cells[0].text = 'Time Step'
    hdr_cells[1].text = 'Temperature (°C)'
    hdr_cells[2].text = 'AC Status'
    
    for step in range(30):
        row_cells = table.add_row().cells
        row_cells[0].text = str(step + 1)
        row_cells[1].text = f"{history_temp[step]:.2f}"
        row_cells[2].text = 'ON' if history_ac[step] == 1 else 'OFF'
        
    # 11. VISUALIZATION
    doc.add_heading('11. VISUALIZATION', level=2)
    doc.add_paragraph('The graphs below illustrate the temperature variation and AC status over 30 time steps. The shaded green region represents the optimal comfortable temperature range.')
    
    if os.path.exists('temperature_plot.png'):
        doc.add_picture('temperature_plot.png', width=Inches(6.0))
    if os.path.exists('ac_status_plot.png'):
        doc.add_picture('ac_status_plot.png', width=Inches(6.0))

    # 12. COMPLETE PYTHON CODE
    doc.add_heading('12. COMPLETE PYTHON CODE', level=2)
    code_text = """
import random
import numpy as np
import matplotlib.pyplot as plt

class RoomEnvironment:
    def __init__(self, initial_temperature):
        self.current_temperature = initial_temperature

    def get_temperature(self):
        return self.current_temperature

    def update_temperature(self, ac_status):
        # Add random variation for realism
        variation = random.uniform(-0.2, 0.2)
        if ac_status == 1: # AC is ON
            self.current_temperature -= (0.5 + variation)
        else: # AC is OFF
            self.current_temperature += (0.4 + variation)

class TemperatureAgent:
    def __init__(self, lower_threshold, upper_threshold):
        self.ac_status = 0 # 0 for OFF, 1 for ON
        self.lower_threshold = lower_threshold
        self.upper_threshold = upper_threshold

    def perceive(self, environment):
        return environment.get_temperature()

    def decide(self, temperature):
        if temperature >= self.upper_threshold:
            self.ac_status = 1
            return "Turning AC ON"
        elif temperature <= self.lower_threshold:
            self.ac_status = 0
            return "Turning AC OFF"
        else:
            return "Maintaining AC " + ("ON" if self.ac_status == 1 else "OFF")

    def act(self):
        return self.ac_status

def main():
    random.seed(42) # For reproducible results
    room = RoomEnvironment(initial_temperature=22.0)
    agent = TemperatureAgent(lower_threshold=23.0, upper_threshold=25.0)

    time_steps = 30
    history_temp = []
    history_ac = []

    print("Simulation Started...")
    print("-" * 50)
    
    for step in range(1, time_steps + 1):
        # Agent perceives the environment
        temp = agent.perceive(room)
        
        # Agent makes a decision
        action_desc = agent.decide(temp)
        
        # Agent acts
        ac_state = agent.act()
        
        # Store data
        history_temp.append(temp)
        history_ac.append(ac_state)
        
        print(f"Step {step:2d} | Temperature: {temp:.2f}°C | AC: {'ON' if ac_state == 1 else 'OFF':3s} | Action: {action_desc}")
        
        # Environment reacts to the action
        room.update_temperature(ac_state)

    print("-" * 50)
    print("Simulation Completed.")

    # Visualization
    steps = np.arange(1, time_steps + 1)

    # Plot 1: Temperature variation
    plt.figure(figsize=(10, 5))
    plt.plot(steps, history_temp, marker='o', linestyle='-', color='b', label='Room Temperature')
    plt.axhline(y=25.0, color='r', linestyle='--', label='Upper Threshold (25°C)')
    plt.axhline(y=23.0, color='g', linestyle='--', label='Lower Threshold (23°C)')
    plt.fill_between(steps, 23.0, 25.0, color='green', alpha=0.1, label='Comfortable Range')
    plt.xlabel('Time Step')
    plt.ylabel('Temperature (°C)')
    plt.title('Room Temperature Control Over Time')
    plt.legend()
    plt.grid(True)
    plt.tight_layout()
    plt.show()

    # Plot 2: AC Status variation
    plt.figure(figsize=(10, 3))
    plt.step(steps, history_ac, where='mid', color='orange', linewidth=2)
    plt.yticks([0, 1], ['OFF (0)', 'ON (1)'])
    plt.xlabel('Time Step')
    plt.ylabel('AC Status')
    plt.title('Air Conditioner Status Over Time')
    plt.grid(axis='x')
    plt.tight_layout()
    plt.show()

if __name__ == "__main__":
    main()
"""
    doc.add_paragraph(code_text, style='No Spacing')

    # 13. EXPECTED OUTPUT
    doc.add_heading('13. EXPECTED OUTPUT', level=2)
    doc.add_paragraph('The console outputs the discrete time steps. Note: Numerical values are illustrative and actual values may vary depending on the simulation variations.')
    sample_output = """
Step  1 | Temperature: 22.00°C | AC: OFF | Action: Turning AC OFF
Step  2 | Temperature: 22.35°C | AC: OFF | Action: Turning AC OFF
...
Step 10 | Temperature: 25.40°C | AC: ON  | Action: Turning AC ON
Step 11 | Temperature: 24.80°C | AC: ON  | Action: Maintaining AC ON
...
"""
    doc.add_paragraph(sample_output, style='No Spacing')
    doc.add_paragraph('The first graph should demonstrate the temperature fluctuating within and around the comfortable range (23°C - 25°C). The second graph should show a step plot toggling between 0 (OFF) and 1 (ON) correlated with the temperature crossing the thresholds.')

    # 14. RESULT
    doc.add_heading('14. RESULT', level=2)
    doc.add_paragraph('The goal-based intelligent agent successfully monitors the simulated room temperature and controls the AC according to the defined temperature goal, preventing extreme temperatures.')

    # 15. CONCLUSION
    doc.add_heading('15. CONCLUSION', level=2)
    doc.add_paragraph('The experiment effectively demonstrated the functioning of a goal-based intelligent agent. The agent perceives the environment through the simulated temperature value, evaluates it against the objective function (comfortable temperature thresholds), and makes deterministic decisions to turn the AC ON or OFF. The feedback loop established by these actions modifying the environment dictates the agent\'s subsequent decisions, showcasing how intelligent agents interact continuously to achieve a steady state.')

    # 16. APPLICATION
    doc.add_heading('16. APPLICATION', level=2)
    doc.add_paragraph('1. Smart home temperature control and intelligent thermostat devices.')
    doc.add_paragraph('2. HVAC (Heating, Ventilation, and Air Conditioning) automation in commercial buildings.')
    doc.add_paragraph('3. Energy management systems aimed at reducing power consumption.')
    doc.add_paragraph('4. Industrial IoT-based automation systems where maintaining environmental parameters is critical.')

    doc.save('Smart_Home_Temperature_Intelligent_Agent.docx')
    print("Report generated successfully: Smart_Home_Temperature_Intelligent_Agent.docx")

if __name__ == "__main__":
    temp, ac = run_simulation_and_plot()
    generate_word_document(temp, ac)
