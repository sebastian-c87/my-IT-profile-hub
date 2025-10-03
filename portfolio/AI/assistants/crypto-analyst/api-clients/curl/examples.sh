#!/bin/bash
# =============================================================================
# Cryptocurrency Market Analyst - cURL Examples
# Advanced bash script demonstrating OpenAI Responses API and Anthropic API calls
# 
# Author: Sebastian C.
# License: CC-BY-NC-ND-4.0
# =============================================================================

# ============================
# BASH FUNDAMENTALS EXPLAINED
# ============================
# - #!/bin/bash          - "shebang" - informuje system, że to bash script
# - #                    - komentarz (jak // w JavaScript lub # w Python)
# - $VARIABLE            - odwołanie do zmiennej ($HOME, $USER, $PATH)
# - ${VARIABLE}          - bezpieczne odwołanie do zmiennej (gdy są inne znaki)
# - export VARIABLE=val  - eksport zmiennej do environment
# - function nazwa() {}  - definicja funkcji
# - if [ condition ]     - instrukcja warunkowa
# - curl                 - narzędzie do HTTP requests (jak fetch() w JS)

# ============================
# CONFIGURATION SECTION
# ============================

# Set script directory for relative paths
# $0 = nazwa pliku skryptu, dirname pobiera folder
SCRIPT_DIR="$(dirname "$0")"

# Color codes for pretty output (ANSI escape sequences)
RED='\033[0;31m'      # Czerwony
GREEN='\033[0;32m'    # Zielony
YELLOW='\033[1;33m'   # Żółty
BLUE='\033[0;34m'     # Niebieski
PURPLE='\033[0;35m'   # Purpurowy
CYAN='\033[0;36m'     # Cyjan
WHITE='\033[1;37m'    # Biały
NC='\033[0m'          # No Color - reset koloru

# API endpoints
OPENAI_URL="https://api.openai.com/v1/responses"
ANTHROPIC_URL="https://api.anthropic.com/v1/messages"
ANTHROPIC_BATCH_URL="https://api.anthropic.com/v1/messages/batches"

# Default models
DEFAULT_OPENAI_MODEL="gpt-5-nano"
DEFAULT_ANTHROPIC_MODEL="claude-3-5-haiku-20241022"

# ============================
# UTILITY FUNCTIONS
# ============================

# Function to print colored output
# Parametry: $1 = kolor, $2 = tekst
print_colored() {
    echo -e "${1}${2}${NC}"
}

# Function to print section headers
print_header() {
    echo ""
    print_colored $CYAN "==============================="
    print_colored $CYAN "  $1"
    print_colored $CYAN "==============================="
    echo ""
}

# Function to print step information
print_step() {
    print_colored $YELLOW "🔹 $1"
}

# Function to print success message
print_success() {
    print_colored $GREEN "✅ $1"
}

# Function to print error message
print_error() {
    print_colored $RED "❌ $1"
}

# Function to print info message
print_info() {
    print_colored $BLUE "ℹ️  $1"
}

# ============================
# VALIDATION FUNCTIONS
# ============================

