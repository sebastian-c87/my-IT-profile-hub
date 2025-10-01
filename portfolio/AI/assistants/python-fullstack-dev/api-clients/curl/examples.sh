#!/bin/bash

##############################################################################
# Python Full-Stack Developer Assistant - cURL Examples (Optimized)
# ==================================================================
#
# Optimized for GPT-5-nano (OpenAI Responses API) and Claude Batches API
# Uses actual system.md prompt from repository
#
# License: CC-BY-NC-ND-4.0
# Repository: https://github.com/sebastian-c87/my-IT-profile-hub
##############################################################################


set -e  # Exit on error

# Configuration
OUTPUT_DIR="./curl_outputs"
mkdir -p "$OUTPUT_DIR"

# Colors
RED='\033[0;31m'
GREEN='\033[0;32m'
BLUE='\033[0;34m'
NC='\033[0m'

# API Keys Check with Manual Override for Testing
check_api_keys() {
    # ============================================================================
    # 🔑 MIEJSCE NA KLUCZE API DO TESTÓW LOKALNYCH
    # ============================================================================
    # Odkomentuj i wstaw swoje klucze do testów, potem usuń przed commitem!
    #
    # OPENAI_API_KEY="sk-proj-Your_OPENAI_API_KEY"              # ← WSTAW TUTAJ
    # ANTHROPIC_API_KEY="sk-ant-api03-Your_ANTHROPIC_API_KEY"      # ← WSTAW TUTAJ
    #
    # ============================================================================
    
    # Check OpenAI API Key
    if [ -z "$OPENAI_API_KEY" ]; then
        echo -e "${RED}❌ OPENAI_API_KEY not set${NC}"
        echo "Set environment variable: export OPENAI_API_KEY='sk-...'"
        echo "Or uncomment the line above and add your key for testing"
        OPENAI_AVAILABLE=false
    else
        echo -e "${GREEN}✅ OpenAI API Key found${NC}"
        OPENAI_AVAILABLE=true
    fi
    
    # Check Claude API Key  
    if [ -z "$ANTHROPIC_API_KEY" ]; then
        echo -e "${RED}❌ ANTHROPIC_API_KEY not set${NC}"
        echo "Set environment variable: export ANTHROPIC_API_KEY='sk-ant-...'"
        echo "Or uncomment the line above and add your key for testing"
        CLAUDE_AVAILABLE=false
    else
        echo -e "${GREEN}✅ Claude API Key found${NC}"
        CLAUDE_AVAILABLE=true
    fi
    
    # Must have at least one key
    if [ "$OPENAI_AVAILABLE" = false ] && [ "$CLAUDE_AVAILABLE" = false ]; then
        echo -e "${RED}❌ No API keys available. Cannot proceed.${NC}"
        exit 1
    fi
}

# Load system prompt from actual file
load_system_prompt() {
    if [ -f "../../system.md" ]; then
        cat "../../system.md"
    else
        echo -e "${RED}BŁĄD: Nie znaleziono pliku system.md${NC}" >&2
        echo "Sprawdź czy jesteś w folderze: portfolio/AI/assistants/python-fullstack-dev/api-clients/curl/"
        exit 1
    fi
}

