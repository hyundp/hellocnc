# import streamlit as st
# from pymongo.mongo_client import MongoClient
# from pymongo.server_api import ServerApi
# from datetime import datetime
# import json

# # MongoDB 연결
# uri = "mongodb+srv://cnc1:MiEK12CiftoaYXF3@cnc1.f0c02.mongodb.net/?retryWrites=true&w=majority&appName=cnc1"
# client = MongoClient(uri)
# db = client.estimation_platform
# collection = db.user_preferences

# def init_session():
#     if 'external' not in st.session_state:
#         st.session_state.external = {}
#     if 'internal' not in st.session_state:
#         st.session_state.internal = {}

# def render_external():
#     col1, col2, col3 = st.columns(3)

#     with col1:
#         st.subheader("💖 외모")
#         with st.expander("👀 눈", expanded=True):
#             st.multiselect("눈 특징",  # 라벨 추가
#                 ["눈이 크다", "눈이 작다", "눈이 동그랗다", "눈이 찢어졌다"], 
#                 key="external.eyes"
#             )
    
#     with col2:  # 컬럼 구조 수정
#         st.subheader("👃 코")
#         with st.expander("코 특징", expanded=True):
#             st.multiselect("높이", ["높다", "낮다"], key="external.nose.height")
#             st.multiselect("모양", ["얇다", "두툼하다"], key="external.nose.shape")
    
#     with col3:
#         st.subheader("👄 입")
#         with st.expander("입 특징", expanded=True):
#             st.multiselect("입술 두께", ["두꺼운 입술", "얇은 입술"], key="external.mouth.lips")
#             st.checkbox("치열이 고름", key="external.mouth.teeth")


# def render_internal():
#     with st.expander("🧠 내적 요소 선택", expanded=True):
#         st.subheader("💬 소통 방식")
#         st.multiselect(
#             "의사소통 스타일",
#             ["대화가 잘 통함", "상대 감정 배려", "잘 웃음", "애정 표현 많음"],
#             key="internal.communication"
#         )
        
#         st.subheader("🌟 성격")
#         st.multiselect(
#             "주요 특성",
#             ["외향적", "내향적", "감정적", "이성적", "낙천적", "책임감 강함"],
#             key="internal.personality"
#         )

# def main():
#     st.set_page_config(page_title="차세대 인력추정 플랫폼", layout="wide")
#     init_session()
    
#     st.title("🔍 차세대 인력추정 플랫폼")
    
#     with st.form("profile_form"):
#         col1, col2 = st.columns([3, 2])
        
#         with col1:
#             name = st.text_input("이름", placeholder="홍길동")
            
#             # 외적/내적 요소 선택 탭
#             tab1, tab2 = st.tabs(["외적 요소", "내적 요소"])
            
#             with tab1:
#                 render_external()
                
#             with tab2:
#                 render_internal()
        
#         with col2:
#             st.markdown("### 📋 작성 가이드")
#             st.caption("1. 각 카테고리별 최소 1개 이상 선택")
#             st.caption("2. 정확한 매칭을 위해 구체적으로 선택")
#             st.caption("3. 저장 전 선택사항 다시 확인")
            
#             if st.form_submit_button("✅ 프로필 저장"):
#                 # 유효성 검사
#                 if not name.strip():
#                     st.error("이름을 입력해주세요")
#                     return
                
#                 # if not st.session_state.external or not st.session_state.internal:
#                 #     st.error("외적/내적 요소를 최소 1개 이상 선택해주세요")
#                 #     return
                
#                 try:
#                     profile = {
#                         "name": name.strip(),
#                         "external": st.session_state.external,
#                         "internal": st.session_state.internal,
#                         "created_at": datetime.now()
#                     }
                    
#                     result = collection.insert_one(profile)
#                     if result.inserted_id:
#                         st.success("프로필 저장 성공!")
#                         st.balloons()
#                         st.json(profile)  # 저장된 데이터 확인용
#                 except Exception as e:
#                     st.error(f"데이터베이스 오류: {str(e)}")

# if __name__ == "__main__":
#     main()

import streamlit as st
from pymongo.mongo_client import MongoClient
from pymongo.server_api import ServerApi
from datetime import datetime
from streamlit_tags import st_tags

# MongoDB 연결
uri = "mongodb+srv://cnc1:MiEK12CiftoaYXF3@cnc1.f0c02.mongodb.net/?retryWrites=true&w=majority&appName=cnc1"
client = MongoClient(uri)
db = client.estimation_platform
collection = db.user_preferences

# CSS 인젝션
toggle_style = """
<style>
.stButton > button {
    transition: all 0.3s ease;
    border: 2px solid #4F8BF9;
    color: #4F8BF9;
    background-color: white;
    margin: 2px;
    width: 100%;
}
.stButton > button[aria-pressed="true"] {
    background-color: #4F8BF9 !important;
    color: white !important;
    box-shadow: 0 2px 8px rgba(0,0,0,0.1);
}
</style>
"""


