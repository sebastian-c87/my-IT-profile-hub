/**
 * LLM Engineering Professor - Node.js Client
 */

import OpenAI from 'openai';
import Anthropic from '@anthropic-ai/sdk';
import dotenv from 'dotenv';
import fs from 'fs/promises';
import path from 'path';
import { fileURLToPath } from 'url';

// 1. USTAL ŚCIEŻKĘ DO client.js
const __filename = fileURLToPath(import.meta.url);
const __dirname = path.dirname(__filename);

console.log('🔧 DEBUG: __dirname =', __dirname);

// 2. ZAŁADUJ .env Z GŁÓWNEGO FOLDERU REPO
// Licząc od nodejs/client.js:
// nodejs -> api-clients -> professor-LLM-maker -> assistants -> AI -> portfolio -> my-it-profile-hub
const envPath = path.resolve(__dirname, '../../../../../../.env');

console.log('🔧 DEBUG: Próbuję załadować .env z:', envPath);

const result = dotenv.config({ path: envPath });

if (result.error) {
    console.error('❌ Błąd ładowania .env:', result.error.message);
} else if (result.parsed) {
    console.log(`✅ Załadowano .env`);
    console.log(`   Znaleziono ${Object.keys(result.parsed).length} zmiennych:`);
    Object.keys(result.parsed).forEach(key => {
        console.log(`   - ${key} = ${result.parsed[key].substring(0, 20)}...`);
    });
} else {
    console.warn('⚠️  dotenv.config() wykonał się, ale result.parsed jest undefined');
}

// 3. SPRAWDŹ CZY KLUCZE SĄ W process.env
console.log('\n🔧 DEBUG: Sprawdzanie process.env:');
console.log('   OPENAI_API_KEY:', process.env.OPENAI_API_KEY ? `${process.env.OPENAI_API_KEY.substring(0, 20)}...` : '❌ BRAK');
console.log('   ANTHROPIC_API_KEY:', process.env.ANTHROPIC_API_KEY ? `${process.env.ANTHROPIC_API_KEY.substring(0, 20)}...` : '❌ BRAK');

/**
 * Klient dla LLM Engineering Professor Assistant
 */
export class LLMProfessorClient {
    constructor(options = {}) {
        const {
            openaiApiKey = process.env.OPENAI_API_KEY,
            anthropicApiKey = process.env.ANTHROPIC_API_KEY,
            systemPromptPath = null,
            defaultProvider = 'openai'
        } = options;

        console.log('\n🔧 DEBUG: Konstruktor LLMProfessorClient');
        console.log('   openaiApiKey:', openaiApiKey ? `${openaiApiKey.substring(0, 20)}...` : '❌ BRAK');
        console.log('   anthropicApiKey:', anthropicApiKey ? `${anthropicApiKey.substring(0, 20)}...` : '❌ BRAK');

        // Inicjalizacja klientów
        this.openaiClient = openaiApiKey ? new OpenAI({ apiKey: openaiApiKey }) : null;
        this.anthropicClient = anthropicApiKey ? new Anthropic({ apiKey: anthropicApiKey }) : null;

        this.defaultProvider = defaultProvider;
        this.systemPrompt = null;
        this.systemPromptPath = systemPromptPath || path.resolve(__dirname, '../../system.md');
    }

    async loadSystemPrompt() {
        try {
            this.systemPrompt = await fs.readFile(this.systemPromptPath, 'utf-8');
            console.log(`✅ Załadowano system prompt z: ${this.systemPromptPath}`);
            return this.systemPrompt;
        } catch (error) {
            console.warn(`⚠️  Nie znaleziono system.md w ${this.systemPromptPath}`);
            this.systemPrompt = 'Jesteś ekspertem w inżynierii modeli językowych (LLM).';
            return this.systemPrompt;
        }
    }

    async ask(question, options = {}) {
        const {
            detailLevel = 'intermediate',
            provider = this.defaultProvider,
            reasoningEffort = 'medium',
            verbosity = 'medium',
            ...extraOptions
        } = options;

        if (!this.systemPrompt) {
            await this.loadSystemPrompt();
        }

        if (provider === 'openai') {
            if (!this.openaiClient) {
                throw new Error('OpenAI client nie jest zainicjalizowany (brak API key)');
            }
            return this._askOpenAI(question, detailLevel, reasoningEffort, verbosity, extraOptions);
        } else if (provider === 'anthropic') {
            if (!this.anthropicClient) {
                throw new Error('Anthropic client nie jest zainicjalizowany (brak API key)');
            }
            return this._askAnthropicSync(question, detailLevel, extraOptions);
        } else {
            throw new Error(`Unsupported provider: ${provider}`);
        }
    }

