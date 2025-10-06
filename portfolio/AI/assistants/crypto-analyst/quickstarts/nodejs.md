# Node.js Client

> *JavaScript* z wykorzystaniem globalnie zainstalowanego dependency management. *Wywołanie API* do korzystania z promptu dla **asystenta AI do analiz kryptowalut**

**Instalacja:** cd api-clients/nodejs && node client.js

**Opis Asystenta:** Inteligentny analityk rynku kryptowalut wykorzystujący GPT-5 i Claude 3.5 do generowania precyzyjnych analiz inwestycyjnych. Oferuje real-time market intelligence, on-chain analytics i zaawansowane zarządzanie ryzykiem dla traderów i inwestorów.

**Przykład użycia:**
```js
const { OpenAI } = require('openai');
const fs = require('fs');

const client = new OpenAI();
const systemPrompt = fs.readFileSync('./system.md', 'utf8');

async function analyzeEthereum() {
    const response = await client.responses.create({
        model: "gpt-5-nano",
        input: systemPrompt + "\n\nAnaliza Ethereum (ETH) - perspektywa średnioterminowa z uwzględnieniem nadchodzących update'ów sieci.",
        reasoning: {"effort": "medium"},
        text: {"verbosity": "medium"},
        tools: [{"type": "web_search"}],
        max_output_tokens: 16000
    });
    
    console.log(response.output_text);
}

analyzeEthereum();
```
**Funkcje:** analyzeCryptoOpenAI (analiza przez GPT-5), analyzeCryptoClaude (analiza przez Claude), compareProviders (porównanie AI models). Oczekiwane efekty: profesjonalne raporty analityczne z wykresami trendów, poziomami S/R, sygnałami entry/exit i kompleksowym disclaimer prawnym.
