from flask import Flask, request
from flask_cors import CORS
import openai
import pandas as pd
import os

app = Flask(__name__)
CORS(app)  # Allows frontend to send API requests

# Load dataset from Google Sheets
sheet_url = "https://docs.google.com/spreadsheets/d/e/2PACX-1vTtFuozEPrIMGRyH5EIs0XjdvY1S3IUNXAEFtPyRT0nj7WfoXeMtsyGVnFdfKYNP8AOKnnebArCyigC/pub?output=csv"
df = pd.read_csv(sheet_url)

# ✅ Use environment variable for OpenAI API key
openai.api_key = os.getenv("OPENAI_API_KEY")

@app.route('/generate', methods=['POST'])
def generate():
    if request.content_type == "application/json":
        data = request.json
    else:
        data = request.form  # Handle form data

    age = data.get("age", "")
    difficulty = data.get("difficulty", "")
    category = data.get("category", "")
    skills = data.get("skills", "")
    learning_style = data.get("learning_style", "")

    # Filter dataset based on updated categories
    filtered_df = df[
        (df["Age Group"].str.contains(str(age), na=False)) &
        (df["Difficulty Level"].str.contains(difficulty, case=False, na=False)) &
        (df["Category"].str.contains(category, case=False, na=False)) &
        (df["Skills Developed"].str.contains(skills, case=False, na=False)) &
        (df["Learning Style"].str.contains(learning_style, case=False, na=False))
    ]

    # ✅ Return **formatted HTML** response if a match is found
    if not filtered_df.empty:
        selected_activity = filtered_df.sample(n=1).to_dict(orient="records")[0]
        return f"""
        <h2>Suggested Activity</h2>
        <p><strong>{selected_activity["Activity Name"]}</strong></p>
        <p><strong>Materials Needed:</strong> {selected_activity["Materials Needed"]}</p>
        <p><strong>Link to Activity:</strong> <a href="{selected_activity["Links to Activities"]}" target="_blank">Click Here</a></p>
        """

    # AI Fallback
    prompt = (
        f"Suggest a fun learning activity for a {age}-year-old that is {difficulty} difficulty, "
        f"related to {category}, helps develop {skills}, and works best for a {learning_style} learner."
    )

    response = openai.ChatCompletion.create(  
        model="gpt-4",
        messages=[
            {"role": "system", "content": "You are a helpful assistant who provides engaging learning activities."},
            {"role": "user", "content": prompt}
        ]
    )

    generated_activity = response.choices[0].message.content

    return f"""
    <h2>AI-Generated Activity</h2>
    <p>{generated_activity}</p>
    """

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=10000)
