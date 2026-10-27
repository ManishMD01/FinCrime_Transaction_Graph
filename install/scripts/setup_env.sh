#!/bin/bash
# Setup environment for any machine

PROJECT_ROOT="$(dirname "$(dirname "$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)")")"
CONFIG_DIR="$PROJECT_ROOT/bigquery/config"

echo "Setting up environment configuration..."

# Create .env if not exists
if [ ! -f "$CONFIG_DIR/.env" ]; then
    cp "$CONFIG_DIR/.env.example" "$CONFIG_DIR/.env"
    echo "Created .env from template"
    echo "Please update it with your credentials:"
    echo "  - GCP_PROJECT_ID"
    echo "  - BQ_DATASET_ID"
    echo "  - GOOGLE_APPLICATION_CREDENTIALS"
    nano "$CONFIG_DIR/.env" 2>/dev/null || vi "$CONFIG_DIR/.env" 2>/dev/null || echo "Edit $CONFIG_DIR/.env manually"
else
    echo ".env already exists"
fi

# Validate
python3 -c "
from bigquery.config.config import config
errors = config.validate()
if errors:
    print('Configuration issues:')
    for e in errors:
        print(f'  - {e}')
else:
    print('Configuration valid')
    print(f'Project: {config.project_id}')
" 2>&1
