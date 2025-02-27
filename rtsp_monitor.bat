@echo off

REM 실행 중인 프로세스 종료 (강제 종료 포함)
taskkill /F /IM rtsp_monitor.exe 2>nul

REM 문서 폴더 경로 가져오기
set "DOCS_PATH=%USERPROFILE%\Documents"

cd /d "%DOCS_PATH%"

REM 새로운 프로세스 실행
start rtsp_monitor.exe "rtsp://172.30.1.101:8080/h264.sdp" --interval 1 --timeout 5
