import streamlit as st
from datetime import date

# 감정 분석 함수 (실제 로직으로 대체 가능)
def analyze_emotion(diary_text):
    return {"main_emotion": "행복", "solution_name": "긍정적인 사고", "details": "긍정적인 생각을 유지하고 동기부여를 잃지 마세요!"}

# 일기 저장 상태 관리
if 'diary_entries' not in st.session_state:
    st.session_state['diary_entries'] = {}

# 메인 화면
st.title("감정 분석 일기")
selected_date = st.sidebar.date_input("날짜 선택", date.today())
st.sidebar.write("선택한 날짜:", selected_date)

if selected_date not in st.session_state['diary_entries']:
    st.session_state['diary_entries'][selected_date] = {"text": "", "image": None, "solution": None}

# 일기 입력 팝업
with st.container():
    st.subheader(f"{selected_date}의 일기를 작성하세요")
    diary_text = st.text_area("일기 내용", st.session_state['diary_entries'][selected_date]["text"], height=100)
    
    uploaded_image = st.file_uploader("이미지 업로드", type=["png", "jpg", "jpeg"])
    
    # 일기 저장 버튼
    if st.button("일기 저장"):
        st.session_state['diary_entries'][selected_date]["text"] = diary_text
        st.session_state['diary_entries'][selected_date]["image"] = uploaded_image
        st.success("일기가 저장되었습니다!")

        # 저장 후 솔루션 생성
        solution = analyze_emotion(diary_text)
        st.session_state['diary_entries'][selected_date]["solution"] = solution

    # 솔루션 보기 버튼
    if st.session_state['diary_entries'][selected_date]["solution"]:
        if st.button("솔루션 보기"):
            with st.container():
                st.subheader(f"{selected_date}의 일기")
                st.write(diary_text)
                
                if uploaded_image:
                    st.image(uploaded_image, caption="업로드된 이미지")
                
                st.subheader("추천 솔루션")
                solution = st.session_state['diary_entries'][selected_date]["solution"]
                st.write(f"**대표 감정:** {solution['main_emotion']}")
                st.write(f"**솔루션명:** {solution['solution_name']}")
                st.write(f"**상세 내용:** {solution['details']}")

# 스크롤 기능 추가 (내용이 브라우저 창보다 클 때)
st.markdown("""
    <style>
    .css-1d391kg { 
        overflow: auto;
        height: 100vh;
    }
    </style>
    """, unsafe_allow_html=True)
