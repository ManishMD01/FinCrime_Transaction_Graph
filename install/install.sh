#!/bin/bash

# FinCrime Entity Resolution Engine - Installation Script
# This script installs and configures the project for any environment

set -e

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Get project root directory
SCRIPT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"
PROJECT_ROOT="$(dirname "$SCRIPT_DIR")"

echo -e "${BLUE}"
echo "╔══════════════════════════════════════════════════════════════╗"
echo "║   FinCrime Entity Resolution Engine - Installation           ║"
echo "╚══════════════════════════════════════════════════════════════╝"
echo -e "${NC}"

# Function to print status
print_status() {
    echo -e "${GREEN}[✓]${NC} $1"
}

print_warning() {
    echo -e "${YELLOW}[!]${NC} $1"
}

print_error() {
    echo -e "${RED}[✗]${NC} $1"
}

print_info() {
    echo -e "${BLUE}[i]${NC} $1"
}

# Check prerequisites
echo -e "\n${BLUE}Step 1: Checking Prerequisites${NC}"
echo "=================================="

# Check Python
if command -v python3 &> /dev/null; then
    PYTHON_VERSION=$(python3 --version | cut -d' ' -f2)
    print_status "Python3 found: $PYTHON_VERSION"
else
    print_error "Python3 not found. Please install Python 3.9+"
    exit 1
fi

# Check pip
if command -v pip3 &> /dev/null; then
    print_status "pip3 found"
else
    print_error "pip3 not found. Please install pip"
    exit 1
fi

# Check git
if command -v git &> /dev/null; then
    print_status "git found"
else
    print_warning "git not found (optional)"
fi

# Check gcloud
if command -v gcloud &> /dev/null; then
    print_status "gcloud CLI found"
else
    print_warning "gcloud CLI not found (optional but recommended)"
fi

# Create virtual environment
echo -e "\n${BLUE}Step 2: Setting Up Virtual Environment${NC}"
echo "=========================================="

if [ ! -d "$PROJECT_ROOT/venv" ]; then
    print_info "Creating virtual environment..."
    cd "$PROJECT_ROOT"
    python3 -m venv venv
    print_status "Virtual environment created"
else
    print_status "Virtual environment already exists"
fi

# Activate virtual environment
print_info "Activating virtual environment..."
source "$PROJECT_ROOT/venv/bin/activate"

# Upgrade pip
print_info "Upgrading pip..."
pip install --upgrade pip > /dev/null 2>&1
print_status "pip upgraded"

# Install dependencies
echo -e "\n${BLUE}Step 3: Installing Dependencies${NC}"
echo "==================================="

print_info "Installing Python packages from requirements.txt..."
cd "$PROJECT_ROOT"
pip install -r requirements.txt
print_status "Dependencies installed"

# Create necessary directories
echo -e "\n${BLUE}Step 4: Creating Directory Structure${NC}"
echo "=========================================="

mkdir -p "$PROJECT_ROOT"/{data,logs,uploads,results,keys}
mkdir -p "$PROJECT_ROOT/web"/{uploads,results,assets}
print_status "Directories created"

# Setup configuration
echo -e "\n${BLUE}Step 5: Configuring Environment${NC}"
echo "===================================""

CONFIG_DIR="$PROJECT_ROOT/bigquery/config"
if [ ! -f "$CONFIG_DIR/.env" ]; then
    print_info "Creating .env from template..."
    cp "$CONFIG_DIR/.env.example" "$CONFIG_DIR/.env"
    print_warning "Please edit $CONFIG_DIR/.env with your GCP credentials"
    echo -e "\n${YELLOW}Would you like to configure now? (y/n)${NC}"
    read -r configure_now
    if [ "$configure_now" = "y" ] || [ "$configure_now" = "Y" ]; then
        if command -v nano &> /dev/null; then
            nano "$CONFIG_DIR/.env"
        elif command -v vim &> /dev/null; then
            vim "$CONFIG_DIR/.env"
        else
            print_info "Please edit manually: $CONFIG_DIR/.env"
        fi
    fi
