class SymptomEnvironment {
    constructor() { this.selectedSymptoms = new Set(); }
    setSymptoms(symptoms) { this.selectedSymptoms = new Set(symptoms); }
    getSymptoms() { return [...this.selectedSymptoms]; }
    clearSymptoms() { this.selectedSymptoms.clear(); }
}

class MedicalReasoningAgent {
    constructor(knowledge, ruleBase) {
        this.knowledgeBase = knowledge;
        this.rules = ruleBase;
        this.currentFacts = [];
        this.reasoningTrace = [];
    }

    perceive(symptoms) {
        this.currentFacts = [];
        this.reasoningTrace = [{ type: "perception", message: `Received ${symptoms.length} symptom signal${symptoms.length === 1 ? "" : "s"}.` }];
        this.createFacts(symptoms);
    }

    createFacts(symptoms) {
        this.currentFacts = [...symptoms];
        this.reasoningTrace.push({ type: "facts", message: `Created ${this.currentFacts.length} logical fact${this.currentFacts.length === 1 ? "" : "s"}.` });
    }

    evaluateRules() {
        const evaluations = this.rules.map(rule => {
            const matchedSymptoms = rule.requiredSymptoms.filter(symptom => this.currentFacts.includes(symptom));
            const score = Math.round((matchedSymptoms.length / rule.requiredSymptoms.length) * 100);
            const evaluation = {
                ruleId: rule.id,
                condition: rule.condition,
                conclusion: rule.conclusion,
                explanation: rule.explanation,
                requiredSymptoms: rule.requiredSymptoms,
                matchedSymptoms,
                matchedCount: matchedSymptoms.length,
                totalRequired: rule.requiredSymptoms.length,
                score,
                useful: score >= 40
            };
            this.reasoningTrace.push({ type: "rule", ...evaluation });
            return evaluation;
        });
        this.reasoningTrace.push({ type: "inference", message: `${evaluations.filter(item => item.useful).length} useful rule match${evaluations.filter(item => item.useful).length === 1 ? "" : "es"} derived.` });
        return evaluations;
    }

    infer() { return this.evaluateRules().filter(result => result.useful).sort((a, b) => b.score - a.score || a.ruleId.localeCompare(b.ruleId)); }
    explain() { return this.reasoningTrace; }
    generateResult() { return this.infer(); }
}

const testCases = {
    flu: ["fever", "cough", "body_ache", "fatigue", "headache"],
    cold: ["runny_nose", "sneezing", "sore_throat", "mild_cough"],
    migraine: ["headache", "nausea", "sensitivity_to_light"],
    allergy: ["sneezing", "runny_nose", "itchy_eyes"],
    stomach: ["stomach_pain", "vomiting", "diarrhea", "nausea"],
    "no-match": ["fever", "itchy_eyes"]
};

const environment = new SymptomEnvironment();
const agent = new MedicalReasoningAgent(knowledgeBase, rules);
let matchChartInstance = null;

