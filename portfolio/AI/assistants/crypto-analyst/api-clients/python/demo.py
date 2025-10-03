"""
Interactive Demo for Cryptocurrency Market Analyst
Simple menu-driven interface for crypto analysis with file output

Author: Sebastian C.
License: CC-BY-NC-ND-4.0
Repository: https://github.com/sebastian-c87/my-IT-profile-hub
"""

from client import CryptoAnalyst
import time
import os
from pathlib import Path

def create_demo_output_folder():
    """Create demo_output folder if it doesn't exist"""
    output_dir = Path("demo_output")
    output_dir.mkdir(exist_ok=True)
    return output_dir

def print_header():
    """Print demo header"""
    print("\n" + "="*60)
    print("🚀 CRYPTOCURRENCY MARKET ANALYST - INTERACTIVE DEMO")
    print("="*60)
    print("Professional crypto market analysis powered by AI")
    print("Supports OpenAI GPT-5 and Claude Sonnet 4")
    print("📁 Results saved to: demo_output/ folder as .md files")

def print_menu():
    """Print main menu"""
    print("\n📋 MAIN MENU:")
    print("1. Analyze specific cryptocurrency")
    print("2. Get trading signals")  
    print("3. Portfolio analysis")
    print("4. Market overview")
    print("5. View saved analyses")
    print("0. Exit")

def get_crypto_input():
    """Get cryptocurrency choice from user"""
    print("\n💰 SELECT CRYPTOCURRENCY:")
    print("1. Bitcoin (BTC)")
    print("2. Ethereum (ETH)")
    print("3. Cardano (ADA)")
    print("4. Solana (SOL)")
    print("5. Binance Coin (BNB)")
    print("6. Custom (enter symbol)")
    
    choice = input("\nYour choice (1-6): ").strip()
    
    crypto_map = {
        "1": ("Bitcoin", "BTC"),
        "2": ("Ethereum", "ETH"), 
        "3": ("Cardano", "ADA"),
        "4": ("Solana", "SOL"),
        "5": ("Binance Coin", "BNB")
    }
    
    if choice in crypto_map:
        return crypto_map[choice]
    elif choice == "6":
        symbol = input("Enter crypto symbol (e.g., DOT, LINK): ").strip().upper()
        if symbol:
            return (symbol, symbol)
        return ("Bitcoin", "BTC")
    else:
        return ("Bitcoin", "BTC")

def get_timeframe():
    """Get analysis timeframe"""
    print("\n⏱️ SELECT TIMEFRAME:")
    print("1. Short-term (1-7 days)")
    print("2. Medium-term (1-4 weeks)")
    print("3. Long-term (1-6 months)")
    
    choice = input("Your choice (1-3): ").strip()
    
    timeframe_map = {
        "1": "short-term",
        "2": "medium-term", 
        "3": "long-term"
    }
    
    return timeframe_map.get(choice, "medium-term")

def get_analysis_type():
    """Get type of analysis"""
    print("\n📊 SELECT ANALYSIS TYPE:")
    print("1. Comprehensive (technical + fundamental)")
    print("2. Technical analysis only")
    print("3. Fundamental analysis only") 
    print("4. Trading signals")
    
    choice = input("Your choice (1-4): ").strip()
    
    type_map = {
        "1": "comprehensive analysis",
        "2": "technical analysis only",
        "3": "fundamental analysis only",
        "4": "trading signals and entry/exit points"
    }
    
    return type_map.get(choice, "comprehensive analysis")

def get_model_choice(analyst):
    """Get AI model choice"""
    models = analyst.get_available_models()
    
    if not models:
        print("❌ No AI models available! Check your API keys.")
        return None
        
    print(f"\n🤖 SELECT AI MODEL:")
    for i, model in enumerate(models, 1):
        print(f"{i}. {model}")
    
    try:
        choice = int(input(f"Your choice (1-{len(models)}): ").strip())
        if 1 <= choice <= len(models):
            return models[choice - 1]
    except ValueError:
        pass
    
    return models[0]  # Default to first model

