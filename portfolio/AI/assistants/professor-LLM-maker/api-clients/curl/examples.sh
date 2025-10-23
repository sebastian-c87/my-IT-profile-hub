#!/bin/bash

################################################################################
# LLM Engineering Professor - cURL Examples
################################################################################

GREEN='\033[0;32m'
BLUE='\033[0;34m'
YELLOW='\033[1;33m'
RED='\033[0;31m'
NC='\033[0m'

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
ENV_FILE="$SCRIPT_DIR/.env"

load_env() {
    if [ -f "$ENV_FILE" ]; then
        echo -e "${GREEN}✅ Ładowanie zmiennych z $ENV_FILE${NC}"
        export $(grep -v '^#' "$ENV_FILE" | xargs)
    else
        echo -e "${RED}❌ Plik .env nie znaleziony${NC}"
        exit 1
    fi
}

check_api_keys() {
    if [ -z "$OPENAI_API_KEY" ]; then
        echo -e "${RED}❌ OPENAI_API_KEY nie jest ustawiony${NC}"
        exit 1
    fi
    
    if [ -z "$ANTHROPIC_API_KEY" ]; then
        echo -e "${YELLOW}⚠️  ANTHROPIC_API_KEY nie jest ustawiony${NC}"
    fi
}

example_openai_single() {
    echo ""
    echo -e "${BLUE}================================================================${NC}"
    echo -e "${BLUE}PRZYKŁAD 1: OpenAI Responses API - Pojedyncze pytanie${NC}"
    echo -e "${BLUE}================================================================${NC}"
    echo ""
    
    SYSTEM_PROMPT=$(cat "$SCRIPT_DIR/../../system.md" 2>/dev/null || echo "Expert LLM Engineer")
    QUESTION="Jak stworzyć tokenizer BPE w Pythonie?"
    
    echo -e "${GREEN}📤 Wysyłam zapytanie do OpenAI (gpt-5-nano)...${NC}"
    echo -e "${YELLOW}   Pytanie: $QUESTION${NC}"
    echo ""
    
    PAYLOAD=$(cat <<EOF
{
  "model": "gpt-5-nano",
  "instructions": $(echo "$SYSTEM_PROMPT" | jq -sR .),
  "input": "## Pytanie o LLM Engineering\n$QUESTION\n\n## Poziom skomplikowania\nintermediate",
  "tools": [{"type": "web_search"}],
  "tool_choice": "auto",
  "reasoning": {"effort": "medium"},
  "text": {"verbosity": "medium"},
  "max_output_tokens": 16000,
  "store": true
}
EOF
)
    
    RESPONSE=$(curl -s https://api.openai.com/v1/responses \
        -H "Content-Type: application/json" \
        -H "Authorization: Bearer $OPENAI_API_KEY" \
        -d "$PAYLOAD")
    
    if echo "$RESPONSE" | jq -e '.error' > /dev/null 2>&1; then
        echo -e "${RED}❌ Błąd API:${NC}"
        echo "$RESPONSE" | jq '.error'
        return 1
    fi
    
    # POPRAWKA: Wyciągnij CAŁY tekst (usuń | head -n 1)
    OUTPUT_TEXT=$(echo "$RESPONSE" | jq -r '
        .output[]? 
        | select(.type == "message") 
        | .content[]? 
        | select(.type == "output_text") 
        | .text
    ')
    
    if [ -z "$OUTPUT_TEXT" ] || [ "$OUTPUT_TEXT" == "null" ]; then
        echo -e "${RED}❌ Brak tekstu w odpowiedzi${NC}"
        echo "$RESPONSE" | jq '.' > "$SCRIPT_DIR/debug_response.json"
        return 1
    fi
    
    echo -e "${GREEN}✅ Odpowiedź otrzymana!${NC}"
    echo ""
    echo -e "${BLUE}📄 Pełna odpowiedź (czytelna):${NC}"
    echo ""
    # Dekoduj unicode escapes i wyświetl czytelnie
    echo "$OUTPUT_TEXT" | sed 's/\\n/\n/g' | head -100
    echo ""
    echo -e "${YELLOW}... (pierwsze 100 linii, pełna w pliku JSON)${NC}"
    echo ""
    
    echo -e "${BLUE}📊 Metadata:${NC}"
    echo "   Model: $(echo "$RESPONSE" | jq -r '.model')"
    echo "   Response ID: $(echo "$RESPONSE" | jq -r '.id')"
    echo "   Długość: $(echo "$OUTPUT_TEXT" | wc -c) znaków"
    echo "   Input tokens: $(echo "$RESPONSE" | jq -r '.usage.input_tokens')"
    echo "   Output tokens: $(echo "$RESPONSE" | jq -r '.usage.output_tokens')"
    echo ""
    
    # Zapisz pełny JSON
    OUTPUT_FILE="$SCRIPT_DIR/output_openai_$(date +%Y%m%d_%H%M%S).json"
    echo "$RESPONSE" > "$OUTPUT_FILE"
    
    # Zapisz CZYTELNY tekst (bez unicode escapes)
    TEXT_FILE="$SCRIPT_DIR/output_openai_$(date +%Y%m%d_%H%M%S).txt"
    echo "$OUTPUT_TEXT" | sed 's/\\n/\n/g' > "$TEXT_FILE"
    
    echo -e "${GREEN}💾 Pełna odpowiedź JSON: $OUTPUT_FILE${NC}"
    echo -e "${GREEN}📄 Czytelny tekst: $TEXT_FILE${NC}"
}


example_openai_multiturn() {
    echo ""
    echo -e "${BLUE}================================================================${NC}"
    echo -e "${BLUE}PRZYKŁAD 2: OpenAI Responses API - Multi-turn${NC}"
    echo -e "${BLUE}================================================================${NC}"
    echo ""
    
    echo -e "${GREEN}📤 Pytanie 1: Co to jest tokenizacja?${NC}"
    
    RESPONSE1=$(curl -s https://api.openai.com/v1/responses \
        -H "Content-Type: application/json" \
        -H "Authorization: Bearer $OPENAI_API_KEY" \
        -d '{
          "model": "gpt-5-nano",
          "input": "Co to jest tokenizacja w NLP?",
          "reasoning": {"effort": "low"},
          "text": {"verbosity": "low"},
          "store": true
        }')
    
    RESPONSE1_ID=$(echo "$RESPONSE1" | jq -r '.id')
    echo -e "${GREEN}✅ Odpowiedź 1 (ID: $RESPONSE1_ID)${NC}"
    echo ""
    
    echo -e "${GREEN}📤 Pytanie 2: Jakie są popularne algorytmy?${NC}"
    
    RESPONSE2=$(curl -s https://api.openai.com/v1/responses \
        -H "Content-Type: application/json" \
        -H "Authorization: Bearer $OPENAI_API_KEY" \
        -d "{
          \"model\": \"gpt-5-nano\",
          \"input\": \"Jakie są popularne algorytmy tokenizacji?\",
          \"previous_response_id\": \"$RESPONSE1_ID\",
          \"reasoning\": {\"effort\": \"low\"},
          \"text\": {\"verbosity\": \"low\"},
          \"store\": true
        }")
    
    OUTPUT2=$(echo "$RESPONSE2" | jq -r '.output_text // .output[0].content // empty')
    echo -e "${GREEN}✅ Odpowiedź 2 (z kontekstem):${NC}"
    echo "$OUTPUT2" | head -c 500
    echo "..."
}

example_anthropic_single() {
    echo ""
    echo -e "${BLUE}================================================================${NC}"
    echo -e "${BLUE}PRZYKŁAD 3: Anthropic Messages API${NC}"
    echo -e "${BLUE}================================================================${NC}"
    echo ""
    
    if [ -z "$ANTHROPIC_API_KEY" ]; then
        echo -e "${RED}❌ ANTHROPIC_API_KEY nie jest ustawiony${NC}"
        return 1
    fi
    
    SYSTEM_PROMPT=$(sed '1s/^\xEF\xBB\xBF//' "$SCRIPT_DIR/../../system.md")
    QUESTION="Czym jest RLHF i jak go zastosować?"
    
    echo -e "${GREEN}📤 Wysyłam do Anthropic (Claude 4)...${NC}"
    
    PAYLOAD=$(cat <<EOF
{
  "model": "claude-sonnet-4-20250514",
  "max_tokens": 16000,
  "system": $(echo "$SYSTEM_PROMPT" | jq -sR .),
  "messages": [
    {
      "role": "user",
      "content": "## Pytanie\n$QUESTION\n\n## Poziom\nintermediate"
    }
  ]
}
EOF
)
    
    RESPONSE=$(curl -s https://api.anthropic.com/v1/messages \
        -H "Content-Type: application/json" \
        -H "x-api-key: $ANTHROPIC_API_KEY" \
        -H "anthropic-version: 2023-06-01" \
        -d "$PAYLOAD")
    
    if echo "$RESPONSE" | jq -e '.error' > /dev/null 2>&1; then
        echo -e "${RED}❌ Błąd:${NC}"
        echo "$RESPONSE" | jq '.error'
        return 1
    fi
    
    OUTPUT=$(echo "$RESPONSE" | jq -r '.content[0].text')
    echo -e "${GREEN}✅ Odpowiedź otrzymana${NC}"
    echo "$OUTPUT" | head -c 500
    echo "..."
}

show_menu() {
    echo ""
    echo -e "${BLUE}================================================================${NC}"
    echo -e "${BLUE}      LLM Engineering Professor - cURL Examples${NC}"
    echo -e "${BLUE}================================================================${NC}"
    echo ""
    echo "1) OpenAI - Pojedyncze pytanie"
    echo "2) OpenAI - Multi-turn"
    echo "3) Anthropic - Pojedyncze pytanie"
    echo "0) Wyjście"
    echo ""
    echo -n "Wybór: "
}

main() {
    load_env
    check_api_keys
    
    if ! command -v jq &> /dev/null; then
        echo -e "${RED}❌ jq nie jest zainstalowane${NC}"
        exit 1
    fi
    
    if [ $# -eq 1 ]; then
        case $1 in
            1) example_openai_single ;;
            2) example_openai_multiturn ;;
            3) example_anthropic_single ;;
            *) echo "Nieprawidłowy numer"; exit 1 ;;
        esac
        exit 0
    fi
    
    while true; do
        show_menu
        read -r choice
        
        case $choice in
            1) example_openai_single ;;
            2) example_openai_multiturn ;;
            3) example_anthropic_single ;;
            0) echo -e "${GREEN}👋 Do zobaczenia!${NC}"; exit 0 ;;
            *) echo -e "${RED}❌ Nieprawidłowy wybór${NC}" ;;
        esac
    done
}

main "$@"
