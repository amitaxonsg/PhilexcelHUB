@echo off
setlocal EnableDelayedExpansion
title AXON 1Pro - Philexcel NAS Setup and Repair
color 0B
echo =========================================================
echo    A X O N   1PRO SOLUTIONS
echo    PHILEXCEL HUB - NAS SETUP AND REPAIR
echo =========================================================
echo Welcome. This assistant checks and repairs approved NAS drives.
echo Use your personal Philexcel NAS account. Do not share passwords.
echo Correct drives are preserved; changes need your approval.
echo.
set "NAS=PHILEXCEL-HUB"
powershell.exe -NoProfile -Command "exit ([int](-not (Test-NetConnection -ComputerName '%NAS%' -Port 445 -InformationLevel Quiet -WarningAction SilentlyContinue)))" >nul 2>&1
if errorlevel 1 (
 echo Sorry, the Philexcel NAS cannot be detected on this network.
 echo Connect to the approved office Wi-Fi or Ethernet.
 echo Contact your company administrator if you are in the office.
 goto END
)
set /a ATTEMPT=0
:LOGIN
set /a ATTEMPT+=1
set /p "USER=Personal NAS username: "
if not defined USER goto LOGIN
echo Enter your personal NAS password at the hidden Windows prompt.
net use "\\%NAS%\IPC$" /user:"%NAS%\%USER%" * /persistent:no >nul
if not errorlevel 1 goto AUDIT
echo Login failed or another NAS account is already connected.
if !ATTEMPT! GEQ 3 (echo Three attempts reached. Contact IT.&goto END)
echo Existing NAS sessions:
net use | findstr /I "PHILEXCEL-HUB"
choice /C YN /M "Close NAS files and disconnect conflicting NAS sessions before retry"
if errorlevel 2 goto END
for /f "delims=" %%P in ('powershell.exe -NoProfile -Command "Get-SmbMapping | Where-Object { $_.RemotePath -like '\\PHILEXCEL-HUB\*' } | Select-Object -ExpandProperty RemotePath"') do net use "%%P" /delete /y >nul 2>&1
goto LOGIN
:AUDIT
echo.
echo Welcome back, %USER%.
echo Your eligible folders are determined by current NAS permissions.
echo These are the accessible departmental shares and current mappings.
set /a ELIGIBLE=0
set /a NEEDS=0
for %%D in (X H R F E M Z) do (
 call :SHARE %%D
 dir "\\%NAS%\!SHARE!" >nul 2>&1
 if not errorlevel 1 (
  set /a ELIGIBLE+=1
  set "OLD="
  for /f "delims=" %%P in ('powershell.exe -NoProfile -Command "(Get-SmbMapping -LocalPath '%%D:' -ErrorAction SilentlyContinue).RemotePath"') do set "OLD=%%P"
  if /I "!OLD!"=="\\%NAS%\!SHARE!" (echo [CORRECT] %%D: !SHARE!) else (
   set /a NEEDS+=1
   if defined OLD (echo [WRONG] %%D: !OLD! - expected \\%NAS%\!SHARE!) else (echo [MISSING] %%D: \\%NAS%\!SHARE!)
  )
 )
)
echo.
echo Accessible shares: !ELIGIBLE!   Missing or wrong: !NEEDS!
if !ELIGIBLE! EQU 0 (echo No approved shares accessible. Contact your NAS administrator.&goto END)
if !NEEDS! EQU 0 goto VERIFY
choice /C YN /M "Install or troubleshoot the missing / incorrect drives"
if errorlevel 2 goto VERIFY
for %%D in (X H R F E M Z) do (
 call :SHARE %%D
 dir "\\%NAS%\!SHARE!" >nul 2>&1
 if not errorlevel 1 (
  set "OLD="
  for /f "delims=" %%P in ('powershell.exe -NoProfile -Command "(Get-SmbMapping -LocalPath '%%D:' -ErrorAction SilentlyContinue).RemotePath"') do set "OLD=%%P"
  if /I not "!OLD!"=="\\%NAS%\!SHARE!" (
   if defined OLD (
    echo %%D: is currently !OLD!
    choice /C YN /M "Replace this mapping"
    if not errorlevel 2 net use %%D: /delete /y
   )
   if not exist %%D:\ (
    echo Installing %%D: \\%NAS%\!SHARE!
    net use %%D: "\\%NAS%\!SHARE!" /persistent:yes
   ) else (echo Occupied drive %%D: skipped.)
  )
 )
)
:VERIFY
echo.
echo ===== FINAL VERIFICATION =====
set /a PASSED=0
for %%D in (X H R F E M Z) do (
 call :SHARE %%D
 dir "\\%NAS%\!SHARE!" >nul 2>&1
 if not errorlevel 1 (
  set "OLD="
  for /f "delims=" %%P in ('powershell.exe -NoProfile -Command "(Get-SmbMapping -LocalPath '%%D:' -ErrorAction SilentlyContinue).RemotePath"') do set "OLD=%%P"
  if /I "!OLD!"=="\\%NAS%\!SHARE!" (
   dir %%D:\ >nul 2>&1
   if not errorlevel 1 (echo [PASS] %%D: !SHARE! & set /a PASSED+=1)
  ) else (echo [CHECK] %%D: !SHARE! not correctly mapped)
 )
)
echo Verified: !PASSED! of !ELIGIBLE! accessible shares.
goto END
:SHARE
if /I "%~1"=="X" set "SHARE=Executive"
if /I "%~1"=="H" set "SHARE=AdminHR"
if /I "%~1"=="R" set "SHARE=AdminMarketing"
if /I "%~1"=="F" set "SHARE=FinancePurchasing"
if /I "%~1"=="E" set "SHARE=Engineering"
if /I "%~1"=="M" set "SHARE=Marketing"
if /I "%~1"=="Z" set "SHARE=CompanyShared"
exit /b
:END
echo.
echo Thank you. If any drive remains missing, take a screenshot
echo and contact your company administrator or AXON IT support.
echo Never include passwords in screenshots.
pause
endlocal