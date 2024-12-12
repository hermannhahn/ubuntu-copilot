#!/bin/bash -e

# ==============================================================================
# This script install dependencies and the extension.
# ==============================================================================

echo "Installing dependencies..."
sudo apt update
npm install
echo "Dependencies installed."
exit 0
