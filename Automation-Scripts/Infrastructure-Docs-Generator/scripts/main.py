"""
Infrastructure Documentation Generator
Script główny: Orchestracja całego procesu

Autor: Sebastian
Data: 2026-01-28
"""

import sys
import argparse
from pathlib import Path

# Import naszych modułów
from collect_configs import ConfigCollector
from generate_docs import DocumentationGenerator


def main():
    """Główna funkcja - orchestracja procesu"""
    
    # Parser argumentów wiersza poleceń
    parser = argparse.ArgumentParser(
        description='Infrastructure Documentation Generator - Automatyczne generowanie dokumentacji sieci'
    )
    
    parser.add_argument(
        '--collect-only',
        action='store_true',
        help='Tylko zbieranie konfiguracji (bez generowania dokumentacji)'
    )
    
    parser.add_argument(
        '--generate-only',
        action='store_true',
        help='Tylko generowanie dokumentacji (z istniejących plików)'
    )
    
    parser.add_argument(
        '--test',
        action='store_true',
        help='Tryb testowy (tylko sprawdzenie konfiguracji)'
    )
    
    parser.add_argument(
        '--device',
        type=str,
        help='Testuj tylko konkretne urządzenie (IP lub hostname)'
    )
    
    args = parser.parse_args()
    
    # Banner
    print("="*70)
    print("   Infrastructure Documentation Generator")
    print("   Automatyczna dokumentacja infrastruktury sieciowej")
    print("="*70)
    print()
    
    # Sprawdź czy pliki konfiguracyjne istnieją
    if not Path('config/devices.yml').exists():
        print("✗ BŁĄD: Brak pliku config/devices.yml")
        print("  Utwórz plik i dodaj listę urządzeń sieciowych")
        sys.exit(1)
    
    if not Path('config/settings.yml').exists():
        print("✗ BŁĄD: Brak pliku config/settings.yml")
        print("  Utwórz plik z ustawieniami projektu")
        sys.exit(1)
    
    if not Path('.env').exists():
        print("⚠ OSTRZEŻENIE: Brak pliku .env")
        print("  Skopiuj .env.example i uzupełnij dane")
        print()
    
    try:
        # TRYB TESTOWY
        if args.test:
            print("🧪 Tryb testowy - sprawdzanie konfiguracji...\n")
            
            collector = ConfigCollector()
            print(f"✓ Załadowano {len(collector.devices)} urządzeń")
            print(f"✓ Konfiguracja: {collector.config['openai']['model']}")
            print(f"✓ Output dir: {collector.config['output']['documentation_dir']}")
            print("\n✓ Konfiguracja poprawna!")
            return
        
        # TYLKO ZBIERANIE
        if args.collect_only:
            print("📥 Uruchamiam zbieranie konfiguracji...\n")
            collector = ConfigCollector()
            success = collector.collect_all()
            
            if not success:
                sys.exit(1)
            return
        
        # TYLKO GENEROWANIE
        if args.generate_only:
            print("📝 Uruchamiam generowanie dokumentacji...\n")
            generator = DocumentationGenerator()
            success = generator.generate_all()
            
            if not success:
                sys.exit(1)
            return
        
        # PEŁNY PROCES (domyślnie)
        print("🚀 Uruchamiam pełny proces dokumentacji...\n")
        
        # Krok 1: Zbieranie konfiguracji
        print("KROK 1/2: Zbieranie konfiguracji z urządzeń")
        print("-" * 70)
        collector = ConfigCollector()
        collect_success = collector.collect_all()
        
        if not collect_success:
            print("\n✗ Zbieranie konfiguracji zakończone z błędami")
            print("  Kontynuować generowanie dokumentacji? (t/n): ", end='')
            response = input().lower()
            
            if response != 't':
                print("\nPrzerwano.")
                sys.exit(1)
        
        print("\n")
        
        # Krok 2: Generowanie dokumentacji
        print("KROK 2/2: Generowanie dokumentacji AI")
        print("-" * 70)
        generator = DocumentationGenerator()
        generate_success = generator.generate_all()
        
        if not generate_success:
            print("\n✗ Generowanie dokumentacji zakończone z błędami")
            sys.exit(1)
        
        # Podsumowanie końcowe
        print("\n" + "="*70)
        print("✓ PROCES ZAKOŃCZONY POMYŚLNIE!")
        print("="*70)
        print(f"\n📁 Dokumentacja dostępna w: {generator.config['output']['documentation_dir']}")
        print(f"📁 Backup konfiguracji w: {collector.config['output']['backup_dir']}")
        print(f"📋 Logi w: {collector.config['output']['logs_dir']}")
        print()
        
    except KeyboardInterrupt:
        print("\n\n⚠ Przerwano przez użytkownika (Ctrl+C)")
        sys.exit(1)
    
    except Exception as e:
        print(f"\n✗ NIEOCZEKIWANY BŁĄD: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)


if __name__ == "__main__":
    main()
