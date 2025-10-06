# Python Client

> Wywołanie API poprzez Python'a do korzystania z promptu do analizy kryptowalut. 

**Instalacja:** cd api-clients/python && pip install -r requirements.txt

**Opis Asystenta:** Zaawansowany AI asystent specjalizujący się w profesjonalnej analizie rynków kryptowalut. Dostarcza wielowymiarowe analizy łączące aspekty techniczne, fundamentalne i sentymentalne. Generuje konkretne sygnały handlowe z precyzyjnymi punktami wejścia, wyjścia i zarządzaniem ryzykiem.

**Przykład użycia:**
```python
import os
from openai import OpenAI

client = OpenAI()
system_prompt = open("./system.md", "r", encoding="utf-8").read()

resp = client.responses.create(
    model="gpt-5-nano",
    input=system_prompt + "\n\nPrzeprowadź kompleksową analizę Bitcoin (BTC) z uwzględnieniem obecnych trendów rynkowych, wskaźników technicznych i czynników fundamentalnych.",
    reasoning={"effort": "medium"},
    text={"verbosity": "medium"},
    tools=[{"type": "web_search"}],
    max_output_tokens=16000
)

print(resp.output_text)
```
**Funkcje:** analyze_crypto (kompleksowa analiza), get_trading_signals (sygnały handlowe), technical_analysis (wskaźniki techniczne), risk_assessment (ocena ryzyka portfela). Oczekiwane efekty: strukturyzowane raporty z Executive Summary, analizą techniczną, fundamentalną, oceną ryzyka i konkretnymi rekomendacjami.
