/**
 * Interactive Demo for Cryptocurrency Market Analyst
 * Simple menu-driven interface for crypto analysis with file output
 * 
 * @author Sebastian C.
 * @license CC-BY-NC-ND-4.0
 */

import fs from 'fs';
import path from 'path';
import { createInterface } from 'readline';
import { fileURLToPath } from 'url';
import CryptoAnalyst from './client.js';

// Setup for ES modules - FIXED for Windows
const __filename = fileURLToPath(import.meta.url);
const __dirname = path.dirname(__filename);

// Create readline interface with proper configuration
const rl = createInterface({
    input: process.stdin,
    output: process.stdout,
    terminal: true // FIXED: Explicitly enable terminal mode
});

/**
 * Promisify readline question - FIXED with proper cleanup
 */
const question = (query) => new Promise((resolve) => {
    rl.question(query, (answer) => {
        resolve(answer);
    });
});

/**
 * Create demo_output folder if it doesn't exist
 */
function createDemoOutputFolder() {
    const outputDir = path.join(__dirname, 'demo_output');
    if (!fs.existsSync(outputDir)) {
        fs.mkdirSync(outputDir, { recursive: true });
    }
    return outputDir;
}

/**
 * Print demo header
 */
function printHeader() {
    console.log("\n" + "=".repeat(60));
    console.log("🚀 CRYPTOCURRENCY MARKET ANALYST - INTERACTIVE DEMO");
    console.log("=".repeat(60));
    console.log("Professional crypto market analysis powered by AI");
    console.log("Supports OpenAI GPT-5 and Claude Sonnet 4");
    console.log("📁 Results saved to: demo_output/ folder as .md files");
}

/**
 * Print main menu
 */
function printMenu() {
    console.log("\n📋 MAIN MENU:");
    console.log("1. Analyze specific cryptocurrency");
    console.log("2. Get trading signals");
    console.log("3. Portfolio analysis");
    console.log("4. Market overview");
    console.log("5. View saved analyses");
    console.log("0. Exit");
}

/**
 * Get cryptocurrency choice from user
 */
async function getCryptoInput() {
    console.log("\n💰 SELECT CRYPTOCURRENCY:");
    console.log("1. Bitcoin (BTC)");
    console.log("2. Ethereum (ETH)");
    console.log("3. Cardano (ADA)");
    console.log("4. Solana (SOL)");
    console.log("5. Binance Coin (BNB)");
    console.log("6. Custom (enter symbol)");

    const choice = await question("\nYour choice (1-6): ");

    const cryptoMap = {
        "1": ["Bitcoin", "BTC"],
        "2": ["Ethereum", "ETH"],
        "3": ["Cardano", "ADA"],
        "4": ["Solana", "SOL"],
        "5": ["Binance Coin", "BNB"]
    };

    if (cryptoMap[choice.trim()]) {
        return cryptoMap[choice.trim()];
    } else if (choice.trim() === "6") {
        const symbol = (await question("Enter crypto symbol (e.g., DOT, LINK): ")).trim().toUpperCase();
        return symbol ? [symbol, symbol] : ["Bitcoin", "BTC"];
    } else {
        return ["Bitcoin", "BTC"];
    }
}

/**
 * Get analysis timeframe
 */
async function getTimeframe() {
    console.log("\n⏱️ SELECT TIMEFRAME:");
    console.log("1. Short-term (1-7 days)");
    console.log("2. Medium-term (1-4 weeks)");
    console.log("3. Long-term (1-6 months)");

    const choice = await question("Your choice (1-3): ");

    const timeframeMap = {
        "1": "short-term",
        "2": "medium-term",
        "3": "long-term"
    };

    return timeframeMap[choice.trim()] || "medium-term";
}

/**
 * Get type of analysis
 */
async function getAnalysisType() {
    console.log("\n📊 SELECT ANALYSIS TYPE:");
    console.log("1. Comprehensive (technical + fundamental)");
    console.log("2. Technical analysis only");
    console.log("3. Fundamental analysis only");
    console.log("4. Trading signals");

    const choice = await question("Your choice (1-4): ");

    const typeMap = {
        "1": "comprehensive analysis",
        "2": "technical analysis only",
        "3": "fundamental analysis only",
        "4": "trading signals and entry/exit points"
    };

    return typeMap[choice.trim()] || "comprehensive analysis";
}

/**
 * Get AI model choice
 */
