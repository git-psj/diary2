import streamlit as st
import firebase_admin
from firebase_admin import credentials, auth, firestore

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

# 파싱된 dict로 Firebase 초기화
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
    if st.button("회원가입"):
        if password != password_confirm:
            st.error("비밀번호가 일치하지 않습니다.")
        else:
            register_user(email, password, nickname, age_group, gender, address)

def login_page():
    st.title("로그인 페이지")
    username = st.text_input("이메일")
    password = st.text_input("비밀번호", type="password")
    
    if st.button("로그인"):
        try:
            user = auth.sign_in_with_email_and_password(email, password)
            # 여기에 로그인 로직 추가
            # 예를 들어, 사용자의 비밀번호를 확인하는 추가적인 로직이 필요합니다.
            st.success(f"{user.email}님, 로그인 성공!")
        except auth.AuthError as e:
            st.error(f"로그인 실패: {str(e)}")


if st.button("회원가입 하러 가기", key="select_signup"):  # 고유 키
    signup_page()
elif st.button("로그인 하러 가기", key="select_login"):  # 고유 키
    login_page()
# else:
#     st.write("회원가입 또는 로그인 버튼을 클릭하세요.")