def format_query(crypto_name, crypto_symbol, timeframe, analysis_type):
    """Format the complete query for AI"""
    return f"""
    Przeprowadź {analysis_type} dla {crypto_name} ({crypto_symbol}).
    
    Horyzont czasowy: {timeframe}
    
    Proszę o szczegółową analizę uwzględniającą:
    - Obecne trendy cenowe
    - Kluczowe poziomy wsparcia i oporu
    - Sentiment rynkowy
    - Ocenę ryzyka
    - Konkretne rekomendacje
    
    Zakończ analizę disclaimer o ryzyku inwestowania.
    """.strip()

def create_filename(crypto_symbol, analysis_type, timeframe):
    """Create filename for the analysis"""
    # Clean up strings for filename
    analysis_clean = analysis_type.replace(" ", "_").replace("/", "_")
    timestamp = int(time.time())
    
    return f"Analiza_{crypto_symbol}_{analysis_clean}_{timeframe}_{timestamp}.md"

def save_analysis_to_file(output_dir, filename, analysis_data):
    """Save analysis to markdown file"""
    
    # Create markdown header with metadata
    markdown_content = f"""# Analiza Kryptowaluty: {analysis_data['crypto_name']} ({analysis_data['crypto_symbol']})

## Informacje o Analizie

- **Data analizy:** {analysis_data['timestamp']}
- **Kryptowaluta:** {analysis_data['crypto_name']} ({analysis_data['crypto_symbol']})
- **Horyzont czasowy:** {analysis_data['timeframe']}
- **Typ analizy:** {analysis_data['analysis_type']}
- **Model AI:** {analysis_data['model']}
- **Czas przetwarzania:** {analysis_data['processing_time']:.1f} sekund
- **Status walidacji:** {"✅ Kompletna" if analysis_data['validation']['is_complete'] else "⚠️ Częściowa"}
- **Wygenerowano znaków:** {analysis_data['validation']['total_chars']:,}

---

{analysis_data['response']}

---

## Informacje Techniczne

- **ID odpowiedzi:** {analysis_data.get('response_id', 'N/A')}
- **Sekcje znalezione:** {analysis_data['validation']['successful_sections']}/{analysis_data['validation']['total_sections']}
- **Generator:** Cryptocurrency Market Analyst v1.0.0
- **Plik utworzony:** {time.strftime('%Y-%m-%d %H:%M:%S')}
"""
    
    file_path = output_dir / filename
    
    try:
        with open(file_path, "w", encoding="utf-8") as f:
            f.write(markdown_content)
        return file_path
    except Exception as e:
        print(f"❌ Error saving file: {str(e)}")
        return None

def list_saved_analyses(output_dir):
    """List all saved analysis files"""
    try:
        md_files = list(output_dir.glob("Analiza_*.md"))
        
        if not md_files:
            print("📂 No saved analyses found in demo_output/ folder")
            return
        
        print(f"\n📁 SAVED ANALYSES ({len(md_files)} files):")
        print("="*50)
        
        # Sort by modification time (newest first)
        md_files.sort(key=lambda x: x.stat().st_mtime, reverse=True)
        
        for i, file_path in enumerate(md_files[:10], 1):  # Show max 10 recent
            file_size = file_path.stat().st_size
            mod_time = time.strftime('%Y-%m-%d %H:%M', time.localtime(file_path.stat().st_mtime))
            
            print(f"{i:2d}. {file_path.name}")
            print(f"    📅 {mod_time} | 📊 {file_size:,} bytes")
        
        if len(md_files) > 10:
            print(f"    ... and {len(md_files) - 10} more files")
            
    except Exception as e:
        print(f"❌ Error listing files: {str(e)}")

