#!/bin/bash

# FinCrime Transaction Graph - Complete Uninstall Script
# This script removes all components of the Entity Resolution Engine setup
# Including Airflow, virtual environment, data, logs, configs, and optionally the entire project

set -e

RED='\033[0;31m'
YELLOW='\033[1;33m'
GREEN='\033[0;32m'
NC='\033[0m' # No Color

PROJECT_DIR="/home/pritsingh000/Git/FinCrime_Transaction_Graph"
DRY_RUN=false

# Parse arguments
if [[ "$1" == "--dry-run" ]]; then
    DRY_RUN=true
    echo -e "${YELLOW}[DRY RUN MODE]${NC} No files will be deleted"
    echo ""
fi

echo -e "${RED}=== FinCrime Transaction Graph - Complete Uninstall ===${NC}"
echo ""
echo "This script will remove:"
echo "  - All running processes (Airflow, uvicorn, PHP dev server, fincrime processes)"
echo "  - Apache Airflow (from venv and any related files)"
echo "  - Python virtual environment (venv/)"
echo "  - Data directories (data/airflow_input, data/airflow_processed, and optionally others)"
echo "  - Logs, outputs, temporary files, caches"
echo "  - Configuration files with credentials/secrets (.env, service account keys)"
echo "  - Python cache (__pycache__, *.pyc)"
echo "  - Optionally the entire project directory"
echo ""
echo -e "${YELLOW}WARNING: This action is IRREVERSIBLE!${NC}"
echo ""

# Confirmation
read -p "Are you sure you want to continue? (yes/no): " CONFIRM
if [[ "$CONFIRM" != "yes" ]]; then
    echo "Uninstall cancelled."
    exit 0
fi

echo ""
read -p "Do you want to DELETE the entire project directory ($PROJECT_DIR)? (yes/no): " DELETE_PROJECT
echo ""

if [[ "$DRY_RUN" == true ]]; then
    echo -e "${YELLOW}[DRY RUN]${NC} Would perform the following actions:"
    echo "  1. Kill processes: airflow, apache-airflow, uvicorn, php, fincrime"
    echo "  2. Uninstall apache-airflow from venv if exists"
    echo "  3. Remove: $PROJECT_DIR/airflow, $PROJECT_DIR/venv"
    echo "  4. Remove: $PROJECT_DIR/data/airflow_input, $PROJECT_DIR/data/airflow_processed"
    echo "  5. Remove: logs/, outputs/, tmp/, __pycache__, *.pyc"
    echo "  6. Remove: .env*, *credentials*.json, *service-account*.json"
    if [[ "$DELETE_PROJECT" == "yes" ]]; then
        echo "  7. Remove entire directory: $PROJECT_DIR"
    fi
    echo ""
    echo -e "${GREEN}[DRY RUN]${NC} No changes made. Run without --dry-run to actually uninstall."
    exit 0
fi

# Step 1: Stop all related processes
echo -e "${GREEN}[1/9]${NC} Stopping all related processes..."
pkill -9 -f "airflow" 2>&1 || true
pkill -9 -f "apache-airflow" 2>&1 || true
pkill -9 -f "fincrime" 2>&1 || true
pkill -9 -f "uvicorn" 2>&1 || true
pkill -9 -f "gunicorn" 2>&1 || true
pkill -9 -f "php.*-S" 2>&1 || true
pkill -9 -f "celery" 2>&1 || true
sleep 3
echo "  Done"

# Step 2: Uninstall Airflow from virtual environment
echo -e "${GREEN}[2/9]${NC} Uninstalling Apache Airflow from virtual environment..."
if [ -f "$PROJECT_DIR/venv/bin/pip" ]; then
    $PROJECT_DIR/venv/bin/pip show apache-airflow >/dev/null 2>&1 && \
        $PROJECT_DIR/venv/bin/pip uninstall -y apache-airflow apache-airflow-providers-* 2>&1 | tail -3 || \
        echo "  Airflow not installed in venv or already removed"
elif [ -f "$PROJECT_DIR/venv/bin/python" ]; then
    $PROJECT_DIR/venv/bin/python -m pip show apache-airflow >/dev/null 2>&1 && \
        $PROJECT_DIR/venv/bin/python -m pip uninstall -y apache-airflow apache-airflow-providers-* 2>&1 | tail -3 || \
        echo "  Airflow not installed in venv or already removed"
