/**
 * Interaktywne demo LLM Engineering Professor Client
 * 
 * Funkcje:
 * - Wybór przykładowego pytania lub własne
 * - Wybór poziomu zaawansowania
 * - Wybór providera (OpenAI/Anthropic)
 * - Export odpowiedzi do .md i .json
 */

import prompts from 'prompts';
import chalk from 'chalk';
import fs from 'fs/promises';
import path from 'path';
import { fileURLToPath } from 'url';
import { LLMProfessorClient } from './client.js';

const __filename = fileURLToPath(import.meta.url);
const __dirname = path.dirname(__filename);

class InteractiveDemo {
    constructor() {
        this.client = new LLMProfessorClient({ defaultProvider: 'openai' });
        this.outputDir = path.resolve(__dirname, './outputs');
    }

    async ensureOutputDir() {
        try {
            await fs.mkdir(this.outputDir, { recursive: true });
        } catch (error) {
            // Folder już istnieje
        }
    }

    displayBanner() {
        console.log('\n' + chalk.cyan('='.repeat(80)));
        console.log(chalk.bold.green('🎓 LLM Engineering Professor - Interaktywne Demo'));
        console.log(chalk.cyan('='.repeat(80)));
        console.log(chalk.gray('\nWitaj! Ten asystent pomoże Ci nauczyć się tworzenia modeli LLM.\n'));
    }

    async selectExampleQuestion() {
        console.log(chalk.cyan('='.repeat(80)));
        console.log(chalk.bold('📝 KROK 1: Wybierz pytanie'));
        console.log(chalk.cyan('='.repeat(80)));

        const examples = [
            'Jak stworzyć tokenizer BPE w Pythonie?',
            'Jak zaimplementować LoRA dla fine-tuningu?',
            'Czym jest RLHF i jak go zastosować?',
            'Jak zmierzyć hallucination rate w modelu LLM?',
            'Jak zbudować pipeline przetwarzania danych dla LLM?',
            '[WŁASNE PYTANIE]'
        ];

        const response = await prompts({
            type: 'select',
            name: 'value',
            message: 'Wybierz pytanie:',
            choices: examples.map((q, idx) => ({ title: q, value: idx })),
            initial: 0
        });

        if (response.value === examples.length - 1) {
            const custom = await prompts({
                type: 'text',
                name: 'value',
                message: 'Wpisz swoje pytanie:',
                validate: value => value.length > 0 || 'Pytanie nie może być puste!'
            });
            return custom.value;
        }

        return examples[response.value];
    }

    async selectDetailLevel() {
        console.log('\n' + chalk.cyan('='.repeat(80)));
        console.log(chalk.bold('🎯 KROK 2: Wybierz poziom zaawansowania'));
        console.log(chalk.cyan('='.repeat(80)));

        const levels = [
            { title: 'Początkujący - podstawowe wyjaśnienia', value: 'beginner' },
            { title: 'Średniozaawansowany - balans teorii i praktyki', value: 'intermediate' },
            { title: 'Zaawansowany - głębokie szczegóły techniczne', value: 'advanced' }
        ];

        const response = await prompts({
            type: 'select',
            name: 'value',
            message: 'Wybierz poziom:',
            choices: levels,
            initial: 1
        });

        return response.value;
    }

    async selectProvider() {
        console.log('\n' + chalk.cyan('='.repeat(80)));
        console.log(chalk.bold('⚡ KROK 3: Wybierz provider AI'));
        console.log(chalk.cyan('='.repeat(80)));

        const providers = [
            { title: 'OpenAI (gpt-5-nano) - SZYBKI, standardowa cena', value: 'openai' },
            { title: 'Anthropic (Claude 4 Sonnet) - DOKŁADNY, lepsza jakość', value: 'anthropic' }
        ];

        const response = await prompts({
            type: 'select',
            name: 'value',
            message: 'Wybierz provider:',
            choices: providers,
            initial: 0
        });

        return response.value;
    }

    async generateResponse(question, detailLevel, provider) {
        console.log('\n' + chalk.cyan('='.repeat(80)));
        console.log(chalk.bold('🤖 Generowanie odpowiedzi...'));
        console.log(chalk.cyan('='.repeat(80)));
        console.log(chalk.gray(`\n📤 Wysyłam zapytanie do ${provider.toUpperCase()}...\n`));

        return await this.client.ask(question, {
            detailLevel,
            provider,
            reasoningEffort: 'medium',
            verbosity: 'medium'
        });
    }

