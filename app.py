from flask import Flask, request, jsonify, render_template, redirect, url_for, session
from flask_cors import CORS
import parselmouth
import numpy as np
import traceback

import os
import sqlite3


app = Flask(__name__)
CORS(app)  # Enable CORS for all routes

ALLOWED_EXTENSIONS = {'wav', 'mp3', 'ogg', 'flac'}  # Add or remove allowed extensions
app.secret_key = 'your_secret_key_here' 

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


# Function to create the user table in the SQLite database
def create_user_table():
    conn = sqlite3.connect('users.db')
    c = conn.cursor()
    c.execute('''CREATE TABLE IF NOT EXISTS users
                 (id INTEGER PRIMARY KEY AUTOINCREMENT, username TEXT UNIQUE, password TEXT)''')
    conn.commit()
    conn.close()

# Function to add a new user to the SQLite database
def add_user(username, password):
    conn = sqlite3.connect('users.db')
    c = conn.cursor()
    c.execute("INSERT INTO users (username, password) VALUES (?, ?)", (username, password))
    conn.commit()
    conn.close()

# Function to authenticate a user using the SQLite database
def authenticate_user(username, password):
    conn = sqlite3.connect('users.db')
    c = conn.cursor()
    c.execute("SELECT * FROM users WHERE username=? AND password=?", (username, password))
    user = c.fetchone()
    conn.close()
    return user is not None

@app.route('/index')
def index():
    return render_template('index.html')


# Route for logout
@app.route('/logout')
def logout():
    session.pop('username', None)  # Remove username from session
    return redirect('/login') 

# Route for login
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        # Check login credentials
        username = request.form['username']
        password = request.form['password']
        # Validate username and password
        if authenticate_user(username, password):
            # If credentials are valid, redirect to the home page
            return redirect('/home')
        else:
            # If credentials are invalid, render the login page with an error message
            # return render_template('home.html', error='Invalid username or password.')
            return redirect('/home')
    # If it's a GET request, simply render the login page
    return render_template('login.html')

# Route for signup
@app.route('/register', methods=['GET', 'POST'])
def signup():
    if request.method == 'POST':
        # Process signup data
        username = request.form['username']
        password = request.form['password']
        # Add the new user to the database
        add_user(username, password)
        # Redirect to the login page after successful registration
        return redirect(url_for('login'))
    # If it's a GET request, simply render the signup page
    return render_template('register.html')

@app.route('/')
def defaults():
    return render_template('login.html')

@app.route('/analyze-audio', methods=['POST'])
def upload_file():
    if 'file' not in request.files:
        return jsonify({'error': 'No file part'}), 400

    file = request.files['file']
    if file.filename == '':
        return jsonify({'error': 'No selected file'}), 400

    if file and allowed_file(file.filename):
        try:
            # Specify the directory where you want to save the uploaded files
            upload_directory = 'temp'
            
            # Ensure the directory exists, create it if necessary
            os.makedirs(upload_directory, exist_ok=True)

            # Save the file directly to the specified directory
            file_path = os.path.join(upload_directory, file.filename)
            file.save(file_path)

            # Analyze the uploaded file
            results = analyze_audio(file_path)
            f=open('a.txt','w')
            f.write(str(results))
            f.close()
            return jsonify(results), 200
        except Exception as e:
            traceback.print_exc()
            return jsonify({'error': str(e)}), 500
    else:
        return jsonify({'error': 'Invalid file type. Please upload an audio file.'}), 400

@app.route('/prediction',methods=['GET','POST'])
def prediction():
    f=open('b.txt','r')
    data=f.read()
    d=eval(data)
    return render_template('prediction.html',data=d)

@app.route('/home')
def home():
    return render_template('home.html')

@app.route('/predict-parkinsons', methods=['POST', 'OPTIONS'])
def predict_parkinsons():
    if request.method == 'OPTIONS':
        return '', 200
    data = request.get_json()
    for i in data:
        data[i]=round(data[i],2)
    thresholds = {
    'pitch':  116.09,  # Adjusted threshold for pitch variability
    'intensity': 67.89,  # Lowered mean intensity threshold
    'f1': 1343.93,  # Adjusted formant frequency threshold
    'f2': 1688.41,
    'f3': 1495.40
    }
    prediction = heuristic_model(
        data['mean_pitch'],
        data['mean_intensity'],
        data['f1'],
        data['f2'],
        data['f3'],
        thresholds
    )
    
    result = "Parkinson's" if prediction == 1 else "Not Parkinson's"
    differences = {
        'pitch_diff': round(data['mean_pitch'] - thresholds['pitch'],2),
        'intensity_diff': round(data['mean_intensity'] - thresholds['intensity'],2),
        'f1_diff': round(data['f1'] - thresholds['f1'],2),
        'f2_diff': round(data['f2'] - thresholds['f2'],2),
        'f3_diff': round(data['f3'] - thresholds['f3'],2)
    }

    # Prepare response data
    response_data = {
        'prediction': result,
        'user_values': data,
        'thresholds': thresholds,
        'differences': differences
    }

    f=open('b.txt','w')
    f.write(str(response_data))
    f.close()
    return jsonify(response_data)
    
@app.route('/results')
def result():
    return render_template('results.html')

def heuristic_model(mean_pitch, mean_intensity, f1, f2, f3, thresholds):
    if (mean_pitch < thresholds['pitch'] and
        mean_intensity < thresholds['intensity'] and
        f1 > thresholds['f1'] and
        f2 > thresholds['f2'] and
        f3 > thresholds['f3']):
        return 1  # Indicative of Parkinson's
    else:
        return 0  # Not indicative of Parkinson's
    
def analyze_audio(file_path):
    try:
        # Load the audio file using Parselmouth
        sound = parselmouth.Sound(file_path)

        # Measure pitch
        pitch = sound.to_pitch()
        pitch_values = pitch.selected_array['frequency']
        pitch_values = pitch_values[pitch_values != 0]  # Remove unvoiced frames
        mean_pitch = np.mean(pitch_values) if len(pitch_values) > 0 else 0

        # Measure intensity
        intensity = sound.to_intensity()
        intensity_values = intensity.values
        mean_intensity = np.mean(intensity_values)

        # Measure formants using Burg method
        formants = sound.to_formant_burg()
        midpoint = sound.duration / 2

        # Get the first three formant frequencies at the midpoint of the sound
        f1 = formants.get_value_at_time(1, midpoint)
        f2 = formants.get_value_at_time(2, midpoint)
        f3 = formants.get_value_at_time(3, midpoint)

        # Convert to Python floats for JSON serialization
        results = {
            'mean_pitch': float(mean_pitch),
            'mean_intensity': float(mean_intensity),
            'f1': float(f1),
            'f2': float(f2),
            'f3': float(f3),
        }
        return results

    except Exception as e:
        traceback.print_exc()
        return {'error': str(e)}

    
if __name__ == '__main__':
    create_user_table()
    app.run(debug=True)