    async _askOpenAI(question, detailLevel, reasoningEffort, verbosity, extraOptions) {
        try {
            const response = await this.openaiClient.responses.create({
                model: 'gpt-5-nano',
                instructions: this.systemPrompt,
                input: `
## Pytanie o LLM Engineering
${question}

## Poziom skomplikowania
${detailLevel}
                `.trim(),
                tools: [{ type: 'web_search' }],
                tool_choice: 'auto',
                reasoning: { effort: reasoningEffort },
                text: { verbosity: verbosity },
                max_output_tokens: extraOptions.maxTokens || 16000,
                store: extraOptions.store !== undefined ? extraOptions.store : true,
                ...extraOptions
            });

            return {
                output: response.output_text,
                metadata: {
                    provider: 'openai',
                    model: 'gpt-5-nano',
                    responseId: response.id,
                    createdAt: response.created_at,
                    reasoningEffort,
                    verbosity
                },
                rawResponse: response
            };
        } catch (error) {
            return {
                output: null,
                error: error.message,
                metadata: { provider: 'openai', model: 'gpt-5-nano' }
            };
        }
    }

    async _askAnthropicSync(question, detailLevel, extraOptions) {
        try {
            const message = await this.anthropicClient.messages.create({
                model: 'claude-sonnet-4-20250514',
                max_tokens: extraOptions.maxTokens || 16000,
                system: this.systemPrompt,
                messages: [
                    {
                        role: 'user',
                        content: `
## Pytanie o LLM Engineering
${question}

## Poziom skomplikowania
${detailLevel}
                        `.trim()
                    }
                ]
            });

            return {
                output: message.content[0].text,
                metadata: {
                    provider: 'anthropic',
                    model: 'claude-sonnet-4-20250514',
                    messageId: message.id,
                    usage: {
                        inputTokens: message.usage.input_tokens,
                        outputTokens: message.usage.output_tokens
                    }
                },
                rawResponse: message
            };
        } catch (error) {
            return {
                output: null,
                error: error.message,
                metadata: { provider: 'anthropic', model: 'claude-sonnet-4-20250514' }
            };
        }
    }
}

// =============================================
// QUICK TEST - ZAWSZE SIĘ WYKONUJE
// =============================================

console.log('\n' + '='.repeat(80));
console.log('🧪 LLM Engineering Professor Client - Quick Test');
console.log('='.repeat(80));

const client = new LLMProfessorClient();

(async () => {
    console.log('\n1️⃣  Testowanie inicjalizacji...');
    await client.loadSystemPrompt();

    console.log('\n2️⃣  Sprawdzanie klientów API:');
    console.log(`   OpenAI client: ${client.openaiClient ? '✅ OK' : '❌ Brak'}`);
    console.log(`   Anthropic client: ${client.anthropicClient ? '✅ OK' : '❌ Brak'}`);

    console.log('\n3️⃣  System prompt:');
    console.log(`   Długość: ${client.systemPrompt.length} znaków`);

    if (client.openaiClient) {
        console.log('\n4️⃣  Test zapytania (OpenAI)...');
        
        const testResponse = await client.ask('Czym jest tokenizacja w NLP? (krótko)', {
            detailLevel: 'beginner'
        });

        if (testResponse.output) {
            console.log(`\n✅ Odpowiedź otrzymana (${testResponse.output.length} znaków)`);
            console.log('\n📄 Podgląd:\n');
            console.log(testResponse.output.substring(0, 500) + '...');
        } else {
            console.log(`\n❌ Błąd: ${testResponse.error}`);
        }
    } else {
        console.log('\n⚠️  Brak OpenAI API key');
    }

    console.log('\n' + '='.repeat(80));
    console.log('✅ Test zakończony!');
    console.log('='.repeat(80) + '\n');
})().catch(error => {
    console.error('\n❌ Błąd:', error.message);
    console.error(error.stack);
});
