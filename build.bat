@echo off
setlocal

set PYINSTALLER=pyinstaller
set OPTIONS=--onefile --console

rmdir /s /q build 2>nul
rmdir /s /q dist 2>nul
del *.spec 2>nul

echo 🚀 Compilation de loveservice.py...
%PYINSTALLER% %OPTIONS% lovservice.py > log_lovservice.txt 2>&1

echo 🚀 Compilation de fusion.py...
%PYINSTALLER% %OPTIONS% fusion.py > log_fusion.txt 2>&1

echo ✅ Compilation terminée !
echo 🔍 Vérifie log_lovservice.txt si l'exe n'apparait pas.
pause
