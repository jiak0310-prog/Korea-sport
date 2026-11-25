
import streamlit as st
import pandas as pd

# ==========================================
# 한국체육대학교 실기 가이드 앱
# 2027학년도 정시 일반 실기 기준
# ==========================================

st.set_page_config(
    page_title="한체대 실기 가이드",
    page_icon="🏃",
    layout="centered"
)

# ------------------------------------------
# 1. 공식 점수 기준 데이터
# ------------------------------------------

SCORES = [38, 37, 35, 33, 31, 29, 27, 25, 23, 21, 19]

# 시간 종목: 제한 시간 이하일수록 높은 점수
# 거리 종목: 최소 기록 이상일수록 높은 점수

STANDARD = {
    "남성": {
        "10m 왕복달리기": [
            8.27, 8.45, 8.63, 8.81, 8.99,
            9.18, 9.36, 9.54, 9.72, 9.90
        ],
        "제자리멀리뛰기": [
            284, 276, 269, 261, 253,
            246, 238, 230, 223, 215
        ],
        "메디신볼 던지기": [
            12.4, 12.0, 11.6, 11.2, 10.8,
            10.4, 10.0, 9.6, 9.2, 8.8
        ]
    },

    "여성": {
        "10m 왕복달리기": [
            9.19, 9.44, 9.70, 9.95, 10.21,
            10.46, 10.72, 10.97, 11.23, 11.48
        ],
        "제자리멀리뛰기": [
            231, 222, 212, 203, 193,
            184, 174, 165, 155, 146
        ],
        "메디신볼 던지기": [
            10.0, 9.7, 9.4, 9.1, 8.7,
            8.4, 8.1, 7.8, 7.5, 7.1
        ]
    }
}

EVENTS = list(STANDARD["남성"].keys())


# ------------------------------------------
# 2. 보강운동 데이터
# ------------------------------------------

EXERCISES = {
    "10m 왕복달리기": [
        ["사이드 스텝", "10~15회", "2세트", "주 2회"],
        ["방향전환 발놀림", "5회", "2세트", "주 2회"],
        ["짧은 거리 가속 연습", "10m 3회", "2세트", "주 1~2회"]
    ],

    "제자리멀리뛰기": [
        ["스쿼트", "10회", "2세트", "주 2회"],
        ["글루트 브릿지", "12회", "2세트", "주 2회"],
        ["가벼운 점프 연습", "5회", "2세트", "주 1회"]
    ],

    "메디신볼 던지기": [
        ["무릎 대고 푸시업", "8회", "2세트", "주 2회"],
        ["밴드 로우", "12회", "2세트", "주 2회"],
        ["가벼운 공 던지기 연습", "5회", "2세트", "주 1~2회"]
    ]
}


# ------------------------------------------
# 3. 점수 계산 함수
# ------------------------------------------

def calculate_score(event, record, gender):

    standards = STANDARD[gender][event]

    if event == "10m 왕복달리기":

        record = round(record, 2)

        for i, standard in enumerate(standards):

            if record <= standard:
                return SCORES[i]

        return 19

    elif event == "제자리멀리뛰기":

        record = int(record)

        for i, standard in enumerate(standards):

            if record >= standard:
                return SCORES[i]

        return 19

    elif event == "메디신볼 던지기":

        record = round(record, 1)

        for i, standard in enumerate(standards):

            if record >= standard:
                return SCORES[i]

        return 19


# ------------------------------------------
# 4. 보강운동 분석 함수
# ------------------------------------------

def analyze_weakness(results):

    weak_events = []

    for event, score in results.items():

        # 29점 이하일 때 보강운동 권장
        if score <= 29:
            weak_events.append(event)

    return weak_events


# ------------------------------------------
# 5. 결과 표 출력 함수
# ------------------------------------------

def show_exercises(weak_events):

    if not weak_events:

        st.success("현재 입력 기록에서는 보강운동이 권장되는 종목이 없습니다.")
        return

    st.subheader("💪 맞춤형 보강운동")

    for event in weak_events:

        st.markdown(f"### {event}")

        df = pd.DataFrame(
            EXERCISES[event],
            columns=["보강운동", "횟수", "세트", "주기"]
        )

        st.dataframe(
            df,
            hide_index=True,
            use_container_width=True
        )


# ==========================================
# 6. 앱 화면
# ==========================================

