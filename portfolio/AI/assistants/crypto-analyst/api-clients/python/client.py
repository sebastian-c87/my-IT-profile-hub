"""
Cryptocurrency Market Analyst - Simple Python Client
Uses OpenAI Responses API (GPT-5) and Anthropic Batch API

Author: Sebastian C.
License: CC-BY-NC-ND-4.0
Repository: https://github.com/sebastian-c87/my-IT-profile-hub
"""

import os
import re
from openai import OpenAI
import anthropic
from dotenv import load_dotenv

# Load environment
load_dotenv()

class CryptoAnalyst:
    """Simple Cryptocurrency Market Analyst using OpenAI GPT-5 and Claude"""
    
    def __init__(self):
        # Setup OpenAI client
        openai_key = os.getenv("OPENAI_API_KEY")
        if openai_key:
            self.openai_client = OpenAI(api_key=openai_key)
            print("✅ OpenAI API key loaded successfully")
            print("✅ OpenAI client initialized and connected")
        else:
            self.openai_client = None
            print("❌ OpenAI API key not found in environment")
            
        # Setup Anthropic client  
        anthropic_key = os.getenv("ANTHROPIC_API_KEY")
        if anthropic_key:
            self.anthropic_client = anthropic.Anthropic(api_key=anthropic_key)
            print("✅ Anthropic API key loaded successfully")
            print("✅ Claude client initialized and connected")
        else:
            self.anthropic_client = None
            print("❌ Anthropic API key not found in environment")
        
        # Load system prompt
        self._load_prompt()
        
        # Required sections from prompt
        self.required_sections = [
            ("🎯 Executive Summary", "## 🎯 Executive Summary"),
            ("📊 Analiza Techniczna", "## 📊 Analiza Techniczna"),
            ("🔍 Analiza Fundamentalna", "## 🔍 Analiza Fundamentalna"),
            ("🌊 Sentiment & On-chain", "## 🌊 Sentiment & On-chain"),
            ("⚠️ Risk Assessment", "## ⚠️ Risk Assessment"),
            ("🎯 Rekomendacje & Sygnały", "## 🎯 Rekomendacje & Sygnały"),
            ("📋 Disclaimer", "## 📋 Disclaimer")
        ]
    
    def _load_prompt(self):
        """Load system prompt from file"""
        try:
            with open("../../system.md", "r", encoding="utf-8") as f:
                self.system_prompt = f.read()
            print("✅ System prompt loaded from ../../system.md")
        except FileNotFoundError:
            self.system_prompt = "You are a cryptocurrency market analyst."
            print("⚠️ System prompt file not found - using fallback prompt")
    
    def _validate_response_structure(self, response_text):
        """
        Validate if response contains all required sections from prompt
        
        Args:
            response_text (str): AI response to validate
            
        Returns:
            dict: Validation results with success/fail for each section
        """
        validation_results = {}
        total_chars = len(response_text)
        
        print(f"\n📊 VALIDATING RESPONSE STRUCTURE:")
        print("="*50)
        
        for section_name, section_header in self.required_sections:
            # Check if section header exists in response
            if section_header in response_text:
                validation_results[section_name] = "✅ SUCCESS"
                print(f"{section_name}: ✅ SUCCESS")
            else:
                validation_results[section_name] = "❌ FAIL"
                print(f"{section_name}: ❌ FAIL")
        
        # Overall validation
        successful_sections = sum(1 for result in validation_results.values() if "SUCCESS" in result)
        total_sections = len(self.required_sections)
        
        print("="*50)
        print(f"📈 RESPONSE SUMMARY:")
        print(f"   ✅ Successful sections: {successful_sections}/{total_sections}")
        print(f"   📝 Total characters generated: {total_chars}")
        
        if successful_sections == total_sections:
            print(f"🎉 RESPONSE VALIDATION: ✅ SUCCESS - All required elements present!")
        else:
            print(f"⚠️  RESPONSE VALIDATION: ⚠️ PARTIAL - Missing {total_sections - successful_sections} sections")
        
        return {
            'validation_results': validation_results,
            'total_chars': total_chars,
            'successful_sections': successful_sections,
            'total_sections': total_sections,
            'is_complete': successful_sections == total_sections
        }
    
    def analyze_crypto_openai(self, crypto_query, model="gpt-5-nano"):
        """
        Analyze cryptocurrency using OpenAI GPT-5 via Responses API
        
        Args:
            crypto_query (str): User's crypto question
            model (str): GPT-5 model to use
            
        Returns:
            dict: Analysis results with validation info
        """
        if not self.openai_client:
            return {
                'success': False,
                'error': "OpenAI client not available - check API key",
                'response': None,
                'validation': None
            }
        
        try:
            print(f"\n🚀 STARTING ANALYSIS:")
            print(f"   🤖 Model: {model}")
            print(f"   🔗 API: OpenAI Responses API")
            print(f"   📝 Query: {crypto_query[:100]}...")
            print(f"   ⏳ Processing...")
            
            # Simple Responses API call - CORRECT FORMAT
            response = self.openai_client.responses.create(
                model=model,
                input=f"{self.system_prompt}\n\nUser query: {crypto_query}",
                reasoning={"effort": "medium"},
                text={"verbosity": "medium"},
                max_output_tokens=16000,
                tools=[
                    {"type": "web_search"}
                    # Removed code_interpreter to avoid container error
                ]
            )
            
            response_text = response.output_text
            print(f"✅ AI response generated successfully!")
            
            # Validate response structure
            validation_info = self._validate_response_structure(response_text)
            
            return {
                'success': True,
                'model_used': model,
                'response': response_text,
                'validation': validation_info,
                'response_id': response.id if hasattr(response, 'id') else 'unknown'
            }
            
        except Exception as e:
            print(f"❌ OpenAI API Error: {str(e)}")
            return {
                'success': False,
                'error': str(e),
                'response': None,
                'validation': None
            }
    
    def analyze_crypto_claude_simple(self, crypto_query):
        """
        Simple Claude analysis (not batch)
        
        Args:
            crypto_query (str): User's crypto question
            
        Returns:
            dict: Analysis results with validation info
        """
        if not self.anthropic_client:
            return {
                'success': False,
                'error': "Claude client not available - check API key",
                'response': None,
                'validation': None
            }
            
        try:
            print(f"\n🚀 STARTING ANALYSIS:")
            print(f"   🤖 Model: claude-3-5-haiku-20241022")
            print(f"   🔗 API: Anthropic Messages API") 
            print(f"   📝 Query: {crypto_query[:100]}...")
            print(f"   ⏳ Processing...")
            
            response = self.anthropic_client.messages.create(
                model="claude-3-5-haiku-20241022",
                max_tokens=16000,
                messages=[{
                    "role": "user",
                    "content": f"{self.system_prompt}\n\nUser query: {crypto_query}"
                }]
            )
            
            response_text = response.content[0].text
            print(f"✅ Claude response generated successfully!")
            
            # Validate response structure  
            validation_info = self._validate_response_structure(response_text)
            
            return {
                'success': True,
                'model_used': 'claude-3-5-haiku-20241022',
                'response': response_text,
                'validation': validation_info,
                'response_id': response.id if hasattr(response, 'id') else 'unknown'
            }
            
        except Exception as e:
            print(f"❌ Claude API Error: {str(e)}")
            return {
                'success': False,
                'error': str(e),
                'response': None,
                'validation': None
            }
    
    def get_available_models(self):
        """Get list of available models"""
        models = []
        if self.openai_client:
            models.extend(["gpt-5", "gpt-5-mini", "gpt-5-nano"])
        if self.anthropic_client:
            models.extend(["claude-3-5-haiku-20241022"])
        return models
    
    def export_to_file(self, content, filename="analysis.txt"):
        """Save analysis to file"""
        try:
            with open(filename, "w", encoding="utf-8") as f:
                f.write(content)
            print(f"✅ Analysis saved to {filename}")
            return True
        except Exception as e:
            print(f"❌ Failed to save: {str(e)}")
            return False


if __name__ == "__main__":
    # Simple test when running client.py directly
    print("🧪 TESTING CRYPTO ANALYST CLIENT")
    print("="*40)
    
    analyst = CryptoAnalyst()
    
    if analyst.openai_client:
        print(f"\n🔬 Running test analysis...")
        test_result = analyst.analyze_crypto_openai(
            "Przeanalizuj Bitcoin (BTC) pod kątem obecnych trendów rynkowych", 
            model="gpt-5-nano"
        )
        
        if test_result['success']:
            print(f"\n✅ TEST COMPLETED SUCCESSFULLY!")
            print(f"   📊 Validation: {'✅ PASSED' if test_result['validation']['is_complete'] else '⚠️ PARTIAL'}")
        else:
            print(f"\n❌ TEST FAILED: {test_result['error']}")
    else:
        print("\n❌ Cannot run test - OpenAI client not available")
