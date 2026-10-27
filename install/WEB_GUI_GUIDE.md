# Web GUI Guide - FinCrime Entity Resolution Engine

## Overview

The FinCrime Entity Resolution Engine comes with a PHP-based web GUI for uploading data, running the engine, and viewing results through an interactive dashboard.

## Starting the PHP Server

The installation script **does not** automatically start the PHP server. You need to start it manually after installation.

### Option 1: Local Development (localhost only)
```bash
cd /home/pritsingh000/Git/FinCrime_Transaction_Graph/web
php -S localhost:8080
```

### Option 2: Access from Other Machines (GCP VM, Remote Server)
```bash
cd /home/pritsingh000/Git/FinCrime_Transaction_Graph/web
php -S 0.0.0.0:8080
```

### Option 3: Run in Background
```bash
cd /home/pritsingh000/Git/FinCrime_Transaction_Graph/web
nohup php -S 0.0.0.0:8080 > ../logs/php-server.log 2>&1 &
echo "PHP server started in background. PID: $!"
```

To stop the background server:
```bash
pkill -f "php -S 0.0.0.0:8080"
```

## Accessing the GUI

Once the PHP server is running, open your web browser and navigate to:

| Environment | URL |
|-------------|-----|
| Local Machine | `http://localhost:8080` |
| Remote/GCP VM | `http://<YOUR_VM_IP>:8080` |
| With Domain | `http://your-domain.com:8080` |

**Note:** If you're using a GCP VM, make sure to open port `8080` in your firewall rules.

## Login / Access

The web GUI currently has **no authentication/login required**. It's designed for internal/compliance team use. Simply access the URL and you'll be taken directly to the dashboard.

> ⚠️ **Security Note:** For production deployments, it's recommended to add authentication (basic auth, OAuth, or put behind a VPN/firewall). 

## Using the GUI

### 1. Upload Data
- Go to the homepage (`index.php`)
- Upload your **Customer Profiles CSV** and **Transaction Logs CSV**
- Adjust the match threshold (default: 0.75)
- Click "Run Entity Resolution & Detection"

### 2. View Results
After processing, you'll see:
- **Summary Stats** - Total customers, golden entities, transactions, alerts
- **Alerts Dashboard** - All AML/Fraud alerts with severity
- **Golden Entities** - Consolidated entity records
- **Resolved Customers** - Mapping of source customers to golden entities
- **Node/Edge Features** - Graph analytics
- **Download Options** - Export all results as CSV/JSON

### 3. Download Sample Data
Click "Download Sample Data" on the homepage to get test CSV files.

## CSV Format Requirements

### Customers CSV
Required columns:
```
customer_id, name, dob, address, phone, email, ssn, zip, device_id, ip_address, location
```

### Transactions CSV
Required columns:
```
transaction_id, sender_id, receiver_id, amount, timestamp, channel, location, transaction_type
```

## Troubleshooting

### Port Already in Use
```bash
# Find process using port 8080
sudo lsof -i :8080
# or
sudo netstat -tlnp | grep 8080

# Kill it
kill <PID>
```

### Permission Denied
```bash
chmod -R 755 web/
```

### PHP Not Found
```bash
# Install PHP
sudo apt-get install php php-cli
# or
sudo yum install php
```

### File Upload Errors
Check PHP settings in `php.ini`:
```ini
upload_max_filesize = 50M
post_max_size = 50M
max_execution_time = 300
```

## Running as a Service (Production)

For long-running deployments, use systemd:

Create `/etc/systemd/system/fincrime-web.service`:
```ini
[Unit]
Description=FinCrime Entity Resolution Web GUI
After=network.target

[Service]
Type=simple
User=www-data
WorkingDirectory=/home/pritsingh000/Git/FinCrime_Transaction_Graph/web
ExecStart=/usr/bin/php -S 0.0.0.0:8080
Restart=always

[Install]
WantedBy=multi-user.target
```

Then:
```bash
sudo systemctl daemon-reload
sudo systemctl enable fincrime-web
sudo systemctl start fincrime-web
sudo systemctl status fincrime-web
```
