from flask import Flask, request
from flask_cors import CORS
import pandas as pd
import os
from openai import OpenAI

app = Flask(__name__)
CORS(app)

# Load dataset
sheet_url = "https://docs.google.com/spreadsheets/d/e/2PACX-1vTtFuozEPrIMGRyH5EIs0XjdvY1S3IUNXAEFtPyRT0nj7WfoXeMtsyGVnFdfKYNP8AOKnnebArCyigC/pub?output=csv"
df = pd.read_csv(sheet_url)

# OpenAI client
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

@app.route('/generate', methods=['POST'])
def generate():
    data = request.json if request.content_type == "application/json" else request.form

    age = data.get("age", "")
    difficulty = data.get("difficulty", "")
    category = data.get("category", "")
    skills = data.get("skills", "")
    learning_style = data.get("learning_style", "")

    # Filter dataset
    filtered_df = df[
        (df["Age Group"].str.contains(str(age), na=False)) &
        (df["Difficulty Level"].str.contains(difficulty, case=False, na=False)) &
        (df["Category"].str.contains(category, case=False, na=False)) &
        (df["Skills Developed"].str.contains(skills, case=False, na=False)) &
        (df["Learning Style"].str.contains(learning_style, case=False, na=False))
    ]

    if not filtered_df.empty:
        selected_activity = filtered_df.sample(n=1).to_dict(orient="records")[0]
        return f"""
        <h2>Suggested Activity</h2>
        <p><strong>{selected_activity["Activity Name"]}</strong></p>
        <p><strong>Materials Needed:</strong> {selected_activity["Materials Needed"]}</p>
        <p><strong>Link to Activity:</strong> <a href="{selected_activity["Links to Activities"]}" target="_blank">Click Here</a></p>
        """

    # AI fallback (with error handling)
    prompt = (
        f"Suggest a fun learning activity for a {age}-year-old that is {difficulty} difficulty, "
        f"related to {category}, helps develop {skills}, and works best for a {learning_style} learner."
    )

    try:
        response = client.chat.completions.create(
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
    except Exception as e:
        # Log the error if needed: print(e)
        return f"""
        <h2>No Activity Available Yet</h2>
        <p>We're working on adding more activities soon! Please try a different combination or check back later.</p>
        """

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=10000)
