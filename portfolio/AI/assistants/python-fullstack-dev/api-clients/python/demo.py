#!/usr/bin/env python3
"""
Interactive Demo - Python Full-Stack Developer Assistant
=======================================================

Complete demonstration of the assistant's capabilities with
multiple example applications and interactive features.

License: CC-BY-NC-ND-4.0
Author: Sebastian C.
Repository: https://github.com/sebastian-c87/my-IT-profile-hub
"""

import os
import sys
import time
from pathlib import Path
from client import PythonFullStackAssistant, APIResponse

class AssistantDemo:
    def __init__(self):
        """Initialize demo with assistant and create output directory"""
        self.assistant = PythonFullStackAssistant()
        self.output_dir = Path("demo_outputs")
        self.output_dir.mkdir(exist_ok=True)
        
    def run_demo(self):
        """Main demo loop"""
        self._print_header()
        
        while True:
            self._show_menu()
            choice = input("\n👉 Wybierz opcję (1-6): ").strip()
            
            if choice == "1":
                self._demo_simple_app()
            elif choice == "2":
                self._demo_complex_app()
            elif choice == "3":
                self._demo_custom_app()
            elif choice == "4":
                self._demo_provider_comparison()
            elif choice == "5":
                self._show_provider_status()
            elif choice == "6":
                print("\n👋 Dziękuję za wypróbowanie demo!")
                break
            else:
                print("❌ Niepoprawny wybór. Spróbuj ponownie.")
            
            input("\n⏸️  Naciśnij Enter aby kontynuować...")
    
    def _print_header(self):
        """Print demo header"""
        print("=" * 70)
        print("🤖 PYTHON FULL-STACK DEVELOPER ASSISTANT - DEMO")
        print("=" * 70)
        print(f"📍 Repository: https://github.com/sebastian-c87/my-IT-profile-hub")
        print(f"📄 License: CC-BY-NC-ND-4.0")
        print(f"🔧 Available providers: {self.assistant.get_available_providers()}")
        print()
    
    def _show_menu(self):
        """Display main menu"""
        print("📋 DOSTĘPNE OPCJE:")
        print("1. 🏃‍♂️ Quick Demo - Prosta aplikacja TODO")
        print("2. 🚀 Advanced Demo - Złożona aplikacja e-commerce") 
        print("3. ✏️  Custom Demo - Twoja aplikacja")
        print("4. ⚖️  Provider Comparison - Claude vs OpenAI")
        print("5. 📊 Provider Status - Sprawdź dostępność")
        print("6. 🚪 Wyjście")
    
    def _demo_simple_app(self):
        """Demo simple TODO application"""
        print("\n🏃‍♂️ QUICK DEMO - APLIKACJA TODO")
        print("-" * 35)
        
        app_idea = "Aplikacja TODO z możliwością dodawania, edycji i usuwania zadań"
        requirements = "FastAPI backend, React frontend, SQLite database, responsive design"
        
        print(f"💡 Pomysł: {app_idea}")
        print(f"📋 Wymagania: {requirements}")
        print("\n⏱️  Generuję aplikację...")
        
        response = self.assistant.create_application(app_idea, requirements)
        self._display_result(response, "simple_todo_app")
    
    def _demo_complex_app(self):
        """Demo complex e-commerce application"""
        print("\n🚀 ADVANCED DEMO - APLIKACJA E-COMMERCE")
        print("-" * 42)
        
        app_idea = """Kompleksowa platforma e-commerce z koszykiem, płatnościami, 
        zarządzaniem produktami, systemem użytkowników, panelem admina, 
        i integracją z zewnętrznymi API płatniczymi"""
        
        requirements = """
        - Django REST Framework backend
        - React TypeScript frontend z Redux
        - PostgreSQL database
        - JWT authentication
        - Stripe payments integration
        - Email notifications
        - Admin dashboard
        - Docker deployment setup
        - Unit i integration tests
        """
        
        print(f"💡 Pomysł: {app_idea}")
        print(f"📋 Wymagania: {requirements}")
        print("\n⏱️  Generuję złożoną aplikację... (może potrwać 3-5 minut)")
        
        response = self.assistant.create_application(app_idea, requirements)
        self._display_result(response, "complex_ecommerce_app")
    
    def _demo_custom_app(self):
        """Demo with user's custom application idea"""
        print("\n✏️  CUSTOM DEMO - TWOJA APLIKACJA")
        print("-" * 33)
        
        print("Opisz swoją aplikację (im więcej detali, tym lepszy rezultat):")
        app_idea = input("💡 Pomysł: ").strip()
        
        if not app_idea:
            print("❌ Brak pomysłu. Wracam do menu.")
            return
        
        print("\nOpcjonalne wymagania techniczne:")
        requirements = input("📋 Wymagania (lub Enter): ").strip()
        
        print(f"\n⏱️  Generuję aplikację: '{app_idea[:50]}{'...' if len(app_idea) > 50 else ''}'")
        
        response = self.assistant.create_application(app_idea, requirements)
        filename = f"custom_{app_idea.lower().replace(' ', '_')[:20]}"
        self._display_result(response, filename)
    
    def _demo_provider_comparison(self):
        """Compare Claude vs OpenAI responses"""
        print("\n⚖️  PROVIDER COMPARISON - CLAUDE VS OPENAI")
        print("-" * 45)
        
        app_idea = "Aplikacja do zarządzania przepisami kulinarnymi z wyszukiwaniem i ocenami"
        requirements = "Flask backend, Vue.js frontend, MongoDB, search functionality"
        
        print(f"💡 Test case: {app_idea}")
        print(f"📋 Wymagania: {requirements}")
        print()
        
        # Test Claude
        if self.assistant.claude_client:
            print("🟦 Testing Claude...")
            claude_response = self.assistant.create_application(
                app_idea, requirements, provider="claude"
            )
            self._display_comparison_result("Claude", claude_response)
        else:
            print("🟦 Claude: Not available")
        
        print()
        
        # Test OpenAI  
        if self.assistant.openai_client:
            print("🟩 Testing OpenAI...")
            openai_response = self.assistant.create_application(
                app_idea, requirements, provider="openai" 
            )
            self._display_comparison_result("OpenAI", openai_response)
        else:
            print("🟩 OpenAI: Not available")
    
    def _show_provider_status(self):
        """Display detailed provider status"""
        print("\n📊 PROVIDER STATUS")
        print("-" * 20)
        
        providers = self.assistant.get_available_providers()
        
        for provider, available in providers.items():
            status = "✅ Available" if available else "❌ Not available"
            env_var = "ANTHROPIC_API_KEY" if provider == "claude" else "OPENAI_API_KEY"
            key_status = "Set" if os.getenv(env_var) else "Not set"
            
            print(f"{provider.upper():<8} {status}")
            print(f"         API Key ({env_var}): {key_status}")
            print()
        
        if not any(providers.values()):
            print("⚠️  No providers available. Please check your API key configuration.")
            print("\nSetup instructions:")
            print("1. Create .env file in this directory")
            print("2. Add: ANTHROPIC_API_KEY=your_claude_key")
            print("3. Add: OPENAI_API_KEY=your_openai_key")
    
    def _display_result(self, response: APIResponse, filename: str):
        """Display and save generation result"""
        print(f"\n{'✅ SUCCESS' if response.success else '❌ FAILED'}")
        print("-" * 50)
        
        if response.success:
            # Display stats
            lines = response.content.count('\n')
            words = len(response.content.split())
            chars = len(response.content)
            
            print(f"📊 Statistics:")
            print(f"   • Provider: {response.provider} ({response.model})")
            print(f"   • Generation time: {response.response_time:.1f} seconds")
            print(f"   • Tokens used: {response.tokens_used or 'N/A'}")
            print(f"   • Lines: {lines:,}")
            print(f"   • Words: {words:,}")
            print(f"   • Characters: {chars:,}")
            
            # Save to file
            output_file = self.output_dir / f"{filename}.md"
            with open(output_file, 'w', encoding='utf-8') as f:
                f.write(f"# Generated Application - {filename}\n\n")
                f.write(f"**Provider:** {response.provider} ({response.model})\n")
                f.write(f"**Generated:** {time.strftime('%Y-%m-%d %H:%M:%S')}\n")
                f.write(f"**Time:** {response.response_time:.1f}s\n")
                f.write(f"**Tokens:** {response.tokens_used or 'N/A'}\n\n")
                f.write("---\n\n")
                f.write(response.content)
            
            print(f"\n💾 Saved to: {output_file}")
            
            # Show preview
            print(f"\n📖 PREVIEW (first 500 characters):")
            print("-" * 50)
            preview = response.content[:500]
            if len(response.content) > 500:
                preview += "\n\n[... content truncated ...]"
            print(preview)
            
        else:
            print(f"❌ Error: {response.error_message}")
    
    def _display_comparison_result(self, provider_name: str, response: APIResponse):
        """Display comparison result summary"""
        if response.success:
            lines = response.content.count('\n')
            words = len(response.content.split())
            
            print(f"   ✅ {provider_name}: {response.response_time:.1f}s, {lines:,} lines, {words:,} words")
        else:
            print(f"   ❌ {provider_name}: {response.error_message}")

def main():
    """Main entry point"""
    # Check if any API keys are available
    has_claude = bool(os.getenv('ANTHROPIC_API_KEY'))
    has_openai = bool(os.getenv('OPENAI_API_KEY'))
    
    if not has_claude and not has_openai:
        print("❌ BRAK KONFIGURACJI API")
        print("\nPotrzebny jest przynajmniej jeden klucz API:")
        print("1. Utwórz plik .env w tym folderze")
        print("2. Dodaj klucz Claude: ANTHROPIC_API_KEY=sk-ant-...")
        print("3. LUB dodaj klucz OpenAI: OPENAI_API_KEY=sk-...")
        print("4. Uruchom demo ponownie")
        sys.exit(1)
    
    try:
        demo = AssistantDemo()
        demo.run_demo()
    except KeyboardInterrupt:
        print("\n\n👋 Demo interrupted. See you next time!")
    except Exception as e:
        print(f"\n❌ Unexpected error: {str(e)}")
        print("Please check your configuration and try again.")

if __name__ == "__main__":
    main()
