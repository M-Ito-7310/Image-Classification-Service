@echo off
echo Starting Image Classification Service Development Environment...

echo.
echo Building Docker images...
docker-compose build

echo.
echo Starting database and redis...
docker-compose up -d database redis

echo.
echo Waiting for database to be ready...
timeout /t 15 /nobreak > nul

echo.
echo Starting backend and frontend...
docker-compose up backend frontend

echo.
echo Development environment started!
echo.
echo Access the application at:
echo Frontend: http://localhost:3000
echo Backend API: http://localhost:8000
echo API Documentation: http://localhost:8000/docs
echo.
echo Press Ctrl+C to stop the services.

pause