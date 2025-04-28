# 🧠 AI-Powered Activity Generator

This project is a simple **Python-based activity generator** designed to recommend learning activities based on a child's **age**, **interests**, and **learning style**.

It’s part of a larger system for building personalized learning dashboards for children.

---

## 📚 Features

- Input: child’s **age**, **interests**, and **learning style** (e.g., visual, hands-on, inquiry-based).
- Output: customized learning activities or project ideas.
- Prebuilt activity bank (can be expanded).
- Lightweight, easy to modify.
- Built with **Python 3.8+**.
- (Optional) Future plan: connect to an **OpenAI API** for dynamic generation.

---

## 🚀 Getting Started

### Requirements
- Python 3.8+
- No external libraries needed (for basic local generation)

(If expanded for AI, you will need `openai` Python library.)

```bash
pip install openai
```

---

## 🛠 How It Works

1. **Activities Database**:  
   A simple dictionary or list of activities tagged by learning style and age range.

2. **User Input**:  
   You provide the child’s profile.

3. **Generator Logic**:  
   It matches the child’s interests + learning style to suitable activities.

4. **(Optional Expansion)**:  
   Use OpenAI's GPT models to generate even richer, custom activities dynamically based on the child's profile.

---

## 📝 Example Usage

```python
from activity_generator import suggest_activity

child_profile = {
    "age": 7,
    "learning_style": "Visual",
    "interests": ["Art", "Nature"]
}

suggested = suggest_activity(child_profile)
print(suggested)
```

Output:

```
🎨 Create a nature journal with drawings of different plants you find outdoors.
```

---

## 📈 Future Improvements

- Integrate with OpenAI API for real-time idea generation.
- Build a simple CLI or web interface (Flask, Streamlit, or Django).
- Save suggested activities into Firebase under each child's profile.
- Add tagging system (difficulty, duration, materials needed).

---

## 📂 Project Structure

```
activity_generator/
├── activity_generator.py
├── activities.json   # Optional - external file for activities
├── README.md
└── requirements.txt  # (only if using OpenAI API)
```

---

## 🤝 Contributing

This project is part of a broader **personalized parenting dashboard** system.  
Contributions are welcome as the project expands into a full AI-powered learning companion.

---

## 🔥 Author

Eric Chang  
Founder of **A Tiger Cub** — Bridging Parenting, Education, and Culture
