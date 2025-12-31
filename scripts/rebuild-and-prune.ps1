$SCRIPT_DIR = Split-Path -Parent (Split-Path -Parent $MyInvocation.MyCommand.Path)

Set-Location $SCRIPT_DIR

Write-Host "Stopping containers..."
docker-compose down

Write-Host "Rebuilding and starting containers..."
docker-compose up -d --build

Write-Host "Pruning unused images..."
docker image prune -f

Write-Host "Rebuild and prune complete"