# OpenAI Responses API (GPT-5-nano)
call_openai() {
    local app_idea="$1"
    local requirements="$2"
    
    if [ "$OPENAI_AVAILABLE" = false ]; then
        echo -e "${RED}❌ OpenAI API key not available${NC}"
        return 1
    fi
    
    local system_prompt
    system_prompt=$(load_system_prompt)
    
    local user_message="**Pomysł na aplikację:** $app_idea

**Dodatkowe wymagania:** ${requirements:-Brak}"
    
    echo -e "${BLUE}📡 Calling OpenAI Responses API (GPT-5-nano)...${NC}"
    
    local response
    response=$(curl -s "https://api.openai.com/v1/responses" \
        -H "Content-Type: application/json" \
        -H "Authorization: Bearer $OPENAI_API_KEY" \
        -d "{
            \"model\": \"gpt-5-nano\",
            \"instructions\": $(printf '%s' "$system_prompt" | jq -R -s .),
            \"input\": $(printf '%s' "$user_message" | jq -R -s .),
            \"reasoning\": {\"effort\": \"minimal\"},
            \"text\": {\"verbosity\": \"low\"},
            \"store\": false
        }")
    
    # Check for API error first
    if echo "$response" | jq -e '.error' > /dev/null 2>&1; then
        echo -e "${RED}❌ API Error:${NC}"
        echo "$response" | jq -r '.error.message'
        return 1
    
    # Check for new response format - multiple possible fields
    elif echo "$response" | jq -e '.status == "completed"' > /dev/null 2>&1; then
        echo -e "${GREEN}✅ Success!${NC}"
        
        # Try different content fields (OpenAI keeps changing this)
        local content=""
        
        # Option 1: output_text field
        if echo "$response" | jq -e '.output_text' > /dev/null 2>&1; then
            content=$(echo "$response" | jq -r '.output_text')
        
        # Option 2: choices array (like Chat Completions)
        elif echo "$response" | jq -e '.choices[0].message.content' > /dev/null 2>&1; then
            content=$(echo "$response" | jq -r '.choices[0].message.content')
        
        # Option 3: output field
        elif echo "$response" | jq -e '.output' > /dev/null 2>&1; then
            content=$(echo "$response" | jq -r '.output')
        
        # Option 4: response field
        elif echo "$response" | jq -e '.response' > /dev/null 2>&1; then
            content=$(echo "$response" | jq -r '.response')
            
        # Option 5: text field
        elif echo "$response" | jq -e '.text' > /dev/null 2>&1; then
            content=$(echo "$response" | jq -r '.text')
            
        else
            echo -e "${RED}❌ Could not extract content from response${NC}"
            echo -e "${BLUE}Available fields:${NC}"
            echo "$response" | jq 'keys'
            return 1
        fi
        
        if [ -n "$content" ] && [ "$content" != "null" ]; then
            local char_count=$(echo "$content" | wc -c)
            echo -e "${GREEN}📊 Generated: $char_count characters${NC}"
            
            # Show token usage if available
            local tokens=$(echo "$response" | jq -r '.usage.total_tokens // "N/A"')
            echo -e "${GREEN}📊 Tokens used: $tokens${NC}"
            
            # Save and show preview
            local output_file="$OUTPUT_DIR/openai_result_$(date +%Y%m%d_%H%M%S).md"
            echo "$content" > "$output_file"
            echo -e "${GREEN}💾 Saved to: $output_file${NC}"
            echo ""
            echo -e "${BLUE}📝 Preview (first 20 lines):${NC}"
            echo "$content" | head -20
            echo ""
            echo -e "${BLUE}... [truncated for readability - full content saved to file]${NC}"
        else
            echo -e "${RED}❌ Empty content received${NC}"
            return 1
        fi
        
    else
        echo -e "${RED}❌ Unexpected response format:${NC}"
        echo "$response" | jq -r '.' | head -10
        echo ""
        echo -e "${BLUE}Debug - Available fields:${NC}"
        echo "$response" | jq 'keys'
        return 1
    fi
}


