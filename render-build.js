#!/usr/bin/env node

const { execSync } = require('child_process');
const path = require('path');

console.log('Starting Render build process...');

// Set environment variables
process.env.NODE_ENV = 'production';
process.env.STATIC_EXPORT = 'true';

try {
  console.log('Installing dependencies with Yarn v4...');
  
  // Use the project's Yarn binary directly to avoid Render's default flags
  const yarnPath = path.join(__dirname, '.yarn', 'releases', 'yarn-4.5.0.cjs');
  
  // Install dependencies
  execSync(`node "${yarnPath}" install --frozen-lockfile`, {
    stdio: 'inherit',
    cwd: __dirname
  });
  
  console.log('Building static site...');
  
  // Build the static site
  execSync(`node "${yarnPath}" build:static`, {
    stdio: 'inherit',
    cwd: __dirname,
    env: { ...process.env, STATIC_EXPORT: 'true' }
  });
  
  console.log('Build completed successfully!');
  
} catch (error) {
  console.error('Build failed:', error.message);
  process.exit(1);
}
