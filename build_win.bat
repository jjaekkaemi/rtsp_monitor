@echo off
:: venv 폴더가 있으면 삭제
if exist venv (
    echo Deleting existing venv folder...
    rmdir /s /q venv
)

:: 가상환경 생성
echo Creating virtual environment...
python -m venv venv

:: 가상환경 활성화
echo Activating virtual environment...
call venv\Scripts\activate

:: requirements.txt에 있는 모듈 설치
echo Installing dependencies...
pip install -r requirements.txt

:: pyinstaller로 .exe 파일 생성
echo Building executable with pyinstaller...
pyinstaller --onefile --noconsole rtsp_monitor.py --name rtsp_monitor.exe

:: venv 비활성화
deactivate

:: venv 폴더 삭제
echo Deleting venv folder...
rmdir /s /q venv

:: 완료 메시지
echo Build process completed successfully!
pause
