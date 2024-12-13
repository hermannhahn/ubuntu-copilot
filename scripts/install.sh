#!/bin/bash -e

# ==============================================================================
# This script install dependencies and the extension.
# ==============================================================================

echo "Installing dependencies..."
sudo apt update
npm install
pip install -r requirements.txt
echo "Dependencies installed."
exit 0
