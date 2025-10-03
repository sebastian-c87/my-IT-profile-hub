/**
 * Cryptocurrency Market Analyst - Node.js Client
 * Uses OpenAI Responses API (GPT-5) and Anthropic Messages API
 * 
 * @author Sebastian C.
 * @license CC-BY-NC-ND-4.0
 */

import fs from 'fs';
import path from 'path';
import { fileURLToPath } from 'url';

// MANUAL .env loading - SOLUTION for dotenv issue
function loadEnvFile() {
    try {
        const __filename = fileURLToPath(import.meta.url);
        const __dirname = path.dirname(__filename);
        const envPath = path.join(__dirname, '.env');
        
        if (fs.existsSync(envPath)) {
            const envContent = fs.readFileSync(envPath, 'utf-8');
            
            envContent.split('\n').forEach(line => {
                const trimmedLine = line.trim();
                if (trimmedLine && !trimmedLine.startsWith('#')) {
                    const [key, ...valueParts] = trimmedLine.split('=');
                    if (key && valueParts.length > 0) {
                        const value = valueParts.join('=').replace(/^["']|["']$/g, '');
                        process.env[key.trim()] = value.trim();
                    }
                }
            });
            console.log("✅ .env file loaded manually");
            return true;
        } else {
            console.log("⚠️ .env file not found");
            return false;
        }
    } catch (error) {
        console.log(`⚠️ Error loading .env file: ${error.message}`);
        return false;
    }
}

// Load .env file first
loadEnvFile();

// FORCE global modules path for Windows
const GLOBAL_MODULES_PATH = 'C:/Users/Sebastian/AppData/Roaming/npm/node_modules';

// Try to set NODE_PATH if not set
if (!process.env.NODE_PATH) {
    process.env.NODE_PATH = GLOBAL_MODULES_PATH;
    console.log("🔧 Setting NODE_PATH programmatically");
}

// Module loading
let OpenAI, Anthropic;

try {
    // Method 1: Try standard import
    OpenAI = (await import('openai')).default;
    console.log("✅ OpenAI loaded via standard import");
} catch (error1) {
    try {
        // Method 2: Force explicit global path
        const openaiPath = path.join(GLOBAL_MODULES_PATH, 'openai', 'index.js').replace(/\\/g, '/');
        OpenAI = (await import(`file:///${openaiPath}`)).default;
        console.log("✅ OpenAI loaded via explicit global path");
    } catch (error2) {
        console.log("❌ OpenAI loading failed:");
        console.log(`   Error 1: ${error1.message}`);
        console.log(`   Error 2: ${error2.message}`);
        process.exit(1);
    }
}

try {
    Anthropic = (await import('@anthropic-ai/sdk')).default;
    console.log("✅ Anthropic SDK loaded via standard import");
} catch (error1) {
    try {
        const anthropicPath = path.join(GLOBAL_MODULES_PATH, '@anthropic-ai', 'sdk', 'index.js').replace(/\\/g, '/');
        Anthropic = (await import(`file:///${anthropicPath}`)).default;
        console.log("✅ Anthropic SDK loaded via explicit global path");
    } catch (error2) {
        console.log("⚠️ Anthropic SDK loading failed - continuing without Claude support");
        Anthropic = null;
    }
}

// Get current directory for ES modules
const __filename = fileURLToPath(import.meta.url);
const __dirname = path.dirname(__filename);

class CryptoAnalyst {
    constructor() {
        this.requiredSections = [
            { name: "🎯 Executive Summary", header: "## 🎯 Executive Summary" },
            { name: "📊 Analiza Techniczna", header: "## 📊 Analiza Techniczna" },
            { name: "🔍 Analiza Fundamentalna", header: "## 🔍 Analiza Fundamentalna" },
            { name: "🌊 Sentiment & On-chain", header: "## 🌊 Sentiment & On-chain" },
            { name: "⚠️ Risk Assessment", header: "## ⚠️ Risk Assessment" },
            { name: "🎯 Rekomendacje & Sygnały", header: "## 🎯 Rekomendacje & Sygnały" },
            { name: "📋 Disclaimer", header: "## 📋 Disclaimer" }
        ];

        this._setupClients();
        this._loadPrompt();
    }

    _setupClients() {
        // Setup OpenAI client
        const openaiKey = process.env.OPENAI_API_KEY;
        if (openaiKey) {
            this.openaiClient = new OpenAI({ apiKey: openaiKey });
            console.log("✅ OpenAI API key loaded successfully");
            console.log("✅ OpenAI client initialized and connected");
        } else {
            this.openaiClient = null;
            console.log("❌ OpenAI API key not found in environment");
            console.log("💡 Make sure .env file exists with OPENAI_API_KEY=your_key");
        }

        // Setup Anthropic client
        const anthropicKey = process.env.ANTHROPIC_API_KEY;
        if (anthropicKey && Anthropic) {
            this.anthropicClient = new Anthropic({ apiKey: anthropicKey });
            console.log("✅ Anthropic API key loaded successfully");
            console.log("✅ Claude client initialized and connected");
        } else {
            this.anthropicClient = null;
            if (!anthropicKey) {
                console.log("❌ Anthropic API key not found in environment");
            } else if (!Anthropic) {
                console.log("❌ Anthropic SDK not loaded");
            }
        }
    }

    _loadPrompt() {
        try {
            const possiblePaths = [
                path.resolve(__dirname, '../../system.md'),
                path.resolve(__dirname, '../../../system.md'),
                path.join(__dirname, '..', '..', 'system.md')
            ];

            let promptLoaded = false;
            for (const promptPath of possiblePaths) {
                try {
                    if (fs.existsSync(promptPath)) {
                        this.systemPrompt = fs.readFileSync(promptPath, 'utf-8');
                        console.log(`✅ System prompt loaded from: ${promptPath}`);
                        promptLoaded = true;
                        break;
                    }
                } catch (err) {
                    continue;
                }
            }

            if (!promptLoaded) {
                throw new Error("System prompt not found");
            }
        } catch (error) {
            this.systemPrompt = "You are a cryptocurrency market analyst.";
            console.log("⚠️ System prompt file not found - using fallback prompt");
        }
    }

    _validateResponseStructure(responseText) {
        const validationResults = {};
        const totalChars = responseText.length;

        console.log("\n📊 VALIDATING RESPONSE STRUCTURE:");
        console.log("=".repeat(50));

        for (const section of this.requiredSections) {
            const hasSection = responseText.includes(section.header);
            validationResults[section.name] = hasSection ? "✅ SUCCESS" : "❌ FAIL";
            console.log(`${section.name}: ${validationResults[section.name]}`);
        }

        const successfulSections = Object.values(validationResults)
            .filter(result => result.includes("SUCCESS")).length;
        const totalSections = this.requiredSections.length;

        console.log("=".repeat(50));
        console.log("📈 RESPONSE SUMMARY:");
        console.log(`   ✅ Successful sections: ${successfulSections}/${totalSections}`);
        console.log(`   📝 Total characters generated: ${totalChars.toLocaleString()}`);

        if (successfulSections === totalSections) {
            console.log("🎉 RESPONSE VALIDATION: ✅ SUCCESS - All required elements present!");
        } else {
            console.log(`⚠️  RESPONSE VALIDATION: ⚠️ PARTIAL - Missing ${totalSections - successfulSections} sections`);
        }

        return {
            validationResults,
            totalChars,
            successfulSections,
            totalSections,
            isComplete: successfulSections === totalSections
        };
    }

    async analyzeCryptoOpenAI(cryptoQuery, model = "gpt-5-nano") {
        if (!this.openaiClient) {
            return {
                success: false,
                error: "OpenAI client not available - check API key",
                response: null,
                validation: null
            };
        }

        try {
            console.log("\n🚀 STARTING ANALYSIS:");
            console.log(`   🤖 Model: ${model}`);
            console.log(`   🔗 API: OpenAI Responses API`);
            console.log(`   📝 Query: ${cryptoQuery.substring(0, 100)}...`);
            console.log("   ⏳ Processing...");

            const response = await this.openaiClient.responses.create({
                model: model,
                input: `${this.systemPrompt}\n\nUser query: ${cryptoQuery}`,
                reasoning: { effort: "medium" },
                text: { verbosity: "medium" },
                max_output_tokens: 16000,
                tools: [
                    { type: "web_search" }
                ]
            });

            const responseText = response.output_text;
            console.log("✅ AI response generated successfully!");

            const validationInfo = this._validateResponseStructure(responseText);

            return {
                success: true,
                modelUsed: model,
                response: responseText,
                validation: validationInfo,
                responseId: response.id || 'unknown'
            };

        } catch (error) {
            console.log(`❌ OpenAI API Error: ${error.message}`);
            return {
                success: false,
                error: error.message,
                response: null,
                validation: null
            };
        }
    }

    getAvailableModels() {
        const models = [];
        if (this.openaiClient) {
            models.push("gpt-5", "gpt-5-mini", "gpt-5-nano");
        }
        if (this.anthropicClient) {
            models.push("claude-3-5-haiku-20241022");
        }
        return models;
    }

    exportToFile(content, filename = "analysis.txt") {
        try {
            fs.writeFileSync(filename, content, 'utf-8');
            console.log(`✅ Analysis saved to ${filename}`);
            return true;
        } catch (error) {
            console.log(`❌ Failed to save: ${error.message}`);
            return false;
        }
    }
}

// Test function
async function runTest() {
    console.log("🧪 TESTING CRYPTO ANALYST CLIENT");
    console.log("=".repeat(40));
    
    // Debug info
    console.log("🔍 DEBUG INFO:");
    console.log(`   NODE_PATH: ${process.env.NODE_PATH || 'NOT SET'}`);
    console.log(`   OPENAI_API_KEY: ${process.env.OPENAI_API_KEY ? '***SET***' : 'NOT SET'}`);
    console.log(`   ANTHROPIC_API_KEY: ${process.env.ANTHROPIC_API_KEY ? '***SET***' : 'NOT SET'}`);

    const analyst = new CryptoAnalyst();

    if (analyst.openaiClient) {
        console.log("\n🔬 Running test analysis...");
        
        try {
            const testResult = await analyst.analyzeCryptoOpenAI(
                "Przeanalizuj Bitcoin (BTC) pod kątem obecnych trendów rynkowych",
                "gpt-5-nano"
            );

            if (testResult.success) {
                console.log("\n✅ TEST COMPLETED SUCCESSFULLY!");
                console.log(`   📊 Validation: ${testResult.validation.isComplete ? '✅ PASSED' : '⚠️ PARTIAL'}`);
            } else {
                console.log(`\n❌ TEST FAILED: ${testResult.error}`);
            }
        } catch (error) {
            console.log(`\n❌ TEST ERROR: ${error.message}`);
        }
    } else {
        console.log("\n❌ Cannot run test - OpenAI client not available");
    }
}

// Run test if executed directly
const isMainModule = process.argv[1] === fileURLToPath(import.meta.url);
if (isMainModule) {
    runTest().catch(error => {
        console.error(`❌ Test error: ${error.message}`);
        process.exit(1);
    });
}

export default CryptoAnalyst;