def init_session():
    if 'external' not in st.session_state:
        st.session_state.external = {'eyes': set(), 'nose': {'height': set(), 'shape': set()}, 'mouth': {'lips': set()}}
    if 'internal' not in st.session_state:
        st.session_state.internal = {'communication': set(), 'personality': set()}

def create_toggle_button(option, key, parent_key=None):
    full_key = f"{parent_key}.{option}" if parent_key else option
    current_set = st.session_state[parent_key.split('.')[0]][parent_key.split('.')[1]] if parent_key else st.session_state[key]
    
    is_selected = option in current_set
    button_type = "primary" if is_selected else "secondary"
    
    if st.button(option, key=full_key, type=button_type):
        if is_selected:
            current_set.remove(option)
        else:
            current_set.add(option)
        st.rerun()

# def render_external():
#     col1, col2, col3 = st.columns(3)

#     with col1:
#         st.subheader("💖 외모")
#         with st.expander("👀 눈", expanded=True):
#             eye_options = ["눈이 크다", "눈이 작다", "눈이 동그랗다", "눈이 찢어졌다", "기타"]
#             selected_eyes = st.multiselect("눈 특징", eye_options, key="external.eyes")

#             # 2. "기타"가 선택된 경우에만 입력창 노출
#             eyes_extra = ""
#             if "기타" in selected_eyes:
#                 eyes_extra = st.text_input("기타 눈 특징을 입력하세요", key="external.eyes.extra")

#             # 3. 값 합치기 (폼 제출 시 활용)
#             st.session_state['external_eyes_final'] = [
#                 x for x in selected_eyes if x != "기타"
#             ]
#             if "기타" in selected_eyes and eyes_extra.strip():
#                 # 쉼표로 여러 개 입력 가능
#                 st.session_state['external_eyes_final'] += [x.strip() for x in eyes_extra.split(",") if x.strip()]

#     with col2:
#         st.subheader("👃 코")
#         with st.expander("코 특징", expanded=True):
#             st.write("높이")
#             cols = st.columns(2)
#             for idx, option in enumerate(["높다", "낮다"]):
#                 with cols[idx%2]:
#                     create_toggle_button(option, "height", parent_key="external.nose.height")
            
#             st.write("모양")
#             cols = st.columns(2)
#             for idx, option in enumerate(["얇다", "두툼하다"]):
#                 with cols[idx%2]:
#                     create_toggle_button(option, "shape", parent_key="external.nose.shape")

#     with col3:
#         st.subheader("👄 입")
#         with st.expander("입 특징", expanded=True):
#             cols = st.columns(2)
#             for idx, option in enumerate(["두꺼운 입술", "얇은 입술"]):
#                 with cols[idx%2]:
#                     create_toggle_button(option, "lips", parent_key="external.mouth.lips")
#             st.checkbox("치열이 고름", key="external.mouth.teeth")

# def render_internal():
#     with st.expander("🧠 내적 요소 선택", expanded=True):
#         st.subheader("💬 소통 방식")
#         cols = st.columns(2)
#         comm_options = ["대화가 잘 통함", "상대 감정 배려", "잘 웃음", "애정 표현 많음"]
#         for idx, option in enumerate(comm_options):
#             with cols[idx%2]:
#                 create_toggle_button(option, "communication", parent_key="internal.communication")
        
#         st.subheader("🌟 성격")
#         cols = st.columns(2)
#         personality_options = ["외향적", "내향적", "감정적", "이성적", "낙천적", "책임감 강함"]
#         for idx, option in enumerate(personality_options):
#             with cols[idx%2]:
#                 create_toggle_button(option, "personality", parent_key="internal.personality")


def convert_sets_to_lists(obj):
    if isinstance(obj, set):
        return list(obj)
    elif isinstance(obj, dict):
        return {k: convert_sets_to_lists(v) for k, v in obj.items()}
    else:
        return obj

