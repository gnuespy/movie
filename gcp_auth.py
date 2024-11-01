# gcp_auth.py
import os
import json
import tempfile
from google.cloud import secretmanager

def setup_google_cloud_credentials(project_id, secret_id):
    # Secret Manager 클라이언트 생성
    client = secretmanager.SecretManagerServiceClient()

    # 비밀의 최신 버전 가져오기
    secret_version_name = f"projects/{project_id}/secrets/{secret_id}/versions/latest"
    response = client.access_secret_version(name=secret_version_name)

    # 비밀의 내용을 JSON으로 변환
    service_account_info = json.loads(response.payload.data.decode("UTF-8"))

    # 임시 파일에 서비스 계정 JSON 저장
    with tempfile.NamedTemporaryFile(delete=False, suffix=".json") as temp_file:
        temp_file.write(json.dumps(service_account_info).encode("UTF-8"))
        service_account_file_path = temp_file.name

    # 환경 변수에 서비스 계정 JSON 파일 경로 설정
    os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = service_account_file_path
