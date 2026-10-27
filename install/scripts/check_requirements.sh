#!/bin/bash
# Check system requirements

echo "Checking system requirements..."
echo "================================"

# Check Python version
python3 -c "
import sys
version = sys.version_info
if version.major >= 3 and version.minor >= 9:
    print(f'✓ Python {version.major}.{version.minor}.{version.micro} - OK')
else:
    print(f'✗ Python {version.major}.{version.minor}.{version.micro} - Need 3.9+')
    sys.exit(1)
"

# Check pip
pip3 --version > /dev/null 2>&1 && echo "✓ pip3 - OK" || echo "✗ pip3 - Missing"

# Check available memory
if [ -f /proc/meminfo ]; then
    MEM=$(grep MemTotal /proc/meminfo | awk '{print $2}')
    MEM_GB=$((MEM / 1024 / 1024))
    echo "✓ Memory: ${MEM_GB}GB available"
fi

# Check disk space
DISK=$(df -h . | awk 'NR==2 {print $4}')
echo "✓ Disk space: $DISK available"

echo "================================"
echo "Requirements check complete"
