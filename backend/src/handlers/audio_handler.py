# from typing import Optional, Tuple, Any
# import base64
# import io
# import logging
# from pathlib import Path
# from tenacity import retry, wait_random, stop_after_attempt

# # Audio processing
# from pydub import AudioSegment
# from io import BytesIO
# import soundfile as sf
# import numpy as np

# # LangChain imports
# from langchain_groq import ChatGroq
# from langchain.prompts import PromptTemplate
# from langchain.chains import LLMChain


# class AudioHandler:
#     """Handler for audio processing and transcription"""

#     def __init__(self, config: dict):
#         """Initialize AudioHandler with configuration

#         Args:
#             config: Application configuration dictionary
#         """
#         self.config = config
#         self.groq_api_key = config["groq"]["api_key"]
#         self.model_name = "whisper-large-v3"
#         self.llm_model = "llama-3.1-70b-versatile"

#     def extract_audio_segment(self, audio_file: str) -> Tuple[AudioSegment, bytes]:
#         """Extract audio segment from base64 encoded audio file

#         Args:
#             audio_file: Base64 encoded audio string

#         Returns:
#             Tuple containing AudioSegment and raw audio bytes
#         """
#         try:
#             audio_data = base64.b64decode(audio_file)
#             audio_segment = AudioSegment.from_file(BytesIO(audio_data))
#             return audio_segment, audio_data
#         except Exception as e:
#             logging.error(f"Error extracting audio: {str(e)}")
#             raise

#     @retry(wait=wait_random(min=1, max=5), stop=stop_after_attempt(5))
#     async def transcribe_audio(self, audio_file: Any) -> str:
#         """Transcribe audio file using Groq Whisper

#         Args:
#             audio_file: Audio file object

#         Returns:
#             Transcribed text
#         """
#         try:
#             # Read and prepare audio data
#             audio_data = audio_file.read()
#             buffer = io.BytesIO(audio_data)
#             buffer.seek(0)

#             # Convert audio to required format
#             audio_array, sample_rate = sf.read(buffer)
#             wav_buffer = io.BytesIO()
#             sf.write(wav_buffer, audio_array, sample_rate, format="wav")
#             wav_buffer.seek(0)

#             # Initialize Groq client
#             from groq import Client

#             client = Client(api_key=self.groq_api_key)

#             # Transcribe audio
#             completion = client.audio.transcriptions.create(
#                 model=self.model_name,
#                 file=("audio.wav", wav_buffer),
#                 response_format="text",
#             )

#             return completion

#         except Exception as e:
#             logging.error(f"Transcription error: {str(e)}")
#             raise

#     async def generate_response(self, transcription: str) -> str:
#         """Generate response using Groq LLM

#         Args:
#             transcription: Transcribed text to respond to

#         Returns:
#             Generated response text
#         """
#         try:
#             if not transcription:
#                 return "No transcription available. Please try speaking again."

#             # Initialize LLM
#             llm = ChatGroq(
#                 temperature=0.3, model=self.llm_model, api_key=self.groq_api_key
#             )

#             # Setup prompt
#             prompt = PromptTemplate(
#                 input_variables=["transcription"],
#                 template="""
#                 You are a helpful assistant processing voice commands.
                
#                 User said: {transcription}
                
#                 Please provide a clear and concise response:
#                 """,
#             )

#             # Create and run chain
#             chain = LLMChain(llm=llm, prompt=prompt)
#             response = chain.run(transcription=transcription)

#             return response

#         except Exception as e:
#             logging.error(f"Response generation error: {str(e)}")
#             raise
