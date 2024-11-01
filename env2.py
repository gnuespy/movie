import os
import streamlit as st
from google.cloud import bigquery

# 서비스 계정 JSON 파일의 경로를 환경 변수로 설정
os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = "semiotic-vial-440207-q4-8235ac99e900.json"

# BigQuery 클라이언트 생성
project_id = "semiotic-vial-440207-q4"
client = bigquery.Client(project=project_id)

# Streamlit 앱 UI
st.title("BigQuery Datasets Check")

# BigQuery 데이터 세트 확인
try:
    datasets = client.list_datasets()  # 데이터 세트 목록 가져오기
    st.write("Datasets in project:")
    for dataset in datasets:
        st.write(dataset.dataset_id)
except Exception as e:
    st.error(f"An error occurred: {str(e)}")
