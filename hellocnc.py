import streamlit as st
from pymongo.mongo_client import MongoClient
from pymongo.server_api import ServerApi
from datetime import datetime
import json

# MongoDB 연결
uri = "mongodb+srv://cnc1:MiEK12CiftoaYXF3@cnc1.f0c02.mongodb.net/?retryWrites=true&w=majority&appName=cnc1"
client = MongoClient(uri)
db = client.estimation_platform
collection = db.user_preferences

def init_session():
    if 'external' not in st.session_state:
        st.session_state.external = {}
    if 'internal' not in st.session_state:
        st.session_state.internal = {}

def render_external():
    with st.expander("💖 외적 요소 선택", expanded=True):
        col1, col2, col3 = st.columns(3)
        
        # 눈
        with col1:
            st.subheader("👀 눈")
            st.multiselect("크기", ["크다", "작다"], key="external.eyes.size")
            st.multiselect("모양", ["동그랗다", "찢어졌다", "사슴 같은 맑은 눈"], key="external.eyes.shape")
        
        # 코
        with col2:
            st.subheader("👃 코")
            st.multiselect("높이", ["높다", "낮다"], key="external.nose.height")
            st.multiselect("모양", ["얇다", "두툼하다"], key="external.nose.shape")
        
        # 입
        with col3:
            st.subheader("👄 입")
            st.multiselect("입술 두께", ["두꺼운 입술", "얇은 입술"], key="external.mouth.lips")
            st.checkbox("치열이 고름", key="external.mouth.teeth")

    # 체형 및 기타 섹션 추가 구현...

def render_internal():
    with st.expander("🧠 내적 요소 선택", expanded=True):
        st.subheader("💬 소통 방식")
        st.multiselect(
            "의사소통 스타일",
            ["대화가 잘 통함", "상대 감정 배려", "잘 웃음", "애정 표현 많음"],
            key="internal.communication"
        )
        
        st.subheader("🌟 성격")
        st.multiselect(
            "주요 특성",
            ["외향적", "내향적", "감정적", "이성적", "낙천적", "책임감 강함"],
            key="internal.personality"
        )

def main():
    st.set_page_config(page_title="차세대 인력추정 플랫폼", layout="wide")
    init_session()
    
    st.title("🔍 차세대 인력추정 플랫폼")
    
    with st.form("profile_form"):
        col1, col2 = st.columns([3, 2])
        
        with col1:
            name = st.text_input("이름", placeholder="홍길동")
            
            # 외적/내적 요소 선택 탭
            tab1, tab2 = st.tabs(["외적 요소", "내적 요소"])
            
            with tab1:
                render_external()
                
            with tab2:
                render_internal()
        
        with col2:
            st.markdown("### 📋 작성 가이드")
            st.caption("1. 각 카테고리별 최소 1개 이상 선택")
            st.caption("2. 정확한 매칭을 위해 구체적으로 선택")
            st.caption("3. 저장 전 선택사항 다시 확인")
            
            if st.form_submit_button("✅ 프로필 저장"):
                # 유효성 검사
                if not name.strip():
                    st.error("이름을 입력해주세요")
                    return
                
                # if not st.session_state.external or not st.session_state.internal:
                #     st.error("외적/내적 요소를 최소 1개 이상 선택해주세요")
                #     return
                
                try:
                    profile = {
                        "name": name.strip(),
                        "external": st.session_state.external,
                        "internal": st.session_state.internal,
                        "created_at": datetime.now()
                    }
                    
                    result = collection.insert_one(profile)
                    if result.inserted_id:
                        st.success("프로필 저장 성공!")
                        st.balloons()
                        st.json(profile)  # 저장된 데이터 확인용
                except Exception as e:
                    st.error(f"데이터베이스 오류: {str(e)}")

if __name__ == "__main__":
    main()
