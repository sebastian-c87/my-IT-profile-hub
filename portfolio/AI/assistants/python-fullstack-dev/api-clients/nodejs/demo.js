

/**
 * Interactive Demo - Python Full-Stack Developer Assistant (Node.js)
 * =================================================================
 * 
 * Complete demonstration of assistant capabilities with interactive menu.
 * 
 * License: CC-BY-NC-ND-4.0
 * Author: Sebastian C.
 * Repository: https://github.com/sebastian-c87/my-IT-profile-hub
 */

const readline = require('readline');
const fs = require('fs-extra');
const path = require('path');
const { PythonFullStackAssistant } = require('./client');

class AssistantDemo {
    constructor() {
        this.assistant = new PythonFullStackAssistant();
        this.outputDir = path.join(__dirname, 'demo_outputs');
        fs.ensureDirSync(this.outputDir);
        
        this.rl = readline.createInterface({
            input: process.stdin,
            output: process.stdout
        });
    }
    
    async runDemo() {
        this._printHeader();
        
        while (true) {
            this._showMenu();
            const choice = await this._askQuestion('\n👉 Wybierz opcję (1-6): ');
            
            switch (choice.trim()) {
                case '1':
                    await this._demoSimpleApp();
                    break;
                case '2':
                    await this._demoComplexApp();
                    break;
                case '3':
                    await this._demoCustomApp();
                    break;
                case '4':
                    await this._demoProviderComparison();
                    break;
                case '5':
                    this._showProviderStatus();
                    break;
                case '6':
                    console.log('\n👋 Dziękuję za wypróbowanie demo!');
                    this.rl.close();
                    return;
                default:
                    console.log('❌ Niepoprawny wybór. Spróbuj ponownie.');
            }
            
            await this._askQuestion('\n⏸️  Naciśnij Enter aby kontynuować...');
        }
    }
    
    _printHeader() {
        console.log('='.repeat(70));
        console.log('🤖 PYTHON FULL-STACK DEVELOPER ASSISTANT - NODE.JS DEMO');
        console.log('='.repeat(70));
        console.log('📍 Repository: https://github.com/sebastian-c87/my-IT-profile-hub');
        console.log('📄 License: CC-BY-NC-ND-4.0');
        console.log(`🔧 Available providers: ${JSON.stringify(this.assistant.getAvailableProviders())}`);
        console.log();
    }
    
    _showMenu() {
        console.log('📋 DOSTĘPNE OPCJE:');
        console.log('1. 🏃‍♂️ Quick Demo - Prosta aplikacja blog');
        console.log('2. 🚀 Advanced Demo - Złożona aplikacja CRM');
        console.log('3. ✏️  Custom Demo - Twoja aplikacja');
        console.log('4. ⚖️  Provider Comparison - Claude vs OpenAI');
        console.log('5. 📊 Provider Status - Sprawdź dostępność');
        console.log('6. 🚪 Wyjście');
    }
    
    async _demoSimpleApp() {
        console.log('\n🏃‍♂️ QUICK DEMO - APLIKACJA BLOG');
        console.log('-'.repeat(30));
        
        const appIdea = 'Personal blog z możliwością dodawania postów, komentarzy i tagów';
        const requirements = 'Flask backend, Bootstrap frontend, SQLite database, WYSIWYG editor';
        
        console.log(`💡 Pomysł: ${appIdea}`);
        console.log(`📋 Wymagania: ${requirements}`);
        console.log('\n⏱️  Generuję aplikację...');
        
        const response = await this.assistant.createApplication(appIdea, requirements);
        await this._displayResult(response, 'simple_blog_app');
    }
    
    async _demoComplexApp() {
        console.log('\n🚀 ADVANCED DEMO - APLIKACJA CRM');
        console.log('-'.repeat(35));
        
        const appIdea = `System CRM do zarządzania klientami, leadami, kontaktami 
        z automatyzacją email marketing i dashboardem analitycznym`;
        
        const requirements = `
        - Django REST Framework backend
        - React TypeScript frontend
        - PostgreSQL database
        - JWT authentication
        - SendGrid email integration  
        - Chart.js dla analytics
        - Docker deployment
        - Comprehensive testing
        `;
        
        console.log(`💡 Pomysł: ${appIdea}`);
        console.log(`📋 Wymagania: ${requirements}`);
        console.log('\n⏱️  Generuję złożoną aplikację... (może potrwać kilka minut)');
        
        const response = await this.assistant.createApplication(appIdea, requirements);
        await this._displayResult(response, 'complex_crm_app');
    }
    
    async _demoCustomApp() {
        console.log('\n✏️  CUSTOM DEMO - TWOJA APLIKACJA');
        console.log('-'.repeat(33));
        
        const appIdea = await this._askQuestion('💡 Opisz swoją aplikację: ');
        if (!appIdea.trim()) {
            console.log('❌ Brak pomysłu. Wracam do menu.');
            return;
        }
        
        const requirements = await this._askQuestion('📋 Wymagania techniczne (opcjonalne): ');
        
        console.log(`\n⏱️  Generuję aplikację: '${appIdea.slice(0, 50)}${appIdea.length > 50 ? '...' : ''}'`);
        
        const response = await this.assistant.createApplication(appIdea, requirements);
        const filename = `custom_${appIdea.toLowerCase().replace(/[^a-z0-9]/g, '_').slice(0, 20)}`;
        await this._displayResult(response, filename);
    }
    
