import streamlit as st
import firebase_admin
from firebase_admin import credentials, auth, firestore

# Firebase 초기화
firebase_credentials = {
  "type": "service_account",
  "project_id": "e-diary-61dc0",
  "private_key_id": "64aa1667bb5fb2eccafbcb305cbb667914e38623",
  "private_key": "-----BEGIN PRIVATE KEY-----\nMIIEvQIBADANBgkqhkiG9w0BAQEFAASCBKcwggSjAgEAAoIBAQC6J19a0sBA76d6\nr5jN4unuI7BiD20SKmpd3AJO44J+eCA/ZZqdua0ZtIup4MFseK3Vaar2vKwF8qiu\n2RK8YKeTQOfcoJbzru37+uFhf9sY5L3m/zZoncA6+IBcVxfRnsk6n70YgFTQKf8N\nmyP9MVS9l/peIvNUsSsw0yWIGosv8DbxVBuSSckhTX0mZ/2A12VucRvTwlWBvvoY\nPbYr0HxwDgjjAznHXdWKhqRavw65q3vNOoX49cRL9FD3rhOnGTYtR4UFwuzZGr9d\nlIZmFEMyFCckyrZOFCE741d7zR16ikZ2eOhY5+7meXnWp9zpcBFq+nU8L08I2cIl\nczOvST5lAgMBAAECggEADjFvG8Wl0uc/pbyg5R6MwRNt7b9I8z5r2oXDx0mhawy0\nDyFec76MbCe2RL8jAECgDTCy6eavI8tbASA1eLEF4qK4PiIgYEQEirz+IijvBsVD\nlWRjPM0j5ifvexricTqu4EFkCx79vtr03CmDMCYEVNBMzpCe00sO0ZIuJZc6G+8O\neh+cpt+mmefSqmJqbPvWsgghegaMcegKAzxQpQ7FOXUlbQqxrczpmUvtg7YZd98K\nyXVFKCrDnIOgbd3uMd9WUqvcDXQ7b8/bMnLthvoMxYvjX1T7j0Y7HIS5CzMVyhel\nuWqu2DPtnF36kt8hHM+bwIAtq6vvcf9P7Gs9FXN5oQKBgQDy3h4XCjeKA5ZGbx95\nD/ooYGpsdQJFzmoCU11nQpzc4fFQHOtOmCFwdlDI+OXhzqI4mL0BSIfrnTf0Lq+I\nPBAwVCBSXPmttn0uhc/ESLUTDz2ZFAm8NsuMNKxKJN1kC+f3oJAXw5JgJWG3tbME\nosbkAFfRdibci8h/Pj5QtVBrwwKBgQDEODJPSTlQFixIOhjPEQucQH/TFORKH6I7\nJYaDd4kq5YmOciXBb2kZwYt/Q39QbyZO+8MvE8ika82mutCth1w3AsPpovOUq9Un\nJOs0XmXMuWNBLJs0EsPpErMejstHJKmH6nayGw2dqHspx8Pd+eXO5Y58ebdhdlPO\neZyBOt2StwKBgQCpUnhSAdqEy0lq47Bim+QBYG7yHIWwG1/HLU3SXxuz14aBHxhi\nnCe8G5Do/LZwvrpUkRA8o8+3Uc4f3KieZ5m1yAEcyxt7o94UoFAg/bvYhOiiH9lF\nskIpBtQTgS4kwTRBbVzoZH5Zr9Y32WLs2XumnCKdsy0W2BG5vLB/XlmqNwKBgEyz\ncucPRnoJ0NGC9EOs9A7mH5FRb1OSPgZEyuoFBfdgtn6aHCwa8siAoZjjt5anfCAP\nxeJXJ20uPrtX9059xQwz5oUjj3ekG7QreE2GQODf7u6BE0Itu6sWBjKBuvBaYnKg\nsjk43f+s5kgUsHnKv4w6q5H4ujg82tGxM/5IFmjNAoGAZhyL4xvIEsxKi4Am9wnu\n/5nx3fD3NzfBhuEzkTSKe+i2QURvX7ziYIQ2A20DSfnSoG9t55Gk79YgeA3B0rg+\n8I4uN72R452u21f2bzHGO/S9/KqcanmWmnxln3hlUOEt2/p2rDFPifDDzNdLHxGn\nt7zdnzeN/fQFf6PZRTy9jUQ=\n-----END PRIVATE KEY-----\n",
  "client_email": "firebase-adminsdk-iig30@e-diary-61dc0.iam.gserviceaccount.com",
  "client_id": "112991912909130790639",
  "auth_uri": "https://accounts.google.com/o/oauth2/auth",
  "token_uri": "https://oauth2.googleapis.com/token",
  "auth_provider_x509_cert_url": "https://www.googleapis.com/oauth2/v1/certs",
  "client_x509_cert_url": "https://www.googleapis.com/robot/v1/metadata/x509/firebase-adminsdk-iig30%40e-diary-61dc0.iam.gserviceaccount.com",
  "universe_domain": "googleapis.com"
}
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
