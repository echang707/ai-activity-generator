import openai
import pandas as pd

# Load dataset from Google Sheets
sheet_url = "https://docs.google.com/spreadsheets/d/e/2PACX-1vTtFuozEPrIMGRyH5EIs0XjdvY1S3IUNXAEFtPyRT0nj7WfoXeMtsyGVnFdfKYNP8AOKnnebArCyigC/pub?output=csv"
df = pd.read_csv(sheet_url)

openai.api_key = "HIDDEN"


def generate_activity(age, difficulty, category, skills, learning_style):
    # Apply filters based on user selections
    filtered_df = df[
        (df["Age Group"].str.contains(str(age), na=False)) &
        (df["Difficulty Level"].str.contains(difficulty, case=False, na=False)) &
        (df["Category"].str.contains(category, case=False, na=False)) &
        (df["Skills Developed"].str.contains(skills, case=False, na=False)) &
        (df["Learning Style"].str.contains(learning_style, case=False, na=False))
    ]

    # If there are matching activities, pick one at random
    if not filtered_df.empty:
        selected_activity = filtered_df.sample(n=1).to_dict(orient="records")[0]
        return f"{selected_activity['Activity Name']} - {selected_activity['Links to Activities']}"

    # Otherwise, use AI to generate a new activity
    else:
        prompt = (f"Suggest a fun learning activity for a {age}-year-old that is {difficulty} difficulty, "
                  f"related to {category}, helps develop {skills}, and works best for a {learning_style} learner.")
        response = openai.ChatCompletion.create(
            model="gpt-4",
            messages=[{"role": "system", "content": prompt}]
        )
        return response["choices"][0]["message"]["content"]
