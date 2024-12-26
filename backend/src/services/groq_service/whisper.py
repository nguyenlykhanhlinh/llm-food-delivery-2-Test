# from groq import Groq


# async def whisper(audio_file, CONFIG, client=None):
#     """Transcribes audio using Groq's Whisper model"""

#     groq_client = Groq(api_key=CONFIG["groq"]["api_key"])

#     transcription = groq_client.audio.transcriptions.create(file=audio_file, model="whisper-large-v3")

#     return transcription.text
