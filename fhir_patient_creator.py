from fhir.resources.patient import Patient
from fhir.resources.humanname import HumanName

# Create a synthetic FHIR Patient
patient = Patient(
    id="P001",
    name=[
        HumanName(
            family="Khan",
            given=["Ali"]
        )
    ],
    gender="male",
    birthDate="1990-07-12"
)

# Print directly as JSON (handles dates internally)
print(patient.json(indent=2))