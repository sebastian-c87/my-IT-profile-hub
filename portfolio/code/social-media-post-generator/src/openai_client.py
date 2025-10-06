"""
OpenAI GPT-5-nano Client with Web Search Integration
Optimized for cost-effective social media content generation
"""
import os
import logging
from typing import Optional, Dict, Any, List
from openai import OpenAI

# Direct import instead of relative
from config import Config

class SocialMediaAI:
    """GPT-5-nano client with web search for enhanced content generation"""
    
    def __init__(self, config: Config):
        self.config = config
        self.client = OpenAI(api_key=config.openai_api_key)
        self.logger = logging.getLogger(__name__)
        
    def generate_post(self, topic: str, platform: str = "universal", 
                     style: str = "engaging", max_length: int = 300,
                     context: str = "", language: str = "polish", 
                     use_web_search: bool = True) -> str:
        """
        Generate social media post using GPT-5-nano with web search
        
        Args:
            topic: Main topic for the post
            platform: Target platform
            style: Content style
            max_length: Maximum character length
            context: Additional context
            language: Language for the post (polish, english)
            use_web_search: Whether to use web search for current info
            
        Returns:
            Generated social media post
        """
        try:
            # Language settings
            language_settings = {
                "polish": {
                    "instruction": "Napisz post w języku polskim",
                    "tone_desc": "naturalnym, polskim stylem",
                    "cta_examples": "Co myślisz?, Zgodziłbyś się?, Podziel się opinią, Jaka jest Twoja opinia?"
                },
                "english": {
                    "instruction": "Write the post in English",
                    "tone_desc": "natural English style", 
                    "cta_examples": "What do you think?, Do you agree?, Share your thoughts, What's your opinion?"
                }
            }
            
            lang_setting = language_settings.get(language, language_settings["polish"])
            
            # Platform-specific guidelines
            platform_specs = {
                "twitter": {
                    "format": "post na Twitter (max 280 znaków)" if language == "polish" else "Twitter post (max 280 chars)",
                    "requirements": "Dodaj 1-2 hashtagi, zwięzłe i angażujące" if language == "polish" else "Include 1-2 hashtags, keep it punchy and engaging",
                    "tone": "rozmówkowy i możliwy do udostępnienia" if language == "polish" else "conversational and shareable"
                },
                "linkedin": {
                    "format": "profesjonalny post na LinkedIn" if language == "polish" else "LinkedIn professional post", 
                    "requirements": "Skupiony na wartości biznesowej, 3-5 hashtagów, profesjonalny ton" if language == "polish" else "Business value focused, 3-5 hashtags, professional tone",
                    "tone": "autorytatywny i wnikliwy" if language == "polish" else "authoritative and insightful"
                },
                "facebook": {
                    "format": "angażujący post na Facebook" if language == "polish" else "Facebook engaging post",
                    "requirements": "Zachęcaj do komentarzy i udostępnień, narracyjne podejście" if language == "polish" else "Encourage comments and shares, storytelling approach", 
                    "tone": "przyjazny i rozmówkowy" if language == "polish" else "friendly and conversational"
                },
                "instagram": {
                    "format": "post na Instagram skupiony na wizualizacji" if language == "polish" else "Instagram visual-first post",
                    "requirements": "Opisz elementy wizualne, użyj odpowiednich hashtagów" if language == "polish" else "Describe visual elements, use relevant hashtags",
                    "tone": "kreatywny i inspirujący" if language == "polish" else "creative and inspiring"
                },
                "universal": {
                    "format": "uniwersalny post w social media" if language == "polish" else "Universal social media post",
                    "requirements": "Neutralny dla platform, adaptowalna treść" if language == "polish" else "Platform-neutral, adaptable content",
                    "tone": "angażujący i wszechstronny" if language == "polish" else "engaging and versatile"
                }
            }
            
            spec = platform_specs.get(platform, platform_specs["universal"])
            
            # Build comprehensive prompt for GPT-5-nano with Polish language
            system_message = f"""{lang_setting['instruction']}. Jesteś profesjonalnym twórcą treści w social media.
            
            ZADANIE: Stwórz {style} {spec['format']} na zadany temat.
            
            WYMAGANIA PLATFORMY:
            - Format: {spec['format']}
            - Wymagania: {spec['requirements']}
            - Ton: {spec['tone']}
            - Limit znaków: MAKSYMALNIE {max_length} znaków
            
            WYTYCZNE TREŚCI:
            1. Zacznij od przyciągającego uwagę hooku
            2. Podaj wartość lub wgląd w temat
            3. Dołącz naturalne emotikony (maksymalnie 2-3)
            4. Dodaj odpowiednie hashtagi dla platformy
            5. Zakończ wezwaniem do działania lub angażującym pytaniem
            6. Zachowaj autentyczność i możliwość udostępnienia
            7. Używaj {lang_setting['tone_desc']}
            
            KRYTYCZNE: Twoja odpowiedź musi zawierać TYLKO treść postu w języku polskim, nic więcej."""
            
            # Build user message with context
            user_message = f"Temat: {topic}"
            if context:
                user_message += f"\nDodatkowy kontekst: {context}"
            
            # Create tools list - include web search if requested
            tools = []
            if use_web_search:
                tools.append({
                    "type": "web_search"
                })
            
            # Generate with GPT-5-nano
            if tools:
                # Use tools for enhanced content
                response = self.client.responses.create(
                    model="gpt-5-nano",
                    input=user_message,
                    instructions=system_message,
                    tools=tools,
                    reasoning={"effort": "low"},
                    text={"verbosity": "low"},  # Keep it concise for nano
                    max_output_tokens=200  # Limit for cost efficiency
                )
            else:
                # Standard generation without tools
                response = self.client.responses.create(
                    model="gpt-5-nano", 
                    input=user_message,
                    instructions=system_message,
                    reasoning={"effort": "low"},
                    text={"verbosity": "low"},
                    max_output_tokens=200
                )
            
            # Extract content
            generated_content = response.output_text.strip()
            
            # Validate and clean content
            if not generated_content:
                # Fallback generation without tools if empty
                self.logger.warning("Empty response, trying fallback generation")
                return self._fallback_generation(topic, platform, style, max_length, language)
            
            # Ensure character limit
            if len(generated_content) > max_length:
                # Smart truncation preserving hashtags
                if '#' in generated_content:
                    # Split at last hashtag if over limit
                    parts = generated_content.rsplit('#', 1)
                    if len(parts[0].strip()) <= max_length - 20:  # Leave room for hashtag
                        generated_content = parts[0].strip() + ' #' + parts[1]
                    else:
                        generated_content = generated_content[:max_length-3] + "..."
                else:
                    generated_content = generated_content[:max_length-3] + "..."
            
            self.logger.info(f"Successfully generated {platform} post for topic: {topic}")
            return generated_content
            
        except Exception as e:
            self.logger.error(f"Error generating social media post: {str(e)}")
            # Return fallback generation instead of error message
            return self._fallback_generation(topic, platform, style, max_length, language)
    
    def _fallback_generation(self, topic: str, platform: str, style: str, max_length: int, language: str = "polish") -> str:
        """Fallback content generation using simpler approach"""
        try:
            # Simple, direct prompt for GPT-5-nano in Polish
            if language == "polish":
                simple_prompt = f"""Napisz {style} post na {platform} o temacie: {topic}

Wymagania:
- Maksymalnie {max_length} znaków
- Dołącz 1-2 hashtagi
- Ton {style}
- Angażujący i możliwy do udostępnienia
- Język polski

Post:"""
            else:
                simple_prompt = f"""Write a {style} {platform} post about: {topic}

Requirements:
- Max {max_length} characters
- Include 1-2 hashtags
- {style} tone
- Engaging and shareable

Post:"""
            
            response = self.client.responses.create(
                model="gpt-5-nano",
                input=simple_prompt,
                reasoning={"effort": "low"},
                text={"verbosity": "low"},
                max_output_tokens=150
            )
            
            content = response.output_text.strip()
            
            if len(content) > max_length:
                content = content[:max_length-3] + "..."
                
            return content if content else self._template_fallback(topic, platform, style, language)
            
        except Exception as e:
            self.logger.error(f"Fallback generation failed: {str(e)}")
            # Ultimate fallback - template-based generation
            return self._template_fallback(topic, platform, style, language)
    
    def _template_fallback(self, topic: str, platform: str, style: str, language: str = "polish") -> str:
        """Template-based fallback when API fails"""
        if language == "polish":
            templates = {
                "engaging": f"🔥 Porozmawiajmy o {topic}! To naprawdę ważny temat. Jakie macie doświadczenia? #{topic.replace(' ', '').lower()}",
                "professional": f"Spostrzeżenia na temat {topic}: Ten temat zasługuje na uwagę w naszej branży. Kluczowe kwestie do rozważenia. #{topic.replace(' ', '').lower()}",
                "casual": f"No więc... {topic} to dość interesujący temat! Ktoś jeszcze to śledzi? Chętnie usłyszę wasze opinie! #{topic.replace(' ', '').lower()}",
                "humorous": f"Kiedy ktoś wspomina o {topic} 😄 Wiecie, że będzie ciekawa rozmowa! #{topic.replace(' ', '').lower()}",
                "inspirational": f"✨ {topic} przypomina nam, że rozwój wynika z podejmowania nowych wyzwań. Każdy krok naprzód się liczy! #{topic.replace(' ', '').lower()}"
            }
        else:
            templates = {
                "engaging": f"🔥 Let's talk about {topic}! This is something that really matters. What are your thoughts? #{topic.replace(' ', '').lower()}",
                "professional": f"Insights on {topic}: This topic deserves attention in our industry. Key considerations ahead. #{topic.replace(' ', '').lower()}",
                "casual": f"So... {topic} is pretty interesting! Anyone else following this? Would love to hear your take! #{topic.replace(' ', '').lower()}",
                "humorous": f"When someone mentions {topic} 😄 You know it's going to be an interesting conversation! #{topic.replace(' ', '').lower()}",
                "inspirational": f"✨ {topic} reminds us that growth comes from embracing new challenges. Every step forward counts! #{topic.replace(' ', '').lower()}"
            }
        
        return templates.get(style, templates["engaging"])
    
    def analyze_post_performance(self, post_content: str, language: str = "polish") -> Dict[str, Any]:
        """Analyze potential performance of social media post"""
        try:
            if not post_content.strip():
                analysis_text = "Nie można analizować pustego posta. Proszę podać treść do analizy." if language == "polish" else "Cannot analyze empty post. Please provide content to analyze."
                return {
                    "analysis": analysis_text,
                    "success": False
                }
            
            if language == "polish":
                analysis_instructions = """Przeanalizuj ten post w social media pod kątem potencjału angażowania.
                
                Podaj:
                1. Ocenę angażowania (1-10)
                2. Mocne i słabe strony
                3. Konkretne sugestie poprawy
                4. Najlepsze godziny publikacji
                5. Skuteczność hashtagów
                
                Bądź zwięzły i praktyczny."""
                
                analysis_prompt = f"Przeanalizuj ten post: \"{post_content}\""
            else:
                analysis_instructions = """Analyze this social media post for engagement potential.
                
                Provide:
                1. Engagement score (1-10)
                2. Strengths and weaknesses
                3. Specific improvement suggestions
                4. Best posting times
                5. Hashtag effectiveness
                
                Be concise and actionable."""
                
                analysis_prompt = f"Analyze this post: \"{post_content}\""
            
            response = self.client.responses.create(
                model="gpt-5-nano",
                input=analysis_prompt,
                instructions=analysis_instructions,
                reasoning={"effort": "medium"},
                text={"verbosity": "medium"},
                max_output_tokens=400
            )
            
            return {
                "analysis": response.output_text,
                "success": True
            }
            
        except Exception as e:
            self.logger.error(f"Error analyzing post: {str(e)}")
            error_text = f"Analiza niedostępna: {str(e)}" if language == "polish" else f"Analysis unavailable: {str(e)}"
            return {
                "analysis": error_text,
                "success": False
            }
    
    def search_trending_topics(self, category: str = "general", language: str = "polish") -> List[str]:
        """Search for trending topics to inspire content"""
        try:
            if language == "polish":
                search_prompt = f"Znajdź aktualne trendy w kategorii {category}, które nadawałyby się na treści w social media w Polsce"
            else:
                search_prompt = f"Find current trending topics in {category} that would make good social media content"
            
            response = self.client.responses.create(
                model="gpt-5-nano",
                input=search_prompt,
                tools=[{"type": "web_search"}],
                reasoning={"effort": "low"},
                text={"verbosity": "low"}
            )
            
            # Extract topics from response
            topics = []
            for line in response.output_text.split('\n'):
                line = line.strip()
                if line and not line.startswith('Here') and not line.startswith('Based') and not line.startswith('Oto') and not line.startswith('Znalazłem'):
                    # Clean up the line and add to topics
                    clean_topic = line.replace('•', '').replace('-', '').replace('*', '').strip()
                    if len(clean_topic) > 5 and len(clean_topic) < 100:
                        topics.append(clean_topic)
            
            return topics[:10]  # Return top 10 topics
            
        except Exception as e:
            self.logger.error(f"Error searching trending topics: {str(e)}")
            return []