# Check if required tools are installed
check_dependencies() {
    print_step "Checking dependencies..."
    
    # Array of required commands
    # W bash, arrays tworzymy tak: ARRAY=(element1 element2 element3)
    local required_commands=("curl" "jq")
    local missing_commands=()
    
    # Loop through required commands
    # for VARIABLE in ARRAY - pętla po elementach tablicy
    for cmd in "${required_commands[@]}"; do
        # command -v sprawdza czy komenda istnieje
        if ! command -v "$cmd" &> /dev/null; then
            missing_commands+=("$cmd")
        fi
    done
    
    # Check if any commands are missing
    # ${#ARRAY[@]} - długość tablicy
    if [ ${#missing_commands[@]} -gt 0 ]; then
        print_error "Missing required commands: ${missing_commands[*]}"
        print_info "Please install missing dependencies:"
        print_info "  Ubuntu/Debian: sudo apt-get install curl jq"
        print_info "  macOS: brew install curl jq"
        print_info "  Windows: Install via chocolatey or manually"
        return 1
    fi
    
    print_success "All dependencies are installed"
    return 0
}

# Check if API keys are set
check_api_keys() {
    print_step "Checking API keys..."
    
    local keys_missing=0
    
    # -z sprawdza czy zmienna jest pusta
    if [ -z "$OPENAI_API_KEY" ]; then
        print_error "OPENAI_API_KEY not set"
        keys_missing=1
    else
        # ${VARIABLE:0:20} - pierwsze 20 znaków zmiennej
        print_success "OpenAI API key found: ${OPENAI_API_KEY:0:20}..."
    fi
    
    if [ -z "$ANTHROPIC_API_KEY" ]; then
        print_error "ANTHROPIC_API_KEY not set"  
        keys_missing=1
    else
        print_success "Anthropic API key found: ${ANTHROPIC_API_KEY:0:20}..."
    fi
    
    if [ $keys_missing -eq 1 ]; then
        print_info "Please set your API keys:"
        print_info "  export OPENAI_API_KEY='your-openai-key'"
        print_info "  export ANTHROPIC_API_KEY='your-anthropic-key'"
        print_info "Or create a .env file in the same directory"
        return 1
    fi
    
    return 0
}

# Load environment variables from .env file if it exists
load_env() {
    local env_file="$SCRIPT_DIR/.env"
    
    # -f sprawdza czy plik istnieje i jest zwykłym plikiem
    if [ -f "$env_file" ]; then
        print_step "Loading environment variables from .env file..."
        
        # Read .env file line by line
        # while read - czyta plik linia po linii
        while IFS='=' read -r key value; do
            # Skip comments and empty lines
            # [[ ]] - extended test condition (bardziej zaawansowane niż [ ])
            # =~ - regex matching operator
            if [[ $key =~ ^[[:space:]]*# ]] || [[ -z $key ]]; then
                continue
            fi
            
            # Remove quotes from value
            # ${VARIABLE//pattern/replacement} - replace pattern with replacement
            value="${value//\"/}"
            value="${value//\'/}"
            
            # Export the variable
            export "$key"="$value"
            print_info "Loaded: $key"
            
        # < "$env_file" - przekierowanie pliku do while loop
        done < "$env_file"
        
        print_success "Environment variables loaded successfully"
    else
        print_info "No .env file found, using system environment variables"
    fi
}

# ============================
# SYSTEM PROMPT LOADER
# ============================

# Load system prompt from file
load_system_prompt() {
    local prompt_file="$SCRIPT_DIR/../../system.md"
    
    if [ -f "$prompt_file" ]; then
        # cat - wyświetla zawartość pliku
        SYSTEM_PROMPT=$(cat "$prompt_file")
        print_success "System prompt loaded from: $prompt_file"
    else
        SYSTEM_PROMPT="You are a cryptocurrency market analyst."
        print_info "Using fallback system prompt"
    fi
}

# ============================
# API CALL FUNCTIONS
# ============================

# OpenAI Responses API call
# Parametry: $1 = user query, $2 = model (optional)
call_openai_api() {
    local user_query="$1"
    local model="${2:-$DEFAULT_OPENAI_MODEL}"  # ${VAR:-default} - użyj default jeśli VAR jest pusty
    
    print_step "Making OpenAI Responses API call..."
    print_info "Model: $model"
    print_info "Query: ${user_query:0:100}..."  # Pierwsze 100 znaków
    
    # Create JSON payload using jq for proper escaping
    # jq -n - null input (tworzy JSON od zera)
    # --arg - przekazuje argument do jq
    local json_payload
    json_payload=$(jq -n \
        --arg model "$model" \
        --arg system_prompt "$SYSTEM_PROMPT" \
        --arg user_query "$user_query" \
        '{
            "model": $model,
            "input": ($system_prompt + "\n\nUser query: " + $user_query),
            "reasoning": {"effort": "medium"},
            "text": {"verbosity": "medium"}, 
            "max_output_tokens": 16000,
            "tools": [{"type": "web_search"}],
            "store": true
        }')
    
    # Make API call with curl
    local response
    # \\ - escape backslash w bash
    # 2>/dev/null - przekieruj stderr do /dev/null (ukryj błędy)
    response=$(curl -s \
        -X POST "$OPENAI_URL" \
        -H "Content-Type: application/json" \
        -H "Authorization: Bearer $OPENAI_API_KEY" \
        -d "$json_payload" \
        2>/dev/null)
    
    # Check if curl succeeded
    # $? - exit code ostatniej komendy (0 = success)
    if [ $? -ne 0 ]; then
        print_error "Failed to make API call to OpenAI"
        return 1
    fi
    
    # Check for API errors using jq
    local error_message
    error_message=$(echo "$response" | jq -r '.error.message // empty')
    
    if [ ! -z "$error_message" ]; then
        print_error "OpenAI API Error: $error_message"
        return 1
    fi
    
    print_success "OpenAI API call successful"
    
    # Save response to file with timestamp
    # date +%Y%m%d_%H%M%S - formatowanie daty
    local timestamp=$(date +%Y%m%d_%H%M%S)
    local output_file="$SCRIPT_DIR/outputs/openai_response_$timestamp.json"
    
    # Create outputs directory if it doesn't exist
    # -p - create parent directories if they don't exist
    mkdir -p "$SCRIPT_DIR/outputs"
    
    # Save full response
    echo "$response" | jq '.' > "$output_file"
    print_success "Full response saved to: $output_file"
    
    # Extract and display key information
    local output_text model_used response_id
    output_text=$(echo "$response" | jq -r '.output_text // "No output text found"')
    model_used=$(echo "$response" | jq -r '.model // "Unknown"')
    response_id=$(echo "$response" | jq -r '.id // "Unknown"')
    
    print_info "Response ID: $response_id"
    print_info "Model used: $model_used"
    print_info "Output length: ${#output_text} characters"
    
    # Create markdown file with formatted output
    local md_file="$SCRIPT_DIR/outputs/OpenAI_Analysis_$timestamp.md"
    {
        echo "# OpenAI Cryptocurrency Analysis"
        echo ""
        echo "**Generated:** $(date)"
        echo "**Model:** $model_used"  
        echo "**Response ID:** $response_id"
        echo "**Query:** $user_query"
        echo ""
        echo "---"
        echo ""
        echo "$output_text"
        echo ""
        echo "---"
        echo "*Generated using OpenAI Responses API via cURL*"
    } > "$md_file"
    
    print_success "Formatted analysis saved to: $md_file"
    
    return 0
}

# Anthropic Messages API call  
call_anthropic_api() {
    local user_query="$1"
    local model="${2:-$DEFAULT_ANTHROPIC_MODEL}"
    
    print_step "Making Anthropic Messages API call..."
    print_info "Model: $model"
    print_info "Query: ${user_query:0:100}..."
    
    # Create JSON payload
    local json_payload
    json_payload=$(jq -n \
        --arg model "$model" \
        --arg system_prompt "$SYSTEM_PROMPT" \
        --arg user_query "$user_query" \
        '{
            "model": $model,
            "max_tokens": 16000,
            "messages": [
                {
                    "role": "user",
                    "content": ($system_prompt + "\n\nUser query: " + $user_query)
                }
            ]
        }')
    
    # Make API call
    local response
    response=$(curl -s \
        -X POST "$ANTHROPIC_URL" \
        -H "Content-Type: application/json" \
        -H "x-api-key: $ANTHROPIC_API_KEY" \
        -H "anthropic-version: 2023-06-01" \
        -d "$json_payload" \
        2>/dev/null)
    
    if [ $? -ne 0 ]; then
        print_error "Failed to make API call to Anthropic"
        return 1
    fi
    
    # Check for errors
    local error_message
    error_message=$(echo "$response" | jq -r '.error.message // empty')
    
    if [ ! -z "$error_message" ]; then
        print_error "Anthropic API Error: $error_message"
        return 1
    fi
    
    print_success "Anthropic API call successful"
    
    # Save response
    local timestamp=$(date +%Y%m%d_%H%M%S)
    local output_file="$SCRIPT_DIR/outputs/anthropic_response_$timestamp.json"
    
    mkdir -p "$SCRIPT_DIR/outputs"
    echo "$response" | jq '.' > "$output_file"
    print_success "Full response saved to: $output_file"
    
    # Extract information
    local content_text model_used response_id usage_info
    content_text=$(echo "$response" | jq -r '.content[0].text // "No content found"')
    model_used=$(echo "$response" | jq -r '.model // "Unknown"')
    response_id=$(echo "$response" | jq -r '.id // "Unknown"')
    
    print_info "Response ID: $response_id"
    print_info "Model used: $model_used" 
    print_info "Output length: ${#content_text} characters"
    
    # Create markdown file
    local md_file="$SCRIPT_DIR/outputs/Claude_Analysis_$timestamp.md"
    {
        echo "# Claude Cryptocurrency Analysis"
        echo ""
        echo "**Generated:** $(date)"
        echo "**Model:** $model_used"
        echo "**Response ID:** $response_id"
        echo "**Query:** $user_query"
        echo ""
        echo "---"
        echo ""
        echo "$content_text"
        echo ""
        echo "---"
        echo "*Generated using Anthropic Messages API via cURL*"
    } > "$md_file"
    
    print_success "Formatted analysis saved to: $md_file"
    
    return 0
}

# Anthropic Batch API example
create_batch_analysis() {
    local symbols=("BTC" "ETH" "ADA" "SOL" "DOT")
    
    print_step "Creating Anthropic Batch analysis for multiple cryptocurrencies..."
    
    # Build requests array for batch
    local requests_json=""
    local counter=1
    
    for symbol in "${symbols[@]}"; do
        local query="Przeprowadź krótką analizę $symbol - trendy, poziomy S/R, sentiment. Focus na kluczowe informacje."
        
        # Build single request JSON
        local single_request
        single_request=$(jq -n \
            --arg custom_id "crypto-analysis-$symbol-$(date +%s)-$counter" \
            --arg model "$DEFAULT_ANTHROPIC_MODEL" \
            --arg system_prompt "$SYSTEM_PROMPT" \
            --arg user_query "$query" \
            '{
                "custom_id": $custom_id,
                "params": {
                    "model": $model,
                    "max_tokens": 8000,
                    "messages": [
                        {
                            "role": "user",
                            "content": ($system_prompt + "\n\nUser query: " + $user_query)
                        }
                    ]
                }
            }')
        
        # Add to requests array
        if [ "$counter" -eq 1 ]; then
            requests_json="[$single_request"
        else
            requests_json="$requests_json,$single_request"
        fi
        
        ((counter++))
    done
    
    requests_json="$requests_json]"
    
    # Create batch payload
    local batch_payload
    batch_payload=$(echo "$requests_json" | jq '{requests: .}')
    
    print_info "Creating batch with ${#symbols[@]} requests..."
    
    # Make batch API call
    local batch_response
    batch_response=$(curl -s \
        -X POST "$ANTHROPIC_BATCH_URL" \
        -H "Content-Type: application/json" \
        -H "x-api-key: $ANTHROPIC_API_KEY" \
        -H "anthropic-version: 2023-06-01" \
        -d "$batch_payload" \
        2>/dev/null)
    
    if [ $? -ne 0 ]; then
        print_error "Failed to create batch"
        return 1
    fi
    
    # Check for errors
    local error_message
    error_message=$(echo "$batch_response" | jq -r '.error.message // empty')
    
    if [ ! -z "$error_message" ]; then
        print_error "Batch API Error: $error_message"
        return 1
    fi
    
    # Extract batch info
    local batch_id batch_status
    batch_id=$(echo "$batch_response" | jq -r '.id')
    batch_status=$(echo "$batch_response" | jq -r '.processing_status')
    
    print_success "Batch created successfully!"
    print_info "Batch ID: $batch_id"
    print_info "Status: $batch_status"
    
    # Save batch info
    local timestamp=$(date +%Y%m%d_%H%M%S)
    local batch_file="$SCRIPT_DIR/outputs/batch_info_$timestamp.json"
    echo "$batch_response" | jq '.' > "$batch_file"
    
    print_info "Batch processing may take several minutes..."
    print_info "You can check batch status using: check_batch_status $batch_id"
    
    return 0
}

# ============================
# INTERACTIVE FUNCTIONS
# ============================

# Interactive menu
show_menu() {
    print_header "🚀 CRYPTOCURRENCY ANALYST - cURL EXAMPLES"
    
    print_colored $WHITE "Available options:"
    echo "1. 🔹 Test OpenAI Responses API (GPT-5)"  
    echo "2. 🔹 Test Anthropic Messages API (Claude)"
    echo "3. 🔹 Create Anthropic Batch Analysis"
    echo "4. 🔹 Custom OpenAI Analysis"
    echo "5. 🔹 Custom Claude Analysis"
    echo "6. 🔹 Compare Models (OpenAI vs Claude)"
    echo "7. 🔹 System Information"
    echo "0. 🔹 Exit"
    echo ""
}

# Get user input for crypto analysis
get_crypto_input() {
    local crypto_options=("Bitcoin (BTC)" "Ethereum (ETH)" "Cardano (ADA)" "Solana (SOL)" "Binance Coin (BNB)" "Custom")
    
    print_colored $YELLOW "💰 Select cryptocurrency:"
    for i in "${!crypto_options[@]}"; do
        echo "$((i+1)). ${crypto_options[$i]}"
    done
    
    echo -n "Your choice (1-6): "
    read choice
    
    # Validate input
    case $choice in
        1) echo "Bitcoin (BTC)" ;;
        2) echo "Ethereum (ETH)" ;;
        3) echo "Cardano (ADA)" ;;
        4) echo "Solana (SOL)" ;;
        5) echo "Binance Coin (BNB)" ;;
        6) 
            echo -n "Enter cryptocurrency symbol or name: "
            read custom_crypto
            echo "$custom_crypto"
            ;;
        *) echo "Bitcoin (BTC)" ;;  # Default
    esac
}