st.title("🏃 한체대 실기 가이드")
st.caption("한국체육대학교 2027학년도 정시 일반 실기 기준")

st.divider()

st.markdown("### ① 성별 선택")

gender = st.radio(
    "성별을 선택하세요.",
    ["남성", "여성"],
    horizontal=True
)

st.divider()

st.markdown("### ② 실기 종목 선택")

st.write("측정하고 싶은 종목만 선택하세요.")

selected_events = st.multiselect(
    "실기 종목",
    EVENTS,
    default=EVENTS,
    format_func=lambda x: x
)

st.divider()

st.markdown("### ③ 실기 기록 입력")

records = {}

if selected_events:

    with st.form("record_form"):

        for event in selected_events:

            st.markdown(f"**{event}**")

            if event == "10m 왕복달리기":

                records[event] = st.number_input(
                    "기록 (초)",
                    min_value=0.01,
                    max_value=30.0,
                    value=10.0,
                    step=0.01,
                    key="time"
                )

            elif event == "제자리멀리뛰기":

                records[event] = st.number_input(
                    "기록 (cm)",
                    min_value=1,
                    max_value=500,
                    value=200,
                    step=1,
                    key="jump"
                )

            elif event == "메디신볼 던지기":

                records[event] = st.number_input(
                    "기록 (m)",
                    min_value=0.1,
                    max_value=30.0,
                    value=8.0,
                    step=0.1,
                    key="ball"
                )

        st.divider()

        submitted = st.form_submit_button(
            "실기 점수 분석하기",
            use_container_width=True
        )

else:

    submitted = False
    st.info("최소 한 개 이상의 종목을 선택해주세요.")


# ==========================================
# 7. 결과 화면
# ==========================================

if submitted:

    results = {}

    for event, record in records.items():

        results[event] = calculate_score(
            event, record, gender
        )

    st.divider()

    st.header("📊 실기 측정 결과")

    result_data = []

    for event, score in results.items():

        record = records[event]

        if event == "10m 왕복달리기":
            record_text = f"{record:.2f}초"

        elif event == "제자리멀리뛰기":
            record_text = f"{record:.0f}cm"

        else:
            record_text = f"{record:.1f}m"

        result_data.append({
            "실기 종목": event,
            "입력 기록": record_text,
            "취득 점수": f"{score}점",
            "만점": "38점"
        })

    result_df = pd.DataFrame(result_data)

    st.dataframe(
        result_df,
        hide_index=True,
        use_container_width=True
    )

    # --------------------------------------
    # 8. 총점 계산
    # --------------------------------------

    total = sum(results.values())

    st.subheader("🏆 종합 점수")

    if len(results) == 3:

        converted = total / 114 * 100

        st.metric(
            "100점 환산 점수",
            f"{converted:.2f}점"
        )

        st.progress(converted / 100)

        st.write(f"공식 실기 취득 점수: {total} / 114점")

    else:

        average = total / (38 * len(results)) * 100

        st.metric(
            "선택 종목 평균 환산 점수",
            f"{average:.2f}점"
        )

        st.info(
            "일부 종목만 선택했으므로 전체 실기 총점이 아닌 "
            "선택 종목 평균 참고 점수입니다."
        )

    # --------------------------------------
    # 9. 종목별 그래프
    # --------------------------------------

    st.subheader("📈 종목별 점수 그래프")

    chart_df = pd.DataFrame({
        "점수": results
    })

    st.bar_chart(chart_df)

    # --------------------------------------
    # 10. 보강운동 분석
    # --------------------------------------

    st.divider()

    st.header("💪 보강운동 분석")

    weak_events = analyze_weakness(results)

    if weak_events:

        st.warning("보강운동이 권장되는 종목이 있습니다.")

        for event in weak_events:
            st.write(f"🔸 {event}")

    else:

        st.success("현재 입력 기록에서 보강운동 권장 종목이 없습니다.")

    show_exercises(weak_events)

    st.divider()

    st.caption(
        "보강운동 권장 기준 29점 이하는 프로그램의 훈련용 기준이며 "
        "대학의 공식 합격 기준이 아닙니다. "
        "운동 강도는 개인 체력에 맞게 조절하세요."
    )

st.divider()

st.caption(
    "한국체육대학교 2027학년도 정시 일반 실기 참고 프로그램 | "
    "실제 전형 적용 전 최신 모집요강 확인 필수"
)
