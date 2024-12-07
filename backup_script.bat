@echo off
:: Define log file
set LOGFILE=E:\Backuper\backup_log.txt

:: Start logging
echo ==== Backup Started at %DATE% %TIME% ==== >> %LOGFILE%

:: Map drives with credentials
echo Mapping drive B:... >> %LOGFILE%
net use B: \\192.168.1.1\DocumentServer /user:administrator pass123 >> %LOGFILE% 2>&1
if errorlevel 1 (
    echo Failed to map drive B:. Exiting... >> %LOGFILE%
    goto end
)

echo Mapping drive S:... >> %LOGFILE%
net use S: \\192.168.1.2\TallyServer /user:administrator pass123 >> %LOGFILE% 2>&1
if errorlevel 1 (
    echo Failed to map drive S:. Exiting... >> %LOGFILE%
    goto end
)

:: Run Python script
echo Running Python script... >> %LOGFILE%
python E:\Backuper\Incremental_backuper.py >> %LOGFILE% 2>&1
if errorlevel 1 (
    echo Python script encountered an error. >> %LOGFILE%
)

:: Disconnect mapped drives
echo Disconnecting drive B:... >> %LOGFILE%
net use B: /delete >> %LOGFILE% 2>&1
echo Disconnecting drive S:... >> %LOGFILE%
net use S: /delete >> %LOGFILE% 2>&1

:end
:: End logging
echo ==== Backup Ended at %DATE% %TIME% ==== >> %LOGFILE%
pause
