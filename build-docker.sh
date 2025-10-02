#!/bin/bash

# Docker-specific build script for Emrys
set -e

echo "🐳 Starting Docker build process for Emrys..."

# Set Node.js memory options
export NODE_OPTIONS="--max-old-space-size=4096"
export NEXT_TELEMETRY_DISABLED=1

# Enable corepack for Yarn
echo "📦 Enabling corepack..."
corepack enable

# Clean previous build
echo "🧹 Cleaning previous build..."
rm -rf .next

# Install dependencies
echo "📥 Installing dependencies..."
yarn install --frozen-lockfile --network-timeout 100000

# Build with retry logic
echo "🔨 Building application..."
yarn build:docker || {
    echo "⚠️  First build attempt failed, retrying..."
    rm -rf .next
    yarn build:docker
}

echo "✅ Docker build completed successfully!"
