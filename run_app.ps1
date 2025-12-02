# PowerShell script to start the Diabetes Tracker server and open the browser
# Run this script by right-clicking and selecting 'Run with PowerShell' or from an elevated PowerShell

$scriptDir = Split-Path -Parent $MyInvocation.MyCommand.Definition
Set-Location $scriptDir

Write-Host "Starting Diabetes Tracker..." -ForegroundColor Cyan

# Start the server in a new window so it continues running
Start-Process -FilePath "$PSScriptRoot\venv\Scripts\python.exe" -ArgumentList "app.py" -WorkingDirectory $PSScriptRoot

Start-Sleep -Seconds 2

# Open default browser to the app
Start-Process "http://127.0.0.1:5000/static/index.html"

Write-Host "Server started (if not visible, check the new window)." -ForegroundColor Green
