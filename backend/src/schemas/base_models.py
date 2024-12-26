from pydantic import BaseModel
from typing import Optional, List, Any, Dict


## Groq schema for Chat Completion
class FunctionCall(BaseModel):
    name: str
    arguments: str


class Message(BaseModel):
    content: str
    role: str
    function_call: Optional[FunctionCall] = None


class GroqChatCompletionResponse(BaseModel):
    text: str
    model: str
    usage: Dict[str, int]
    finish_reason: str


## Vector Search Models
class RestaurantSearchQuery(BaseModel):
    name_of_restaurant: Optional[str] = None
    type_of_restaurant: Optional[str] = None
    food_requested: Optional[List[str]] = None
    other_information: Optional[str] = None
    quantity: int = 1


class RestaurantSearchResult(BaseModel):
    restaurant_id: int
    restaurant_name: str
    restaurant_description: str
    restaurant_menu: str
    text: str
    score: float


## Message System
class InputMessage(BaseModel):
    role: str
    content: Any
    name: Optional[str] = None


class InputChatHistory(BaseModel):
    history: List[InputMessage]


class ChatRequest(BaseModel):
    query: InputChatHistory
    function_call: bool = True


## Audio system
class AudioTranscriptRequest(BaseModel):
    audio: str


class AudioResponse(BaseModel):
    message: str


class AudioTTSRequest(BaseModel):
    text: str
