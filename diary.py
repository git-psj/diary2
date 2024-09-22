import streamlit as st
import calendar
from datetime import date, datetime

# 감정 분석 함수 (실제 로직으로 대체 가능)
def analyze_emotion(diary_text):
    return {"main_emotion": "행복", "solution_name": "긍정적인 사고", "details": "긍정적인 생각을 유지하고 동기부여를 잃지 마세요!"}

# 일기 저장 상태 관리
if 'diary_entries' not in st.session_state:
    st.session_state['diary_entries'] = {}
if 'selected_day' not in st.session_state:
    st.session_state['selected_day'] = None

# 메인 화면
st.title("감정 분석 일기")

# 현재 월의 달력 표시
today = date.today()
current_year = today.year
current_month = today.month
cal = calendar.Calendar()

st.subheader(f"{current_year}년 {current_month}월")

# 날짜 선택 후 달력 크기 조정 및 일기 창 표시
if st.session_state['selected_day'] is None:
    # 달력 전체 크기로 출력
    cols = st.columns(7)
    weekdays = ['월', '화', '수', '목', '금', '토', '일']

    # 요일 출력
    for i, weekday in enumerate(weekdays):
        cols[i].write(weekday)

    # 달력 그리기
    days = [day for day in cal.itermonthdays(current_year, current_month) if day != 0]
    for i, day in enumerate(days):
        button_label = f"{day}"
        if cols[i % 7].button(button_label):
            st.session_state['selected_day'] = day
else:
    # 선택한 날짜 저장
    selected_date = date(current_year, current_month, st.session_state['selected_day'])
    
    # 달력을 작은 크기로 왼쪽에 표시하고 일기 입력창을 오른쪽에 표시
    left_col, right_col = st.columns([1, 2])

    # 왼쪽에 작은 달력 표시
    with left_col:
        st.write(f"선택한 날짜: {selected_date}")
        st.subheader(f"{current_year}년 {current_month}월")
        
        # 작은 달력 그리기
        cols = st.columns(7)
        weekdays = ['월', '화', '수', '목', '금', '토', '일']

        for i, weekday in enumerate(weekdays):
            cols[i].write(weekday)

        for i, day in enumerate(days):
            button_label = f"{day}"
            cols[i % 7].write(button_label)
    
    # 오른쪽에 일기 입력 창 표시
    with right_col:
        st.subheader(f"{selected_date}의 일기를 작성하세요")
        
        if selected_date not in st.session_state['diary_entries']:
            st.session_state['diary_entries'][selected_date] = {"text": "", "image": None, "solution": None}

        # 일기 입력창을 자동 확장, 그러나 브라우저 창 크기를 넘어가면 스크롤이 생기도록 설정
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
                st.subheader(f"{selected_date}의 일기")
                st.write(diary_text)

                if uploaded_image:
                    st.image(uploaded_image, caption="업로드된 이미지")

                st.subheader("추천 솔루션")
                solution = st.session_state['diary_entries'][selected_date]["solution"]
                st.write(f"**대표 감정:** {solution['main_emotion']}")
                st.write(f"**솔루션명:** {solution['solution_name']}")
                st.write(f"**상세 내용:** {solution['details']}")

# CSS를 사용하여 일기 입력창이 커지다가 브라우저 창보다 길어지면 스크롤이 생기도록 설정
st.markdown("""
    <style>
    textarea {
        min-height: 100px;
        max-height: 60vh; /* 브라우저 창의 60%까지만 입력창이 확장 */
        overflow-y: auto; /* 그 이상일 경우 스크롤 */
    }
    </style>
    """, unsafe_allow_html=True)
