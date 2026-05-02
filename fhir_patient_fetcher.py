import requests

# Public FHIR test server – Patient search (returns up to 10 by default)
url = "https://hapi.fhir.org/baseR4/Patient"

# Send the GET request
response = requests.get(url)

# Turn the response into a Python dictionary
data = response.json()

# The patients are inside data["entry"] (each entry has a "resource" key)
entries = data.get("entry", [])

print("=== Live FHIR Patients (first 5) ===")
for idx, entry in enumerate(entries[:5]):
    patient = entry["resource"]
    
    # Extract name: FHIR stores names as a list of HumanName objects
    names = patient.get("name", [])
    if names:
        family = names[0].get("family", "No family name")
        given = " ".join(names[0].get("given", []))
        full_name = f"{given} {family}"
    else:
        full_name = "No name provided"
    
    patient_id = patient.get("id", "No ID")
    
    print(f"{idx+1}. {full_name} (ID: {patient_id})")