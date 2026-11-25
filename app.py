
import streamlit as st
import pandas as pd

# =====================================
# 1. 앱 기본 설정
# =====================================

st.set_page_config(
    page_title="한체대 실기 가이드",
    page_icon="🏃",
    layout="centered"
)

st.title("🏃 한체대 체대입시 실기 가이드")
st.write("나의 실기 기록을 측정하고 보강운동을 확인해 보세요!")

st.divider()


# =====================================
# 2. 실기 종목 및 만점 기준
# =====================================

EVENTS = [
    "10m 왕복달리기",
    "제자리멀리뛰기",
    "메디신볼 던지기"
]

MAX_RECORD = {
    "남성": {
        "10m 왕복달리기": 8.27,
        "제자리멀리뛰기": 284,
        "메디신볼 던지기": 12.4
    },
    "여성": {
        "10m 왕복달리기": 9.19,
        "제자리멀리뛰기": 231,
        "메디신볼 던지기": 10.0
    }
}

UNITS = {
    "10m 왕복달리기": "초",
    "제자리멀리뛰기": "cm",
    "메디신볼 던지기": "m"
}

# 아래 점수 구간은 앱 자체 참고용입니다.
# 공식 세부 배점표와 대조한 뒤 수정해야 합니다.
SCORE_LEVELS = {
    "남성": {
        "10m 왕복달리기": [
            (38, 8.27), (37, 8.45), (35, 8.63),
            (33, 8.81), (31, 8.99), (29, 9.18),
            (27, 9.36), (25, 9.54), (23, 9.72),
            (21, 9.90), (19, 99)
        ],
        "제자리멀리뛰기": [
            (38, 284), (37, 276), (35, 269),
            (33, 261), (31, 253), (29, 246),
            (27, 238), (25, 230), (23, 223),
            (21, 215), (19, 0)
        ],
        "메디신볼 던지기": [
            (38, 12.4), (37, 12.0), (35, 11.6),
            (33, 11.2), (31, 10.8), (29, 10.4),
            (27, 10.0), (25, 9.6), (23, 9.2),
            (21, 8.8), (19, 0)
        ]
    },
    "여성": {
        "10m 왕복달리기": [
            (38, 9.19), (37, 9.44), (35, 9.70),
            (33, 9.95), (31, 10.21), (29, 10.46),
            (27, 10.72), (25, 10.97), (23, 11.23),
            (21, 11.48), (19, 99)
        ],
        "제자리멀리뛰기": [
            (38, 231), (37, 222), (35, 212),
            (33, 203), (31, 193), (29, 184),
            (27, 174), (25, 165), (23, 155),
            (21, 146), (19, 0)
        ],
        "메디신볼 던지기": [
            (38, 10.0), (37, 9.7), (35, 9.4),
            (33, 9.1), (31, 8.7), (29, 8.4),
            (27, 8.1), (25, 7.8), (23, 7.5),
            (21, 7.1), (19, 0)
        ]
    }
}


# =====================================
# 3. 보강운동 목록
# =====================================

EXERCISES = {
    "10m 왕복달리기": [
        ["사이드 스텝", "좌우 8회", "2세트", "주 2회"],
        ["방향 전환 연습", "4회", "2세트", "주 1~2회"],
        ["가벼운 가속 달리기", "3회", "2세트", "주 1~2회"]
    ],

    "제자리멀리뛰기": [
        ["스쿼트", "8~10회", "2세트", "주 2회"],
        ["글루트 브릿지", "10회", "2세트", "주 2회"],
        ["가벼운 제자리 점프", "5회", "2세트", "주 1회"]
    ],

    "메디신볼 던지기": [
        ["무릎 대고 푸시업", "6~8회", "2세트", "주 2회"],
        ["밴드 로우", "10회", "2세트", "주 2회"],
        ["가벼운 공 던지기", "5회", "2세트", "주 1회"]
    ]
}


# =====================================
# 4. 점수 계산 함수
# =====================================

def calculate_score(event, record, gender):

    standards = SCORE_LEVELS[gender][event]

    if event == "10m 왕복달리기":

        for score, limit in standards:
            if record <= limit:
                return score

    else:

        for score, limit in standards:
            if record >= limit:
                return score

    return 19


# =====================================
# 5. 성별 선택
# =====================================

st.header("1. 성별 선택")

gender = st.radio(
    "성별을 선택하세요.",
    ["남성", "여성"],
    horizontal=True
)


# =====================================
# 6. 종목 선택
# =====================================

st.header("2. 실기 종목 선택")

selected_events = st.multiselect(
    "측정하고 싶은 종목을 선택하세요.",
    EVENTS,
    default=EVENTS
)