function labelFor(symptom) { return symptomLabels[symptom] || symptom; }
function escapeHtml(value) { return String(value).replace(/[&<>'"]/g, char => ({ "&": "&amp;", "<": "&lt;", ">": "&gt;", "'": "&#39;", '"': "&quot;" }[char])); }

function renderSymptoms() {
    const container = document.getElementById("symptoms-container");
    Object.entries(symptomGroups).forEach(([group, symptoms]) => {
        const section = document.createElement("div");
        section.className = "symptom-group";
        section.innerHTML = `<h3>${escapeHtml(group)}</h3><div class="symptom-grid">${symptoms.map(symptom => `<label class="symptom-card" for="symptom-${symptom}"><input type="checkbox" id="symptom-${symptom}" value="${symptom}"><span class="checkmark"></span><span>${escapeHtml(labelFor(symptom))}</span></label>`).join("")}</div>`;
        container.appendChild(section);
    });
    container.addEventListener("change", updateSelectionPreview);
}

function selectedFromInputs() { return [...document.querySelectorAll("input[type=checkbox]:checked")].map(input => input.value); }
function updateSelectionPreview() {
    const selected = selectedFromInputs();
    document.getElementById("selection-count").textContent = `${selected.length} selected`;
    document.getElementById("summary-number").textContent = selected.length;
    document.getElementById("fact-status").textContent = selected.length ? "Facts ready" : "Waiting for input";
    const list = document.getElementById("selected-symptoms-list");
    list.innerHTML = selected.length ? selected.map(symptom => `<span class="selected-chip"><span>✓</span>${escapeHtml(labelFor(symptom))}</span>`).join("") : '<p class="empty-state">Select symptoms to populate the environment.</p>';
}

function setActiveSteps() { document.querySelectorAll(".timeline-step").forEach((step, index) => { step.classList.remove("is-active"); window.setTimeout(() => step.classList.add("is-active"), index * 90); }); }

function renderReasoning(selected, evaluations, results) {
    document.getElementById("reasoning-panel").classList.add("is-visible");
    document.getElementById("trace-status").textContent = "Trace complete";
    document.getElementById("perception-output").textContent = `Agent perceived ${selected.length} signal${selected.length === 1 ? "" : "s"} from the environment.`;
    document.getElementById("facts-box").innerHTML = selected.map(symptom => `<span class="fact-chip">${escapeHtml(labelFor(symptom))}</span>`).join("");
    document.getElementById("eval-log").innerHTML = evaluations.map(item => `<div class="rule-trace-row"><span class="trace-rule">${item.ruleId}</span><span>${escapeHtml(item.condition)}</span><strong>${item.matchedCount}/${item.totalRequired}</strong><span class="trace-bar"><i style="width:${item.score}%"></i></span></div>`).join("");
    document.getElementById("inference-output").innerHTML = results.length ? `<strong>${results.length} conclusion${results.length === 1 ? "" : "s"} derived.</strong> Ranked by rule-match score.` : "No rule reached the demonstration threshold of 40%.";
    setActiveSteps();
}

function renderResults(results) {
    const resultContainer = document.getElementById("results-container");
    const noMatch = document.getElementById("no-match-message");
    document.getElementById("results-panel").classList.add("is-visible");
    if (!results.length) {
        resultContainer.innerHTML = "";
        noMatch.hidden = false;
        document.getElementById("chart-card").hidden = true;
        return;
    }
    noMatch.hidden = true;
    document.getElementById("chart-card").hidden = false;
    resultContainer.innerHTML = results.map((result, index) => `<article class="result-card"><div class="result-top"><div class="rank">0${index + 1}</div><div><p class="result-label">Possible condition pattern</p><h3>${escapeHtml(result.condition)}</h3></div><div class="score"><strong>${result.score}%</strong><span>rule match</span></div></div><div class="score-track"><i style="width:${result.score}%"></i></div><div class="result-meta"><span><b>Rule</b> ${result.ruleId}</span><span><b>Matched</b> ${result.matchedCount} / ${result.totalRequired}</span></div><p class="matched-line"><b>Matched symptoms:</b> ${result.matchedSymptoms.map(labelFor).map(escapeHtml).join(", ")}</p><p class="result-reason">${escapeHtml(result.explanation)}</p></article>`).join("");
    renderChart(results);
}

function renderChart(results) {
    if (!window.Chart) return;
    if (matchChartInstance) matchChartInstance.destroy();
    matchChartInstance = new Chart(document.getElementById("matchChart"), { type: "bar", data: { labels: results.map(item => item.condition), datasets: [{ data: results.map(item => item.score), backgroundColor: ["#19a79b", "#f17b62", "#6c63c9", "#e0a83e", "#3d7ea6", "#7b8794"], borderRadius: 6, borderSkipped: false, barThickness: 28 }] }, options: { responsive: true, maintainAspectRatio: false, plugins: { legend: { display: false }, tooltip: { callbacks: { label: context => ` ${context.raw}% rule match` } } }, scales: { y: { beginAtZero: true, max: 100, ticks: { callback: value => `${value}%` }, grid: { color: "#e7eceb" } }, x: { grid: { display: false }, ticks: { color: "#52615f" } } } } });
}

function analyzeSymptoms() {
    const selected = selectedFromInputs();
    if (!selected.length) { document.getElementById("selection-count").textContent = "Select at least one"; document.querySelector(".symptoms-panel").classList.add("shake"); window.setTimeout(() => document.querySelector(".symptoms-panel").classList.remove("shake"), 450); return; }
    environment.setSymptoms(selected);
    agent.perceive(environment.getSymptoms());
    const evaluations = agent.evaluateRules();
    const results = evaluations.filter(result => result.useful).sort((a, b) => b.score - a.score || a.ruleId.localeCompare(b.ruleId));
    renderReasoning(selected, evaluations, results);
    renderResults(results);
    document.getElementById("results-panel").scrollIntoView({ behavior: "smooth", block: "start" });
}

function resetApp() {
    document.querySelectorAll("input[type=checkbox]").forEach(input => { input.checked = false; });
    environment.clearSymptoms();
    updateSelectionPreview();
    document.getElementById("reasoning-panel").classList.remove("is-visible");
    document.getElementById("results-panel").classList.remove("is-visible");
    document.getElementById("no-match-message").hidden = true;
    document.getElementById("results-container").innerHTML = "";
    document.getElementById("chart-card").hidden = false;
    if (matchChartInstance) { matchChartInstance.destroy(); matchChartInstance = null; }
}

function loadTestCase(type) {
    resetApp();
    (testCases[type] || []).forEach(symptom => { const checkbox = document.getElementById(`symptom-${symptom}`); if (checkbox) checkbox.checked = true; });
    updateSelectionPreview();
    document.querySelector(".symptoms-panel").scrollIntoView({ behavior: "smooth", block: "center" });
}

document.addEventListener("DOMContentLoaded", () => {
    renderSymptoms();
    updateSelectionPreview();
    document.getElementById("analyze-btn").addEventListener("click", analyzeSymptoms);
    document.getElementById("reset-btn").addEventListener("click", resetApp);
    document.querySelectorAll(".test-case").forEach(button => button.addEventListener("click", () => loadTestCase(button.dataset.case)));
});

window.loadTestCase = loadTestCase;