# Claude Message Batches API (50% discount)
call_claude_batch() {
    local app_idea="$1"
    local requirements="$2"
    
    if [ "$CLAUDE_AVAILABLE" = false ]; then
        echo -e "${RED}❌ Claude API key not available${NC}"
        return 1
    fi
    
    local system_prompt
    system_prompt=$(load_system_prompt)
    
    local user_message="**Pomysł na aplikację:** $app_idea

**Dodatkowe wymagania:** ${requirements:-Brak}"
    
    echo -e "${BLUE}📦 Creating Claude batch (50% discount)...${NC}"
    
    # Create batch
    local batch_response
    batch_response=$(curl -s "https://api.anthropic.com/v1/messages/batches" \
        -H "Content-Type: application/json" \
        -H "x-api-key: $ANTHROPIC_API_KEY" \
        -H "anthropic-version: 2023-06-01" \
        -d "{
            \"requests\": [{
                \"custom_id\": \"app-$(date +%s)\",
                \"params\": {
                    \"model\": \"claude-3-5-haiku-20241022\",
                    \"max_tokens\": 8192,
                    \"system\": $(printf '%s' "$system_prompt" | jq -R -s .),
                    \"messages\": [{\"role\": \"user\", \"content\": $(printf '%s' "$user_message" | jq -R -s .)}]
                }
            }]
        }")
    
    local batch_id
    batch_id=$(echo "$batch_response" | jq -r '.id // empty')
    
    if [ -z "$batch_id" ]; then
        echo -e "${RED}❌ Batch creation failed${NC}"
        echo "$batch_response" | jq -r '.error.message // "Unknown error"'
        return 1
    fi
    
    echo -e "${BLUE}📦 Batch ID: $batch_id${NC}"
    echo -e "${BLUE}⏳ Waiting for completion (max 10 min for demo)...${NC}"
    
    # Poll for completion (reduced for demo)
    for i in {1..10}; do
        sleep 30
        echo -e "${BLUE}🔄 Check $i/10...${NC}"
        
        local status_response
        status_response=$(curl -s "https://api.anthropic.com/v1/messages/batches/$batch_id" \
            -H "x-api-key: $ANTHROPIC_API_KEY" \
            -H "anthropic-version: 2023-06-01")
        
        local status
        status=$(echo "$status_response" | jq -r '.processing_status')
        
        if [ "$status" = "ended" ]; then
            echo -e "${GREEN}✅ Batch completed!${NC}"
            
            # Get results
            local results_response
            results_response=$(curl -s "https://api.anthropic.com/v1/messages/batches/$batch_id/results" \
                -H "x-api-key: $ANTHROPIC_API_KEY" \
                -H "anthropic-version: 2023-06-01")
            
            local content=$(echo "$results_response" | jq -r '.results[0].result.message.content[0].text // "No content"')
            local char_count=$(echo "$content" | wc -c)
            echo -e "${GREEN}📊 Generated: $char_count characters${NC}"
            
            # Show token usage
            local tokens_in=$(echo "$results_response" | jq -r '.results[0].result.message.usage.input_tokens // 0')
            local tokens_out=$(echo "$results_response" | jq -r '.results[0].result.message.usage.output_tokens // 0')
            local tokens_total=$((tokens_in + tokens_out))
            echo -e "${GREEN}📊 Tokens used: $tokens_total (50% discount applied)${NC}"
            
            # Save and show preview
            echo "$content" > "$OUTPUT_DIR/claude_result_$(date +%Y%m%d_%H%M%S).md"
            echo -e "${GREEN}💾 Saved to: $OUTPUT_DIR/claude_result_$(date +%Y%m%d_%H%M%S).md${NC}"
            echo ""
            echo -e "${BLUE}📝 Preview (first 20 lines):${NC}"
            echo "$content" | head -20
            echo ""
            echo -e "${BLUE}... [truncated for readability - full content saved to file]${NC}"
            
            return 0
        elif [ "$status" = "failed" ]; then
            echo -e "${RED}❌ Batch failed${NC}"
            return 1
        fi
    done
    
    echo -e "${RED}⏰ Timeout - check batch manually: $batch_id${NC}"
    echo "Check status: curl 'https://api.anthropic.com/v1/messages/batches/$batch_id' -H 'x-api-key: \$ANTHROPIC_API_KEY' -H 'anthropic-version: 2023-06-01'"
    return 1
}

# Main menu
main_menu() {
    echo -e "${BLUE}🤖 Python Full-Stack Developer Assistant - cURL Examples${NC}"
    echo -e "${BLUE}============================================================${NC}"
    echo ""
    
    # Show available providers
    if [ "$OPENAI_AVAILABLE" = true ]; then
        echo -e "${GREEN}✅ OpenAI GPT-5-nano available${NC}"
    else
        echo -e "${RED}❌ OpenAI not available${NC}"
    fi
    
    if [ "$CLAUDE_AVAILABLE" = true ]; then
        echo -e "${GREEN}✅ Claude Haiku Batch available${NC}"
    else
        echo -e "${RED}❌ Claude not available${NC}"
    fi
    
    echo ""
    echo "Choose an option:"
    
    if [ "$OPENAI_AVAILABLE" = true ]; then
        echo "1. 🏃‍♂️ Quick Test - OpenAI GPT-5-nano"
    fi
    
    if [ "$CLAUDE_AVAILABLE" = true ]; then
        echo "2. 📦 Advanced Test - Claude Batch (50% discount)"
    fi
    
    if [ "$OPENAI_AVAILABLE" = true ] && [ "$CLAUDE_AVAILABLE" = true ]; then
        echo "3. ⚖️  Provider Comparison"
    fi
    
    echo "4. ✏️  Custom Application Test"
    echo "5. 🚪 Exit"
    echo ""
}

# Example functions
example_openai() {
    echo -e "${BLUE}🏃‍♂️ QUICK TEST - OpenAI GPT-5-nano${NC}"
    call_openai "Task management app with kanban board" "FastAPI backend, React frontend, PostgreSQL, JWT authentication"
}

example_claude() {
    echo -e "${BLUE}📦 ADVANCED TEST - Claude Batch (50% discount)${NC}"
    call_claude_batch "E-commerce platform with payment integration" "Django REST Framework, React TypeScript, PostgreSQL, Stripe API, Docker deployment"
}

