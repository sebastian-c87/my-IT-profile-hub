# Anthropic Claude Integration

> Konfiguracja Claude API dla crypto analysis. 
### Uzyskanie Klucza API
1. Idź na [console.anthropic.com](https://console.anthropic.com)
2. Zarejestruj się / zaloguj
3. Navigate to **API Keys**
4. Kliknij **Create Key**
5. Skopiuj klucz (zaczyna się od `sk-ant-`)

**Instalacja:** export ANTHROPIC_API_KEY="sk-ant-your-key-here"

**Opis Asystenta:** Claude 3.5 Haiku/Sonnet zoptymalizowany do zaawansowanych analiz kryptowalut z emphasis na risk management i portfolio optimization. Oferuje alternatywną perspektywę analityczną do GPT-5 z focus na conservative approach i comprehensive disclaimers.

**Przykład użycia:**
```python
import anthropic

client = anthropic.Anthropic()

message = client.messages.create(
    model="claude-4.0-sonnet",
    max_tokens=16000,
    system=open("system.md", "r").read(),
    messages=[
        {
            "role": "user",
            "content": "Przeprowadź conservative analysis dla Polkadot (DOT) z uwzględnieniem ecosystem development, tokenomics i long-term sustainability projektów parachain."
        }
    ]
)

print(message.content[0].text)

```

**Funkcje:** Claude 3.5 Haiku (cost-effective analysis), Claude 3.5 Sonnet (advanced reasoning), Batch processing (multiple assets), Conservative approach (risk-focused). Oczekiwane efekty: balanced market perspective, detailed risk assessment, conservative trading recommendations z emphasis na capital preservation i sustainable growth strategies.
