import streamlit as st
import firebase_admin
from firebase_admin import credentials, auth, firestore

# Firebase 초기화
firebase_credentials = st.secrets["firebase"]
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

def main():
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

if __name__ == "__main__":
    main()
