pip install git+https://github.com/username/repository.git


import streamlit as st
import firebase_admin
from firebase_admin import credentials, firestore

# Firebase 서비스 계정 파일 경로
cred = credentials.Certificate("path_to_your_firebase_credentials.json")
firebase_admin.initialize_app(cred)

# Firestore 데이터베이스에 연결
db = firestore.client()

# Firestore 데이터 추가 예시
def add_user_data(user_id, user_data):
    db.collection("users").document(user_id).set(user_data)

# Streamlit을 통해 사용자 정보를 입력받아 Firestore에 저장하는 예시
st.title("Firebase 연결 예시")

user_id = st.text_input("사용자 ID 입력")
user_name = st.text_input("사용자 이름 입력")

if st.button("사용자 데이터 추가"):
    user_data = {
        "name": user_name
    }
    add_user_data(user_id, user_data)
    st.write(f"사용자 {user_name} 데이터가 Firestore에 추가되었습니다!")





import streamlit as st

# 페이지 레이아웃 설정
st.set_page_config(layout="centered")

# 페이지 배경 설정
page_bg_img = '''
<style>
body {
    background-image: url("https://images.unsplash.com/photo-1499084732479-de2c02d45fc4?crop=entropy&cs=tinysrgb&fit=max&fm=jpg&ixid=MnwzNjUyOXwwfDF8c2VhcmNofDN8fGNsb3VkeXxlbnwwfHx8fDE2NjQwNjE2Mzc&ixlib=rb-1.2.1&q=80&w=1080");
    background-size: cover;
}
</style>
'''

st.markdown(page_bg_img, unsafe_allow_html=True)

# 회원가입 제목
st.markdown("<h1 style='text-align: center; color: white;'>회원가입</h1>", unsafe_allow_html=True)

# 입력 필드
st.text_input("아이디", placeholder="아이디를 입력하세요")
st.text_input("비밀번호", type="password", placeholder="비밀번호를 입력하세요")
st.text_input("비밀번호 확인", type="password", placeholder="비밀번호를 다시 입력하세요")
st.text_input("닉네임", placeholder="닉네임을 입력하세요")

# 연령대 선택
age_group = st.selectbox("연령대", ["10대", "20대", "30대", "40대", "50대", "60대 이상"])

# 성별 선택
gender = st.radio("성별", ["남성", "여성", "기타"])

# 주소 (시/도) 입력
address = st.text_input("주소 (시/도)", placeholder="거주하는 시/도를 입력하세요")

# 중복 확인과 회원가입 버튼
col1, col2 = st.columns([3, 1])

with col1:
    st.button("중복 확인")

with col2:
    st.button("회원가입", key="submit")

# 제출 후 처리
if st.session_state.get("submit"):
    st.success("회원가입이 완료되었습니다!")