else
    echo "  No venv found"
fi
echo "  Done"

# Step 3: Remove Airflow directories and files from repo
echo -e "${GREEN}[3/9]${NC} Removing Airflow files from repository..."
cd "$PROJECT_DIR" 2>/dev/null || exit 1
rm -rf airflow/ 2>&1 || true
rm -rf dags/ 2>&1 || true
rm -rf plugins/ 2>&1 || true
find . -name "*airflow*" -not -path "*/venv/*" -not -path "*/.git/*" -delete 2>&1 || true
find . -name "*dag*.py" -not -path "*/venv/*" -not -path "*/.git/*" -delete 2>&1 || true
echo "  Done"

# Step 4: Remove Airflow-related data directories
echo -e "${GREEN}[4/9]${NC} Removing Airflow data directories..."
rm -rf data/airflow_input 2>&1 || true
rm -rf data/airflow_processed 2>&1 || true
rm -rf data/airflow 2>&1 || true
echo "  Done"

# Step 5: Remove virtual environment
echo -e "${GREEN}[5/9]${NC} Removing virtual environment..."
rm -rf venv/ 2>&1 || true
rm -rf .venv/ 2>&1 || true
rm -rf env/ 2>&1 || true
echo "  Done"

# Step 6: Remove logs, outputs, temp files, and caches
echo -e "${GREEN}[6/9]${NC} Removing logs, outputs, and caches..."
rm -rf logs/ 2>&1 || true
rm -rf output/ 2>&1 || true
rm -rf outputs/ 2>&1 || true
rm -rf tmp/ 2>&1 || true
rm -rf temp/ 2>&1 || true
rm -rf .pytest_cache/ 2>&1 || true
rm -rf .mypy_cache/ 2>&1 || true
rm -rf __pycache__/ 2>&1 || true
find . -name "*.pyc" -not -path "*/.git/*" -delete 2>&1 || true
find . -name "*.pyo" -not -path "*/.git/*" -delete 2>&1 || true
find . -type d -name "__pycache__" -not -path "*/.git/*" -empty -delete 2>&1 || true
find . -type d -name "__pycache__" -not -path "*/.git/*" -delete 2>&1 || true
echo "  Done"

# Step 7: Remove configuration files with credentials/secrets
echo -e "${GREEN}[7/9]${NC} Removing credential and config files..."
rm -f .env 2>&1 || true
rm -f .env.local 2>&1 || true
rm -f .env.* 2>&1 || true
find . -name "*service-account*.json" -not -path "*/.git/*" -delete 2>&1 || true
find . -name "*credentials*.json" -not -path "*/.git/*" -delete 2>&1 || true
find . -name "*key*.json" -not -path "*/.git/*" -delete 2>&1 || true
rm -f config.json 2>&1 || true
rm -rf config/secrets/ 2>&1 || true
echo "  Done"

# Step 8: Remove Docker artifacts if present
echo -e "${GREEN}[8/9]${NC} Removing Docker artifacts..."
rm -f Dockerfile 2>&1 || true
rm -f docker-compose.yml 2>&1 || true
rm -f docker-compose.yaml 2>&1 || true
rm -f .dockerignore 2>&1 || true
echo "  Done"

# Step 9: Optionally remove entire project directory
if [[ "$DELETE_PROJECT" == "yes" ]]; then
    echo -e "${GREEN}[9/9]${NC} Removing entire project directory..."
    cd / 2>&1 || true
    rm -rf "$PROJECT_DIR" 2>&1 || true
    echo -e "${GREEN}=== Uninstall Complete ===${NC}"
    echo "Entire project directory has been removed."
    exit 0
else
    echo -e "${GREEN}[9/9]${NC} Skipping project directory removal..."
    echo ""
    echo -e "${GREEN}=== Uninstall Complete ===${NC}"
    echo ""
    echo "Removed:"
    echo "  - All Airflow processes and files"
    echo "  - Virtual environment (venv/)"
    echo "  - Airflow data directories"
    echo "  - Logs, caches, and temporary files"
    echo "  - Credential/config files"
    echo "  - Docker artifacts"
    echo ""
    echo "Project directory remains at: $PROJECT_DIR"
    echo "You may want to review remaining files manually."
    exit 0
fi
