from fastapi import FastAPI, Request, Form
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from transformers import pipeline
import os, traceback
import openai
from openai import OpenAI
from dotenv import load_dotenv

# =====================================
# Load OpenAI API Key securely
# =====================================
load_dotenv()
def load_openai_api_key(key_name):
    """
    Loads the OpenAI API key from the environment variables.
    Returns the key if found, otherwise prints an error message.
    """
    try:
        key = os.getenv(key_name)
        if key:
            print("✅ Key is accessed successfully")
        else:
            print("❌ Key is not loaded. Please check your .env file or key name.")
        return key
    except Exception as e:
        print("Something went wrong while loading the key:", e)
        return None

openai_key = load_openai_api_key("openai_sec_key")

# =====================================
# Initialize FastAPI App
# =====================================
app = FastAPI(
    title="Marriage Prediction App",
    description="An AI-powered tool that predicts when a person is likely to get married based on multiple personal and social factors.",
    version="1.0.0"
)

# =====================================
# Initialize OpenAI Client
# =====================================
client = OpenAI(api_key=openai_key)
if client:
    print("✅ OpenAI Client successfully created")
else:
    print("❌ Failed to create OpenAI Client")


# =====================================
# Generate AI Response using GPT Model
# =====================================
def get_ai_response(prompt):
    """
    Sends a structured prompt to the GPT model and retrieves a response.
    The AI is instructed to:
    - Predict how soon the person may get married.
    - Give 10 actionable, personalized suggestions for improvement.
    - Reject predictions if age < 16.
    """
    message = [
        {
            "role": "system",
            "content": (
                "You are an intelligent assistant that predicts when a person is likely to get married "
                "based on their detailed personal, social, financial, and health information. "
                "If the user's age is below 16, clearly state that the person is too young and not eligible for marriage. "
                "At the end of each prediction, provide 10 practical and insightful suggestions "
                "to help the user improve their chances of getting married sooner."
            ),
        },
        {"role": "user", "content": prompt},
    ]

    try:
        response = client.chat.completions.create(
            model="gpt-4.1-mini",
            messages=message,
            temperature=0.7,
            max_tokens=250
        )
        ai_text = response.choices[0].message.content.strip()
        return ai_text
    except Exception as e:
        print("Something went wrong:", e)
        return None


# =====================================
# Configure Templates Directory
# =====================================
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
templates = Jinja2Templates(directory=os.path.join(BASE_DIR, "templates"))


# =====================================
# Homepage Route
# =====================================
@app.get("/", response_class=HTMLResponse)
async def home(request: Request):
    """
    Displays the homepage form where the user enters their personal information
    for the marriage prediction system.
    """
    return templates.TemplateResponse("form.html", {"request": request})


# =====================================
# Handle Form Submission & Generate Prediction
# =====================================
@app.post("/predict_form", response_class=HTMLResponse)
async def predict_from_form(
    request: Request,
    name: str = Form(...),
    age: int = Form(...),
    gender: str = Form(...),
    height: float = Form(...),
    weight: float = Form(...),
    income: float = Form(...),
    education: str = Form(...),
    occupation: str = Form(...),
    social_life: str = Form(...),
    relationship_status: str = Form(...),
    exercise_habits: str = Form(...),
    health_conditions: str = Form(...),
    skin_color: str = Form(...),
    hobbies: str = Form(...),
    family_background: str = Form(...),
    religion: str = Form(...),
    intention: str = Form(...)
):
    """
    Handles user input submission from the HTML form and passes all the collected
    details to the GPT model for generating a marriage prediction report.
    Includes 15+ personal, social, and lifestyle attributes for accurate analysis.
    """
    try:
        # Build detailed user profile for AI model
        prompt = f"""
        Below is a user's personal information.
        Name: {name}
        Age: {age}
        Gender: {gender}
        Height: {height}
        Weight: {weight}
        Income: {income}
        Education: {education}
        Occupation: {occupation}
        Social Life: {social_life}
        Relationship Status: {relationship_status}
        Exercise Habits: {exercise_habits}
        Health Conditions: {health_conditions}
        Skin Color: {skin_color}
        Hobbies: {hobbies}
        Family Background: {family_background}
        Religion: {religion}
        Intention: {intention}

        Task: Predict just in one sentense, how many years/months this user might get married.
        Also provide 10 clear, realistic, and practical suggestions to improve the chances of marriage. Each point should contain maximum two sentence.
                
        ⚠️ Do not repeat the user information in your answer.
        ⚠️ Start directly with "### Prediction:" followed by "### 10 Suggestions:"
        """

        prediction = get_ai_response(prompt)
        if not prediction:
            prediction = "⚠️ Unable to generate prediction. Please try again later."

        return templates.TemplateResponse(
            "result.html",
            {"request": request, "name": name, "result": prediction},
        )

    except Exception as e:
        error_message = f"❌ Internal Error:\n{str(e)}\n\n{traceback.format_exc()}"
        return templates.TemplateResponse(
            "result.html",
            {"request": request, "name": name, "result": error_message},
        )

