@echo off
echo ========================================
echo  DEMARRAGE BACKEND BREASTCARE
echo ========================================
echo.

cd backend

echo Verification de l'environnement Python...
python --version
if %ERRORLEVEL% NEQ 0 (
    echo ERREUR: Python n'est pas installe ou pas dans le PATH
    pause
    exit /b 1
)

echo.
echo Activation de l'environnement virtuel (si existe)...
if exist venv\Scripts\activate.bat (
    call venv\Scripts\activate.bat
    echo Environnement virtuel active
) else (
    echo Pas d'environnement virtuel trouve, utilisation de Python global
)

echo.
echo Demarrage du serveur FastAPI...
echo URL: http://localhost:8000
echo Documentation: http://localhost:8000/docs
echo Health Check: http://localhost:8000/health
echo.
echo Appuyez sur CTRL+C pour arreter le serveur
echo.

python -m uvicorn app.main:app --reload --host 0.0.0.0 --port 8000

pause