def main():
    """Main demo function"""
    print_header()
    
    # Create output folder
    output_dir = create_demo_output_folder()
    print(f"✅ Output folder ready: {output_dir.absolute()}")
    
    # Initialize analyst
    print("\n🔧 Initializing Crypto Analyst...")
    analyst = CryptoAnalyst()
    
    if not analyst.openai_client and not analyst.anthropic_client:
        print("\n❌ CRITICAL ERROR: No API clients available!")
        print("Please check your .env file and API keys.")
        return
    
    while True:
        print_menu()
        choice = input("\nYour choice (0-5): ").strip()
        
        if choice == "0":
            print("\n👋 Thanks for using Crypto Analyst! Goodbye!")
            print(f"📁 Your analyses are saved in: {output_dir.absolute()}")
            break
            
        elif choice in ["1", "2", "3", "4"]:
            # Get user preferences
            crypto_name, crypto_symbol = get_crypto_input()
            timeframe = get_timeframe()
            
            if choice == "1":
                analysis_type = get_analysis_type()
            elif choice == "2":
                analysis_type = "trading signals with precise entry/exit points"
            elif choice == "3":
                analysis_type = "portfolio analysis and risk assessment"
            else:  # choice == "4"
                analysis_type = "general market overview and trends"
                crypto_name = "major cryptocurrencies (BTC, ETH, top altcoins)"
                crypto_symbol = "MARKET"
            
            model = get_model_choice(analyst)
            if not model:
                continue
                
            # Build query
            query = format_query(crypto_name, crypto_symbol, timeframe, analysis_type)
            
            # Display summary
            print(f"\n📋 ANALYSIS SUMMARY:")
            print(f"   Crypto: {crypto_name} ({crypto_symbol})")
            print(f"   Timeframe: {timeframe}")
            print(f"   Analysis: {analysis_type}")
            print(f"   AI Model: {model}")
            
            input("\nPress Enter to start analysis...")
            
            # Perform analysis
            print(f"\n🔄 Starting {analysis_type.lower()} for {crypto_name}...")
            print("This may take 30-60 seconds...")
            
            start_time = time.time()
            
            if "gpt" in model.lower():
                result = analyst.analyze_crypto_openai(query, model)
            else:
                result = analyst.analyze_crypto_claude_simple(query)
            
            end_time = time.time()
            processing_time = end_time - start_time
            
            if result['success']:
                # Prepare analysis data
                analysis_data = {
                    'timestamp': time.strftime('%Y-%m-%d %H:%M:%S'),
                    'crypto_name': crypto_name,
                    'crypto_symbol': crypto_symbol,
                    'timeframe': timeframe,
                    'analysis_type': analysis_type,
                    'model': result['model_used'],
                    'processing_time': processing_time,
                    'response': result['response'],
                    'validation': result['validation'],
                    'response_id': result.get('response_id', 'unknown')
                }
                
                # Create filename and save
                filename = create_filename(crypto_symbol, analysis_type, timeframe)
                file_path = save_analysis_to_file(output_dir, filename, analysis_data)
                
                if file_path:
                    print(f"\n✅ Analysis completed successfully!")
                    print(f"📁 Saved to: {file_path.name}")
                    print(f"📊 File size: {file_path.stat().st_size:,} bytes")
                    print(f"⚡ Processing time: {processing_time:.1f} seconds")
                    
                    # Show validation summary
                    validation = result['validation']
                    print(f"🎯 Validation: {validation['successful_sections']}/{validation['total_sections']} sections complete")
                    
                else:
                    print("\n❌ Analysis completed but failed to save to file")
                    
            else:
                print(f"\n❌ Analysis failed: {result['error']}")
                
        elif choice == "5":
            list_saved_analyses(output_dir)
                
        else:
            print("❌ Invalid choice. Please try again.")
        
        # Pause before next iteration
        input("\nPress Enter to continue...")

if __name__ == "__main__":
    main()
