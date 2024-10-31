import os
import streamlit as st
from google.cloud import bigquery

# 서비스 계정 JSON 파일의 경로를 환경 변수로 설정
os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = "semiotic-vial-440207-q4-898f401704c0.json"

# BigQuery 클라이언트 생성
client = bigquery.Client()

# Streamlit 앱 UI
st.title("Streamlit to GCP BigQuery")
st.write("Enter data to insert into BigQuery")

# 사용자 입력을 받아 데이터 생성
name = st.text_input("Name")
age = st.number_input("Age", min_value=0, step=1)

# BigQuery 테이블 설정
project_id = "semiotic-vial-440207-q4"  # 사용자의 GCP 프로젝트 ID
dataset_id = "json_test"                  # 사용자의 데이터셋 이름
table_id = "userstest"                    # 테이블 이름
table_ref = f"{project_id}.{dataset_id}.{table_id}"

# 데이터 삽입 버튼
if st.button("Insert into BigQuery"):
    try:
        rows_to_insert = [
            {u"name": name, u"age": age}
        ]
        
        errors = client.insert_rows_json(table_ref, rows_to_insert)
        
        if errors == []:
            st.success("Data inserted successfully!")
        else:
            st.error(f"Encountered errors while inserting: {errors}")
    except Exception as e:
        st.error(f"An error occurred: {str(e)}")
