import streamlit as st
import firebase_admin
from firebase_admin import credentials, auth, firestore
from streamlit_option_menu import option_menu
from datetime import datetime

# secrets.toml에서 Firebase 자격 증명 정보 가져오기
firebase_credentials = {
    "type": st.secrets["firebase"]["type"],
    "project_id": st.secrets["firebase"]["project_id"],
    "private_key_id": st.secrets["firebase"]["private_key_id"],
    "private_key": st.secrets["firebase"]["private_key"].replace('\\n', '\n'),
    "client_email": st.secrets["firebase"]["client_email"],
    "client_id": st.secrets["firebase"]["client_id"],
    "auth_uri": st.secrets["firebase"]["auth_uri"],
    "token_uri": st.secrets["firebase"]["token_uri"],
    "auth_provider_x509_cert_url": st.secrets["firebase"]["auth_provider_x509_cert_url"],
    "client_x509_cert_url": st.secrets["firebase"]["client_x509_cert_url"]
}

# Firebase 초기화 중복 방지
if not firebase_admin._apps:
    cred = credentials.Certificate(firebase_credentials)
    firebase_admin.initialize_app(cred)

# Firestore 초기화
db = firestore.client()

def register_user(email, password, nickname, age_group, gender, address):
    try:
        # Firebase Authentication으로 사용자 등록
        user = auth.create_user(email=email, password=password)
        st.success(f"회원가입 성공! 사용자 ID: {user.uid}")

        # Firestore에 사용자 정보 저장
        user_data = {
            "email": email,
            "nickname": nickname,
            "age_group": age_group,
            "gender": gender,
            "address": address
        }
        db.collection("users").document(user.uid).set(user_data)
        st.success("사용자 정보가 Firestore에 저장되었습니다.")

    except Exception as e:
        st.error(f"오류 발생: {e}")

def signup_page():
    st.title("회원가입")

    # 회원가입 입력 폼
    email = st.text_input("이메일")
    password = st.text_input("비밀번호", type="password")
    password_confirm = st.text_input("비밀번호 확인", type="password")
    nickname = st.text_input("닉네임")
    age_group = st.selectbox("연령대", ["10대", "20대", "30대", "40대", "50대 이상"])
    gender = st.selectbox("성별", ["남성", "여성", "기타"])
    address = st.text_input("주소 (시/도)")

    # 회원가입 버튼
    if st.button("회원가입", key="signup"):
        if password != password_confirm:
            st.error("비밀번호가 일치하지 않습니다.")
        else:
            register_user(email, password, nickname, age_group, gender, address)

def login_page():
    st.title("로그인 페이지")
    email = st.text_input("이메일")
    password = st.text_input("비밀번호", type="password")
    
    if st.button("로그인", key="login"):
        try:
            user = auth.sign_in_with_email_and_password(email, password)
            # 로그인 성공 시 처리 로직 추가
            st.success(f"{email}님, 로그인 성공!")
        except auth.AuthError as e:
            st.error(f"로그인 실패: {str(e)}")

# 기본 페이지 설정
st.set_page_config(page_title="일기 작성", layout="wide")

# 왼쪽에 달력 표시
with st.sidebar:
    selected_date = st.date_input("날짜 선택", datetime.now())

# 일기 작성 레이아웃
st.markdown(f"## {selected_date} 일기 작성")
st.markdown(auth.get_user_by_email(username))

# 일기 내용 입력
diary_text = st.text_area("일기 내용 입력", height=200)

# 이미지 업로드
uploaded_image = st.file_uploader("이미지 삽입", type=['jpg', 'png', 'jpeg'])

# 저장 버튼
if st.button("저장"):
    # 파이어베이스에 저장
    diary_entry = {
        "id" : auth.get_user_by_email(username),
        "date": selected_date.strftime("%Y-%m-%d"),
        "content": diary_text,
        "image": uploaded_image.name if uploaded_image else None
    }
    
    # 파이어베이스에 일기 저장
    db.collection("diaries").add(diary_entry)
    
    st.success("일기가 저장되었습니다.")

# 솔루션 보기 버튼
if st.button("솔루션 보러가기"):
    st.write("솔루션 페이지로 이동합니다.")

# 세션 상태 확인 및 페이지 설정
if "page" not in st.session_state:
    st.session_state.page = "login" 

if st.button("회원가입 하러 가기", key="select_signup"):  # 고유 키
    st.session_state.page = "signup"
elif st.button("로그인 하러 가기", key="select_login"):  # 고유 키
    st.session_state.page = "login"

# 세션 상태에 따라 로그인 또는 회원가입 페이지 표시
if st.session_state.page == "login":
    login_page()
else:
    signup_page()
