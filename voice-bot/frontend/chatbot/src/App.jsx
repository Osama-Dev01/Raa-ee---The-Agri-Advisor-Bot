// App.jsx
import { useState , useRef , useEffect } from 'react';
import {  HelpCircle, Sprout, X } from 'lucide-react';
import './App.css';
import axios from "axios";
import { Mic, MicOff } from "lucide-react";

function App() {
  const [isRecording, setIsRecording] = useState(false);
  const [transcription, setTranscription] = useState('');
  const [botResponse, setBotResponse] = useState('');
  const [showGuide, setShowGuide] = useState(false);
  const mediaRecorderRef = useRef(null);
  const audioChunksRef = useRef([]);
  const [isLoading, setIsLoading] = useState(false);


 






   const handleRecordToggle = async () => {
    if (!isRecording) {
      // ✅ Start recording
      setIsRecording(true);
      setTranscription("");
      setBotResponse("");

      try {
        const stream = await navigator.mediaDevices.getUserMedia({ audio: true });
        const mediaRecorder = new MediaRecorder(stream);
        mediaRecorderRef.current = mediaRecorder;
        audioChunksRef.current = [];

        mediaRecorder.ondataavailable = (event) => {
          if (event.data.size > 0) {
            audioChunksRef.current.push(event.data);
          }
        };

        mediaRecorder.onstop = async () => {
          // Combine chunks into one Blob
          const audioBlob = new Blob(audioChunksRef.current, { type: "audio/webm" });
          const formData = new FormData();
          formData.append("audio", audioBlob, "recording.webm");
           setIsLoading(true);

          try {
            const res = await axios.post("https://raa-ee-the-agri-advisor-bot-production.up.railway.app/process_audio", formData, {
              headers: { "Content-Type": "multipart/form-data" },
            });

            setTranscription(res.data.transcription);
            setBotResponse(res.data.response);
          } catch (err) {
            console.error("Error sending audio:", err);
            setBotResponse("⚠️ Server error while processing audio.");
          }

           setIsLoading(false);

          

        };

        mediaRecorder.start();
      } catch (error) {
        console.error("Mic access denied:", error);
        alert("Microphone access denied.");
        setIsRecording(false);
      }
    } else {
      // ✅ Stop recording
      setIsRecording(false);
      if (mediaRecorderRef.current) {
        mediaRecorderRef.current.stop();
      }
    }
  };



// 🔊 Automatically speak bot responses in Urdu using ElevenLabs
useEffect(() => {
  const speakUrdu = async (text) => {
    if (!text) return;

    try {
      const response = await fetch("https://api.elevenlabs.io/v1/text-to-speech/IKne3meq5aSn9XLyUdCD", {
        method: "POST",
        headers: {
          "xi-api-key": "sk_aa8725cddffb3ec5b5ba68e20c97a240f31b017b67773770",
          "Content-Type": "application/json",
        },
        body: JSON.stringify({
          text,
          model_id: "eleven_multilingual_v2", // multilingual model supports Urdu
          voice_settings: {
            stability: 0.4,
            similarity_boost: 0.8,
          },
        }),
      });

      if (!response.ok) throw new Error("TTS request failed");

      const audioBlob = await response.blob();
      const audioUrl = URL.createObjectURL(audioBlob);
      const audio = new Audio(audioUrl);
      audio.play();
    } catch (err) {
      console.error("Urdu TTS Error:", err);
    }
  };

  if (botResponse) {
    speakUrdu(botResponse);
  }
}, [botResponse]);






  return (
    <div className="app-container">
      {/* Animated background elements */}
      <div className="background-overlay">
        <div className="bg-orb bg-orb-1"></div>
        <div className="bg-orb bg-orb-2"></div>
      </div>

      {/* Help Button */}
      <button
        onClick={() => setShowGuide(true)}
        className="help-button"
      >
        <HelpCircle className="icon-medium" />
      </button>

      {/* User Guide Modal */}
      {showGuide && (
        <div className="modal-overlay">
          <div className="modal-content">
            <button
              onClick={() => setShowGuide(false)}
              className="modal-close"
            >
              <X className="icon-small" />
            </button>
            
            <h3 className="modal-title">
              <HelpCircle className="icon-large" />
              استعمال کی رہنمائی
            </h3>
            <div className="guide-list">
              <p className="guide-item">
                <span className="guide-number">1.</span>
                <span>دائیں طرف مائیک بٹن دبائیں اور اپنا سوال بولیں</span>
              </p>
              <p className="guide-item">
                <span className="guide-number">2.</span>
                <span>آپ کا سوال درمیان میں ظاہر ہوگا</span>
              </p>
              <p className="guide-item">
                <span className="guide-number">3.</span>
                <span>رائے بوٹ کا جواب نیچے دیکھیں</span>
              </p>
              <p className="guide-item">
                <span className="guide-number">4.</span>
                <span>مزید سوالات کے لیے دوبارہ ریکارڈ کریں</span>
              </p>
            </div>
          </div>
        </div>
      )}

     

      {/* Main Content */}
      <div className="main-content">
        
        {/* Header with animated logo */}
        <div className="header">
          <div className="logo-section">
            <div className="logo-icon">
              <Sprout className="icon-xlarge" />
            </div>
            <h1 className="main-title">رائے</h1>
          </div>
          <p className="subtitle">Raa'ee - The Agri-Advisor Bot</p>
          <p className="tagline">
            آپ کا ذاتی زرعی مشیر - کاشتکاری کے ہر سوال کا جواب
          </p>
        </div>

        {/* Chat Interface */}
        <div className="chat-container">
          
          {/* User Transcription Box */}
          <div className="chat-box">
            <div className="chat-header">
              <div className="status-dot"></div>
              <h3 className="chat-title">آپ کا سوال</h3>
            </div>
            <div className="chat-content">
              {transcription ? (
                <p className="chat-text">{transcription}</p>
              ) : (
                <p className="chat-placeholder">مائیک بٹن دبا کر اپنا سوال بولیں...</p>
              )}
            </div>
          </div>

          {/* Bot Response Box */}
          <div className="chat-box">
            <div className="chat-header">
              <Sprout className="icon-small" />
              <h3 className="chat-title">رائے کا جواب</h3>
            </div>
            <div className="chat-content chat-content-response">
              {botResponse ? (
                <p className="chat-text">{botResponse}</p>
              ) : (
                <p className="chat-placeholder">جواب یہاں ظاہر ہوگا...</p>
              )}
            </div>
          </div>
        </div>

        {/* Recording Button - Fixed on Right */}
         <div className="recording-button-container">
      <button
        onClick={handleRecordToggle}
        className={`recording-button ${isRecording ? "recording-active" : ""}`}
      >
        {isRecording ? <MicOff className="icon-xlarge" /> : <Mic className="icon-xlarge" />}

        {isRecording && (
          <>
            <div className="pulse-ring pulse-ring-1"></div>
            <div className="pulse-ring pulse-ring-2"></div>
          </>
        )}
      </button>

      <p className="recording-label">
        {isRecording ? "سن رہا ہے..." : "بولیں"}
      </p>
    </div>

      </div>

      {/* Loading Spinner Overlay */}
{isLoading && (
  <div className="spinner-overlay">
    <div className="spinner"></div>
  </div>
)}

      {/* Footer */}
      <div className="footer">
        <p>پاکستانی کسانوں کے لیے بنایا گیا</p>
      </div>
    </div>
  );
}

export default App;