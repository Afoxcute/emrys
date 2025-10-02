#!/bin/bash

# Build script for Emrys application
set -e

echo "🚀 Starting Emrys build process..."

# Set Node.js memory options
export NODE_OPTIONS="--max-old-space-size=4096"

# Enable corepack for Yarn
echo "📦 Enabling corepack..."
corepack enable

# Install dependencies
echo "📥 Installing dependencies..."
yarn install --frozen-lockfile --network-timeout 100000

# Clean previous build
echo "🧹 Cleaning previous build..."
rm -rf .next

# Build the application
echo "🔨 Building application..."
yarn build

echo "✅ Build completed successfully!"
