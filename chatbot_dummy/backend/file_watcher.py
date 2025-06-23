import os
import time
import boto3
from dotenv import load_dotenv
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler

# 📌 1. .env 파일 로드
load_dotenv(dotenv_path=os.path.join(os.path.dirname(__file__), '..', '.env'))

ACCESS_KEY = os.getenv('AWS_ACCESS_KEY_ID')
SECRET_KEY = os.getenv('AWS_SECRET_ACCESS_KEY')
REGION = os.getenv('AWS_DEFAULT_REGION')
BUCKET_NAME = os.getenv('S3_BUCKET_NAME')

# 📌 2. 감시할 폴더 경로 (chatbot_dummy/dummy_data)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))  # chatbot_dummy
WATCH_FOLDER = os.path.join(BASE_DIR, 'dummy_data')

# 📌 3. S3 클라이언트 생성
s3 = boto3.client(
    's3',
    aws_access_key_id=ACCESS_KEY,
    aws_secret_access_key=SECRET_KEY,
    region_name=REGION
)

# 📌 4. 감지 이벤트 핸들러 정의
class JsonUploadHandler(FileSystemEventHandler):
    def on_created(self, event):
        if event.is_directory:
            return
        if event.src_path.endswith('.json'):
            filename = os.path.basename(event.src_path)
            s3_key = f'project/{filename}'

            try:
                s3.upload_file(event.src_path, BUCKET_NAME, s3_key)
                print(f"✅ 자동 업로드 완료: {filename} → S3://{BUCKET_NAME}/{s3_key}")
            except Exception as e:
                print(f"❌ 업로드 실패: {filename} | 에러: {e}")

# 📌 5. 감시 시작 함수
def start_watching():
    if not os.path.exists(WATCH_FOLDER):
        print(f"❌ 감시 폴더가 없습니다: {WATCH_FOLDER}")
        return

    print(f"👀 감시 시작: {WATCH_FOLDER}")
    event_handler = JsonUploadHandler()
    observer = Observer()
    observer.schedule(event_handler, path=WATCH_FOLDER, recursive=False)
    observer.start()

    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        observer.stop()
    observer.join()
