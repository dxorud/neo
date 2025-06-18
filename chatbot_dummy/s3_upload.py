import os
import boto3
from dotenv import load_dotenv

# 환경변수 로드
load_dotenv()

ACCESS_KEY = os.getenv('AWS_ACCESS_KEY_ID')
SECRET_KEY = os.getenv('AWS_SECRET_ACCESS_KEY')
REGION = os.getenv('AWS_DEFAULT_REGION')
BUCKET_NAME = os.getenv('S3_BUCKET_NAME')

# 경로 자동 계산 (스크립트 위치 기준)
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
dummy_data_path = os.path.join(BASE_DIR, 'dummy_data')

# S3 클라이언트 생성
s3 = boto3.client(
    's3',
    aws_access_key_id=ACCESS_KEY,
    aws_secret_access_key=SECRET_KEY,
    region_name=REGION
)

# 업로드 함수
def upload_files():
    if not os.path.exists(dummy_data_path):
        print(f"❌ 폴더 없음: {dummy_data_path}")
        return

    files = [f for f in os.listdir(dummy_data_path) if f.endswith('.json')]
    
    if not files:
        print("❌ 업로드할 JSON 파일이 없습니다.")
        return

    for filename in files:
        local_file_path = os.path.join(dummy_data_path, filename)
        s3_key = f'project/{filename}'

        try:
            s3.upload_file(local_file_path, BUCKET_NAME, s3_key)
            print(f"✅ {filename} → S3://{BUCKET_NAME}/{s3_key} 업로드 완료")
        except Exception as e:
            print(f"❌ {filename} 업로드 실패: {e}")

if __name__ == "__main__":
    upload_files()
    print("✅ 업로드 완료!")