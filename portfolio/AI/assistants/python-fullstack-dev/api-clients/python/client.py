"""
Python Full-Stack Developer Assistant Client
=====================================================

OpenAI Responses API (GPT-5) 
and Claude Message Batches API.

Author: Sebastian C.
License: CC-BY-NC-ND-4.0
Repository: https://github.com/sebastian-c87/my-IT-profile-hub
"""

import os
import time
from dataclasses import dataclass
from enum import Enum
from dotenv import load_dotenv
import anthropic
import openai

load_dotenv()

class AIProvider(Enum):
    """AI Service Providers"""
    OPENAI = "openai"
    CLAUDE = "claude"

@dataclass
class APIResponse:
    content: str
    model: str
    provider: AIProvider
    tokens_used: int = None
    response_time: float = None
    success: bool = True
    error_message: str = None

class PythonFullStackAssistant:
    def __init__(self):
        # Load API keys from .env
        self.openai_client = openai.OpenAI(api_key=os.getenv('OPENAI_API_KEY')) if os.getenv('OPENAI_API_KEY') else None
        self.claude_client = anthropic.Anthropic(api_key=os.getenv('ANTHROPIC_API_KEY')) if os.getenv('ANTHROPIC_API_KEY') else None
        
        if not self.openai_client and not self.claude_client:
            raise ValueError("No API keys found. Set OPENAI_API_KEY or ANTHROPIC_API_KEY in .env file")
    
    def get_available_providers(self) -> list:
        """Get list of available AI providers"""
        providers = []
        if self.openai_client:
            providers.append("openai")
        if self.claude_client:
            providers.append("claude")
        return providers
    
    def create_application(self, app_idea: str, requirements: str = "") -> APIResponse:
        if not app_idea.strip():
            return APIResponse("", "", AIProvider.OPENAI, success=False, error_message="App idea cannot be empty")
        
        system_prompt = self._load_system_prompt()
        user_message = f"**Pomysł na aplikację:** {app_idea}\n**Dodatkowe wymagania:** {requirements or 'Brak'}"
        
        # Try OpenAI first
        if self.openai_client:
            return self._call_openai(system_prompt, user_message)
        
        # Fallback to Claude Batch
        if self.claude_client:
            return self._call_claude_batch(system_prompt, user_message)
        
        return APIResponse("", "", AIProvider.OPENAI, success=False, error_message="No providers available")
    
    def _call_openai(self, system_prompt: str, user_message: str) -> APIResponse:
        start_time = time.time()
        
        try:
            # FIXED: Proper Responses API usage
            response = self.openai_client.responses.create(
                model="gpt-5-nano",
                instructions=system_prompt,
                input=user_message,
                reasoning={"effort": "minimal"}, # W pełnej wersji ustawić "high" dla zwiększenia efektu rozumowania modelu
                text={"verbosity": "low"}, # W pełnej wersji zmienić na "medium" aby model więcej się wypowiadał
                store=False # W pełnej wersji zmienić na True lub usunąć atrybut "store". Zapewnia kontynuacje pracy na podstawie historii wiadomości
            )
            
            # Handle Responses API structure properly
            content = ""
            tokens_used = 0
            
            # Extract content from response.output array
            if hasattr(response, 'output') and response.output:
                for item in response.output:
                    if item.type == "message" and hasattr(item, 'content'):
                        for content_item in item.content:
                            if content_item.type == "output_text":
                                content = content_item.text
                                break
            
            # Extract token usage
            if hasattr(response, 'usage') and response.usage:
                tokens_used = response.usage.total_tokens
            
            # Fallback if no content found
            if not content and hasattr(response, 'output_text'):
                content = response.output_text
            
            if not content:
                raise Exception("No content returned from OpenAI Responses API")
            
            return APIResponse(
                content=content,
                model="gpt-5-nano", 
                provider=AIProvider.OPENAI,
                tokens_used=tokens_used,
                response_time=time.time() - start_time,
                success=True
            )
            
        except Exception as e:
            return APIResponse(
                content="",
                model="gpt-5-nano",
                provider=AIProvider.OPENAI,
                response_time=time.time() - start_time,
                success=False,
                error_message=f"OpenAI API Error: {str(e)}"
            )
    
    def _call_claude_batch(self, system_prompt: str, user_message: str) -> APIResponse:
        start_time = time.time()
        
        try:
            # Create batch
            batch = self.claude_client.messages.batches.create(
                requests=[{
                    "custom_id": f"app-{int(time.time())}",
                    "params": {
                        "model": "claude-3-5-haiku-20241022",
                        "max_tokens": 8192,
                        "system": system_prompt,
                        "messages": [{"role": "user", "content": user_message}]
                    }
                }]
            )
            
            # Poll for completion (simplified - max 30 minutes)
            for _ in range(60):  # 60 * 30s = 30 min
                time.sleep(30)
                batch_status = self.claude_client.messages.batches.retrieve(batch.id)
                
                if batch_status.processing_status == "ended":
                    for result in self.claude_client.messages.batches.results(batch.id):
                        if result.result.type == "succeeded":
                            return APIResponse(
                                content=result.result.message.content[0].text,
                                model="claude-3-5-haiku-20241022",
                                provider=AIProvider.CLAUDE,
                                tokens_used=result.result.message.usage.input_tokens + result.result.message.usage.output_tokens,
                                response_time=time.time() - start_time,
                                success=True
                            )
            
            return APIResponse("", "claude-3-5-haiku-20241022", AIProvider.CLAUDE, response_time=time.time() - start_time, success=False, error_message="Batch timeout")
            
        except Exception as e:
            return APIResponse("", "claude-3-5-haiku-20241022", AIProvider.CLAUDE, response_time=time.time() - start_time, success=False, error_message=str(e))
    
    def _load_system_prompt(self) -> str:
        try:
            with open('../../system.md', 'r', encoding='utf-8') as f:
                return f.read()
        except FileNotFoundError:
            return """# Rola
Jesteś ekspertem **Programistą Python Full-Stack** z ponad 10-letnim doświadczeniem w tworzeniu nowoczesnych aplikacji web.

# Cel
Przekształcenie pomysłu użytkownika w kompletną, działającą aplikację web z profesjonalną strukturą plików i kodem production-ready."""

if __name__ == "__main__":
    assistant = PythonFullStackAssistant()
    print(f"Available providers: {assistant.get_available_providers()}")
    result = assistant.create_application("Task management app", "FastAPI + React + SQLite")
    print(f"Success: {result.success}, Provider: {result.provider.value}, Time: {result.response_time:.1f}s")
    if result.success:
        print(f"Generated: {len(result.content)} characters")
    else:
        print(f"Error: {result.error_message}")