def main():
    st.title("🔍 차세대 인력추정 플랫폼")

    col1, col2 = st.columns([3, 2])
    with col1:
        name = st.text_input("이름", placeholder="홍길동")
        tab1, tab2 = st.tabs(["외적 요소", "내적 요소"])
        with tab1:
            st.subheader("👀 눈")
            
            eye_options = ["눈이 크다", "눈이 작다", "눈이 동그랗다", "눈이 찢어졌다", "기타"]

            selected_eyes = st.multiselect("눈 특징", eye_options)

            # 2. "기타"가 선택된 경우 입력창 노출
            eyes_extra = []
            if "기타" in selected_eyes:
                eyes_extra = st_tags(
                label='눈 특징 (엔터로 추가)',
                text='직접 입력',
                suggestions=eye_options,
                maxtags=10,
                key='eyes'
            )

            # 3. 기타를 제외한 선택값과 직접입력값 합치기
            eyes_final = [x for x in selected_eyes if x != "기타"]
            if "기타" in selected_eyes and eyes_extra:
                eyes_final += [x.strip() for x in eyes_extra if x.strip()]

            st.subheader("👃 코")
            
            # 2. 코 높이
            nose_height_options = ["높다", "낮다", "기타"]
            selected_nose_height = st.multiselect("코 높이", nose_height_options)
            nose_height_extra = []
            if "기타" in selected_nose_height:
                nose_height_extra = st_tags(
                    label='코 높이 (엔터로 추가)',
                    text='직접 입력',
                    suggestions=nose_height_options,
                    maxtags=10,
                    key='nose_height_extra'
                )
            nose_height_final = [x for x in selected_nose_height if x != "기타"]
            if "기타" in selected_nose_height and nose_height_extra:
                nose_height_final += [x.strip() for x in nose_height_extra if x.strip()]

            # 3. 코 모양
            nose_shape_options = ["얇다", "두툼하다", "기타"]
            selected_nose_shape = st.multiselect("코 모양", nose_shape_options)
            nose_shape_extra = []
            if "기타" in selected_nose_shape:
                nose_shape_extra = st_tags(
                    label='코 모양 (엔터로 추가)',
                    text='직접 입력',
                    suggestions=nose_shape_options,
                    maxtags=10,
                    key='nose_shape_extra'
                )
            nose_shape_final = [x for x in selected_nose_shape if x != "기타"]
            if "기타" in selected_nose_shape and nose_shape_extra:
                nose_shape_final += [x.strip() for x in nose_shape_extra if x.strip()]

            st.subheader("👄 입")

            # 4. 입술 두께
            lips_options = ["두꺼운 입술", "얇은 입술", "기타"]
            selected_lips = st.multiselect("입술 두께", lips_options)
            lips_extra = []
            if "기타" in selected_lips:
                lips_extra = st_tags(
                    label='입술 두께 (엔터로 추가)',
                    text='직접 입력',
                    suggestions=lips_options,
                    maxtags=10,
                    key='lips_extra'
                )
            lips_final = [x for x in selected_lips if x != "기타"]
            if "기타" in selected_lips and lips_extra:
                lips_final += [x.strip() for x in lips_extra if x.strip()]

            # 5. 치아
            teeth_options = ["치열이 고름", "기타"]
            selected_teeth = st.multiselect("치아", teeth_options)
            teeth_extra = []
            if "기타" in selected_teeth:
                teeth_extra = st_tags(
                    label='치아 (엔터로 추가)',
                    text='직접 입력',
                    suggestions=teeth_options,
                    maxtags=10,
                    key='teeth_extra'
                )
            teeth_final = [x for x in selected_teeth if x != "기타"]
            if "기타" in selected_teeth and teeth_extra:
                teeth_final += [x.strip() for x in teeth_extra if x.strip()]

        with tab2:
            st.subheader("💬 소통 방식")
            comm_options = ["대화가 잘 통함", "상대 감정 배려", "잘 웃음", "애정 표현 많음", "기타"]
            selected_comm = st.multiselect("의사소통 스타일", comm_options)
            comm_extra = []
            if "기타" in selected_comm:
                comm_extra = st_tags(
                    label='💬 소통 방식 (엔터로 추가)',
                    text='',
                    suggestions=comm_options,
                    maxtags=10,
                    key='comm_extra'
                )
            communication = [x for x in selected_comm if x != "기타"]
            if "기타" in selected_comm and comm_extra:
                communication += [x.strip() for x in comm_extra if x.strip()]

            st.subheader("🌟 성격")
            personality_options = ["외향적", "내향적", "감정적", "이성적", "낙천적", "책임감 강함", "기타"]
            selected_personality = st.multiselect("주요 특성", personality_options)
            personality_extra = []
            if "기타" in selected_personality:
                personality_extra = st_tags(
                    label='🌟 성격 (엔터로 추가)',
                    text='',
                    suggestions=personality_options,
                    maxtags=10,
                    key='personality_extra'
                )
            personality = [x for x in selected_personality if x != "기타"]
            if "기타" in selected_personality and personality_extra:
                personality += [x.strip() for x in personality_extra if x.strip()]
    with col2:
        st.markdown("### 📋 작성 가이드")
        st.caption("1. 각 카테고리별 최소 1개 이상 선택")
        st.caption("2. 정확한 매칭을 위해 구체적으로 선택")
        st.caption("3. 저장 전 선택사항 다시 확인")


    with st.form("profile_form"):
        submitted = st.form_submit_button("✅ 프로필 저장")
        if submitted:
            if not name.strip():
                st.error("이름을 입력해주세요")
                return
            try:
                profile = {
                    "name": name.strip(),
                    "external": {
                        "eyes": eyes_final,
                        "nose": {"height": nose_height_final, "shape": nose_shape_final},
                        "mouth": {"lips": lips_final, "teeth": teeth_final}
                    },
                    "internal": {
                        "communication": communication,
                        "personality": personality
                    },
                    "created_at": datetime.now()
                }
                result = collection.insert_one(profile)
                if result.inserted_id:
                    st.success("프로필 저장 성공!")
                    st.balloons()
                    st.json(profile)
            except Exception as e:
                st.error(f"데이터베이스 오류: {str(e)}")

if __name__ == "__main__":
    main()