/**
 * Goal-Based Intelligent Agent for Smart Home Temperature Control
 */

// --- CLASSES ---

class RoomEnvironment {
    constructor(initialTemp) {
        this.temperature = initialTemp;
        this.step = 0;
    }

    getTemperature() {
        return this.temperature;
    }

    updateTemperature(acState) {
        this.step++;
        // Small random noise between -0.15 and +0.15
        const noise = (Math.random() * 0.3) - 0.15;
        
        if (acState === 1) { // AC is ON
            // Cooling the room
            this.temperature -= (0.5 + noise);
        } else { // AC is OFF
            // Room naturally heats up
            this.temperature += (0.4 + noise);
        }
        
        // Keep temperature rounded to 2 decimals internally
        this.temperature = Math.round(this.temperature * 100) / 100;
    }
}

class TemperatureAgent {
    constructor(lowerThreshold, upperThreshold) {
        this.lowerThreshold = lowerThreshold;
        this.upperThreshold = upperThreshold;
        this.acState = 0; // 0 = OFF, 1 = ON
        this.decisionLog = "";
    }

    perceive(environment) {
        return environment.getTemperature();
    }

    decide(temp) {
        if (temp >= this.upperThreshold) {
            this.acState = 1;
            this.decisionLog = "Temperature exceeds upper threshold. Turning AC ON.";
            return "Turn AC ON";
        } else if (temp <= this.lowerThreshold) {
            this.acState = 0;
            this.decisionLog = "Temperature below lower threshold. Turning AC OFF.";
            return "Turn AC OFF";
        } else {
            this.decisionLog = `Temperature is within hysteresis bounds. Maintaining AC ${this.acState === 1 ? 'ON' : 'OFF'}.`;
            return `Maintain AC ${this.acState === 1 ? 'ON' : 'OFF'}`;
        }
    }

    act() {
        return this.acState;
    }
}

// --- DOM ELEMENTS ---
const elTemp = document.getElementById('current-temp');
const elAcStatus = document.getElementById('ac-status');
const elEnergy = document.getElementById('energy-usage');
const elRoomBg = document.getElementById('room-bg');
const elRoomTemp = document.getElementById('room-temp-display');
const elRoomIndicator = document.getElementById('room-ac-indicator');
const elAirflow = document.getElementById('airflow');

const elReasonPerception = document.getElementById('reason-perception');
const elReasonDecision = document.getElementById('reason-decision');
const elReasonAction = document.getElementById('reason-action');

const btnStart = document.getElementById('btn-start');
const btnPause = document.getElementById('btn-pause');
const btnReset = document.getElementById('btn-reset');
const speedInputs = document.querySelectorAll('input[name="speed"]');
const tableBody = document.querySelector('#log-table tbody');

// --- SIMULATION VARIABLES ---
let simulationInterval;
let isRunning = false;
let simSpeed = 1000;
let room, agent;
let energyUsage = 0;

// Chart objects
let tempChart, acChart;

// Data arrays for charts
let chartLabels = [];
let chartTempData = [];
let chartAcData = [];

// --- INITIALIZATION ---

function initCharts() {
    const ctxTemp = document.getElementById('tempChart').getContext('2d');
    const ctxAc = document.getElementById('acChart').getContext('2d');

    Chart.defaults.font.family = "'Inter', sans-serif";

    tempChart = new Chart(ctxTemp, {
        type: 'line',
        data: {
            labels: chartLabels,
            datasets: [
                {
                    label: 'Room Temp (°C)',
                    data: chartTempData,
                    borderColor: '#2563eb',
                    backgroundColor: 'rgba(37, 99, 235, 0.1)',
                    tension: 0.2,
                    fill: false
                },
                {
                    label: 'Upper Threshold (25°C)',
                    data: [], // Will be filled dynamically
                    borderColor: '#ef4444',
                    borderDash: [5, 5],
                    pointRadius: 0,
                    fill: false
                },
                {
                    label: 'Lower Threshold (23°C)',
                    data: [],
                    borderColor: '#10b981',
                    borderDash: [5, 5],
                    pointRadius: 0,
                    fill: '-1',
                    backgroundColor: 'rgba(16, 185, 129, 0.1)'
                }
            ]
        },
        options: {
            responsive: true,
            maintainAspectRatio: false,
            scales: {
                y: { min: 20, max: 32 }
            },
            animation: { duration: 0 } // Disable animation for performance
        }
    });

    acChart = new Chart(ctxAc, {
        type: 'line',
        data: {
            labels: chartLabels,
            datasets: [{
                label: 'AC Status',
                data: chartAcData,
                borderColor: '#f59e0b',
                stepped: 'middle',
                borderWidth: 2,
                pointRadius: 0
            }]
        },
        options: {
            responsive: true,
            maintainAspectRatio: false,
            scales: {
                y: {
                    min: -0.2, 
                    max: 1.2,
                    ticks: {
                        callback: function(value) {
                            if(value === 0) return 'OFF (0)';
                            if(value === 1) return 'ON (1)';
                            return null;
                        }
                    }
                }
            },
            animation: { duration: 0 }
        }
    });
}

