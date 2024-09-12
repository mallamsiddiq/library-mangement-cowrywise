@echo off
setlocal

:: Define service paths
set ADMIN_PATH=admin
set USERS_PATH=users

:: Check the first argument to determine which section to run
if "%1"=="start" goto start
if "%1"=="stop" goto stop
if "%1"=="rebuild" goto rebuild
if "%1"=="status" goto status
if "%1"=="test-admin" goto test-admin
if "%1"=="test-users" goto test-users
if "%1"=="test-all" goto test-all

echo Invalid argument. Usage:
echo   %0 start
echo   %0 stop
echo   %0 rebuild
echo   %0 status
echo   %0 test-admin
echo   %0 test-users
echo   %0 test-all
goto end

:: Start Docker services with delay
:start
cd %ADMIN_PATH%
docker compose up -d --build
:: Wait for 30 seconds before starting the users service
timeout /t 30 /nobreak
cd ..\%USERS_PATH%
docker compose up -d --build
goto end

:: Stop Docker services
:stop
cd %ADMIN_PATH%
docker compose down
cd ..\%USERS_PATH%
docker compose down
goto end

:: Rebuild Docker services
:rebuild
cd %ADMIN_PATH%
docker compose up --build
cd ..\%USERS_PATH%
docker compose up --build
goto end

:: Check status of Docker services
:status
cd %ADMIN_PATH%
docker compose ps
cd ..\%USERS_PATH%
docker compose ps
goto end

:: Run tests for the admin service
:test-admin
cd %ADMIN_PATH%
docker compose run --rm web pytest
goto end

:: Run tests for the users service
:test-users
cd %USERS_PATH%
docker compose run --rm web pytest
goto end

:: Run tests for both services
:test-all
call :test-admin
call :test-users
goto end

:end
endlocal
