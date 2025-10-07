# Raaee Agri Advisor

## Overview
Raaee Agri Advisor is an innovative Urdu-based speech-to-speech agricultural assistance platform designed to empower farmers with immediate, accessible expert guidance. This intelligent bot specializes in addressing farmer queries related to crops, pests, water management, medicines, and fertilizers through natural voice interactions in Urdu.

## Live Deployment
Access the application here: [https://elaborate-crisp-1451fd.netlify.app/](https://elaborate-crisp-1451fd.netlify.app/)

## Key Features
- **Urdu Voice Interface**: Complete speech-to-speech functionality in Urdu, making technology accessible to farmers regardless of literacy levels
- **Comprehensive Agricultural Knowledge**: Specialized expertise in crops, pests, irrigation, fertilizers, and agricultural medicines
- **Real-time Query Resolution**: Instant responses to farmer questions using advanced AI
- **Multimodal Interaction**: Support for both voice and text-based queries
- **Responsive Design**: Accessible across various devices and network conditions

## Technical Architecture

### Frontend
- **Framework**: React.js
- **Deployment**: Netlify
- **UI Components**: Custom-built responsive interface
- **Audio Handling**: Web Audio API for voice interactions

### Backend
- **Framework**: Flask (Python)
- **Deployment**: Railway
- **AI Integration**: Groq LLM for natural language processing
- **Speech Synthesis**: Eleven Labs for high-quality Urdu text-to-speech
- **Knowledge Base**: Custom agricultural database with expert-curated content

## Core Technologies
- **AI/ML**: Groq Language Model
- **Speech Processing**: Eleven Labs TTS
- **Backend API**: Flask RESTful services
- **Frontend**: React with modern hooks and state management
- **Hosting**: Netlify (frontend), Railway (backend)

## User Interface



![App Screenshot](https://raw.githubusercontent.com/Osama-Dev01/Raa-ee---The-Agri-Advisor-Bot/master/voice-bot/frontend/chatbot/raee.PNG)



The application features a clean, intuitive interface designed specifically for farmers, with large buttons, clear voice indicators, and straightforward navigation.

## Problem Statement
Farmers in Urdu-speaking regions often face significant challenges in accessing timely agricultural expertise. Language barriers, remote locations, and limited technical literacy prevent them from utilizing digital farming solutions. Raaee Agri Advisor bridges this gap by providing instant, voice-based agricultural guidance in their native language.

## Solution Benefits
- **Democratized Access**: Voice interface eliminates literacy and technical barriers
- **Timely Interventions**: Immediate pest, disease, and nutrient deficiency identification
- **Cost Reduction**: Reduces dependency on physical agricultural extensions
- **Knowledge Preservation**: Captures and distributes local agricultural wisdom
- **Scalable Impact**: Serves multiple farmers simultaneously across regions

## Installation and Development

### Prerequisites
- Node.js (v14 or higher)
- Python 3.8+
- Groq API access
- Eleven Labs API key

### Frontend Setup
```bash
git clone [repository-url]
cd raaee-agri-advisor-frontend
npm install
npm start
```


### Backend Setup
```bash
cd raaee-agri-advisor-backend
pip install -r requirements.txt
python app.py
```

## Usage

1. **Access the Application**: Navigate to the deployed URL
2. **Initiate Conversation**: Click the microphone button to start speaking
3. **Ask Questions**: Pose queries in Urdu about crops, pests, water management, or fertilizers
4. **Receive Guidance**: Listen to the AI-generated expert advice in Urdu
5. **Follow-up**: Continue the conversation for additional clarifications

## API Integration

### Speech-to-Text
* Urdu speech recognition through Web Speech API
* Real-time audio processing and transcription

### Natural Language Processing
* Groq LLM for understanding agricultural context
* Custom prompt engineering for farming terminology

### Text-to-Speech
* Eleven Labs for natural Urdu speech synthesis
* Optimized for agricultural vocabulary and regional accents

## Agricultural Domains Covered

* **Crop Management**: Growth stages, planting techniques, harvesting
* **Pest Control**: Identification, organic and chemical treatments
* **Water Management**: Irrigation scheduling, water conservation
* **Fertilizers**: Nutrient requirements, application methods, timing
* **Crop Protection**: Disease prevention, treatment protocols
* **Seasonal Guidance**: Crop calendar, weather adaptations

## Contributing

We welcome contributions from developers, agricultural experts, and linguists. Please refer to our contribution guidelines for more information on how to participate in improving this platform.

## Future Enhancements

* Regional dialect support
* Offline functionality
* Image-based pest and disease identification
* Integration with weather data and market prices
* Multi-language expansion
