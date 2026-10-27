# FinCrime Entity Resolution Engine - Installation Guide

This installation directory contains all scripts and configurations needed to deploy the FinCrime Entity Resolution Engine in any environment.

## Quick Start

### One-Command Installation
```bash
cd install
./install.sh
```

### Manual Installation
Follow the steps in this guide or use the individual scripts.

## What This Installer Does

1. **Prerequisites Check** - Verifies Python, pip, git, gcloud CLI
2. **Environment Setup** - Creates virtual environment, installs dependencies
3. **Configuration Setup** - Prompts for GCP credentials and project details
4. **BigQuery Setup** - Creates dataset and all tables
5. **Directory Structure** - Creates necessary directories
6. **Validation** - Tests the installation

## Installation Steps

### Step 1: Clone or Copy Repository
```bash
git clone <repository-url>
cd FinCrime_Transaction_Graph
```

### Step 2: Run Installer
```bash
cd install
chmod +x *.sh scripts/*.sh
./install.sh
```

### Step 3: Configure (if not done during install)
```bash
cp config/.env.example config/.env
nano config/.env
```

### Step 4: Setup BigQuery
```bash
python ../bigquery/etl/setup_bigquery.py
```

### Step 5: Test Installation
```bash
python ../example_usage.py
```

## Configuration

All environment-specific settings are in `config/.env`. Copy from `config/.env.example` and update:

```env
GCP_PROJECT_ID=your-project-id
BQ_DATASET_ID=fincrime_er
BQ_LOCATION=US
GOOGLE_APPLICATION_CREDENTIALS=/path/to/service-account.json
ENVIRONMENT=dev
```

## Moving to Another Environment

When moving this project to a different machine, GCP account, or environment:

1. Copy the entire project directory
2. Run `./install/install.sh` in the new environment
3. Update `config/.env` with new GCP credentials
4. Run `python bigquery/etl/setup_bigquery.py` to create BigQuery resources
5. Load your data

## Requirements

- Python 3.9 or higher
- pip
- Google Cloud SDK (optional but recommended)
- BigQuery API enabled in GCP project
- Service account with appropriate permissions

## Troubleshooting

See `docs/TROUBLESHOOTING.md` for common issues.


## Web GUI Access

The PHP web interface is available for running the engine through a browser. **The installer does not start the PHP server automatically** - you must start it manually.

### Quick Start
```bash
# Activate virtual environment (if not already)
source venv/bin/activate

# Start PHP server
cd web
php -S localhost:8080
```

### Access
- **Local:** http://localhost:8080
- **Remote/GCP VM:** http://<YOUR_SERVER_IP>:8080 (use `php -S 0.0.0.0:8080`)
- **No login required** - Direct access to dashboard

For detailed instructions, see [WEB_GUI_GUIDE.md](WEB_GUI_GUIDE.md).
