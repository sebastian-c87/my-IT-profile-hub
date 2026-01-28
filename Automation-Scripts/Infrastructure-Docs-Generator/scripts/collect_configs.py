"""
Infrastructure Documentation Generator
Script: Zbieranie konfiguracji z urządzeń sieciowych

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
from netmiko import ConnectHandler
from netmiko.exceptions import NetmikoTimeoutException, NetmikoAuthenticationException
from concurrent.futures import ThreadPoolExecutor, as_completed
from typing import List, Dict, Tuple

# Załaduj zmienne środowiskowe z .env
load_dotenv()


class ConfigCollector:
    """Klasa do zbierania konfiguracji z urządzeń sieciowych"""
    
    def __init__(self, config_path: str = "config/settings.yml", devices_path: str = "config/devices.yml"):
        """
        Inicjalizacja Collectora
        
        Args:
            config_path: Ścieżka do pliku settings.yml
            devices_path: Ścieżka do pliku devices.yml
        """
        self.config = self._load_config(config_path)
        self.devices = self._load_devices(devices_path)
        self._setup_logging()
        self._setup_directories()
        
        self.successful_collections = []
        self.failed_collections = []
    
    def _load_config(self, path: str) -> dict:
        """Ładowanie ustawień z settings.yml"""
        try:
            with open(path, 'r', encoding='utf-8') as f:
                # Zamień zmienne środowiskowe w YAML
                content = f.read()
                for key, value in os.environ.items():
                    content = content.replace(f'${{{key}}}', value)
                return yaml.safe_load(content)
        except Exception as e:
            print(f"BŁĄD: Nie można załadować {path}: {e}")
            sys.exit(1)
    
    def _load_devices(self, path: str) -> List[dict]:
        """Ładowanie listy urządzeń z devices.yml"""
        try:
            with open(path, 'r', encoding='utf-8') as f:
                content = f.read()
                # Zamień zmienne środowiskowe
                for key, value in os.environ.items():
                    content = content.replace(f'${{{key}}}', value)
                devices = yaml.safe_load(content)
                
                # Filtruj tylko włączone urządzenia
                return [d for d in devices if d.get('enabled', True)]
        except Exception as e:
            print(f"BŁĄD: Nie można załadować {path}: {e}")
            sys.exit(1)
    
    def _setup_logging(self):
        """Konfiguracja logowania"""
        log_config = self.config.get('logging', {})
        log_level = getattr(logging, log_config.get('level', 'INFO'))
        
        # Format logów
        log_format = log_config.get('format', '[%(asctime)s] [%(levelname)s] %(message)s')
        date_format = log_config.get('date_format', '%Y-%m-%d %H:%M:%S')
        
        # Konfiguruj logger
        self.logger = logging.getLogger('ConfigCollector')
        self.logger.setLevel(log_level)
        
        # Handler do konsoli
        if log_config.get('to_console', True):
            console_handler = logging.StreamHandler()
            console_handler.setFormatter(logging.Formatter(log_format, date_format))
            self.logger.addHandler(console_handler)
        
        # Handler do pliku
        if log_config.get('to_file', True):
            log_dir = Path(self.config['output']['logs_dir'])
            log_dir.mkdir(parents=True, exist_ok=True)
            log_file = log_dir / 'collector.log'
            
            file_handler = logging.FileHandler(log_file, encoding='utf-8')
            file_handler.setFormatter(logging.Formatter(log_format, date_format))
            self.logger.addHandler(file_handler)
    
    def _setup_directories(self):
        """Tworzenie wymaganych folderów"""
        backup_dir = Path(self.config['output']['backup_dir'])
        backup_dir.mkdir(parents=True, exist_ok=True)
        
        temp_dir = Path(self.config['output']['temp_dir'])
        temp_dir.mkdir(parents=True, exist_ok=True)
    
    def _collect_single_device(self, device: dict) -> Tuple[bool, str, str]:
        """
        Zbieranie konfiguracji z pojedynczego urządzenia
        
        Args:
            device: Słownik z danymi urządzenia
            
        Returns:
            Tuple (success, hostname, message)
        """
        hostname = device.get('hostname', 'Unknown')
        ip = device.get('ip', '')
        
        self.logger.info(f"Łączenie z {hostname} ({ip})...")
        
        try:
            # Przygotuj dane do połączenia Netmiko
            connection_params = {
                'device_type': device.get('device_type', 'cisco_ios'),
                'host': ip,
                'username': device.get('username'),
                'password': device.get('password'),
                'port': device.get('port', 22),
                'timeout': self.config['ssh'].get('timeout', 30),
            }
            
            # Dodaj enable password jeśli istnieje
            if device.get('secret'):
                connection_params['secret'] = device['secret']
            
            # Połącz się z urządzeniem
            connection = ConnectHandler(**connection_params)
            
            # Wejdź w tryb enable (jeśli wymagany)
            if device.get('secret'):
                connection.enable()
            
            # Pobierz running-config
            self.logger.info(f"Pobieranie konfiguracji z {hostname}...")
            
            if 'cisco_asa' in device['device_type']:
                config = connection.send_command('show running-config', read_timeout=90)
            elif 'juniper' in device['device_type']:
                config = connection.send_command('show configuration', read_timeout=90)
            else:
                config = connection.send_command('show running-config', read_timeout=90)
            
            # Rozłącz się
            connection.disconnect()
            
            # Zapisz konfigurację do pliku
            backup_dir = Path(self.config['output']['backup_dir'])
            timestamp = datetime.now().strftime('%Y-%m-%d_%H-%M-%S')
            
            filename_template = self.config['backup'].get('filename_format', '{hostname}_{date}_{time}.txt')
            filename = filename_template.format(
                hostname=hostname,
                date=datetime.now().strftime('%Y-%m-%d'),
                time=datetime.now().strftime('%H-%M-%S')
            )
            
            filepath = backup_dir / filename
            
            with open(filepath, 'w', encoding='utf-8') as f:
                f.write(f"# Konfiguracja urządzenia: {hostname}\n")
                f.write(f"# IP: {ip}\n")
                f.write(f"# Data pobrania: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
                f.write(f"# Device Type: {device.get('device_type')}\n")
                f.write("#" + "="*70 + "\n\n")
                f.write(config)
            
            self.logger.info(f"✓ Sukces: {hostname} - zapisano do {filename}")
            return (True, hostname, str(filepath))
            
        except NetmikoAuthenticationException:
            error_msg = f"✗ Błąd autentykacji: {hostname} - sprawdź username/password"
            self.logger.error(error_msg)
            return (False, hostname, error_msg)
            
        except NetmikoTimeoutException:
            error_msg = f"✗ Timeout: {hostname} - urządzenie niedostępne lub firewall blokuje"
            self.logger.error(error_msg)
            return (False, hostname, error_msg)
            
        except Exception as e:
            error_msg = f"✗ Błąd: {hostname} - {str(e)}"
            self.logger.error(error_msg)
            return (False, hostname, error_msg)
    
    def collect_all(self) -> bool:
        """
        Zbieranie konfiguracji ze wszystkich urządzeń
        
        Returns:
            True jeśli przynajmniej jedno urządzenie się powiodło
        """
        if not self.devices:
            self.logger.warning("Brak urządzeń do przetworzenia (sprawdź config/devices.yml)")
            return False
        
        self.logger.info(f"Rozpoczynam zbieranie konfiguracji z {len(self.devices)} urządzeń...")
        
        max_workers = self.config['ssh'].get('max_concurrent', 5)
        
        # Zbieraj równolegle (ThreadPoolExecutor)
        with ThreadPoolExecutor(max_workers=max_workers) as executor:
            futures = {executor.submit(self._collect_single_device, device): device 
                      for device in self.devices}
            
            for future in as_completed(futures):
                success, hostname, message = future.result()
                
                if success:
                    self.successful_collections.append((hostname, message))
                else:
                    self.failed_collections.append((hostname, message))
        
        # Podsumowanie
        self.logger.info("\n" + "="*70)
        self.logger.info("PODSUMOWANIE ZBIERANIA KONFIGURACJI")
        self.logger.info("="*70)
        self.logger.info(f"Sukces: {len(self.successful_collections)} / {len(self.devices)}")
        self.logger.info(f"Błędy: {len(self.failed_collections)} / {len(self.devices)}")
        
        if self.failed_collections:
            self.logger.warning("\nUrządzenia z błędami:")
            for hostname, error in self.failed_collections:
                self.logger.warning(f"  - {hostname}: {error}")
        
        return len(self.successful_collections) > 0


def main():
    """Główna funkcja skryptu"""
    print("="*70)
    print("Infrastructure Documentation Generator - Config Collector")
    print("="*70)
    print()
    
    # Utwórz collector
    collector = ConfigCollector()
    
    # Zbierz konfiguracje
    success = collector.collect_all()
    
    if success:
        print("\n✓ Zbieranie konfiguracji zakończone pomyślnie!")
        print(f"Pliki zapisane w: {collector.config['output']['backup_dir']}")
        sys.exit(0)
    else:
        print("\n✗ Zbieranie konfiguracji zakończone z błędami")
        sys.exit(1)


if __name__ == "__main__":
    main()