    async _demoProviderComparison() {
        console.log('\n⚖️  PROVIDER COMPARISON - CLAUDE VS OPENAI');
        console.log('-'.repeat(45));
        
        const appIdea = 'Aplikacja fitness tracker z treningami, dietą i progress tracking';
        const requirements = 'FastAPI backend, Vue.js frontend, MongoDB, mobile-first design';
        
        console.log(`💡 Test case: ${appIdea}`);
        console.log(`📋 Wymagania: ${requirements}`);
        console.log();
        
        // Test Claude
        if (this.assistant.claudeClient) {
            console.log('🟦 Testing Claude...');
            const claudeResponse = await this.assistant.createApplication(
                appIdea, requirements, null, 'claude'
            );
            this._displayComparisonResult('Claude', claudeResponse);
        } else {
            console.log('🟦 Claude: Not available');
        }
        
        console.log();
        
        // Test OpenAI
        if (this.assistant.openaiClient) {
            console.log('🟩 Testing OpenAI...');
            const openaiResponse = await this.assistant.createApplication(
                appIdea, requirements, null, 'openai'
            );
            this._displayComparisonResult('OpenAI', openaiResponse);
        } else {
            console.log('🟩 OpenAI: Not available');
        }
    }
    
    _showProviderStatus() {
        console.log('\n📊 PROVIDER STATUS');
        console.log('-'.repeat(20));
        
        const providers = this.assistant.getAvailableProviders();
        
        for (const [provider, available] of Object.entries(providers)) {
            const status = available ? '✅ Available' : '❌ Not available';
            const envVar = provider === 'claude' ? 'ANTHROPIC_API_KEY' : 'OPENAI_API_KEY';
            const keyStatus = process.env[envVar] ? 'Set' : 'Not set';
            
            console.log(`${provider.toUpperCase()}:<8} ${status}`);
            console.log(`         API Key (${envVar}): ${keyStatus}`);
            console.log();
        }
        
        if (!Object.values(providers).some(Boolean)) {
            console.log('⚠️  No providers available. Please check your API key configuration.');
            console.log('\nSetup instructions:');
            console.log('1. Create .env file in this directory');
            console.log('2. Add: ANTHROPIC_API_KEY=your_claude_key');
            console.log('3. Add: OPENAI_API_KEY=your_openai_key');
        }
    }
    
    async _displayResult(response, filename) {
        console.log(`\n${response.success ? '✅ SUCCESS' : '❌ FAILED'}`);
        console.log('-'.repeat(50));
        
        if (response.success) {
            // Display stats
            const lines = response.content.split('\n').length;
            const words = response.content.split(/\s+/).length;
            const chars = response.content.length;
            
            console.log('📊 Statistics:');
            console.log(`   • Provider: ${response.provider} (${response.model})`);
            console.log(`   • Generation time: ${response.responseTime?.toFixed(1)} seconds`);
            console.log(`   • Tokens used: ${response.tokensUsed || 'N/A'}`);
            console.log(`   • Lines: ${lines.toLocaleString()}`);
            console.log(`   • Words: ${words.toLocaleString()}`);
            console.log(`   • Characters: ${chars.toLocaleString()}`);
            
            // Save to file
            const outputFile = path.join(this.outputDir, `${filename}.md`);
            const fileContent = `# Generated Application - ${filename}\n\n` +
                `**Provider:** ${response.provider} (${response.model})\n` +
                `**Generated:** ${new Date().toISOString()}\n` +
                `**Time:** ${response.responseTime?.toFixed(1)}s\n` +
                `**Tokens:** ${response.tokensUsed || 'N/A'}\n\n` +
                '---\n\n' +
                response.content;
            
            await fs.writeFile(outputFile, fileContent, 'utf8');
            console.log(`\n💾 Saved to: ${outputFile}`);
            
            // Show preview
            console.log('\n📖 PREVIEW (first 500 characters):');
            console.log('-'.repeat(50));
            const preview = response.content.slice(0, 500);
            if (response.content.length > 500) {
                console.log(preview + '\n\n[... content truncated ...]');
            } else {
                console.log(preview);
            }
            
        } else {
            console.log(`❌ Error: ${response.errorMessage}`);
        }
    }
    
    _displayComparisonResult(providerName, response) {
        if (response.success) {
            const lines = response.content.split('\n').length;
            const words = response.content.split(/\s+/).length;
            
            console.log(`   ✅ ${providerName}: ${response.responseTime?.toFixed(1)}s, ${lines.toLocaleString()} lines, ${words.toLocaleString()} words`);
        } else {
            console.log(`   ❌ ${providerName}: ${response.errorMessage}`);
        }
    }
    
    _askQuestion(question) {
        return new Promise((resolve) => {
            this.rl.question(question, resolve);
        });
    }
}

async function main() {
    // Check API key availability
    const hasClaude = !!process.env.ANTHROPIC_API_KEY;
    const hasOpenAI = !!process.env.OPENAI_API_KEY;
    
    if (!hasClaude && !hasOpenAI) {
        console.log('❌ BRAK KONFIGURACJI API');
        console.log('\nPotrzebny jest przynajmniej jeden klucz API:');
        console.log('1. Utwórz plik .env w tym folderze');
        console.log('2. Dodaj klucz Claude: ANTHROPIC_API_KEY=sk-ant-...');
        console.log('3. LUB dodaj klucz OpenAI: OPENAI_API_KEY=sk-...');
        console.log('4. Uruchom demo ponownie: npm start');
        process.exit(1);
    }
    
    try {
        const demo = new AssistantDemo();
        await demo.runDemo();
    } catch (error) {
        if (error.message.includes('canceled')) {
            console.log('\n\n👋 Demo interrupted. See you next time!');
        } else {
            console.log(`\n❌ Unexpected error: ${error.message}`);
            console.log('Please check your configuration and try again.');
        }
        process.exit(0);
    }
}

if (require.main === module) {
    main();
}
