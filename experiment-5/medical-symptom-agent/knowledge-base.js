// Fictional demonstration knowledge. This is not medical advice or real patient data.
const knowledgeBase = {
    conditions: [
        { name: "Common Cold", symptoms: ["runny_nose", "sneezing", "sore_throat", "mild_cough"], explanation: "Demo rule match for a cluster of common cold-like symptoms." },
        { name: "Influenza", symptoms: ["fever", "cough", "body_ache", "fatigue", "headache"], explanation: "Demo rule match for a cluster of flu-like symptoms." },
        { name: "Migraine", symptoms: ["headache", "nausea", "sensitivity_to_light"], explanation: "Demo rule match for a headache and light-sensitivity pattern." },
        { name: "Allergic Rhinitis", symptoms: ["sneezing", "runny_nose", "itchy_eyes"], explanation: "Demo rule match for a sneezing and itchy-eye pattern." },
        { name: "Gastroenteritis", symptoms: ["stomach_pain", "vomiting", "diarrhea", "nausea"], explanation: "Demo rule match for a gastrointestinal symptom pattern." },
        { name: "Dehydration", symptoms: ["thirst", "dizziness", "fatigue", "dry_mouth"], explanation: "Demo rule match for a fluid-loss symptom pattern." }
    ]
};

const rules = knowledgeBase.conditions.map((condition, index) => ({
    id: `R${index + 1}`,
    condition: condition.name,
    requiredSymptoms: condition.symptoms,
    conclusion: `Possible ${condition.name} pattern`,
    explanation: condition.explanation
}));

const symptomGroups = {
    "General": ["fever", "fatigue", "dizziness", "thirst", "dry_mouth"],
    "Respiratory": ["cough", "mild_cough", "runny_nose", "sneezing", "sore_throat"],
    "Pain & Neurological": ["headache", "body_ache", "sensitivity_to_light"],
    "Digestive": ["nausea", "vomiting", "diarrhea", "stomach_pain"],
    "Allergy": ["itchy_eyes"]
};

const symptomLabels = {
    fever: "Fever", cough: "Cough", mild_cough: "Mild Cough", headache: "Headache",
    body_ache: "Body Ache", fatigue: "Fatigue", runny_nose: "Runny Nose", sneezing: "Sneezing",
    sore_throat: "Sore Throat", nausea: "Nausea", vomiting: "Vomiting", diarrhea: "Diarrhea",
    stomach_pain: "Stomach Pain", dizziness: "Dizziness", thirst: "Thirst", dry_mouth: "Dry Mouth",
    itchy_eyes: "Itchy Eyes", sensitivity_to_light: "Sensitivity to Light"
};
