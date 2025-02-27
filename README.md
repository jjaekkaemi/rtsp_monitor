## 개발 환경 설정

### 가상환경 설정

```
# Windows
python -m venv venv
.\venv\Scripts\activate

# macOS/Linux:
python3 -m venv venv
source venv/bin/activate
```

### 의존성 설치

```
pip install -r requirements.txt
```

### 파이썬 실행 방법

```
python rtsp_monitor.py [rtsp_url] [--interval 초] [--timeout 초] [--image 0/1]
```

### 매개변수

- rtsp_url: 모니터링할 RTSP 스트림 URL (필수)
- --interval: 모니터링 간격 (초 단위, 기본값: 1)
- --timeout: 연결 타임아웃 (초 단위, 기본값: 5)
- --image: 이미지 저장 여부 (0 - False, 1 - True, 기본값: 1)

## 빌드 방법

- 빌드 후에는 dist 폴더 안에 실행 파일 생성

### 수동 빌드

```
pyinstaller --onefile --noconsole rtsp_monitor.py --name rtsp_monitor.exe
```

### 자동 빌드

- Windows: build_win.bat 실행
- macOS/Linux: build_unix.sh 실행

## .exe 실행 방법

Windows:

```
rtsp_monitor.exe [rtsp_url] [--interval 초] [--timeout 초] [--image 0/1]
```

macOS/Linux:

```

```

### 사용 예시

Windows:

```
# 기본 설정으로 실행
rtsp_monitor.exe rtsp://example.com:554/stream --image 0

# 사용자 지정 간격과 타임아웃으로 실행
rtsp_monitor.exe rtsp://example.com:554/stream --interval 2 --timeout 10 --image 0
```

macOS/Linux:

```

```

## 로그 출력 예시

```
[2025-02-26 16:52:42,597] - [INFO] - [Start] - RTSP monitoring initiated for URL: rtsp://172.30.1.101:8080/h264.sdp
[2025-02-26 16:52:42,620] - [INFO] - [Connected] - RTSP URI is accessible
[2025-02-26 16:52:43,935] - [INFO] - [Streaming] - RTSP stream is running: Stream is working
[2025-02-26 16:52:43,935] - [INFO] - [Status] - Current Status: URI Connected, Stream Active
[2025-02-26 16:52:46,501] - [INFO] - [Status] - Current Status: URI Connected, Stream Active
[2025-02-26 16:52:49,496] - [INFO] - [Status] - Current Status: URI Connected, Stream Active
[2025-02-26 16:52:52,643] - [ERROR] - [Error] - Cannot connect to RTSP server at rtsp://172.30.1.101:8080/h264.sdp: [WinError 10061] 대상 컴퓨터에서 연결을 거부했으므로 연결하지 못했습니다
[2025-02-26 16:52:52,644] - [ERROR] - [Disconnected] - Cannot connect to RTSP URI
[2025-02-26 16:52:52,644] - [INFO] - [Status] - Current Status: URI Disconnected, Stream Inactive
[2025-02-26 16:52:55,783] - [INFO] - [Status] - Current Status: URI Disconnected, Stream Inactive
[2025-02-26 16:52:56,816] - [INFO] - [Connected] - RTSP URI is accessible
[2025-02-26 16:52:56,817] - [INFO] - [Time] - RTSP URI reconnected after 4.17 seconds
[2025-02-26 16:52:59,130] - [INFO] - [Status] - Current Status: URI Connected, Stream Active
[2025-02-26 16:53:01,936] - [INFO] - [Status] - Current Status: URI Connected, Stream Active
[2025-02-26 16:53:05,181] - [ERROR] - [Error] - Cannot connect to RTSP server at rtsp://172.30.1.101:8080/h264.sdp: [WinError 10061] 대상 컴퓨터에서 연결을 거부했으므로 연결하지 못했습니다
[2025-02-26 16:53:05,181] - [ERROR] - [Disconnected] - Cannot connect to RTSP URI
[2025-02-26 16:53:05,181] - [INFO] - [Status] - Current Status: URI Disconnected, Stream Inactive
[2025-02-26 16:53:06,204] - [INFO] - [Connected] - RTSP URI is accessible
[2025-02-26 16:53:06,205] - [INFO] - [Time] - RTSP URI reconnected after 1.02 seconds
[2025-02-26 16:53:08,746] - [INFO] - [Status] - Current Status: URI Connected, Stream Active
[2025-02-26 16:53:11,321] - [INFO] - [Status] - Current Status: URI Connected, Stream Active
[2025-02-26 16:53:14,042] - [INFO] - [Status] - Current Status: URI Connected, Stream Active
[2025-02-26 16:53:20,062] - [INFO] - [Status] - Current Status: URI Connected, Stream Active
[2025-02-26 16:53:21,816] - [ERROR] - [Stream Failed] - RTSP stream lost: Failed to read frame
[2025-02-26 16:53:21,817] - [INFO] - [Status] - Current Status: URI Connected, Stream Inactive
[2025-02-26 16:53:27,161] - [INFO] - [Streaming] - RTSP stream is running: Stream is working
[2025-02-26 16:53:27,161] - [INFO] - [Time] - RTSP stream restored after 5.34 seconds
[2025-02-26 16:53:27,161] - [INFO] - [Status] - Current Status: URI Connected, Stream Active
[2025-02-26 16:53:29,665] - [INFO] - [Status] - Current Status: URI Connected, Stream Active
[2025-02-26 16:53:32,495] - [INFO] - [Status] - Current Status: URI Connected, Stream Active
[2025-02-26 16:53:35,581] - [INFO] - [Status] - Current Status: URI Connected, Stream Active
```

