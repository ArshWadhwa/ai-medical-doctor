    # In main.py
    import os
    import shutil
    from fastapi import FastAPI, File, UploadFile, Form
    from fastapi.middleware.cors import CORSMiddleware

    # Import your existing functions
    from brain_of_doc import analyze_image_with_query, encode_image
    from voice_of_doctor import text_to_speech_elevenLabs, transcribe_with_groq

    app = FastAPI()

    # --- CORS Middleware ---
    # This allows your React frontend to communicate with this backend
    app.add_middleware(
        CORSMiddleware,
        allow_origins=["*"],  # IMPORTANT: For production, change "*" to your frontend's URL
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

    @app.post("/analyze-patient")
    async def analyze_patient_data(
        audio_file: UploadFile = File(...),
        image_file: UploadFile = File(...),
        language: str = Form("English") # You can add language later
    ):
        # Save temporary files
        with open(image_file.filename, "wb") as buffer:
            shutil.copyfileobj(image_file.file, buffer)
        with open(audio_file.filename, "wb") as buffer:
            shutil.copyfileobj(audio_file.file, buffer)

        # 1. Transcribe Audio
        # NOTE: This uses your dummy function. Replace with real implementation.
        transcription = transcribe_with_groq(
            GROQ_API_KEY=os.environ.get("GROQ_API_KEY"),
            audio_filepath=audio_file.filename,
            stt_model="whisper-large-v3"
        )

        # 2. Analyze Image with Transcription
        system_prompt = "You are a professional doctor..." # Add your full prompt here
        encoded_img = encode_image(image_file.filename)
        doctor_response = analyze_image_with_query(
            system_prompt + transcription,
            "meta-llama/llama-4-scout-17b-16e-instruct",
            encoded_img
        )

        # 3. Convert Doctor's Response to Speech
        output_audio_path = "response.mp3"
        text_to_speech_elevenLabs(input_text=doctor_response, output_filepath=output_audio_path)

        # Clean up temporary files
        os.remove(image_file.filename)
        os.remove(audio_file.filename)

        return {
            "transcription": transcription,
            "doctor_response": doctor_response,
            "audio_response_url": output_audio_path # We will serve this file
        }

    # Add an endpoint to serve the generated audio file
    from fastapi.responses import FileResponse

    @app.get("/audio/{file_name}")
    def get_audio(file_name: str):
        return FileResponse(path=file_name, media_type='audio/mpeg', filename=file_name)