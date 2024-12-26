# Handlers 
from .prompt_handler import PromptHandler
<<<<<<< HEAD
# from .audio_handler import AudioHandler
=======
>>>>>>> 40731b41b3bfe5317ad9c6b9b89eb31a1ced9642
from .vectordb_handler import VectorDBHandler

# Abstract class creation
from abc import ABC, abstractmethod

# Typing hints
from typing import Optional

# CONFIG
from ..config import CONFIG

# OpenAI
import openai

## Creating main handler
class MainHandler(ABC):
    def __init__(self,):
        self.openai_client = openai.OpenAI(api_key=CONFIG["openai"]["api_key"])
        self.prompt_handler = PromptHandler()
<<<<<<< HEAD
        # self.audio_handler = AudioHandler()
        self.vectordb_handler = VectorDBHandler()
        self.groq_client = groq.Groq(api_key=CONFIG["groq"]["api_key"])
=======
        self.vectordb_handler = VectorDBHandler()
>>>>>>> 40731b41b3bfe5317ad9c6b9b89eb31a1ced9642