- `[Start]` - 첫 시작시
- `[Connected]` - RTSP 네트워크 연결 시
- `[Streaming]` - RTSP 스트림 연결 시
- `[Disconnected]` - RTSP 네트워크 연결 Timeout
- `[Stream Faile]` - RTSP 스트림 연결 실패 시
- `[Status]` - 현재 프로그램이 제대로 동작하는 지 찍는 로그
- `[Time]` - 네트워크 및 스트림 연결 전환(실패->성공)시 시간 간격(초)

## 백그라운드 환경 실행

### .exe 파일 옮기기

- 원하는 경로에 파일 옮기기, 관리자 권한이 필요한 경로는 따로 관리자 권한 주어야 함
  - 보통 `문서` 경로에 넣기

### 배치 파일 생성

```
@echo off

REM 실행 중인 프로세스 종료 (강제 종료 포함)
taskkill /F /IM rtsp_monitor.exe 2>nul

REM 문서 폴더 경로 가져오기
set "DOCS_PATH=%USERPROFILE%\Documents"

cd /d "%DOCS_PATH%"

REM 새로운 프로세스 실행
start rtsp_monitor.exe "[rtsp_url]" --interval 1 --timeout 5

```

- 위 코드를 복사한 후, `[rtsp_url]` 안에 모니터링할 url 넣어준 다음, .bat으로 파일 생성

### 배치 파일을 윈도우 시작 프로그램에 등록

- 자동 실행하려면 윈도우 시작 프로그램에 등록해야 함

1. 윈도우 + R 키를 누르고 `shell:startup` 입력 후 엔터 또는 `%APPDATA%\Microsoft\Windows\Start Menu\Programs\Startup` 경로를 복사하여 파일 탐색기로 직접 이동
2. .bat 파일을 넣어주기
3. 바로가기를 만들어 바탕화면에 놓아주기 (처음 실행 시 직접 실행)

### 프로그램 동작 확인

- 작업관리자에서 해당 프로그램 실행하는 지 체크
- 문서 폴더 안에 log/rtsp_monitor.log 쌓이는 지 체크

---

## 참고사항

- pyinstaller 의 `--uac-admin` 버그 또는 정책 문제로 인해 프로그램이 제대로 동작하지 않을 수 있음. `--uac-admin` 옵션을 제외하여 install 한 후, powershell 의 runas 로 실행

```
powershell Start-Process -FilePath "rtsp_monitor.exe [rtsp_url]" -Verb RunAs
```

- 간혹 카메라가 켜져 있는 데 opencv 로 read 가 안된다면 채널이 부족해서 그럴 수 있음. vlc 플레이어로 확인해보기