    displayResponse(response) {
        console.log('\n' + chalk.cyan('='.repeat(80)));
        console.log(chalk.bold.green('📄 ODPOWIEDŹ PROFESORA'));
        console.log(chalk.cyan('='.repeat(80)) + '\n');

        if (response.output) {
            console.log(response.output);

            console.log('\n' + chalk.cyan('='.repeat(80)));
            console.log(chalk.bold('📊 METADATA'));
            console.log(chalk.cyan('='.repeat(80)));
            const { metadata } = response;
            console.log(chalk.gray(`  Provider: ${metadata.provider}`));
            console.log(chalk.gray(`  Model: ${metadata.model}`));
            console.log(chalk.gray(`  Długość: ${response.output.length} znaków`));

            if (metadata.usage) {
                console.log(chalk.gray(`  Input tokens: ${metadata.usage.inputTokens}`));
                console.log(chalk.gray(`  Output tokens: ${metadata.usage.outputTokens}`));
            }
        } else {
            console.log(chalk.red(`❌ Błąd: ${response.error}`));
        }
    }

    async exportResponse(question, detailLevel, provider, response) {
        console.log('\n' + chalk.cyan('='.repeat(80)));
        console.log(chalk.bold('💾 EKSPORT ODPOWIEDZI'));
        console.log(chalk.cyan('='.repeat(80)));

        if (!response.output) {
            console.log(chalk.red('\n❌ Brak odpowiedzi do eksportu.'));
            return;
        }

        await this.ensureOutputDir();

        // Timestamp dla unikalnej nazwy
        const timestamp = new Date().toISOString().replace(/[:.]/g, '-').slice(0, -5);
        const baseName = `llm_professor_${timestamp}`;

        // Export do Markdown
        const mdPath = path.join(this.outputDir, `${baseName}.md`);
        const mdContent = `# LLM Engineering Professor - Odpowiedź

## Metadane
- **Data:** ${new Date().toLocaleString('pl-PL')}
- **Provider:** ${provider.toUpperCase()}
- **Model:** ${response.metadata.model}
- **Poziom zaawansowania:** ${detailLevel}
- **Długość:** ${response.output.length} znaków

## Pytanie
${question}

---

## Odpowiedź

${response.output}

---

## Metadata (JSON)
\`\`\`json
${JSON.stringify(response.metadata, null, 2)}
\`\`\`
`;

        await fs.writeFile(mdPath, mdContent, 'utf-8');
        console.log(chalk.green(`\n✅ Zapisano Markdown: ${mdPath}`));

        // Export do JSON
        const jsonPath = path.join(this.outputDir, `${baseName}.json`);
        const jsonData = {
            timestamp: new Date().toISOString(),
            question,
            detailLevel,
            provider,
            response: {
                output: response.output,
                metadata: response.metadata
            }
        };

        await fs.writeFile(jsonPath, JSON.stringify(jsonData, null, 2), 'utf-8');
        console.log(chalk.green(`✅ Zapisano JSON: ${jsonPath}`));
        console.log(chalk.gray(`\n📁 Pliki zapisane w: ${this.outputDir}`));
    }

    async run() {
        this.displayBanner();

        // Krok 1: Wybór pytania
        const question = await this.selectExampleQuestion();

        // Krok 2: Poziom zaawansowania
        const detailLevel = await this.selectDetailLevel();

        // Krok 3: Provider
        const provider = await this.selectProvider();

        // Generuj odpowiedź
        const response = await this.generateResponse(question, detailLevel, provider);

        // Wyświetl odpowiedź
        this.displayResponse(response);

        // Eksport
        const exportChoice = await prompts({
            type: 'confirm',
            name: 'value',
            message: '💾 Czy chcesz zapisać odpowiedź do pliku?',
            initial: true
        });

        if (exportChoice.value) {
            await this.exportResponse(question, detailLevel, provider, response);
        }

        console.log('\n' + chalk.cyan('='.repeat(80)));
        console.log(chalk.bold.green('✅ Demo zakończone! Dziękujemy za korzystanie z LLM Professor.'));
        console.log(chalk.cyan('='.repeat(80)) + '\n');
    }
}

// Uruchom demo
const demo = new InteractiveDemo();
demo.run().catch(error => {
    console.error(chalk.red('\n❌ Błąd:'), error.message);
    process.exit(1);
});