example_comparison() {
    if [ "$OPENAI_AVAILABLE" = false ] || [ "$CLAUDE_AVAILABLE" = false ]; then
        echo -e "${RED}❌ Both providers needed for comparison${NC}"
        return 1
    fi
    
    echo -e "${BLUE}⚖️  PROVIDER COMPARISON${NC}"
    local app_idea="Social media dashboard with analytics"
    local requirements="Python backend, React frontend, real-time updates via WebSockets"
    
    echo -e "${BLUE}Testing OpenAI GPT-5-nano...${NC}"
    call_openai "$app_idea" "$requirements"
    
    echo ""
    echo -e "${BLUE}Testing Claude Haiku Batch...${NC}"
    call_claude_batch "$app_idea" "$requirements"
}

example_custom() {
    echo -e "${BLUE}✏️  CUSTOM APPLICATION TEST${NC}"
    
    read -p "💡 Describe your application idea: " app_idea
    read -p "📋 Technical requirements (optional): " requirements
    
    if [ "$OPENAI_AVAILABLE" = true ] && [ "$CLAUDE_AVAILABLE" = true ]; then
        echo ""
        echo "Choose provider:"
        echo "1. OpenAI GPT-5-nano (fast & cheap)"
        echo "2. Claude Haiku Batch (50% discount)"
        read -p "👉 Choice (1-2): " provider_choice
        
        case $provider_choice in
            1) call_openai "$app_idea" "$requirements" ;;
            2) call_claude_batch "$app_idea" "$requirements" ;;
            *) echo -e "${RED}❌ Invalid choice${NC}" ;;
        esac
    elif [ "$OPENAI_AVAILABLE" = true ]; then
        call_openai "$app_idea" "$requirements"
    elif [ "$CLAUDE_AVAILABLE" = true ]; then
        call_claude_batch "$app_idea" "$requirements"
    fi
}

# Check dependencies
check_dependencies() {
    command -v curl >/dev/null || { echo -e "${RED}❌ curl required${NC}"; exit 1; }
    command -v jq >/dev/null || { echo -e "${RED}❌ jq required${NC}"; exit 1; }
}

# Main execution
main() {
    # Header
    echo -e "${BLUE}Python Full-Stack Developer Assistant - cURL Examples${NC}"
    echo -e "${BLUE}Repository: https://github.com/sebastian-c87/my-IT-profile-hub${NC}"
    echo -e "${BLUE}License: CC-BY-NC-ND-4.0${NC}"
    echo ""
    
    # Checks
    check_dependencies
    check_api_keys
    
    # Handle command line arguments
    if [ $# -eq 0 ]; then
        # Interactive mode
        while true; do
            main_menu
            read -p "👉 Choose option: " choice
            
            case $choice in
                1)
                    if [ "$OPENAI_AVAILABLE" = true ]; then
                        example_openai
                    else
                        echo -e "${RED}❌ OpenAI not available${NC}"
                    fi
                    ;;
                2)
                    if [ "$CLAUDE_AVAILABLE" = true ]; then
                        example_claude
                    else
                        echo -e "${RED}❌ Claude not available${NC}"
                    fi
                    ;;
                3)
                    if [ "$OPENAI_AVAILABLE" = true ] && [ "$CLAUDE_AVAILABLE" = true ]; then
                        example_comparison
                    else
                        echo -e "${RED}❌ Both providers needed${NC}"
                    fi
                    ;;
                4)
                    example_custom
                    ;;
                5)
                    echo -e "${GREEN}👋 Thanks for testing!${NC}"
                    break
                    ;;
                *)
                    echo -e "${RED}❌ Invalid choice${NC}"
                    ;;
            esac
            
            echo ""
            read -p "⏸️  Press Enter to continue..."
            echo ""
        done
    else
        # Command line mode
        case $1 in
            "openai")
                if [ "$OPENAI_AVAILABLE" = true ]; then
                    call_openai "${2:-Simple web app}" "${3:-}"
                else
                    echo -e "${RED}❌ OpenAI not available${NC}"
                    exit 1
                fi
                ;;
            "claude")
                if [ "$CLAUDE_AVAILABLE" = true ]; then
                    call_claude_batch "${2:-Simple web app}" "${3:-}"
                else
                    echo -e "${RED}❌ Claude not available${NC}"
                    exit 1
                fi
                ;;
            *)
                echo "Usage: $0 [openai|claude] [app_idea] [requirements]"
                exit 1
                ;;
        esac
    fi
}

# Execute main function
main "$@"
