# AI Medical Doctor

An AI-powered medical diagnosis assistant with voice and vision capabilities built with Gradio.

## Features

- Image analysis for medical diagnosis
- Voice-to-text transcription
- Text-to-speech response generation
- Professional medical consultation interface

## Deployment on Render

### Prerequisites

1. Create a Render account
2. Set up environment variables in Render dashboard:
   - `GROQ_API_KEY`: Your Groq API key for speech transcription
   - `ELEVENLABS_API_KEY`: Your ElevenLabs API key for text-to-speech

### Deployment Steps

1. **Connect your GitHub repository** to Render
2. **Create a new Web Service** on Render
3. **Configure the service:**
   - **Build Command:** `chmod +x build.sh && ./build.sh`
   - **Start Command:** `python gradio_app.py`
   - **Environment:** Python 3.9+
   - **Region:** Choose closest to your users

4. **Set Environment Variables** in Render dashboard:
   ```
   GROQ_API_KEY=your_groq_api_key_here
   ELEVENLABS_API_KEY=your_elevenlabs_api_key_here
   ```

5. **Deploy** the service

### Local Development

1. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

2. Set up environment variables:
   ```bash
   export GROQ_API_KEY=your_groq_api_key_here
   export ELEVENLABS_API_KEY=your_elevenlabs_api_key_here
   ```

3. Run the application:
   ```bash
   python gradio_app.py
   ```

## Troubleshooting

### Common Issues

1. **404 errors for manifest.json**: This file is now included in the repository
2. **Import errors**: The app now has fallback functions for missing dependencies
3. **Port issues**: The app automatically uses the PORT environment variable from Render

### Environment Variables

Make sure these are set in your Render dashboard:
- `GROQ_API_KEY`: Required for speech-to-text functionality
- `ELEVENLABS_API_KEY`: Required for text-to-speech functionality

## File Structure

- `gradio_app.py`: Main application file
- `brain_of_doc.py`: Image analysis functionality
- `voice_of_patient.py`: Speech-to-text functionality
- `voice_of_doctor.py`: Text-to-speech functionality
- `requirements.txt`: Python dependencies
- `build.sh`: Build script for deployment
- `manifest.json`: Web app manifest file 