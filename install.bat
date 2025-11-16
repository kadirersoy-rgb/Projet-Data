@echo off
chcp 65001>nul


echo:

python --version >nul 2>&1
if NOT %errorlevel%==0 (
    echo Python n'est pas installé !
    echo:
    exit
)

pip --version >nul 2>&1
if NOT %errorlevel%==0 (
    echo PiP n'est pas installé !
    echo:
    exit
)


echo ==========================
echo Téléchargement des modules
echo ==========================
echo:

pip install -r requirements.txt --quiet

echo:
echo ==================================
echo Téléchargement des modules terminé
echo ==================================
echo: