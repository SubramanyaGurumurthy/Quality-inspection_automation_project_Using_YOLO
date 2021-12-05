SETLOCAL EnableExtensions DisableDelayedExpansion
for /F %%a in ('echo prompt $E ^| cmd') do (
  set "ESC=%%a"
)

SET name_image="server-image-gui"
SET name_container="server-container-gui"
SET filename="gui.py"
SET IP=172.19.0.2
SET PORT=8050
SET NETWORKID="ntwofleads"

echo %ESC%[32mBuilding docker-image...%ESC%[0m
docker build -t %name_image% .

echo %ESC%[32mShow all images:%ESC%[0m
docker image ls

echo %ESC%[32mRun docker-image:%ESC%[0m

(curl --silent --retry 30 --retry-delay 1 --retry-connrefused \
    (timeout /t 4 && python -m webbrowser http://localhost:%PORT%)) &
docker run -it --rm -p %PORT%:%PORT% --network %NETWORKID% --ip %IP% --name %name_container% -i %name_image% "src/%filename%"

echo %ESC%[32mRemove image...%ESC%[0m
docker rmi %name_image%

endlocal