#!/bin/bash

# Set environment variables for static export
export NODE_ENV=production
export STATIC_EXPORT=true

# Install dependencies with Yarn v4 compatible flags
echo "Installing dependencies..."
yarn install --frozen-lockfile

# Build the static site
echo "Building static site..."
yarn build:static

echo "Build completed successfully!"
