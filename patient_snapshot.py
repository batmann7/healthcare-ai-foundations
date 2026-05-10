from dotenv import load_dotenv
import os
import pandas as pd
from google import genai

load_dotenv()
client = genai.Client(api_key=os.getenv("GEMINI_API_KEY"))

# ---- 1. Load vitals CSV ----
df = pd.read_csv("vitals.csv")

# ---- 2. Mock FHIR patients (simulates fetching from a server) ----
fhir_patients = {
    "P001": {"name": "Ali Khan", "birthDate": "1990-01-15"},
    "P002": {"name": "Sara Ahmed", "birthDate": "1985-07-22"},
    "P003": {"name": "Bilal Mahmood", "birthDate": "1972-11-03"},
    "P004": {"name": "Fatima Noor", "birthDate": "2000-05-30"},
    "P005": {"name": "Omar Farooq", "birthDate": "1965-09-12"},
    "P006": {"name": "Ayesha Iqbal", "birthDate": "1998-03-08"},
    "P007": {"name": "Hassan Raza", "birthDate": "1980-12-19"},
    "P008": {"name": "Zainab Tariq", "birthDate": "1993-06-25"},
    "P009": {"name": "Usman Javed", "birthDate": "2002-08-14"},
    "P010": {"name": "Mariam Saeed", "birthDate": "1978-01-02"},
}

# ---- 3. Ask for patient ID ----
patient_id = input("Enter patient ID (e.g., P001): ").strip()

# ---- 4. Get patient info ----
patient = fhir_patients.get(patient_id)
vitals = df[df["patient_id"] == patient_id]

if patient is None or vitals.empty:
    print("Patient not found. Check the ID and try again.")
    exit()

name = patient["name"]
heart_rate = int(vitals["heart_rate"].iloc[0])
spo2 = int(vitals["spo2"].iloc[0])
systolic = int(vitals["systolic_bp"].iloc[0])
diastolic = int(vitals["diastolic_bp"].iloc[0])

# ---- 5. Flag abnormalities ----
flags = []
if heart_rate < 60:
    flags.append("Bradycardia (HR < 60)")
elif heart_rate > 100:
    flags.append("Tachycardia (HR > 100)")
if spo2 < 90:
    flags.append("Hypoxia (SpO2 < 90)")

flag_text = ", ".join(flags) if flags else "No critical abnormalities"

# ---- 6. Build summary for LLM ----
summary = f"""
Patient: {name} (ID: {patient_id})
Vitals: HR={heart_rate}, SpO2={spo2}%, BP={systolic}/{diastolic}
Abnormalities: {flag_text}
"""

# ---- 7. Triage via Gemini ----
triage_prompt = f"""
You are an emergency triage nurse. Based on the following patient snapshot, give a one‑sentence triage recommendation (e.g., 'Routine follow‑up', 'Urgent care within 24h', 'Emergency department immediately').

{summary}
"""

response = client.models.generate_content(
    model="gemini-2.5-flash",
    contents=triage_prompt
)

# ---- 8. Final output ----
print("\n" + "="*50)
print(" PATIENT SNAPSHOT")
print("="*50)
print(summary)
print("TRIAGE RECOMMENDATION:")
print(response.text.strip())