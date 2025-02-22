from flask import Flask, render_template, request
import openai
import os
from dotenv import load_dotenv
import random
from IPython.display import Audio  # For playing audio in Colab

# Load API key from .env file
load_dotenv()
openai.api_key = os.getenv("OPENAI_API_KEY")

app = Flask(__name__)

# List of image paths (replace with your actual paths)
image_paths = ["images/animal_00.png", "images/animal_01.png", "images/animal_02.png", "images/animal_03.png"]
# List of audio paths
audio_paths = ["audio1.mp3", "audio2.wav", "audio3.ogg", "audio4.flac"]  # Replace with your audio file paths


@app.route("/", methods=["GET", "POST"])
def index():
    result = None
    selected_image = None
    animal_phrases = []
    audio_file = None

    if request.method == "POST":
        prompt = request.form["prompt"]  # Not using the prompt for image selection in this version
        try:
            # Generate animal phrases with GPT
            response = openai.chat.completions.create(
              model="gpt-3.5-turbo",  # Or any suitable model
              messages=[
                  {"role": "system", "content": "You are a creative writer. Generate short, fictional phrases in an animal language. Each phrase should be unique and evocative."},
                  {"role": "user", "content": f"Generate 16 phrases in an animal language based on: {prompt}"}
              ],
              temperature=0.7,
              max_tokens=500
            )
            animal_phrases = response.choices[0].message.content.split('\n')
            animal_phrases = [phrase.strip() for phrase in animal_phrases if phrase.strip()]  # Clean up extra whitespace and empty lines

            # Randomly select an image and audio file
            selected_image = random.choice(image_paths)
            audio_file = random.choice(audio_paths) # Select a random audio file

        except Exception as e:
            result = f"Error: {str(e)}"

    return render_template("index.html", result=result, image_url=selected_image, animal_phrases=animal_phrases, audio_file=audio_file)

if __name__ == "__main__":
    app.run(debug=True)
