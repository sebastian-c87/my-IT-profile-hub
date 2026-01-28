"""
Infrastructure Documentation Generator
Script: Generowanie dokumentacji z użyciem AI (GPT-5-nano)

Autor: Sebastian
Data: 2026-01-28
"""

import os
import sys
import yaml
import logging
from datetime import datetime
from pathlib import Path
from dotenv import load_dotenv
from openai import OpenAI
from typing import List, Dict, Tuple
from jinja2 import Template

# Załaduj zmienne środowiskowe
load_dotenv()


class DocumentationGenerator:
    """Klasa do generowania dokumentacji z użyciem AI"""
    
    def __init__(self, config_path: str = "config/settings.yml"):
        """
        Inicjalizacja Generatora
        
        Args:
            config_path: Ścieżka do pliku settings.yml
        """
        self.config = self._load_config(config_path)
        self._setup_logging()
        self._setup_directories()
        self._setup_openai()
        
        self.successful_generations = []
        self.failed_generations = []
    
    def _load_config(self, path: str) -> dict:
        """Ładowanie ustawień z settings.yml"""
        try:
            with open(path, 'r', encoding='utf-8') as f:
                content = f.read()
                for key, value in os.environ.items():
                    content = content.replace(f'${{{key}}}', value)
                return yaml.safe_load(content)
        except Exception as e:
            print(f"BŁĄD: Nie można załadować {path}: {e}")
            sys.exit(1)
    
    def _setup_logging(self):
        """Konfiguracja logowania"""
        log_config = self.config.get('logging', {})
        log_level = getattr(logging, log_config.get('level', 'INFO'))
        
        log_format = log_config.get('format', '[%(asctime)s] [%(levelname)s] %(message)s')
        date_format = log_config.get('date_format', '%Y-%m-%d %H:%M:%S')
        
        self.logger = logging.getLogger('DocumentationGenerator')
        self.logger.setLevel(log_level)
        
        if log_config.get('to_console', True):
            console_handler = logging.StreamHandler()
            console_handler.setFormatter(logging.Formatter(log_format, date_format))
            self.logger.addHandler(console_handler)
        
        if log_config.get('to_file', True):
            log_dir = Path(self.config['output']['logs_dir'])
            log_dir.mkdir(parents=True, exist_ok=True)
            log_file = log_dir / 'generator.log'
            
            file_handler = logging.FileHandler(log_file, encoding='utf-8')
            file_handler.setFormatter(logging.Formatter(log_format, date_format))
            self.logger.addHandler(file_handler)
    
    def _setup_directories(self):
        """Tworzenie wymaganych folderów"""
        docs_dir = Path(self.config['output']['documentation_dir'])
        docs_dir.mkdir(parents=True, exist_ok=True)
    
    def _setup_openai(self):
        """Konfiguracja klienta OpenAI"""
        api_key = os.getenv('OPENAI_API_KEY')
        
        if not api_key:
            self.logger.error("BŁĄD: Brak OPENAI_API_KEY w pliku .env")
            sys.exit(1)
        
        self.openai_client = OpenAI(api_key=api_key)
    
    def _get_config_files(self) -> List[Path]:
        """Pobieranie listy plików konfiguracyjnych z folderu backup"""
        backup_dir = Path(self.config['output']['backup_dir'])
        
        if not backup_dir.exists():
            self.logger.warning(f"Folder backup nie istnieje: {backup_dir}")
            return []
        
        # Znajdź wszystkie pliki .txt
        config_files = list(backup_dir.glob('*.txt'))
        
        # Sortuj po dacie (najnowsze pierwsze)
        config_files.sort(key=lambda x: x.stat().st_mtime, reverse=True)
        
        return config_files
    
    def _extract_hostname_from_file(self, filepath: Path) -> str:
        """Wyciąganie hostname z nazwy pliku"""
        # Format: {hostname}_{date}_{time}.txt
        filename = filepath.stem
        parts = filename.split('_')
        
        if len(parts) >= 1:
            return parts[0]
        return filename
    
    def _generate_prompt(self, config_content: str, hostname: str) -> str:
        """
        Generowanie promptu dla AI
        
        Args:
            config_content: Zawartość pliku konfiguracyjnego
            hostname: Nazwa urządzenia
            
        Returns:
            Prompt dla GPT-5-nano
        """
        sections = self.config['documentation']['sections']
        
        prompt = f"""Przeanalizuj poniższą konfigurację urządzenia sieciowego i wygeneruj profesjonalną dokumentację w formacie Markdown.

Urządzenie: {hostname}

Wygeneruj dokumentację zawierającą następujące sekcje:

"""
        
        if sections.get('device_info', True):
            prompt += "1. INFORMACJE OGÓLNE - hostname, model urządzenia, wersja systemu operacyjnego\n"
        
        if sections.get('interfaces', True):
            prompt += "2. INTERFEJSY - lista interfejsów z adresami IP, opisami, statusem\n"
        
        if sections.get('vlans', True):
            prompt += "3. VLANy - skonfigurowane VLANy z nazwami i opisami\n"
        
        if sections.get('routing', True):
            prompt += "4. ROUTING - protokoły routingu (OSPF, EIGRP, BGP), static routes\n"
        
        if sections.get('acls', True):
            prompt += "5. ACCESS LISTY - skonfigurowane ACL z wyjaśnieniem reguł\n"
        
        if sections.get('security', True):
            prompt += "6. BEZPIECZEŃSTWO - SSH, AAA, password policy, security features\n"
        
        if sections.get('features', True):
            prompt += "7. DODATKOWE FUNKCJE - HSRP, VRRP, VTP, STP, inne protokoły\n"
        
        prompt += """
Dokumentacja powinna być:
- Czytelna i profesjonalna
- Używać tabel Markdown dla przejrzystości
- Zawierać tylko informacje rzeczywiście obecne w konfiguracji
- Nie wymyślać informacji których nie ma w config

Konfiguracja urządzenia:

"""
        prompt += config_content
        
        return prompt
    
    def _generate_single_doc(self, config_file: Path) -> Tuple[bool, str, str]:
        """
        Generowanie dokumentacji dla pojedynczego urządzenia
        
        Args:
            config_file: Ścieżka do pliku konfiguracyjnego
            
        Returns:
            Tuple (success, hostname, message)
        """
        hostname = self._extract_hostname_from_file(config_file)
        
        self.logger.info(f"Generowanie dokumentacji dla: {hostname}...")
        
        try:
            # Odczytaj plik konfiguracyjny
            with open(config_file, 'r', encoding='utf-8') as f:
                config_content = f.read()
            
            # Wygeneruj prompt
            prompt = self._generate_prompt(config_content, hostname)
            
            # Wywołaj API OpenAI (GPT-5-nano z Responses API)
            self.logger.info(f"Wysyłanie zapytania do GPT-5-nano...")
            
            openai_config = self.config['openai']
            
            response = self.openai_client.responses.create(
                model=openai_config.get('model', 'gpt-5-nano'),
                reasoning={
                    "effort": openai_config['reasoning'].get('effort', 'minimal')
                },
                text={
                    "verbosity": openai_config['text'].get('verbosity', 'medium')
                },
                input=prompt
            )
            
            # Pobierz wygenerowaną dokumentację
            documentation = response.output_text
            
            # Zapisz dokumentację do pliku Markdown
            docs_dir = Path(self.config['output']['documentation_dir'])
            
            filename_template = self.config['documentation'].get('filename_format', '{hostname}.md')
            filename = filename_template.format(
                hostname=hostname,
                date=datetime.now().strftime('%Y-%m-%d')
            )
            
            output_file = docs_dir / filename
            
            with open(output_file, 'w', encoding='utf-8') as f:
                f.write(f"# Dokumentacja: {hostname}\n\n")
                f.write(f"**Data wygenerowania:** {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n\n")
                f.write("---\n\n")
                f.write(documentation)
            
            self.logger.info(f"✓ Sukces: {hostname} - zapisano do {filename}")
            return (True, hostname, str(output_file))
            
        except Exception as e:
            error_msg = f"✗ Błąd: {hostname} - {str(e)}"
            self.logger.error(error_msg)
            return (False, hostname, error_msg)
    
    def generate_all(self) -> bool:
        """
        Generowanie dokumentacji dla wszystkich urządzeń
        
        Returns:
            True jeśli przynajmniej jedno urządzenie się powiodło
        """
        # Pobierz pliki konfiguracyjne
        config_files = self._get_config_files()
        
        if not config_files:
            self.logger.warning("Brak plików konfiguracyjnych do przetworzenia")
            self.logger.warning("Uruchom najpierw: python scripts/collect_configs.py")
            return False
        
        # Grupuj pliki po hostname (bierz tylko najnowsze)
        unique_devices = {}
        for config_file in config_files:
            hostname = self._extract_hostname_from_file(config_file)
            if hostname not in unique_devices:
                unique_devices[hostname] = config_file
        
        self.logger.info(f"Rozpoczynam generowanie dokumentacji dla {len(unique_devices)} urządzeń...")
        
        # Generuj dokumentację
        for hostname, config_file in unique_devices.items():
            success, host, message = self._generate_single_doc(config_file)
            
            if success:
                self.successful_generations.append((host, message))
            else:
                self.failed_generations.append((host, message))
        
        # Wygeneruj README.md z przeglądem (jeśli włączone)
        if self.config['documentation'].get('generate_overview', True):
            self._generate_overview()
        
        # Podsumowanie
        self.logger.info("\n" + "="*70)
        self.logger.info("PODSUMOWANIE GENEROWANIA DOKUMENTACJI")
        self.logger.info("="*70)
        self.logger.info(f"Sukces: {len(self.successful_generations)} / {len(unique_devices)}")
        self.logger.info(f"Błędy: {len(self.failed_generations)} / {len(unique_devices)}")
        
        if self.failed_generations:
            self.logger.warning("\nUrządzenia z błędami:")
            for hostname, error in self.failed_generations:
                self.logger.warning(f"  - {hostname}")
        
        return len(self.successful_generations) > 0
    
    def _generate_overview(self):
        """Generowanie pliku README.md z przeglądem sieci"""
        self.logger.info("Generowanie przeglądu sieci (README.md)...")
        
        docs_dir = Path(self.config['output']['documentation_dir'])
        overview_file = docs_dir / self.config['documentation'].get('overview_filename', 'README.md')
        
        with open(overview_file, 'w', encoding='utf-8') as f:
            f.write("# Dokumentacja Infrastruktury Sieciowej\n\n")
            f.write(f"**Data wygenerowania:** {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n\n")
            f.write("---\n\n")
            f.write("## Przegląd Urządzeń\n\n")
            
            if self.successful_generations:
                f.write("| Urządzenie | Dokumentacja | Status |\n")
                f.write("|------------|--------------|--------|\n")
                
                for hostname, filepath in self.successful_generations:
                    filename = Path(filepath).name
                    f.write(f"| {hostname} | [{filename}](./{filename}) | ✓ OK |\n")
            
            if self.failed_generations:
                f.write("\n### Urządzenia z błędami\n\n")
                for hostname, error in self.failed_generations:
                    f.write(f"- **{hostname}**: Błąd generowania dokumentacji\n")
            
            f.write("\n---\n\n")
            f.write("*Dokumentacja wygenerowana automatycznie przez Infrastructure Documentation Generator*\n")
        
        self.logger.info(f"✓ Przegląd zapisany: {overview_file}")


def main():
    """Główna funkcja skryptu"""
    print("="*70)
    print("Infrastructure Documentation Generator - AI Documentation")
    print("="*70)
    print()
    
    # Utwórz generator
    generator = DocumentationGenerator()
    
    # Generuj dokumentację
    success = generator.generate_all()
    
    if success:
        print("\n✓ Generowanie dokumentacji zakończone pomyślnie!")
        print(f"Pliki zapisane w: {generator.config['output']['documentation_dir']}")
        sys.exit(0)
    else:
        print("\n✗ Generowanie dokumentacji zakończone z błędami")
        sys.exit(1)


if __name__ == "__main__":
    main()
