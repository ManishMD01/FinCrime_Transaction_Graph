#!/bin/bash
set -e
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m'
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_ROOT="$(dirname "$SCRIPT_DIR")"
echo -e "${BLUE}FinCrime Entity Resolution Engine - Installation${NC}"
echo ""
echo -e "${BLUE}Step 1: Checking Prerequisites${NC}"
command -v python3 >/dev/null && echo -e "${GREEN}[✓]${NC} Python3 found"
command -v pip3 >/dev/null && echo -e "${GREEN}[✓]${NC} pip3 found"
echo ""
echo -e "${BLUE}Step 2: Setting Up Virtual Environment${NC}"
if [ ! -d "$PROJECT_ROOT/venv" ]; then
  python3 -m venv "$PROJECT_ROOT/venv"
  echo -e "${GREEN}[✓]${NC} Virtual environment created"
else
  echo -e "${GREEN}[✓]${NC} Virtual environment exists"
fi
source "$PROJECT_ROOT/venv/bin/activate"
pip install --upgrade pip >/dev/null 2>&1
echo ""
echo -e "${BLUE}Step 3: Installing Dependencies${NC}"
cd "$PROJECT_ROOT"
pip install -r requirements.txt
echo -e "${GREEN}[✓]${NC} Dependencies installed"
echo ""
echo -e "${BLUE}Step 4: Creating Directory Structure${NC}"
mkdir -p "$PROJECT_ROOT/data"/{incoming,loaded,unloaded,rejected,processed}
mkdir -p "$PROJECT_ROOT/web"/{uploads,results,assets}
mkdir -p "$PROJECT_ROOT/logs" "$PROJECT_ROOT/keys"
echo -e "${GREEN}[✓]${NC} Directories created"
echo ""
echo -e "${BLUE}Step 5: Configuring Environment${NC}"
CONFIG_DIR="$PROJECT_ROOT/bigquery/config"
if [ ! -f "$CONFIG_DIR/.env" ]; then
  cp "$CONFIG_DIR/.env.example" "$CONFIG_DIR/.env"
  echo -e "${YELLOW}[!]${NC} Please edit $CONFIG_DIR/.env with your GCP credentials"
  echo ""
  read -p "Would you like to configure now? (y/n): " configure_now
  if [ "$configure_now" = "y" ] || [ "$configure_now" = "Y" ]; then
    if command -v nano >/dev/null; then nano "$CONFIG_DIR/.env"; elif command -v vim >/dev/null; then vim "$CONFIG_DIR/.env"; fi
  fi
else
  echo -e "${GREEN}[✓]${NC} .env exists"
fi
echo ""
echo -e "${GREEN}Installation Complete!${NC}"
echo ""
echo "Next steps:"
echo "1. source venv/bin/activate"
echo "2. Update bigquery/config/.env with GCP credentials"
echo "3. python bigquery/etl/setup_bigquery.py"
echo "4. python example_usage.py"
echo "5. cd web && php -S localhost:8080"
