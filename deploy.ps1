# Cyber Commission Deployment Script for Windows
# Run this script to deploy to Heroku

Write-Host "🚀 Cyber Commission Deployment Script" -ForegroundColor Green
Write-Host "====================================" -ForegroundColor Green

# Check if Heroku CLI is installed
try {
    $herokuVersion = heroku --version 2>$null
    Write-Host "✅ Heroku CLI found: $herokuVersion" -ForegroundColor Green
} catch {
    Write-Host "❌ Heroku CLI not found. Please install it first:" -ForegroundColor Red
    Write-Host "   https://devcenter.heroku.com/articles/heroku-cli" -ForegroundColor Yellow
    exit 1
}

# Check if git repo exists
if (!(Test-Path ".git")) {
    Write-Host "📝 Initializing git repository..." -ForegroundColor Blue
    git init
    git add .
    git commit -m "Initial commit"
}

# Prompt for app name
$appName = Read-Host "Enter your Heroku app name"

Write-Host "🔧 Creating Heroku app: $appName" -ForegroundColor Blue
heroku create $appName

Write-Host "🔐 Setting environment variables..." -ForegroundColor Blue
Write-Host "Please provide the following values:" -ForegroundColor Yellow

$secretKey = Read-Host "SECRET_KEY"
$emailSender = Read-Host "EMAIL_SENDER"
$emailPassword = Read-Host "EMAIL_PASSWORD"
$emailReceiver = Read-Host "EMAIL_RECEIVER"

heroku config:set SECRET_KEY="$secretKey"
heroku config:set EMAIL_SENDER="$emailSender"
heroku config:set EMAIL_PASSWORD="$emailPassword"
heroku config:set EMAIL_RECEIVER="$emailReceiver"

Write-Host "📤 Pushing to Heroku..." -ForegroundColor Blue
git push heroku main

Write-Host "✅ Deployment complete!" -ForegroundColor Green
Write-Host "🌐 Your app is live at: https://$appName.herokuapp.com" -ForegroundColor Green
Write-Host ""
Write-Host "📧 Default login credentials:" -ForegroundColor Cyan
Write-Host "   Username: admin" -ForegroundColor White
Write-Host "   Password: admin123" -ForegroundColor White