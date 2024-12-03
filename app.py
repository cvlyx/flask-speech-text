from flask import Flask, render_template, request, jsonify
import speech_recognition as sr
import pyttsx3

app = Flask(__name__)

# Root route for the home page
@app.route("/")
def index():
    return render_template("index.html")

# Route for Speech-to-Text functionality
@app.route("/speech_to_text", methods=["POST"])
def speech_to_text():
    recognizer = sr.Recognizer()
    try:
        with sr.Microphone() as source:
            recognizer.adjust_for_ambient_noise(source, duration=1)
            print("Listening for speech...")
            audio = recognizer.listen(source, timeout=5, phrase_time_limit=10)
            print("Processing speech...")
            text = recognizer.recognize_google(audio)
            return jsonify({"success": True, "text": text})
    except sr.UnknownValueError:
        return jsonify({"success": False, "error": "Could not understand the audio."})
    except sr.RequestError as e:
        return jsonify({"success": False, "error": f"API Error: {e}"})
    except sr.WaitTimeoutError:
        return jsonify({"success": False, "error": "No speech detected in the given time."})

# Route for Text-to-Speech functionality
@app.route("/text_to_speech", methods=["POST"])
def text_to_speech():
    text = request.json.get("text", "")
    if not text:
        return jsonify({"success": False, "error": "No text provided."})
    
    try:
        engine = pyttsx3.init()
        engine.say(text)
        engine.runAndWait()
        return jsonify({"success": True})
    except Exception as e:
        return jsonify({"success": False, "error": str(e)})

if __name__ == "__main__":
    app.run(debug=True)