async function getModelChoice(analyst) {
    const models = analyst.getAvailableModels();

    if (models.length === 0) {
        console.log("❌ No AI models available! Check your API keys.");
        return null;
    }

    console.log("\n🤖 SELECT AI MODEL:");
    models.forEach((model, index) => {
        console.log(`${index + 1}. ${model}`);
    });

    const choice = await question(`Your choice (1-${models.length}): `);
    const choiceNum = parseInt(choice.trim());

    if (choiceNum >= 1 && choiceNum <= models.length) {
        return models[choiceNum - 1];
    }

    return models[0]; // Default to first model
}

/**
 * Format the complete query for AI
 */
function formatQuery(cryptoName, cryptoSymbol, timeframe, analysisType) {
    return `
    Przeprowadź ${analysisType} dla ${cryptoName} (${cryptoSymbol}).
    
    Horyzont czasowy: ${timeframe}
    
    Proszę o szczegółową analizę uwzględniającą:
    - Obecne trendy cenowe
    - Kluczowe poziomy wsparcia i oporu
    - Sentiment rynkowy
    - Ocenę ryzyka
    - Konkretne rekomendacje
    
    Zakończ analizę disclaimer o ryzyku inwestowania.
    `.trim();
}

/**
 * Create filename for the analysis
 */
