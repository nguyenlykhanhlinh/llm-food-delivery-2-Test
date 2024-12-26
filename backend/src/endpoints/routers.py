"""File containing root routes"""

from fastapi.routing import APIRouter
from fastapi import Depends, HTTPException, File, UploadFile
from fastapi.encoders import jsonable_encoder
from fastapi.staticfiles import StaticFiles
import base64
import json
import tempfile
import logging
from pathlib import Path
from typing import Dict, List, Any

# Schemas
from src.schemas import (
    ChatRequest,
    FunctionCall,
    AudioTranscriptRequest,
    AudioTTSRequest,
)
from src.handlers import MainHandler
from src.data.data_models import Restaurant, Foods

# Services
from src.services import groq_service, functions

# Data
from sqlalchemy.orm import Session
from src.data.data_utils import get_db
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from typing import List, Dict
from src.data import get_db
from src.data.data_models import Restaurant, Foods

router = APIRouter()
def create_router(handler: MainHandler, CONFIG: Dict) -> APIRouter:
    """Create and configure the API router

    Args:
        handler: Main application handler
        CONFIG: Application configuration

    Returns:
        Configured APIRouter instance
    """
    router = APIRouter()
    client = handler.groq_client

    @router.post("/chat/send_message")
    async def send_message(prompt_request: ChatRequest) -> Dict:
        """Handle chat messages and generate responses"""
        prompt_handler = handler.prompt_handler
        messages = prompt_handler.get_messages(prompt_request)

        functions = []
        if prompt_request.function_call:
            functions = prompt_handler.get_functions()

        try:
            prompt_response = await groq_service.chat_completion(
                messages=messages, CONFIG=CONFIG, functions=functions, client=client
            )
            response = prompt_handler.prepare_response(prompt_response)
        except Exception as e:
            logging.error(f"Chat error: {str(e)}")
            response = {
                "response": "Oops there was an error, please try again",
                "function_call": None,
            }
        return response

    @router.post("/chat/function_call")
    async def function_call(function_call: FunctionCall) -> Dict:
        """Execute function calls from frontend"""
        function_call_properties = jsonable_encoder(function_call)
        function_name = function_call_properties["name"]
        function_arguments = json.loads(function_call_properties["arguments"])

        available_functions = {
            "get_restaurant_pages": lambda kwargs: functions.find_restaurant_pages(
                CONFIG=CONFIG, **kwargs
            ),
            "open_restaurant_page": lambda kwargs: functions.open_restaurant_page(
                CONFIG=CONFIG, **kwargs
            ),
            "close_restaurant_page": lambda _: functions.dummy_function(),
            "get_user_actions": lambda _: functions.dummy_function(),
            "get_menu_of_restaurant": lambda kwargs: functions.get_menu_of_restaurant(
                CONFIG=CONFIG, **kwargs
            ),
            "add_food_to_cart": lambda kwargs: functions.add_food_to_cart(
                CONFIG=CONFIG, **kwargs
            ),
            "remove_food_from_cart": lambda kwargs: functions.remove_food_from_cart(
                CONFIG=CONFIG, **kwargs
            ),
            "open_shopping_cart": lambda _: functions.dummy_function(),
            "close_shopping_cart": lambda _: functions.dummy_function(),
            "place_order": lambda _: functions.dummy_function(),
            "activate_handsfree": lambda _: functions.dummy_function(),
        }

        function_response = await available_functions[function_name](function_arguments)
        return {"response": function_response}

    @router.post("/chat/transcribe")
    async def generate_transcription(audio_req: AudioTranscriptRequest) -> Dict:
        """Transcribe audio to text"""
        audio_handler = handler.audio_handler
        audio_segment, _ = audio_handler.extract_audio_segment(audio_req.audio)

        with tempfile.NamedTemporaryFile(suffix=".mp3", delete=True) as tmp_file:
            audio_segment.export(tmp_file.name, format="mp3")
            speech_filepath = Path(tmp_file.name)
            transcripted_response = await handler.whisper_service(
                audio_file=open(speech_filepath, "rb"), CONFIG=CONFIG
            )
        return {"response": transcripted_response}

    @router.post("/chat/tts")    
    
    
    @router.get("/restaurants/")
    def get_restaurants(db: Session = Depends(get_db)) -> List[Dict]:
        """Get all restaurants with static image paths"""
        restaurants = db.query(Restaurant).all()
        return [
            {
                "id": r.id,
                "name": r.name,
                "description": r.description,
                "image": f"/static/{r.image}" if r.image else None,
            }
            for r in restaurants
        ]
    async def generate_tts(tts_req: AudioTTSRequest) -> Dict:
        """Generate text-to-speech audio"""
        audio = await groq_service.tts(text=tts_req.text, CONFIG=CONFIG, client=client)
        return {"response": audio}

    @router.get("/restaurants/")
    def get_restaurants(db: Session = Depends(get_db)) -> List[Dict]:
        """Get all restaurants with static image paths"""
        restaurants = db.query(Restaurant).all()
        return [
            {
                "id": r.id,
                "name": r.name,
                "description": r.description,
                "image": f"/static/{r.image}" if r.image else None,
            }
            for r in restaurants
        ]

    @router.get("/restaurants/{restaurant_id}/foods/")
    def get_foods_from_restaurant(
        restaurant_id: int, db: Session = Depends(get_db)
    ) -> List[Dict]:
        """Get foods for a specific restaurant with static image paths"""
        restaurant = db.query(Restaurant).filter(Restaurant.id == restaurant_id).first()
        if not restaurant:
            raise HTTPException(status_code=404, detail="Restaurant not found")

        foods = db.query(Foods).filter(Foods.restaurant_id == restaurant_id).all()
        return [
            {
                "id": f.id,
                "name": f.name,
                "description": f.description,
                "image": f"/static/{f.image}" if f.image else None,
                "price": f.price,
            }
            for f in foods
        ]

    return router
