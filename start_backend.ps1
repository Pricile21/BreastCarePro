# Script PowerShell pour démarrer le backend
Write-Host "========================================" -ForegroundColor Cyan
Write-Host "  DEMARRAGE BACKEND BREASTCARE" -ForegroundColor Cyan
Write-Host "========================================" -ForegroundColor Cyan
Write-Host ""

Set-Location backend

Write-Host "Vérification de l'environnement Python..." -ForegroundColor Yellow
$pythonVersion = python --version 2>&1
if ($LASTEXITCODE -ne 0) {
    Write-Host "ERREUR: Python n'est pas installé ou pas dans le PATH" -ForegroundColor Red
    Read-Host "Appuyez sur Entrée pour quitter"
    exit 1
}
Write-Host $pythonVersion -ForegroundColor Green

Write-Host ""
Write-Host "Activation de l'environnement virtuel (si existe)..." -ForegroundColor Yellow
if (Test-Path "venv\Scripts\Activate.ps1") {
    & "venv\Scripts\Activate.ps1"
    Write-Host "Environnement virtuel activé" -ForegroundColor Green
} else {
    Write-Host "Pas d'environnement virtuel trouvé, utilisation de Python global" -ForegroundColor Yellow
}

Write-Host ""
Write-Host "Démarrage du serveur FastAPI..." -ForegroundColor Yellow
Write-Host "URL: http://localhost:8000" -ForegroundColor Cyan
Write-Host "Documentation: http://localhost:8000/docs" -ForegroundColor Cyan
Write-Host "Health Check: http://localhost:8000/health" -ForegroundColor Cyan
Write-Host ""
Write-Host "Appuyez sur CTRL+C pour arrêter le serveur" -ForegroundColor Yellow
Write-Host ""

python -m uvicorn app.main:app --reload --host 0.0.0.0 --port 8000

