import os
import streamlit as st
from google.cloud import secretmanager
from google.cloud import bigquery
import json
import tempfile

# Google Cloud 프로젝트 ID 및 비밀 이름
project_id = "semiotic-vial-440207-q4"  # 올바른 프로젝트 ID 사용
secret_id = "moviejj"  # Secret Manager에 저장된 비밀 이름

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

# 서비스 계정 JSON 파일의 경로를 환경 변수로 설정
os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = service_account_file_path

# BigQuery 클라이언트 생성
bigquery_client = bigquery.Client(project=project_id)

# Streamlit 앱 UI
st.title("Streamlit to GCP BigQuery")
st.write("Enter data to insert into BigQuery")

# 사용자 입력을 받아 데이터 생성
name = st.text_input("Name")
age = st.number_input("Age", min_value=0, step=1)

# BigQuery 테이블 설정
dataset_id = "json_test"
table_id = "userstest"
table_ref = f"{project_id}.{dataset_id}.{table_id}"

# 데이터 삽입 버튼
if st.button("Insert into BigQuery"):
    try:
        rows_to_insert = [
            {u"name": name, u"age": age}
        ]
        
        errors = bigquery_client.insert_rows_json(table_ref, rows_to_insert)
        
        if not errors:
            st.success("Data inserted successfully!")
        else:
            st.error(f"Encountered errors while inserting: {errors}")
    except Exception as e:
        st.error(f"An error occurred: {str(e)}")
