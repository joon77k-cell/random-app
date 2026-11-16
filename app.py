import streamlit as st
import random
from datetime import date

# 페이지 기본 설정
st.set_page_config(page_title="시험 대비 공부 시간 배분기", page_icon="📚", layout="centered")

st.title("📚 시험 대비 D-Day & 공부 시간 배분기")
st.markdown("남은 시험 기간과 오늘 공부할 시간을 입력하고 **배분하기 버튼**을 눌러보세요!")

st.divider()

# 1. 사이드바: 사용자 입력 영역
st.sidebar.header("⚙️ 시험 및 공부 설정")

exam_name = st.sidebar.text_input("시험 이름", value="2학기 기말고사")
exam_date = st.sidebar.date_input("시험 시작일", value=date.today())
daily_hours = st.sidebar.slider("하루 총 공부 가능 시간 (시간)", min_value=1.0, max_value=12.0, value=4.0, step=0.5)

st.sidebar.subheader("📝 공부할 과목 선택")
default_subjects = ["국어", "수학", "영어", "정보", "통합과학", "한국사"]
selected_subjects = st.sidebar.multiselect(
    "과목을 선택하세요 (최소 1개 이상)",
    options=default_subjects,
    default=["국어", "수학", "영어", "정보"]
)

# 2. 메인 화면: D-Day 계산 출력
today = date.today()
d_day = (exam_date - today).days

col1, col2 = st.columns(2)
with col1:
    if d_day > 0:
        st.metric(label=f"🎯 {exam_name}까지", value=f"D-{d_day}")
    elif d_day == 0:
        st.metric(label=f"🎯 {exam_name}", value="D-Day (오늘!)")
    else:
        st.metric(label=f"🎯 {exam_name}", value=f"D+{abs(d_day)} (종료)")

with col2:
    st.metric(label="⏱️ 하루 목표 공부 시간", value=f"{daily_hours} 시간")

st.divider()

# 3. 버튼 클릭 시 random 라이브러리를 활용한 시간 배분
quotes = [
    "오늘 걷지 않으면 내일은 뛰어야 한다!",
    "완벽한 계획보다 중요한 건 지금 당장 책상을 펴는 것!",
    "집중력은 시간의 길이가 아니라 밀도에서 나온다.",
    "정보 수행평가 만점과 시험 대박을 동시에 잡자!",
    "포기하지 마라. 어제의 나보다 1시간 더 성장하는 중이다."
]

if st.button("🎲 오늘의 과목별 공부 시간 배분하기", use_container_width=True, type="primary"):
    if not selected_subjects:
        st.warning("⚠️ 사이드바에서 공부할 과목을 최소 1개 이상 선택해 주세요!")
    else:
        # random.uniform으로 과목별 랜덤 가중치 부여 (1.0 ~ 3.0 사이)
        weights = [random.uniform(1.0, 3.0) for _ in selected_subjects]
        total_weight = sum(weights)
        
        # 총 공부 시간(분 단위 변환)을 가중치 비율대로 배분
        total_minutes = int(daily_hours * 60)
        allocated_minutes = [round((w / total_weight) * total_minutes) for w in weights]
        
        # 반올림 오차 보정 (가장 비중이 큰 과목에 차이 반영)
        diff = total_minutes - sum(allocated_minutes)
        max_idx = allocated_minutes.index(max(allocated_minutes))
        allocated_minutes[max_idx] += diff

        # 결과 출력
        st.success(f"💡 **오늘의 한마디:** {random.choice(quotes)}")
        st.subheader("📊 추천 과목별 시간표")
        
        # 차트용 데이터 생성
        chart_data = {}
        
        for subj, mins in zip(selected_subjects, allocated_minutes):
            hours = mins // 60
            rem_mins = mins % 60
            time_str = f"{hours}시간 {rem_mins}분" if hours > 0 else f"{rem_mins}분"
            
            # 진행률 바와 텍스트 표시
            ratio = mins / total_minutes
            st.write(f"**{subj}** : `{time_str}` ({ratio*100:.1f}%)")
            st.progress(ratio)
            
            chart_data[subj] = mins

        # 막대 그래프로 한눈에 비교
        st.subheader("📈 과목별 배분 비율 (분 단위)")
        st.bar_chart(chart_data)

        # 오늘의 보너스 미션 (random.choice 활용)
        bonus_subject = random.choice(selected_subjects)
        st.info(f"🔥 **오늘의 집중 공략 과목:** 오늘은 **{bonus_subject}** 과목의 오답 노트나 핵심 개념을 한 번 더 복습해 보세요!")
else:
    st.info("👆 위 버튼을 누르면 AI(Random 알고리즘)가 오늘의 과목별 공부 시간을 배분해 줍니다.")
