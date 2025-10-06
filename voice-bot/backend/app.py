from flask import Flask, request, jsonify
from flask_cors import CORS
import speech_recognition as sr
import io
import tempfile
import os
from pydub import AudioSegment
import logging
from translate import Translator
import json

try:
    from llm import find_and_print_crop_data , llm_response
   
except ImportError as e:
    print(" Error importing llm:", e)


# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = Flask(__name__)
CORS(app)  # Enable CORS

def convert_webm_to_wav(webm_data):
    """Convert WebM audio data to WAV format"""
    try:
        # Create temporary files
        with tempfile.NamedTemporaryFile(delete=False, suffix='.webm') as webm_file:
            webm_file.write(webm_data)
            webm_path = webm_file.name

        with tempfile.NamedTemporaryFile(delete=False, suffix='.wav') as wav_file:
            wav_path = wav_file.name

        # Convert WebM to WAV using pydub
        audio = AudioSegment.from_file(webm_path, format="webm")
        audio = audio.set_frame_rate(16000).set_channels(1)  # Standard for speech recognition
        audio.export(wav_path, format="wav")
        
        # Read the converted WAV file
        with open(wav_path, 'rb') as f:
            wav_data = f.read()
        
        # Clean up temporary files
        os.unlink(webm_path)
        os.unlink(wav_path)
        
        return wav_data
        
    except Exception as e:
        logger.error(f"Audio conversion failed: {e}")
        return None

@app.route("/")
def home():
    return jsonify({
        "message": "🌾 Pakistani Farming Chatbot Backend",
        "status": "running",
        "endpoints": {
            "process_audio": "POST /process_audio - Process WebM/WAV audio files"
        }
    })

@app.route("/process_audio", methods=["POST"])
def process_audio():
    try:
        if "audio" not in request.files:
            return jsonify({"error": "No audio file received"}), 400

        audio_file = request.files["audio"]
        
        if audio_file.filename == '':
            return jsonify({"error": "No file selected"}), 400

        # Read the audio data
        audio_data = audio_file.read()
        
        if len(audio_data) == 0:
            return jsonify({"error": "Empty audio file"}), 400

        logger.info(f"Received audio file: {audio_file.filename}, Size: {len(audio_data)} bytes")

        # Handle WebM format (from browser recordings)
        if audio_file.filename.endswith('.webm') or audio_file.content_type == 'audio/webm':
            logger.info("Converting WebM to WAV...")
            wav_data = convert_webm_to_wav(audio_data)
            
            if not wav_data:
                return jsonify({"error": "Failed to convert WebM audio to WAV"}), 400
            
            audio_data = wav_data

        # Process with SpeechRecognition
        recognizer = sr.Recognizer()
        
        with sr.AudioFile(io.BytesIO(audio_data)) as source:
            # Adjust for ambient noise
            recognizer.adjust_for_ambient_noise(source, duration=0.5)
            audio_data = recognizer.record(source)

            try:
                text = recognizer.recognize_google(audio_data, language="ur-PK")
                logger.info(f"Transcription successful: {text}")
                engtext = translate_urdu_to_english(text)


                results = find_and_print_crop_data(engtext , crop_kb)
                logger.info(f"kb successful: {results}")

                resp = llm_response(engtext ,results )

                logger.info(f"llm result successful: {resp}")

            except sr.UnknownValueError:
                text = "آواز کو پہچانا نہیں جا سکا۔ براہ کرم واضح طور پر بولیں۔"
                logger.warning("Speech recognition could not understand audio")
            except sr.RequestError as e:
                text = "گوگل سپیچ سروس سے کنکشن میں مسئلہ ہے۔"
                logger.error(f"Speech recognition API error: {e}")

        # Generate farming-specific responsesS
       

        return jsonify({
            "transcription": text,
            "response": resp,
            "status": "success"
        })

    except Exception as e:
        logger.error(f"Unexpected error: {e}")
        return jsonify({
            "error": "سرور میں مسئلہ ہوا۔",
            "details": str(e)
        }), 500

def translate_urdu_to_english(text):
    """Translate Urdu text to English using translate library"""
    try:
        translator = Translator(from_lang="ur", to_lang="en")
        translation = translator.translate(text)
        return translation
    except Exception as e:
        print(f"Translation error: {e}")
        return None



if __name__ == "__main__":
    print("🚀 Pakistani Farming Chatbot Backend Started!")

    spath = 'data.json'
    try:
        with open(spath, 'r', encoding='utf-8') as f:
            crop_kb = json.load(f)
        print(f" Successfully loaded knowledge base from '{spath}'")
    except Exception as e:
        print(f"⚠️ Failed to load knowledge base: {e}")
        crop_kb = {}

    #  Use Railway-assigned port
    port = int(os.environ.get("PORT", 8080))
    app.run(host="0.0.0.0", port=port)
