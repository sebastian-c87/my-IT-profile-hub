#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Utils Module

Funkcje pomocnicze używane przez inne moduły:
- Ładowanie konfiguracji (YAML, ENV)
- Formatowanie output
- Kolorowanie CLI
- Parsowanie dat
- Logger setup
"""

import os
import yaml
from pathlib import Path
from typing import Any, Dict, Optional
from datetime import datetime
from colorama import Fore, Style, init as colorama_init
from dotenv import load_dotenv
import logging
from logging.handlers import RotatingFileHandler


# Inicjalizuj colorama
colorama_init(autoreset=True)


class ConfigLoader:
    """Klasa do ładowania konfiguracji"""
    
    def __init__(self, project_root: Optional[Path] = None):
        """
        Inicjalizacja
        
        Args:
            project_root: Ścieżka do głównego folderu projektu
        """
        if project_root is None:
            # Znajdź project root (folder scripts jest w głównym)
            self.project_root = Path(__file__).parent.parent
        else:
            self.project_root = project_root
        
        # Załaduj .env
        env_file = self.project_root / ".env"
        if env_file.exists():
            load_dotenv(env_file)
    
    def load_yaml(self, relative_path: str) -> Dict[str, Any]:
        """
        Załaduj plik YAML
        
        Args:
            relative_path: Ścieżka względem project_root
        
        Returns:
            Dictionary z konfiguracją
        """
        file_path = self.project_root / relative_path
        
        if not file_path.exists():
            raise FileNotFoundError(f"Config file not found: {file_path}")
        
        with open(file_path, 'r', encoding='utf-8') as f:
            config = yaml.safe_load(f)
        
        # Zastąp zmienne środowiskowe
        config = self._substitute_env_vars(config)
        
        return config
    
    def _substitute_env_vars(self, obj: Any) -> Any:
        """
        Rekurencyjnie zastąp ${VAR_NAME} zmiennymi z .env
        
        Args:
            obj: Dictionary, list, lub string
        
        Returns:
            Object z podstawionymi wartościami
        """
        if isinstance(obj, dict):
            return {k: self._substitute_env_vars(v) for k, v in obj.items()}
        elif isinstance(obj, list):
            return [self._substitute_env_vars(item) for item in obj]
        elif isinstance(obj, str):
            # Sprawdź czy to ${VAR_NAME}
            if obj.startswith('${') and obj.endswith('}'):
                var_name = obj[2:-1]
                return os.getenv(var_name, obj)  # Zwróć wartość lub original
            return obj
        else:
            return obj
    
    def get_env(self, key: str, default: Any = None) -> Any:
        """
        Pobierz zmienną środowiskową z konwersją typu
        
        Args:
            key: Nazwa zmiennej
            default: Wartość domyślna
        
        Returns:
            Wartość zmiennej
        """
        value = os.getenv(key)
        
        if value is None:
            return default
        
        # Konwersja boolean
        if isinstance(default, bool):
            return value.lower() in ('true', 'yes', '1', 'on')
        
        # Konwersja int
        if isinstance(default, int):
            try:
                return int(value)
            except ValueError:
                return default
        
        # Konwersja float
        if isinstance(default, float):
            try:
                return float(value)
            except ValueError:
                return default
        
        # String
        return value


class ColorPrinter:
    """Klasa do kolorowanego outputu w CLI"""
    
    @staticmethod
    def success(message: str) -> None:
        """Print success message (green)"""
        print(f"{Fore.GREEN}✓ {message}{Style.RESET_ALL}")
    
    @staticmethod
    def error(message: str) -> None:
        """Print error message (red)"""
        print(f"{Fore.RED}✗ {message}{Style.RESET_ALL}")
    
    @staticmethod
    def warning(message: str) -> None:
        """Print warning message (yellow)"""
        print(f"{Fore.YELLOW}⚠ {message}{Style.RESET_ALL}")
    
    @staticmethod
    def info(message: str) -> None:
        """Print info message (blue)"""
        print(f"{Fore.BLUE}ℹ {message}{Style.RESET_ALL}")
    
    @staticmethod
    def header(message: str) -> None:
        """Print header (cyan, bold)"""
        print(f"\n{Fore.CYAN}{Style.BRIGHT}{message}{Style.RESET_ALL}")
        print(f"{Fore.CYAN}{'=' * len(message)}{Style.RESET_ALL}\n")
    
    @staticmethod
    def status_line(
        hostname: str,
        days: int,
        status: str
    ) -> None:
        """
        Print status line dla certyfikatu
        
        Args:
            hostname: Hostname
            days: Dni do wygaśnięcia
            status: Status (OK, WARNING, CRITICAL, EXPIRED)
        """
        # Wybierz kolor i symbol
        if status == "OK":
            color = Fore.GREEN
            symbol = "✓"
        elif status == "WARNING":
            color = Fore.YELLOW
            symbol = "⚠"
        elif status == "CRITICAL":
            color = Fore.RED
            symbol = "⚠"
        elif status == "EXPIRED":
            color = Fore.RED
            symbol = "✗"
        else:
            color = Fore.WHITE
            symbol = "?"
        
        # Format
        print(
            f"{color}{symbol} {hostname:30} "
            f"{days:>4} days    "
            f"{status}{Style.RESET_ALL}"
        )


class DateFormatter:
    """Klasa do formatowania dat"""
    
    @staticmethod
    def format_datetime(dt: datetime, format: str = "%Y-%m-%d %H:%M:%S") -> str:
        """
        Formatuj datetime do string
        
        Args:
            dt: datetime object
            format: Format string
        
        Returns:
            Formatted string
        """
        return dt.strftime(format)
    
    @staticmethod
    def format_date(dt: datetime) -> str:
        """Format tylko data (bez czasu)"""
        return dt.strftime("%Y-%m-%d")
    
    @staticmethod
    def format_relative(days: int) -> str:
        """
        Format względny (np. "in 30 days", "2 days ago")
        
        Args:
            days: Liczba dni (dodatnia = przyszłość, ujemna = przeszłość)
        
        Returns:
            Relative string
        """
        if days > 0:
            if days == 1:
                return "tomorrow"
            return f"in {days} days"
        elif days < 0:
            abs_days = abs(days)
            if abs_days == 1:
                return "yesterday"
            return f"{abs_days} days ago"
        else:
            return "today"
    
    @staticmethod
    def days_to_color(days: int) -> str:
        """
        Zwróć kolor dla liczby dni
        
        Args:
            days: Dni do wygaśnięcia
        
        Returns:
            Colorama color code
        """
        if days < 0:
            return Fore.RED  # Expired
        elif days <= 7:
            return Fore.RED  # Critical
        elif days <= 30:
            return Fore.YELLOW  # Warning
        else:
            return Fore.GREEN  # OK


class LoggerSetup:
    """Klasa do konfiguracji loggera"""
    
    @staticmethod
    def setup_logger(
        name: str,
        log_file: Optional[str] = None,
        level: str = "INFO",
        console: bool = True,
        max_size_mb: int = 10,
        backup_count: int = 5
    ) -> logging.Logger:
        """
        Skonfiguruj logger
    
        Args:
            name: Nazwa loggera
            log_file: Ścieżka do pliku logów
            level: Log level (DEBUG, INFO, WARNING, ERROR, CRITICAL)
            console: Czy logować też do konsoli
            max_size_mb: Max rozmiar pliku logów (MB)
            backup_count: Ile backupów zachować
    
        Returns:
            Configured logger
        """
        # FIX: Konwertuj do int jeśli przyszło jako string z YAML
        if isinstance(max_size_mb, str):
            max_size_mb = int(max_size_mb)
        if isinstance(backup_count, str):
            backup_count = int(backup_count)
    
        logger = logging.getLogger(name)
        logger.setLevel(getattr(logging, level.upper()))
    
        # Clear existing handlers
        logger.handlers.clear()
    
        # Format
        formatter = logging.Formatter(
            '[%(asctime)s] [%(levelname)s] [%(name)s] %(message)s',
            datefmt='%Y-%m-%d %H:%M:%S'
        )
    
        # File handler (z rotacją)
        if log_file:
            # Utwórz folder jeśli nie istnieje
            log_path = Path(log_file)
            log_path.parent.mkdir(parents=True, exist_ok=True)
        
            file_handler = RotatingFileHandler(
                log_file,
                maxBytes=max_size_mb * 1024 * 1024,
                backupCount=backup_count,
                encoding='utf-8'
            )

            file_handler.setFormatter(formatter)
            logger.addHandler(file_handler)
        
        # Console handler
        if console:
            console_handler = logging.StreamHandler()
            console_handler.setFormatter(formatter)
            logger.addHandler(console_handler)
        
        return logger


class FileUtils:
    """Utilities dla operacji na plikach"""
    
    @staticmethod
    def ensure_directory(path: Path) -> None:
        """
        Upewnij się że katalog istnieje
        
        Args:
            path: Ścieżka do katalogu
        """
        path.mkdir(parents=True, exist_ok=True)
    
    @staticmethod
    def get_project_root() -> Path:
        """
        Znajdź główny folder projektu
        
        Returns:
            Path do project root
        """
        # scripts jest w głównym folderze
        return Path(__file__).parent.parent
    
    @staticmethod
    def read_file(path: Path) -> str:
        """
        Przeczytaj plik tekstowy
        
        Args:
            path: Ścieżka do pliku
        
        Returns:
            Zawartość pliku
        """
        with open(path, 'r', encoding='utf-8') as f:
            return f.read()
    
    @staticmethod
    def write_file(path: Path, content: str) -> None:
        """
        Zapisz plik tekstowy
        
        Args:
            path: Ścieżka do pliku
            content: Treść do zapisania
        """
        # Utwórz folder jeśli nie istnieje
        path.parent.mkdir(parents=True, exist_ok=True)
        
        with open(path, 'w', encoding='utf-8') as f:
            f.write(content)


# Przykład użycia
if __name__ == "__main__":
    # Config loader
    print("=== Config Loader ===")
    config_loader = ConfigLoader()
    
    try:
        domains_config = config_loader.load_yaml("config/domains.yml")
        print(f"Loaded {len(domains_config)} domain groups")
    except FileNotFoundError as e:
        print(f"Error: {e}")
    
    # Color printer
    print("\n=== Color Printer ===")
    printer = ColorPrinter()
    
    printer.header("Certificate Status Report")
    printer.success("Certificate is valid")
    printer.warning("Certificate expires soon")
    printer.error("Certificate has expired")
    printer.info("Checking certificate...")
    
    print("\nStatus lines:")
    printer.status_line("google.com:443", 89, "OK")
    printer.status_line("test.local:443", 12, "WARNING")
    printer.status_line("old.local:443", -5, "EXPIRED")
    
    # Date formatter
    print("\n=== Date Formatter ===")
    formatter = DateFormatter()
    
    now = datetime.now()
    print(f"Now: {formatter.format_datetime(now)}")
    print(f"Date only: {formatter.format_date(now)}")
    print(f"30 days: {formatter.format_relative(30)}")
    print(f"-5 days: {formatter.format_relative(-5)}")
    
    # Logger
    print("\n=== Logger Setup ===")
    logger = LoggerSetup.setup_logger(
        name="test_logger",
        log_file="output/logs/test.log",
        level="INFO",
        console=True
    )
    
    logger.info("This is an info message")
    logger.warning("This is a warning")
    logger.error("This is an error")
    
    print("\nLog file created: output/logs/test.log")
