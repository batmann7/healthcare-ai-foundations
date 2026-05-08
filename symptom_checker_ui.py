from dotenv import load_dotenv
import os
from google import genai
import gradio as gr

# 1. Load API key and create Gemini client (same as before)
load_dotenv()
api_key = os.getenv("GEMINI_API_KEY")
client = genai.Client(api_key=api_key)

# 2. The callback function – this is the brain
def symptom_checker(symptoms):
    """
    Takes user symptoms, sends them to Gemini with a safe medical prompt,
    and returns the AI's structured advice.
    """
    system_prompt = """
    You are a helpful and cautious medical triage assistant.
    Based on the symptoms described, provide a structured response with:
    1. Possible causes (list 2-3 common ones)
    2. Recommended next steps (home care, pharmacy visit, or see a doctor)
    3. Urgency level (Low / Medium / High)
    4. A clear disclaimer: "I am an AI, not a doctor. Always consult a healthcare professional."

    Keep your tone calm and informative. Do NOT make a definitive diagnosis.
    """

    full_prompt = f"{system_prompt}\n\nUser symptoms: {symptoms}"

    # 3. Call Gemini
    response = client.models.generate_content(
        model="gemini-2.5-flash",
        contents=full_prompt
    )
    return response.text

# 4. Build the Gradio interface
ui = gr.Interface(
    fn=symptom_checker, # the Python function to call
    inputs=gr.Textbox(lines=4, placeholder="Describe your symptoms here..."),
    outputs=gr.Textbox(label="AI Triage Advice"),
    title="🏥 AI Symptom Checker",
    description="Describe your symptoms, and an AI assistant will provide general guidance. **This is not a medical diagnosis.**"
)

# 5. Launch the web app
if __name__ == "__main__":
    ui.launch()