function createFilename(cryptoSymbol, analysisType, timeframe) {
    const analysisClean = analysisType.replace(/\s+/g, '_').replace(/\//g, '_');
    const timestamp = Math.floor(Date.now() / 1000);
    
    return `Analiza_${cryptoSymbol}_${analysisClean}_${timeframe}_${timestamp}.md`;
}

/**
 * Save analysis to markdown file
 */
function saveAnalysisToFile(outputDir, filename, analysisData) {
    const markdownContent = `# Analiza Kryptowaluty: ${analysisData.cryptoName} (${analysisData.cryptoSymbol})

## Informacje o Analizie

- **Data analizy:** ${analysisData.timestamp}
- **Kryptowaluta:** ${analysisData.cryptoName} (${analysisData.cryptoSymbol})
- **Horyzont czasowy:** ${analysisData.timeframe}
- **Typ analizy:** ${analysisData.analysisType}
- **Model AI:** ${analysisData.model}
- **Czas przetwarzania:** ${analysisData.processingTime.toFixed(1)} sekund
- **Status walidacji:** ${analysisData.validation.isComplete ? "✅ Kompletna" : "⚠️ Częściowa"}
- **Wygenerowano znaków:** ${analysisData.validation.totalChars.toLocaleString()}

---

${analysisData.response}

---

## Informacje Techniczne

- **ID odpowiedzi:** ${analysisData.responseId || 'N/A'}
- **Sekcje znalezione:** ${analysisData.validation.successfulSections}/${analysisData.validation.totalSections}
- **Generator:** Cryptocurrency Market Analyst v1.0.0
- **Plik utworzony:** ${new Date().toLocaleString('pl-PL')}
`;

    const filePath = path.join(outputDir, filename);

    try {
        fs.writeFileSync(filePath, markdownContent, 'utf-8');
        return filePath;
    } catch (error) {
        console.log(`❌ Error saving file: ${error.message}`);
        return null;
    }
}

/**
 * List all saved analysis files
 */
function listSavedAnalyses(outputDir) {
    try {
        const files = fs.readdirSync(outputDir)
            .filter(file => file.startsWith('Analiza_') && file.endsWith('.md'))
            .map(file => {
                const filePath = path.join(outputDir, file);
                const stats = fs.statSync(filePath);
                return {
                    name: file,
                    size: stats.size,
                    mtime: stats.mtime
                };
            })
            .sort((a, b) => b.mtime - a.mtime) // Sort by modification time (newest first)
            .slice(0, 10); // Show max 10 recent files

        if (files.length === 0) {
            console.log("📂 No saved analyses found in demo_output/ folder");
            return;
        }

        console.log(`\n📁 SAVED ANALYSES (${files.length} files):`);
        console.log("=".repeat(50));

        files.forEach((file, index) => {
            const modTime = file.mtime.toLocaleString('pl-PL');
            console.log(`${(index + 1).toString().padStart(2)}. ${file.name}`);
            console.log(`    📅 ${modTime} | 📊 ${file.size.toLocaleString()} bytes`);
        });

        const totalFiles = fs.readdirSync(outputDir)
            .filter(file => file.startsWith('Analiza_') && file.endsWith('.md')).length;

        if (totalFiles > 10) {
            console.log(`    ... and ${totalFiles - 10} more files`);
        }

    } catch (error) {
        console.log(`❌ Error listing files: ${error.message}`);
    }
}

/**
 * Main demo function - FIXED with proper async handling
 */
async function main() {
    try {
        printHeader();

        // Create output folder
        const outputDir = createDemoOutputFolder();
        console.log(`✅ Output folder ready: ${path.resolve(outputDir)}`);

        // Initialize analyst
        console.log("\n🔧 Initializing Crypto Analyst...");
        const analyst = new CryptoAnalyst();

        if (!analyst.openaiClient && !analyst.anthropicClient) {
            console.log("\n❌ CRITICAL ERROR: No API clients available!");
            console.log("Please check your .env file and API keys.");
            rl.close();
            return;
        }

        while (true) {
            printMenu();
            const choice = await question("\nYour choice (0-5): ");

            if (choice.trim() === "0") {
                console.log("\n👋 Thanks for using Crypto Analyst! Goodbye!");
                console.log(`📁 Your analyses are saved in: ${path.resolve(outputDir)}`);
                break;
            }

            if (["1", "2", "3", "4"].includes(choice.trim())) {
                // Get user preferences
                let [cryptoName, cryptoSymbol] = await getCryptoInput();
                const timeframe = await getTimeframe();

                let analysisType;
                if (choice.trim() === "1") {
                    analysisType = await getAnalysisType();
                } else if (choice.trim() === "2") {
                    analysisType = "trading signals with precise entry/exit points";
                } else if (choice.trim() === "3") {
                    analysisType = "portfolio analysis and risk assessment";
                } else { // choice === "4"
                    analysisType = "general market overview and trends";
                    cryptoName = "major cryptocurrencies (BTC, ETH, top altcoins)";
                    cryptoSymbol = "MARKET";
                }

                const model = await getModelChoice(analyst);
                if (!model) {
                    continue;
                }

                // Build query
                const query = formatQuery(cryptoName, cryptoSymbol, timeframe, analysisType);

                // Display summary
                console.log("\n📋 ANALYSIS SUMMARY:");
                console.log(`   Crypto: ${cryptoName} (${cryptoSymbol})`);
                console.log(`   Timeframe: ${timeframe}`);
                console.log(`   Analysis: ${analysisType}`);
                console.log(`   AI Model: ${model}`);

                await question("\nPress Enter to start analysis...");

                // Perform analysis
                console.log(`\n🔄 Starting ${analysisType.toLowerCase()} for ${cryptoName}...`);
                console.log("This may take 30-60 seconds...");

                const startTime = Date.now();

                let result;
                if (model.toLowerCase().includes("gpt")) {
                    result = await analyst.analyzeCryptoOpenAI(query, model);
                } else {
                    result = await analyst.analyzeCryptoClaudeSimple(query);
                }

                const endTime = Date.now();
                const processingTime = (endTime - startTime) / 1000;

                if (result.success) {
                    // Prepare analysis data
                    const analysisData = {
                        timestamp: new Date().toLocaleString('pl-PL'),
                        cryptoName,
                        cryptoSymbol,
                        timeframe,
                        analysisType,
                        model: result.modelUsed,
                        processingTime,
                        response: result.response,
                        validation: result.validation,
                        responseId: result.responseId
                    };

                    // Create filename and save
                    const filename = createFilename(cryptoSymbol, analysisType, timeframe);
                    const filePath = saveAnalysisToFile(outputDir, filename, analysisData);

                    if (filePath) {
                        const stats = fs.statSync(filePath);
                        console.log("\n✅ Analysis completed successfully!");
                        console.log(`📁 Saved to: ${filename}`);
                        console.log(`📊 File size: ${stats.size.toLocaleString()} bytes`);
                        console.log(`⚡ Processing time: ${processingTime.toFixed(1)} seconds`);

                        // Show validation summary
                        const validation = result.validation;
                        console.log(`🎯 Validation: ${validation.successfulSections}/${validation.totalSections} sections complete`);
                    } else {
                        console.log("\n❌ Analysis completed but failed to save to file");
                    }
                } else {
                    console.log(`\n❌ Analysis failed: ${result.error}`);
                }

            } else if (choice.trim() === "5") {
                listSavedAnalyses(outputDir);

            } else {
                console.log("❌ Invalid choice. Please try again.");
            }

            // Pause before next iteration
            await question("\nPress Enter to continue...");
        }

    } catch (error) {
        console.error(`❌ Demo error: ${error.message}`);
    } finally {
        rl.close();
    }
}

// FIXED: Check if this file is being run directly
const isMainModule = process.argv[1] === fileURLToPath(import.meta.url);
if (isMainModule) {
    main().catch(error => {
        console.error(`❌ Demo error: ${error.message}`);
        rl.close();
        process.exit(1);
    });
}
