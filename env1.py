import streamlit as st
from google.cloud import bigquery
from gcp_auth import setup_google_cloud_credentials

# Google Cloud 프로젝트 ID 및 비밀 이름
project_id = "semiotic-vial-440207-q4"  # 올바른 프로젝트 ID 사용
secret_id = "moviejj"  # Secret Manager에 저장된 비밀 이름

# Google Cloud 인증 설정
setup_google_cloud_credentials(project_id, secret_id)

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
