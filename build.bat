pyinstaller app.py
xcopy "resources" "dist/app/resources" /I /f /y
xcopy "assets" "dist/app/assets" /I /f /y
xcopy "config.yaml" "dist/app/config.yaml" /f /y