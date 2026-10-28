@echo off
rem tk for PowerShell / cmd: runs tools\ticket\tk with Git Bash (plain "bash" on Windows is WSL).
rem Works from any folder: tickets always live in this repo's .tickets\.
setlocal
set "GITBASH=%ProgramFiles%\Git\bin\bash.exe"
if not exist "%GITBASH%" for /f "delims=" %%G in ('where git 2^>nul') do set "GITBASH=%%~dpG..\bin\bash.exe"
if not exist "%GITBASH%" (
  echo tk: khong tim thay Git Bash. Cai Git for Windows hoac sua duong dan trong tk.cmd. 1>&2
  exit /b 1
)
set "TICKETS_DIR=%~dp0.tickets"
rem forward slashes: awk in `tk show` reads "\T" in D:\Tools as an escape and finds no file
set "TICKETS_DIR=%TICKETS_DIR:\=/%"
set "PATH=%~dp0tools\ticket;%PATH%"
chcp 65001 >nul
"%GITBASH%" "%~dp0tools\ticket\tk" %*