function updateCharts() {
    // Fill threshold lines
    tempChart.data.datasets[1].data = Array(chartLabels.length).fill(25);
    tempChart.data.datasets[2].data = Array(chartLabels.length).fill(23);
    
    // Keep charts from growing infinitely (max 50 points)
    if (chartLabels.length > 50) {
        chartLabels.shift();
        chartTempData.shift();
        chartAcData.shift();
        tempChart.data.datasets[1].data.shift();
        tempChart.data.datasets[2].data.shift();
    }
    
    tempChart.update();
    acChart.update();
}

function resetSimulation() {
    stopSimulation();
    
    room = new RoomEnvironment(29.0); // Start hot
    agent = new TemperatureAgent(23.0, 25.0);
    energyUsage = 0;
    
    chartLabels.length = 0;
    chartTempData.length = 0;
    chartAcData.length = 0;
    
    tableBody.innerHTML = '';
    
    updateUI(room.getTemperature(), 0, "Initializing", "Agent ready");
    if(tempChart) updateCharts();
    
    btnStart.disabled = false;
    btnPause.disabled = true;
}

// --- UI UPDATES ---

function updateUI(temp, acState, actionShort, reasoningLong) {
    const tempStr = temp.toFixed(1) + "°C";
    
    // Update Dashboard Metrics
    elTemp.textContent = tempStr;
    elAcStatus.textContent = acState === 1 ? "ON" : "OFF";
    elAcStatus.className = "value " + (acState === 1 ? "status-on" : "status-off");
    elEnergy.textContent = energyUsage + " units";

    // Update Room Visuals
    elRoomTemp.textContent = tempStr;
    if (temp >= 25) {
        elRoomBg.style.background = 'linear-gradient(to bottom, #fee2e2, #fca5a5)'; // Hot
    } else if (temp <= 23) {
        elRoomBg.style.background = 'linear-gradient(to bottom, #eff6ff, #93c5fd)'; // Cold
    } else {
        elRoomBg.style.background = 'linear-gradient(to bottom, #ecfdf5, #a7f3d0)'; // Good
    }

    if (acState === 1) {
        elAirflow.classList.remove('hidden');
        elRoomIndicator.textContent = "❄ AC Cooling";
        elRoomIndicator.style.color = "var(--primary)";
    } else {
        elAirflow.classList.add('hidden');
        elRoomIndicator.textContent = "○ AC Off";
        elRoomIndicator.style.color = "var(--text-muted)";
    }

    // Update Agent Reasoning
    elReasonPerception.textContent = tempStr;
    elReasonDecision.textContent = reasoningLong;
    elReasonAction.textContent = actionShort;
    if(actionShort.includes('ON')) {
        elReasonAction.style.color = 'var(--primary)';
    } else {
        elReasonAction.style.color = 'var(--text-main)';
    }
}

function addTableRow(step, temp, acState, action) {
    const tr = document.createElement('tr');
    tr.innerHTML = `
        <td>${step}</td>
        <td>${temp.toFixed(2)}</td>
        <td style="color: ${acState===1?'#2563eb':'#64748b'}; font-weight: bold;">${acState === 1 ? 'ON' : 'OFF'}</td>
        <td>${action}</td>
    `;
    tableBody.prepend(tr);
    
    // Keep max 20 rows in table
    if (tableBody.children.length > 20) {
        tableBody.removeChild(tableBody.lastChild);
    }
}

// --- MAIN LOOP ---

function simulationStep() {
    const currentTemp = agent.perceive(room);
    const actionDesc = agent.decide(currentTemp);
    const acState = agent.act();
    
    if (acState === 1) energyUsage++;
    
    // Log Data
    chartLabels.push(room.step);
    chartTempData.push(currentTemp);
    chartAcData.push(acState);
    
    updateUI(currentTemp, acState, actionDesc, agent.decisionLog);
    updateCharts();
    addTableRow(room.step, currentTemp, acState, actionDesc);
    
    room.updateTemperature(acState);
}

function startSimulation() {
    if (isRunning) return;
    isRunning = true;
    btnStart.disabled = true;
    btnPause.disabled = false;
    
    simulationStep(); // run one immediately
    simulationInterval = setInterval(simulationStep, simSpeed);
}

function stopSimulation() {
    isRunning = false;
    clearInterval(simulationInterval);
    btnStart.disabled = false;
    btnPause.disabled = true;
}

// --- EVENT LISTENERS ---
btnStart.addEventListener('click', startSimulation);
btnPause.addEventListener('click', stopSimulation);
btnReset.addEventListener('click', resetSimulation);

speedInputs.forEach(input => {
    input.addEventListener('change', (e) => {
        simSpeed = parseInt(e.target.value);
        if (isRunning) {
            stopSimulation();
            startSimulation();
        }
    });
});

// Init on load
document.addEventListener("DOMContentLoaded", () => {
    initCharts();
    resetSimulation();
});
