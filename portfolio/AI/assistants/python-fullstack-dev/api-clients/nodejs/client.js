/**
 * Python Full-Stack Developer Assistant - Node.js Client
 * ==================================================================
 * 
 * License: CC-BY-NC-ND-4.0  
 * Author: Sebastian C.
 * Repository: https://github.com/sebastian-c87/my-IT-profile-hub
 */

const Anthropic = require('@anthropic-ai/sdk');
const OpenAI = require('openai');
const fs = require('fs-extra');
const path = require('path');
require('dotenv').config();

class APIResponse {
    constructor(content = '', model = '', provider = '', tokensUsed = null, responseTime = null, success = true, errorMessage = null) {
        Object.assign(this, {content, model, provider, tokensUsed, responseTime, success, errorMessage});
    }
}

class PythonFullStackAssistant {
    constructor() {
        // Load API keys from .env
        this.openaiClient = process.env.OPENAI_API_KEY ? new OpenAI({apiKey: process.env.OPENAI_API_KEY}) : null;
        this.claudeClient = process.env.ANTHROPIC_API_KEY ? new Anthropic({apiKey: process.env.ANTHROPIC_API_KEY}) : null;
        
        if (!this.openaiClient && !this.claudeClient) {
            throw new Error('No API keys found. Set OPENAI_API_KEY or ANTHROPIC_API_KEY in .env file');
        }
    }
    
    getAvailableProviders() {
        const providers = [];
        if (this.openaiClient) providers.push('openai');
        if (this.claudeClient) providers.push('claude');
        return providers;
    }

    async createApplication(appIdea, requirements = '') {
        if (!appIdea.trim()) {
            return new APIResponse('', '', '', null, null, false, 'App idea cannot be empty');
        }
        
        const systemPrompt = await this._loadSystemPrompt();
        const userMessage = `**Pomysł na aplikację:** ${appIdea}\n**Dodatkowe wymagania:** ${requirements || 'Brak'}`;
        
        // Try OpenAI first (cheaper)
        if (this.openaiClient) {
            return await this._callOpenAI(systemPrompt, userMessage);
        }
        
        // Fallback to Claude Batch
        if (this.claudeClient) {
            return await this._callClaudeBatch(systemPrompt, userMessage);
        }
        
        return new APIResponse('', '', '', null, null, false, 'No providers available');
    }
    
    async _callOpenAI(systemPrompt, userMessage) {
        const startTime = Date.now();
        
        try {
            const response = await this.openaiClient.responses.create({
                model: 'gpt-5-nano',
                instructions: systemPrompt,
                input: userMessage,
                reasoning: {effort: 'minimal'},
                text: {verbosity: 'low'},
                store: false
            });
            
            return new APIResponse(
                response.output_text,
                'gpt-5-nano',
                'openai',
                response.usage?.total_tokens,
                (Date.now() - startTime) / 1000,
                true
            );
            
        } catch (error) {
            return new APIResponse(
                '',
                'gpt-5-nano', 
                'openai',
                null,
                (Date.now() - startTime) / 1000,
                false,
                error.message
            );
        }
    }
    
    async _callClaudeBatch(systemPrompt, userMessage) {
        const startTime = Date.now();
        
        try {
            // Create batch
            const batch = await this.claudeClient.messages.batches.create({
                requests: [{
                    custom_id: `app-${Date.now()}`,
                    params: {
                        model: 'claude-3-5-haiku-20241022',
                        max_tokens: 14096,
                        system: systemPrompt,
                        messages: [{role: 'user', content: userMessage}]
                    }
                }]
            });
            
            // Poll for completion (max 30 minutes)
            for (let i = 0; i < 60; i++) {
                await new Promise(resolve => setTimeout(resolve, 30000)); // 30s
                
                const batchStatus = await this.claudeClient.messages.batches.retrieve(batch.id);
                
                if (batchStatus.processing_status === 'ended') {
                    for await (const result of this.claudeClient.messages.batches.results(batch.id)) {
                        if (result.result.type === 'succeeded') {
                            return new APIResponse(
                                result.result.message.content[0].text,
                                'claude-3-5-haiku-20241022',
                                'claude',
                                result.result.message.usage.input_tokens + result.result.message.usage.output_tokens,
                                (Date.now() - startTime) / 1000,
                                true
                            );
                        }
                    }
                }
            }
            
            return new APIResponse('', 'claude-3-5-haiku-20241022', 'claude', null, (Date.now() - startTime) / 1000, false, 'Batch timeout');
            
        } catch (error) {
            return new APIResponse('', 'claude-3-5-haiku-20241022', 'claude', null, (Date.now() - startTime) / 1000, false, error.message);
        }
    }
    
    async _loadSystemPrompt() {
        try {
            return await fs.readFile(path.join(__dirname, '../../system.md'), 'utf8');
        } catch (error) {
            return `# Rola
Jesteś ekspertem **Programistą Python Full-Stack** z ponad 10-letnim doświadczeniem w tworzeniu nowoczesnych aplikacji web.

# Cel
Przekształcenie pomysłu użytkownika w kompletną, działającą aplikację web z profesjonalną strukturą plików i kodem production-ready.`;
        }
    }
}

module.exports = {PythonFullStackAssistant, APIResponse};

// Auto-test when run directly
if (require.main === module) {
    (async () => {
        const assistant = new PythonFullStackAssistant();
        const result = await assistant.createApplication('Task management app', 'FastAPI + React + SQLite');
        console.log(`Success: ${result.success}, Provider: ${result.provider}, Time: ${result.responseTime?.toFixed(1)}s, Generated: ${result.content.length} characters`);
    })().catch(console.error);
}
