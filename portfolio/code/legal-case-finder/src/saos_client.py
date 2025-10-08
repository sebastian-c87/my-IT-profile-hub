"""
Klient API SAOS (System Analizy Orzeczeń Sądowych)
Wyszukiwanie orzeczeń sądowych z oficjalnego źródła
"""
import logging
import requests
from typing import List, Dict, Any, Optional

class SAOSClient:
    """Klient do wyszukiwania orzeczeń w systemie SAOS"""
    
    # NAPRAWIONE: Właściwy endpoint zgodnie z dokumentacją
    BASE_URL = "https://www.saos.org.pl/api/search"
    
    def __init__(self):
        self.logger = logging.getLogger(__name__)
        self.session = requests.Session()
        self.session.headers.update({
            'User-Agent': 'LegalCaseFinder/1.0',
            'Accept': 'application/json'
        })
    
    def search_judgments(
        self,
        query: str,
        page_size: int = 5,
        court_type: Optional[str] = None
    ) -> List[Dict[str, Any]]:
        """
        Wyszukaj orzeczenia w SAOS
        
        Args:
            query: Zapytanie wyszukiwania (słowa kluczowe)
            page_size: Liczba wyników (max 100)
            court_type: Typ sądu (COMMON, SUPREME, ADMINISTRATIVE)
        
        Returns:
            Lista orzeczeń
        """
        try:
            # NAPRAWIONE: Właściwe parametry zgodnie z dokumentacją SAOS
            params = {
                'all': query,  # Wyszukiwanie w całym tekście
                'pageSize': min(page_size, 100),  # Max 100
                'pageNumber': 0,
                'sortingField': 'JUDGMENT_DATE',
                'sortingDirection': 'DESC'
            }
            
            # Dodaj typ sądu jeśli podany
            if court_type:
                params['courtType'] = court_type
            
            # NAPRAWIONE: Właściwy endpoint /judgments
            url = f"{self.BASE_URL}/judgments"
            
            self.logger.info(f"Wysyłam zapytanie do SAOS: {url}")
            self.logger.info(f"Parametry: {params}")
            
            response = self.session.get(url, params=params, timeout=15)
            
            self.logger.info(f"Status odpowiedzi SAOS: {response.status_code}")
            
            if response.status_code == 200:
                data = response.json()
                
                if 'items' in data and data['items']:
                    self.logger.info(f"Znaleziono {len(data['items'])} orzeczeń dla: {query}")
                    return self._parse_judgments(data['items'])
                else:
                    self.logger.warning(f"Brak wyników dla: {query}")
                    return []
            else:
                self.logger.error(f"Błąd API SAOS: {response.status_code}")
                self.logger.error(f"Odpowiedź: {response.text[:500]}")
                return []
                
        except requests.exceptions.RequestException as e:
            self.logger.error(f"Błąd połączenia z SAOS: {str(e)}")
            return []
        except Exception as e:
            self.logger.error(f"Nieoczekiwany błąd SAOS: {str(e)}", exc_info=True)
            return []
    
    def _parse_judgments(self, items: List[Dict]) -> List[Dict[str, Any]]:
        """Parsuj orzeczenia z odpowiedzi API"""
        judgments = []
        
        for item in items:
            try:
                judgment = {
                    'case_number': self._get_case_number(item),
                    'date': item.get('judgmentDate', 'N/A'),
                    'court_name': self._get_court_name(item),
                    'judges': self._get_judges(item),
                    'text_preview': self._get_text_preview(item),
                    'url': self._get_judgment_url(item)
                }
                judgments.append(judgment)
            except Exception as e:
                self.logger.warning(f"Błąd parsowania orzeczenia: {str(e)}")
                continue
        
        return judgments
    
    def _get_case_number(self, item: Dict) -> str:
        """Pobierz sygnaturę sprawy"""
        try:
            if 'courtCases' in item and item['courtCases']:
                return item['courtCases'][0].get('caseNumber', 'N/A')
        except:
            pass
        return 'N/A'
    
    def _get_court_name(self, item: Dict) -> str:
        """Pobierz nazwę sądu"""
        try:
            # Sprawdź różne możliwe lokalizacje nazwy sądu
            if 'courtName' in item:
                return item['courtName']
            elif 'division' in item and 'court' in item['division']:
                return item['division']['court'].get('name', 'N/A')
            elif 'court' in item:
                return item['court'].get('name', 'N/A')
        except:
            pass
        return 'N/A'
    
    def _get_judges(self, item: Dict) -> str:
        """Pobierz listę sędziów"""
        try:
            if 'judges' in item and item['judges']:
                names = [judge.get('name', '') for judge in item['judges']]
                return ', '.join(filter(None, names)) or 'N/A'
        except:
            pass
        return 'N/A'
    
    def _get_text_preview(self, item: Dict) -> str:
        """Pobierz fragment treści orzeczenia"""
        try:
            # Sprawdź różne możliwe nazwy pól z tekstem
            text = item.get('textContent') or item.get('content') or item.get('text') or ''
            if text:
                # Usuń zbędne białe znaki
                text = ' '.join(text.split())
                return text[:300] + '...' if len(text) > 300 else text
        except:
            pass
        return 'Brak podglądu treści'
    
    def _get_judgment_url(self, item: Dict) -> str:
        """Pobierz URL do pełnego orzeczenia"""
        try:
            judgment_id = item.get('id')
            if judgment_id:
                return f"https://www.saos.org.pl/judgments/{judgment_id}"
        except:
            pass
        return 'N/A'
    
    def format_judgment_display(self, judgment: Dict[str, Any]) -> str:
        """Formatuj orzeczenie do wyświetlenia"""
        # Skróć długie pola do 60 znaków dla lepszego wyświetlania
        case_num = str(judgment['case_number'])[:58]
        date = str(judgment['date'])[:58]
        court = str(judgment['court_name'])[:58]
        judges = str(judgment['judges'])[:58]
        preview = str(judgment['text_preview'])[:250]
        url = str(judgment['url'])[:63]
        
        return f"""
╔══════════════════════════════════════════════════════════════════════╗
║ ORZECZENIE SĄDOWE                                                    ║
╠══════════════════════════════════════════════════════════════════════╣
║ Sygnatura:  {case_num:<58} ║
║ Data:       {date:<58} ║
║ Sąd:        {court:<58} ║
║ Sędziowie:  {judges:<58} ║
╠══════════════════════════════════════════════════════════════════════╣
║ Fragment treści:                                                     ║
║ {preview:<68} ║
╠══════════════════════════════════════════════════════════════════════╣
║ Link: {url:<63} ║
╚══════════════════════════════════════════════════════════════════════╝
"""
