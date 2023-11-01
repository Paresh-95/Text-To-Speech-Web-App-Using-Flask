from flask import Flask, render_template, request, send_from_directory
import pyttsx3
import os
import time

app = Flask(__name__)

# Initialize the engine
engine = pyttsx3.init()

# Get available voices on Windows
def get_windows_voices():
    voices = []
    for voice in engine.getProperty('voices'):
        voices.append({
            'id': voice.id,
            'name': voice.name,
        })
    return voices

@app.route('/')
def index():
    return render_template('index.html', audio_file='', voices=get_windows_voices())

@app.route('/speak', methods=['POST'])
def speak():
    text = request.form.get('text')
    voice_id = request.form.get('voice')
    
    # Generate a unique audio file name using a timestamp
    timestamp = str(int(time.time()))
    audio_file = f'static/output_{timestamp}.mp3'
    
    engine.setProperty('voice', voice_id)  # Set the selected voice
    engine.save_to_file(text, audio_file)
    engine.runAndWait()
    
    return render_template('index.html', audio_file=audio_file, voices=get_windows_voices())

@app.route('/download')
def download():
    return send_from_directory('static', 'output.mp3', as_attachment=True)

if __name__ == '__main__':
    app.run(debug=True)
    