# =====================================
# 7. 만점 기준 및 기록 입력
# =====================================

st.header("3. 나의 실기 기록 입력")

records = {}

if selected_events:

    with st.form("record_form"):

        for event in selected_events:

            st.subheader(event)

            max_value = MAX_RECORD[gender][event]

            if event == "10m 왕복달리기":
                max_text = f"{max_value:.2f}초 이하"

                records[event] = st.number_input(
                    "나의 기록 (초)",
                    min_value=0.0,
                    max_value=30.0,
                    value=10.0,
                    step=0.01,
                    format="%.2f",
                    key=f"time_{gender}"
                )

            elif event == "제자리멀리뛰기":
                max_text = f"{max_value:.0f}cm 이상"

                records[event] = st.number_input(
                    "나의 기록 (cm)",
                    min_value=0,
                    max_value=500,
                    value=200,
                    step=1,
                    key=f"jump_{gender}"
                )

            else:
                max_text = f"{max_value:.1f}m 이상"

                records[event] = st.number_input(
                    "나의 기록 (m)",
                    min_value=0.0,
                    max_value=30.0,
                    value=8.0,
                    step=0.1,
                    format="%.1f",
                    key=f"ball_{gender}"
                )

            st.success(f"🏆 만점 기록: {max_text}")
            st.divider()

        submitted = st.form_submit_button(
            "실기 점수 계산하기",
            use_container_width=True
        )

else:
    st.info("실기 종목을 하나 이상 선택해 주세요.")
    submitted = False


# =====================================
# 8. 결과 계산
# =====================================

if submitted:

    results = []

    for event in selected_events:

        record = records[event]

        score = calculate_score(
            event,
            record,
            gender
        )

        results.append({
            "종목": event,
            "내 기록": f"{record} {UNITS[event]}",
            "만점 기준": MAX_RECORD[gender][event],
            "점수": score
        })

    st.session_state["results"] = results


# =====================================
# 9. 결과 화면
# =====================================

if "results" in st.session_state:

    results = st.session_state["results"]

    st.divider()
    st.header("4. 나의 실기 측정 결과")

    result_df = pd.DataFrame(results)

    st.dataframe(
        result_df,
        use_container_width=True,
        hide_index=True
    )

    total_score = sum(
        item["점수"] for item in results
    )

    max_score = len(results) * 38

    average_score = total_score / len(results)

    col1, col2 = st.columns(2)

    col1.metric(
        "획득 점수",
        f"{total_score} / {max_score}"
    )

    col2.metric(
        "종목 평균 점수",
        f"{average_score:.1f}점"
    )

    st.caption(
        "점수는 선택한 종목의 앱 내 참고 점수이며, "
        "실제 대학 환산점수나 합격 가능성을 의미하지 않습니다."
    )


# =====================================
# 10. 점수 그래프
# =====================================

    st.subheader("📊 종목별 점수")

    chart_data = pd.DataFrame({
        "종목": [item["종목"] for item in results],
        "점수": [item["점수"] for item in results]
    })

    st.bar_chart(
        chart_data.set_index("종목")
    )


# =====================================
# 11. 부족한 종목 분석
# =====================================

    st.divider()
    st.header("5. 보강운동 추천")

    weak_events = [
        item["종목"]
        for item in results
        if item["점수"] <= 29
    ]

    if weak_events:

        st.warning(
            "보강운동을 참고하면 좋은 종목입니다."
        )

        exercise_rows = []

        for event in weak_events:

            for exercise in EXERCISES[event]:

                exercise_rows.append({
                    "종목": event,
                    "보강운동": exercise[0],
                    "횟수": exercise[1],
                    "세트": exercise[2],
                    "주기": exercise[3]
                })

        exercise_df = pd.DataFrame(exercise_rows)

        st.dataframe(
            exercise_df,
            use_container_width=True,
            hide_index=True
        )

    else:

        st.success(
            "현재 입력한 기록에서는 보강운동 우선 종목이 없습니다."
        )


# =====================================
# 12. 운동 안전 안내
# =====================================

    st.divider()

    st.header("⚠️ 운동 시 주의사항")

    st.write("""
    - 운동 전 준비운동을 충분히 해주세요.
    - 본인의 체력에 맞는 강도로 운동하세요.
    - 운동 사이에 충분한 휴식을 취하세요.
    - 통증이나 어지러움이 생기면 운동을 중단하세요.
    - 보강운동은 지도자와 상의해 조절하세요.
    """)

    st.caption(
        "본 앱은 체대입시 실기 기록 관리와 운동 참고를 위한 학습용 프로그램입니다."
    )