else
    print_status ".env already exists"
fi

# Copy install config if exists
if [ -f "$SCRIPT_DIR/config/.env" ] && [ ! -f "$CONFIG_DIR/.env" ]; then
    cp "$SCRIPT_DIR/config/.env" "$CONFIG_DIR/.env"
    print_status "Copied config from install directory"
fi

# Make scripts executable
echo -e "\n${BLUE}Step 6: Setting Permissions${NC}"
echo "=============================="
chmod +x "$PROJECT_ROOT/bigquery/etl/"*.py 2>/dev/null || true
chmod +x "$PROJECT_ROOT/example_usage.py" 2>/dev/null || true
print_status "Permissions set"

# BigQuery Setup
echo -e "\n${BLUE}Step 7: BigQuery Setup${NC}"
echo "========================"

# Check if .env has valid config
cd "$PROJECT_ROOT"
if [ -f "$CONFIG_DIR/.env" ]; then
    # Check if project ID is set
    if grep -q "GCP_PROJECT_ID=your-gcp-project-id" "$CONFIG_DIR/.env" || grep -q "^GCP_PROJECT_ID=$" "$CONFIG_DIR/.env"; then
        print_warning "GCP_PROJECT_ID not configured in .env"
        echo -e "${YELLOW}Do you want to setup BigQuery now? (y/n)${NC}"
        echo "Note: You'll need to configure .env first with your GCP project details"
        read -r setup_bq
    else
        echo -e "${YELLOW}Do you want to create BigQuery dataset and tables now? (y/n)${NC}"
        echo "This will create all required tables in your GCP project"
        read -r setup_bq
    fi
    
    if [ "$setup_bq" = "y" ] || [ "$setup_bq" = "Y" ]; then
        print_info "Running BigQuery setup..."
        python bigquery/etl/setup_bigquery.py
        if [ $? -eq 0 ]; then
            print_status "BigQuery tables created successfully"
        else
            print_error "BigQuery setup failed. Check your credentials and permissions"
            print_info "You can run it later: python bigquery/etl/setup_bigquery.py"
        fi
    else
        print_warning "BigQuery setup skipped"
        print_info "Remember to run: python bigquery/etl/setup_bigquery.py after configuring .env"
    fi
else
    print_warning "No .env file found, skipping BigQuery setup"
    print_info "Configure bigquery/config/.env then run: python bigquery/etl/setup_bigquery.py"
fi

# Final instructions
echo -e "\n${GREEN}"
echo "╔══════════════════════════════════════════════════════════════╗"
echo "║                Installation Complete!                        ║"
echo "╚══════════════════════════════════════════════════════════════╝"
echo -e "${NC}"

echo -e "\n${BLUE}Next Steps:${NC}"
echo "============"
echo "1. Activate virtual environment: source venv/bin/activate"
echo "2. If BigQuery not setup: Update bigquery/config/.env and run python bigquery/etl/setup_bigquery.py"
echo "3. Test the engine: python example_usage.py"
echo "4. Start web GUI: cd web && php -S localhost:8080"
echo "5. Use BigQuery: from src.bigquery.bq_er_pipeline import BigQueryERPipeline"

echo -e "\n${YELLOW}BigQuery Tables Created:${NC}"
echo "  Raw: raw_customers, raw_transactions"
echo "  Staging: stg_customers_standardized, stg_transactions_enriched"
echo "  Resolved: resolved_customers, golden_entities"
echo "  Graph: entity_transaction_graph, entity_features, entity_edge_features"
echo "  Alerts: aml_alerts, alert_investigations"

echo -e "\n${BLUE}Documentation:${NC}"
echo "  - README.md - Project overview"
echo "  - bigquery/README.md - BigQuery integration"
echo "  - bigquery/QUICKSTART.md - Quick start guide"
echo "  - install/ENV_MIGRATION.md - Moving to new environments"
echo ""
