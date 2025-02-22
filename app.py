from flask import Flask, render_template, request
import openai
import os
from dotenv import load_dotenv
import random

# Load API key from .env file
load_dotenv()
openai.api_key = os.getenv("OPENAI_API_KEY")

app = Flask(__name__)

# List of animal data
animals = [
    {"name": "Lion", "image": "images/lion.png", "sound": "sounds/lion.mp3", "id": "lion"},
    {"name": "Elephant", "image": "images/elephant.png", "sound": "sounds/elephant.mp3", "id": "elephant"},
    {"name": "Wolf", "image": "images/wolf.png", "sound": "sounds/wolf.mp3", "id": "wolf"},
    {"name": "Eagle", "image": "images/eagle.png", "sound": "sounds/eagle.mp3", "id": "eagle"}
]

@app.route("/", methods=["GET", "POST"])
def index():
    result = None
    selected_animal = None

    if request.method == "POST":
        prompt = request.form["prompt"]
        
        try:
            # Generate animal-related text
            response = openai.chat.completions.create(
                model="gpt-4o",
                messages=[
                    {"role": "system", "content": "You are an animal expert providing fun facts and descriptions."},
                    {"role": "user", "content": f"Tell me about {prompt}"}
                ],
                temperature=0.7,
                max_tokens=300
            )
            result = response.choices[0].message.content

            # Randomly select an animal
            selected_animal = random.choice(animals)
        
        except Exception as e:
            result = f"Error: {str(e)}"

    return render_template("index.html", result=result, animal=selected_animal, animals=animals)

if __name__ == "__main__":
    app.run(debug=True)