# Get analysis type
get_analysis_type() {
    local analysis_options=("Comprehensive" "Technical only" "Fundamental only" "Trading signals")
    
    print_colored $YELLOW "📊 Select analysis type:"
    for i in "${!analysis_options[@]}"; do
        echo "$((i+1)). ${analysis_options[$i]}"
    done
    
    echo -n "Your choice (1-4): "
    read choice
    
    case $choice in
        1) echo "comprehensive analysis including technical, fundamental, and sentiment analysis" ;;
        2) echo "technical analysis focusing on price patterns, indicators, and support/resistance levels" ;;
        3) echo "fundamental analysis focusing on project value, tokenomics, and development progress" ;;
        4) echo "trading signals with specific entry/exit points, stop-loss, and risk management" ;;
        *) echo "comprehensive analysis" ;;  # Default
    esac
}

# ============================
# MAIN EXECUTION FUNCTIONS
# ============================

# Main interactive loop
main() {
    # Initialize
    load_env
    
    # Check dependencies and API keys
    if ! check_dependencies || ! check_api_keys; then
        exit 1
    fi
    
    # Load system prompt
    load_system_prompt
    
    # Main loop
    while true; do
        show_menu
        
        echo -n "Enter your choice (0-7): "
        read choice
        
        case $choice in
            1)
                print_header "OpenAI Responses API Test"
                call_openai_api "Przeanalizuj Bitcoin (BTC) pod kątem obecnych trendów rynkowych" "$DEFAULT_OPENAI_MODEL"
                ;;
            2)
                print_header "Anthropic Messages API Test"
                call_anthropic_api "Przeanalizuj Ethereum (ETH) pod kątem obecnych trendów rynkowych" "$DEFAULT_ANTHROPIC_MODEL"
                ;;
            3)
                print_header "Anthropic Batch Analysis"
                create_batch_analysis
                ;;
            4)
                print_header "Custom OpenAI Analysis"
                local crypto=$(get_crypto_input)
                local analysis=$(get_analysis_type)
                local query="Przeprowadź $analysis dla $crypto. Proszę o szczegółową analizę z konkretnymi rekomendacjami."
                call_openai_api "$query"
                ;;
            5)
                print_header "Custom Claude Analysis"
                local crypto=$(get_crypto_input)
                local analysis=$(get_analysis_type)
                local query="Przeprowadź $analysis dla $crypto. Proszę o szczegółową analizę z konkretnymi rekomendacjami."
                call_anthropic_api "$query"
                ;;
            6)
                print_header "Model Comparison"
                local crypto=$(get_crypto_input)
                local query="Przeprowadź kompleksową analizę $crypto z rekomendacjami inwestycyjnymi."
                
                print_step "Running OpenAI analysis..."
                call_openai_api "$query"
                
                echo ""
                print_step "Running Claude analysis..."
                call_anthropic_api "$query"
                
                print_success "Both analyses completed! Check outputs folder for comparison."
                ;;
            7)
                print_header "System Information"
                print_info "Script directory: $SCRIPT_DIR"
                print_info "OpenAI API URL: $OPENAI_URL"
                print_info "Anthropic API URL: $ANTHROPIC_URL"
                print_info "Default OpenAI model: $DEFAULT_OPENAI_MODEL"
                print_info "Default Anthropic model: $DEFAULT_ANTHROPIC_MODEL"
                
                if [ -f "$SCRIPT_DIR/../../system.md" ]; then
                    local prompt_size=$(wc -c < "$SCRIPT_DIR/../../system.md")
                    print_info "System prompt size: $prompt_size characters"
                fi
                ;;
            0)
                print_colored $GREEN "👋 Thanks for using Crypto Analyst cURL examples!"
                break
                ;;
            *)
                print_error "Invalid choice. Please try again."
                ;;
        esac
        
        # Pause before showing menu again
        echo ""
        print_colored $CYAN "Press Enter to continue..."
        read
    done
}

# ============================
# SCRIPT EXECUTION
# ============================

# Check if script is run directly (not sourced)
# BASH_SOURCE[0] - nazwa skryptu
if [ "${BASH_SOURCE[0]}" = "${0}" ]; then
    main "$@"  # "$@" - wszystkie argumenty przekazane do skryptu
fi
