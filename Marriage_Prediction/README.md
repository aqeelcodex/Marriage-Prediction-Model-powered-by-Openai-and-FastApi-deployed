💍 Marriage Prediction App (FastAPI + OpenAI)
🧠 Overview

This project is an AI-powered web application that predicts when a person might get married based on their personal, social, financial, and health details.
It uses FastAPI for the backend and OpenAI GPT model to generate smart predictions and practical suggestions for improvement.

⚙️ Features

✅ Collects 15+ personal and lifestyle attributes from the user.
✅ Uses OpenAI GPT model (gpt-4.1-mini) for intelligent predictions.
✅ Provides 10 realistic suggestions to improve marriage chances.
✅ Built with FastAPI, HTML, CSS, and Jinja2 templates.
✅ Clean, modern, and mobile-friendly web design.


💡 How It Works

The user opens the web form (form.html) and enters details like age, income, education, etc.

The data is sent to the FastAPI backend (/predict_form route).

The backend sends all user data as a prompt to OpenAI GPT model.

The model returns:

Marriage prediction (in years or months)

10 actionable suggestions

The result is displayed beautifully on result.html.

🧰 Technologies Used
FastAPI – Backend framework
OpenAI API (GPT-4.1-mini) – AI text generation
HTML + CSS + Jinja2 – Frontend templates
dotenv – Securely loads API keys
Python 3.10+


Add your OpenAI API key
Create a .env file in the project root and add:

openai_sec_key=your_openai_api_key_here


Run the app
uvicorn main:app --reload
Open in browser
http://127.0.0.1:8000

🎨 HTML Templates

form.html
A clean, modern form where users enter personal, health, and lifestyle details.
Designed with CSS gradients, rounded boxes, and hover animations.

result.html
Displays the marriage prediction and 10 personalized suggestions beautifully.
Styled to match the theme of the input form for consistency.