# ui with gradioo
import os
import gradio as gr
import logging

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

try:
    from brain_of_doc import encode_image, analyze_image_with_query
    from voice_of_patient import record_audio, transcribe_with_groq
    from voice_of_doctor import text_to_speech, text_to_speech_elevenLabs
except ImportError as e:
    logger.error(f"Import error: {e}")
    # Create dummy functions if imports fail
    def encode_image(image_path):
        return None
    
    def analyze_image_with_query(prompt, model, image_data):
        return "Image analysis not available"
    
    def transcribe_with_groq(api_key, audio_path, model):
        return "Audio transcription not available"
    
    def text_to_speech_elevenLabs(text, output_path):
        return output_path

system_prompt = """
            You have to act as a professional doctor, i know you are not but this is for learning purpose. 
            What's in this image?. Do you find anything wrong with it medically? 
            If you make a differential, suggest some remedies for them. Donot add any numbers or special characters in 
            your response. Your response should be in one long paragraph. Also always answer as if you are answering to a real person.
            Donot say 'In the image I see' but say 'With what I see, I think you have ....'
            Dont respond as an AI model in markdown, your answer should mimic that of an actual doctor not an AI bot, 
            Keep your answer concise (max 2 sentences). No preamble, start your answer right away please
            After providing a diagnosis, match the condition with the most relevant ICD-10 medical code, and display it clearly.
            If unsure, mention possible conditions with their ICD-10 codes and advise follow-up with a certified doctor.
            Your responses should be helpful, concise, and clinically accurate.
            
            Here is a medical image and a patient question. Image: [image]. Patient says: [transcribed audio]. Please answer using both.
"""

def process_inputs(audio_filepath, image_filepath):
    try:
        # Handle audio transcription
        if audio_filepath:
            speech_to_text_output = transcribe_with_groq(
                GROQ_API_KEY=os.environ.get("GROQ_API_KEY"), 
                audio_filepath=audio_filepath,
                stt_model="whisper-large-v3"
            )
        else:
            speech_to_text_output = "No audio provided"

        # Handle the image input
        if image_filepath:
            doctor_response = analyze_image_with_query(
                system_prompt + speech_to_text_output,
                "meta-llama/llama-4-scout-17b-16e-instruct",
                encode_image(image_filepath)
            )
        else:
            doctor_response = "No image provided for me to analyze"

        # Generate audio response
        output_audio_path = "final.mp3"
        try:
            text_to_speech_elevenLabs(input_text=doctor_response, output_filepath=output_audio_path)
        except Exception as e:
            logger.error(f"Audio generation error: {e}")
            output_audio_path = None

        return speech_to_text_output, doctor_response, output_audio_path
    
    except Exception as e:
        logger.error(f"Error in process_inputs: {e}")
        return f"Error: {str(e)}", "An error occurred while processing your request.", None

# Create the interface
iface = gr.Interface(
    fn=process_inputs,
    inputs=[
        gr.Audio(sources=["microphone"], type="filepath"),
        gr.Image(type="filepath")
    ],
    outputs=[
        gr.Textbox(label="Speech to Text"),
        gr.Textbox(label="Doctor's Response"),
        gr.Audio()
    ],
    title="AI Doctor with Vision and Voice",
    description="Upload an image and record audio to get medical analysis",
    theme=gr.themes.Soft()
)

if __name__ == "__main__":
    import os
    port = int(os.environ.get("PORT", 10000))
    logger.info(f"Starting server on port {port}")
    
    # Launch with proper configuration for deployment
    iface.launch(
        server_name="0.0.0.0", 
        server_port=port,
        share=False,
        debug=False,
        show_error=True
    )