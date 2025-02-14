import streamlit as st
from sqlalchemy import create_engine, Column, Integer, String, Text
from sqlalchemy.orm import declarative_base, sessionmaker
from pymongo.mongo_client import MongoClient
from pymongo.server_api import ServerApi
from datetime import datetime

# DB 연결 설정
uri = "mongodb+srv://cnc1:MiEK12CiftoaYXF3@cnc1.f0c02.mongodb.net/?retryWrites=true&w=majority&appName=cnc1"
client = MongoClient(uri, server_api=ServerApi('1'))
db = client.estimation_platform
collection = db.user_preferences

# 데이터 모델 정의

# UI 구성
st.title("🔍 차세대 인력추정 플랫폼")
with st.form("preference_form"):
    col1, col2 = st.columns(2)
    
    with col1:
        name = st.text_input("이름을 입력하세요", placeholder="홍길동")
        
    with col2:
        st.markdown("### 📝 작성 가이드")
        st.caption("- 외적: 키/체형/스타일 등")
        st.caption("- 내적: 성격/가치관/취미 등")

    external = st.text_area("외적 이상형 (최소 10자 이상)", 
                          help="구체적으로 작성할수록 매칭 정확도가 올라갑니다!")
    internal = st.text_area("내적 이상형 (최소 10자 이상)",
                          help="본인의 가치관과 잘 맞는 요소를 강조해주세요")
    
    submitted = st.form_submit_button("✅ 프로필 저장")
    
    if submitted:
        if len(name) == 0:
            st.error("이름을 반드시 입력해주세요")
        elif len(external) < 10 or len(internal) < 10:
            st.warning("각 항목을 10자 이상 작성해주세요")
        else:
            try:
                profile = {
                    "name": name.strip(),
                    "external": external.strip(),
                    "internal": internal.strip(),
                    "created_at": datetime.now()
                }
                result = collection.insert_one(profile)
                if result.inserted_id:
                    st.success("✅ 성공적으로 저장되었습니다!")
                    st.balloons()
                else:
                    st.error("저장에 실패했습니다.")
            except Exception as e:
                st.error(f"데이터베이스 오류: {str(e)}")