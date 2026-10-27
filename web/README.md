# FinCrime Entity Resolution Web GUI

A PHP-based web interface for running the FinCrime Entity Resolution & Transaction Graph Engine.

## Features

- **Data Upload**: Upload customer profiles and transaction logs as CSV files
- **Configurable Threshold**: Adjust entity matching threshold (0.5 - 0.95)
- **Real-time Processing**: Executes Python engine via shell and displays results
- **Interactive Dashboard**: View golden entities, resolved profiles, graph features, and alerts
- **Download Results**: Export all results as CSV/JSON
- **Sample Data**: Generate sample datasets for testing

## Requirements

- PHP 7.4+ with file upload enabled
- Python 3.9+ with required packages installed
- Web server (Apache/Nginx) or PHP built-in server

## Setup

1. Install Python dependencies:
```bash
pip install -r ../requirements.txt
```

2. Start PHP server:
```bash
cd web
php -S localhost:8080
```

3. Open browser to `http://localhost:8080`

## Usage

1. Go to the homepage
2. Upload your Customer Profiles CSV and Transaction Logs CSV
3. Adjust match threshold if needed
4. Click "Run Entity Resolution & Detection"
5. View results in the interactive dashboard

## CSV Format

### Customers CSV
Required columns: `customer_id`, `name`, `dob`, `address`, `phone`, `email`, `ssn`, `zip`, `device_id`, `ip_address`, `location`

### Transactions CSV
Required columns: `transaction_id`, `sender_id`, `receiver_id`, `amount`, `timestamp`, `channel`, `location`, `transaction_type`

## Security Notes

- Files are uploaded to `uploads/` directory
- Results stored in `results/` directory
- Use in controlled environments only
- Sanitize inputs in production

## Architecture

- `index.php` - Main upload interface
- `process.php` - Handles file upload and Python execution
- `results.php` - Displays analysis results
- `sample.php` - Generates sample data
- `download.php` - Downloads result files
