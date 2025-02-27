import cv2
import time
import logging
from logging.handlers import TimedRotatingFileHandler
import os
import socket
import argparse
from datetime import datetime
from urllib.parse import urlparse

# 로그 디렉토리 및 파일 설정
LOG_DIR = "log"
LOG_FILE = os.path.join(LOG_DIR, "rtsp_monitor.log")

if not os.path.exists(LOG_DIR):
    os.makedirs(LOG_DIR)

# TimedRotatingFileHandler: 매일 자정마다 새로운 로그 파일 생성, 최대 7일 보관
log_handler = TimedRotatingFileHandler(LOG_FILE, when="midnight", interval=1, backupCount=7, encoding="utf-8")
log_handler.setFormatter(logging.Formatter("[%(asctime)s] - [%(levelname)s] - %(message)s"))

# 로거 설정
logger = logging.getLogger()
logger.setLevel(logging.INFO)
logger.addHandler(log_handler)
logger.addHandler(logging.StreamHandler())  # 콘솔 출력용 핸들러 추가

# RTSP 서버 접속 가능 체크(네트워크 체크)
def check_rtsp_uri(rtsp_url, last_connection_failed, timeout):
    try:
        parsed_url = urlparse(rtsp_url)
        host = parsed_url.hostname
        port = parsed_url.port or 554  # 기본 RTSP 포트(554) 사용

        if not host or not port:
            raise ValueError(f"Invalid RTSP URL format: {rtsp_url}") 

        with socket.create_connection((host, port), timeout=timeout):
            return True, False  
    except (socket.timeout, socket.error, ValueError) as e:
        if not last_connection_failed: # 실패 시 한번만 로그 출력하기 위해 flag 체크
            logger.error(f"[Error] - Cannot connect to RTSP server at {rtsp_url}: {e}")
        return False, True  

# RTSP 스트림 확인 함수
def check_rtsp_stream(rtsp_url):
    try:
        cap = cv2.VideoCapture(rtsp_url, cv2.CAP_FFMPEG)
        cap.set(cv2.CAP_PROP_BUFFERSIZE, 1)
        cap.set(cv2.CAP_PROP_OPEN_TIMEOUT_MSEC, 1000)
        cap.set(cv2.CAP_PROP_READ_TIMEOUT_MSEC, 1000)

        if not cap.isOpened():
            return False, "Stream not opened"  

        ret, frame = cap.read()
        cap.release()

        if ret and frame is not None:
            return True, "Stream is working"
        else:
            return False, "Failed to read frame"
    except Exception as e:
        if cap:
            cap.release()
        return False, f"Error reading stream: {str(e)}"

# RTSP 모니터링 함수
def monitor_rtsp_stream(rtsp_url, interval, timeout):
    last_uri_status = None  
    last_connection_failed = False  
    last_stream_status = False  
    
    last_connection_time = None  
    last_stream_time = None  
    print_counter = 0
    first_run = True
    
    while True:
        try:
            uri_status, last_connection_failed = check_rtsp_uri(rtsp_url, last_connection_failed, timeout)
            if uri_status != last_uri_status:
                if uri_status:
                    logger.info("[Connected] - RTSP URI is accessible")
                    if last_connection_time:
                        elapsed_time = datetime.now() - last_connection_time
                        logger.info(f"[Time] - RTSP URI reconnected after {elapsed_time.total_seconds():.2f} seconds")
                else:
                    last_connection_time = datetime.now()  
                    last_stream_status = None
                    stream_status = None  
                    logger.error("[Disconnected] - Cannot connect to RTSP URI")
            message = ""  # message 변수 초기화
            if uri_status:
                stream_status, message = check_rtsp_stream(rtsp_url)
            else:
                stream_status = None  

            if first_run or (last_stream_status is not None and stream_status != last_stream_status):
                if stream_status:
                    logger.info(f"[Streaming] - RTSP stream is running: {message}")
                    if last_stream_time:
                        elapsed_time = datetime.now() - last_stream_time
                        logger.info(f"[Time] - RTSP stream restored after {elapsed_time.total_seconds():.2f} seconds")
                else:
                    last_stream_time = datetime.now()  
                    logger.error(f"[Stream Failed] - RTSP stream lost: {message}")
                first_run = False
            last_uri_status = uri_status
            last_stream_status = stream_status

            if print_counter % 5 == 0:
                logger.info(f"[Status] - Current Status: URI {'Connected' if uri_status else 'Disconnected'}, "
                            f"Stream {'Active' if stream_status else 'Inactive'}")
                print_counter = 0  
            else:
                print_counter += 1  

            time.sleep(interval)

        except Exception as e:
            logger.error(f"Unexpected error in monitoring loop: {e}")
            time.sleep(interval)  

if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="""Monitor RTSP stream.
Usage example:
    rtsp_monitor.exe rtsp://example.com:554/stream
    rtsp_monitor.exe rtsp://example.com:554/stream --interval 2 --timeout 10""",
        formatter_class=argparse.RawTextHelpFormatter
    )
    parser.add_argument("rtsp_url", help="RTSP URL to monitor")
    parser.add_argument("--interval", type=int, default=1, help="Monitoring interval in seconds")
    parser.add_argument("--timeout", type=int, default=5, help="Connection timeout in seconds")

    if len(os.sys.argv) == 1: 
        parser.print_help()
        input("Press Enter to exit...")  
    else:
        args = parser.parse_args()
        logger.info(f"[Start] - RTSP monitoring initiated for URL: {args.rtsp_url}")
        monitor_rtsp_stream(args.rtsp_url, args.interval, args.timeout)
