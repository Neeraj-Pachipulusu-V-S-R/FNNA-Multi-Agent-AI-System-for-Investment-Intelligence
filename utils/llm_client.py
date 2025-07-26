import google.generativeai as genai
import os
from typing import Optional
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Configure Gemini API
genai.configure(api_key=os.getenv("GEMINI_API_KEY"))

class GeminiClient:
    """Google Gemini API client for LLM operations"""
    
    def __init__(self, model_name: str = "gemini-1.5-flash"):
        self.model_name = model_name
        self.model = genai.GenerativeModel(model_name)
    
    def generate_response(self, prompt: str, temperature: float = 0.3, max_tokens: int = 500) -> str:
        """
        Generate response using Google Gemini API
        
        Args:
            prompt: Input prompt for the model
            temperature: Controls randomness (0.0 to 1.0)
            max_tokens: Maximum tokens in response
            
        Returns:
            Generated response text
        """
        try:
            generation_config = genai.types.GenerationConfig(
                temperature=temperature,
                max_output_tokens=max_tokens,
            )
            
            response = self.model.generate_content(
                prompt,
                generation_config=generation_config
            )
            
            return response.text.strip()
            
        except Exception as e:
            print(f"Error generating response: {str(e)}")
            return "Error: Unable to generate response"

# Global client instance
_client = GeminiClient()

def llama_prompt(prompt: str, temperature: float = 0.3, max_tokens: int = 500) -> str:
    """
    Legacy function name maintained for backward compatibility
    Now uses Google Gemini instead of Llama
    """
    return _client.generate_response(prompt, temperature, max_tokens)

def gemini_prompt(prompt: str, temperature: float = 0.3, max_tokens: int = 500) -> str:
    """
    New function name for clarity - uses Google Gemini API
    """
    return _client.generate_response(prompt, temperature, max_tokens)
