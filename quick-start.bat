@echo off
echo ========================================
echo Daily Crossword Generator - Quick Start
echo ========================================
echo.

:menu
echo Choose an option:
echo 1. Generate 7 days of puzzles
echo 2. Generate 30 days of puzzles
echo 3. Generate 90 days of puzzles
echo 4. Generate custom range
echo 5. Test locally (start web server)
echo 6. Exit
echo.
set /p choice="Enter your choice (1-6): "

if "%choice%"=="1" goto seven_days
if "%choice%"=="2" goto thirty_days
if "%choice%"=="3" goto ninety_days
if "%choice%"=="4" goto custom
if "%choice%"=="5" goto test_local
if "%choice%"=="6" goto end

:seven_days
echo.
echo Generating 7 days of puzzles...
python generate.py --start 2025-01-01 --days 7 --out site --difficulty easy --categories general,tech,travel,kids,devotional,holiday
echo.
echo Done! Puzzles generated in site/ folder
pause
goto menu

:thirty_days
echo.
echo Generating 30 days of puzzles...
python generate.py --start 2025-01-01 --days 30 --out site --difficulty easy --categories general,tech,travel,kids,devotional,holiday
echo.
echo Done! Puzzles generated in site/ folder
pause
goto menu

:ninety_days
echo.
echo Generating 90 days of puzzles...
python generate.py --start 2025-01-01 --days 90 --out site --difficulty medium --categories general,tech,travel,kids,devotional,holiday
echo.
echo Done! Puzzles generated in site/ folder
pause
goto menu

:custom
echo.
set /p start_date="Enter start date (YYYY-MM-DD): "
set /p num_days="Enter number of days: "
set /p diff="Enter difficulty (easy/medium/hard): "
echo.
echo Generating %num_days% days of puzzles starting from %start_date%...
python generate.py --start %start_date% --days %num_days% --out site --difficulty %diff% --categories general,tech,travel,kids,devotional,holiday
echo.
echo Done! Puzzles generated in site/ folder
pause
goto menu

:test_local
echo.
echo Starting local web server...
echo Open your browser to: http://localhost:8000
echo Press Ctrl+C to stop the server
echo.
cd site
python -m http.server 8000
cd ..
goto menu

:end
echo.
echo Thank you for using Daily Crossword Generator!
echo Visit the site/ folder to see your generated puzzles.
echo.
pause
