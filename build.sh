#!/bin/bash

# Build script for Emrys application
set -e

echo "🚀 Starting Emrys build process..."

# Enable corepack for Yarn
echo "📦 Enabling corepack..."
corepack enable

# Install dependencies
echo "📥 Installing dependencies..."
yarn install --frozen-lockfile --network-timeout 100000

# Build the application
echo "🔨 Building application..."
yarn build

echo "✅ Build completed successfully!"
