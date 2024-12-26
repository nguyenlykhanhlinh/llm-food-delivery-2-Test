# Handlers
from .prompt_handler import PromptHandler
# from .audio_handler import AudioHandler
from .vectordb_handler import VectorDBHandler
from ..services import groq_service
import groq

# Abstract class creation
from abc import ABC, abstractmethod

# Typing hints
from typing import Optional

# CONFIG
from ..config import CONFIG


## Creating main handler
class MainHandler(ABC):
    def __init__(
        self,
    ):
        self.prompt_handler = PromptHandler()
        # self.audio_handler = AudioHandler()
        self.vectordb_handler = VectorDBHandler()
        self.groq_client = groq.Groq(api_key=CONFIG["groq"]["api_key"])
