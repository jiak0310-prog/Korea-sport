
import streamlit as st
import pandas as pd

# =====================================
# 1. 기본 설정
# =====================================

st.set_page_config(
    page_title="한체대 실기 가이드",
    page_icon="🏃",
    layout="centered"
)

st.title("🏃 한체대 체대입시 실기 가이드")
st.caption("2027학년도 한국체육대학교 정시 일반 실기고사 기준")
st.divider()


# =====================================
# 2. 공식 실기 점수 기준
# =====================================

# 형식: (점수, 최소 기록, 최대 기록)
# 최대 기록이 None이면 해당 기록 이상을 의미

STANDARD = {
    "남성": {
        "10m 왕복달리기": [
            (38, 0, 8.27),
            (37, 8.28, 8.45),
            (35, 8.46, 8.63),
            (33, 8.64, 8.81),
            (31, 8.82, 8.99),
            (29, 9.00, 9.18),
            (27, 9.19, 9.36),
            (25, 9.37, 9.54),
            (23, 9.55, 9.72),
            (21, 9.73, 9.90),
            (19, 9.91, None)
        ],

        "제자리멀리뛰기": [
            (38, 284, None),
            (37, 276, 283),
            (35, 269, 275),
            (33, 261, 268),
            (31, 253, 260),
            (29, 246, 252),
            (27, 238, 245),
            (25, 230, 237),
            (23, 223, 229),
            (21, 215, 222),
            (19, 0, 214)
        ],

        "메디신볼 던지기": [
            (38, 12.4, None),
            (37, 12.0, 12.3),
            (35, 11.6, 11.9),
            (33, 11.2, 11.5),
            (31, 10.8, 11.1),
            (29, 10.4, 10.7),
            (27, 10.0, 10.3),
            (25, 9.6, 9.9),
            (23, 9.2, 9.5),
            (21, 8.8, 9.1),
            (19, 0, 8.7)
        ]
    },

    "여성": {
        "10m 왕복달리기": [
            (38, 0, 9.19),
            (37, 9.20, 9.44),
            (35, 9.45, 9.70),
            (33, 9.71, 9.95),
            (31, 9.96, 10.21),
            (29, 10.22, 10.46),
            (27, 10.47, 10.72),
            (25, 10.73, 10.97),
            (23, 10.98, 11.23),
            (21, 11.24, 11.48),
            (19, 11.49, None)
        ],

        "제자리멀리뛰기": [
            (38, 231, None),
            (37, 222, 230),
            (35, 212, 221),
            (33, 203, 211),
            (31, 193, 202),
            (29, 184, 192),
            (27, 174, 183),
            (25, 165, 173),
            (23, 155, 164),
            (21, 146, 154),
            (19, 0, 145)
        ],

        "메디신볼 던지기": [
            (38, 10.0, None),
            (37, 9.7, 9.9),
            (35, 9.4, 9.6),
            (33, 9.1, 9.3),
            (31, 8.7, 9.0),
            (29, 8.4, 8.6),
            (27, 8.1, 8.3),
            (25, 7.8, 8.0),
            (23, 7.5, 7.7),
            (21, 7.1, 7.4),
            (19, 0, 7.0)
        ]
    }
}


# =====================================
# 3. 만점 기준
# =====================================

MAX_RECORD = {
    "남성": {
        "10m 왕복달리기": "8.27초 이하",
        "제자리멀리뛰기": "284cm 이상",
        "메디신볼 던지기": "12.4m 이상"
    },

    "여성": {
        "10m 왕복달리기": "9.19초 이하",
        "제자리멀리뛰기": "231cm 이상",
        "메디신볼 던지기": "10.0m 이상"
    }
}


# =====================================
# 4. 종목별 단위
# =====================================

UNITS = {
    "10m 왕복달리기": "초",
    "제자리멀리뛰기": "cm",
    "메디신볼 던지기": "m"
}


# =====================================
# 5. 점수 계산 함수
# =====================================

def calculate_score(event, record, gender):

    score_table = STANDARD[gender][event]

    for score, minimum, maximum in score_table:

        if maximum is None:
            if record >= minimum:
                return score

        elif minimum <= record <= maximum:
            return score

    return 19


# =====================================
# 6. 점수 기준표 만들기
# =====================================

def make_standard_table(event, gender):

    rows = []

    for score, minimum, maximum in STANDARD[gender][event]:

        if event == "10m 왕복달리기":
            if minimum == 0:
                record_range = f"{maximum:.2f} 이하"
            elif maximum is None:
                record_range = f"{minimum:.2f} 이상"
            else:
                record_range = f"{minimum:.2f} ~ {maximum:.2f}"

        elif event == "제자리멀리뛰기":
            if maximum is None:
                record_range = f"{minimum} 이상"
            elif minimum == 0:
                record_range = f"{maximum} 이하"
            else:
                record_range = f"{minimum} ~ {maximum}"

        else:
            if maximum is None:
                record_range = f"{minimum:.1f} 이상"
            elif minimum == 0:
                record_range = f"{maximum:.1f} 미만"
            else:
                record_range = f"{minimum:.1f} ~ {maximum:.1f}"

        rows.append({
            "점수": score,
            "기록 기준": record_range
        })

    return pd.DataFrame(rows)


# =====================================
# 7. 보강운동 데이터
# =====================================

EXERCISES = {

    "10m 왕복달리기": [
        {
            "운동": "사이드 스텝",
            "횟수": "좌우 8회",
            "세트": "2세트",
            "주기": "주 2회",
            "목적": "좌우 이동 능력"
        },
        {
            "운동": "방향 전환 연습",
            "횟수": "짧은 구간 4회",
            "세트": "2세트",
            "주기": "주 1~2회",
            "목적": "방향 전환 동작 익히기"
        },
        {
            "운동": "가벼운 가속 달리기",
            "횟수": "짧은 거리 3회",
            "세트": "2세트",
            "주기": "주 1~2회",
            "목적": "출발과 가속 능력"
        }
    ],

    "제자리멀리뛰기": [
        {
            "운동": "스쿼트",
            "횟수": "8~10회",
            "세트": "2세트",
            "주기": "주 2회",
            "목적": "하체 근력"
        },
        {
            "운동": "글루트 브릿지",
            "횟수": "10회",
            "세트": "2세트",
            "주기": "주 2회",
            "목적": "엉덩이 근육 강화"
        },
        {
            "운동": "제자리 가벼운 점프",
            "횟수": "5회",
            "세트": "2세트",
            "주기": "주 1회",
            "목적": "착지와 점프 동작 익히기"
        }
    ],

    "메디신볼 던지기": [
        {
            "운동": "무릎 대고 푸시업",
            "횟수": "6~8회",
            "세트": "2세트",
            "주기": "주 2회",
            "목적": "상체 근력"
        },
        {
            "운동": "밴드 로우",
            "횟수": "10회",
            "세트": "2세트",
            "주기": "주 2회",
            "목적": "등과 어깨 주변 근육"
        },
        {
            "운동": "가벼운 공 던지기",
            "횟수": "5회",
            "세트": "2세트",
            "주기": "주 1회",
            "목적": "던지는 동작 연습"
        }
    ]
}


# =====================================
# 8. 성별 선택
# =====================================

st.subheader("1️⃣ 성별 선택")

gender = st.radio(
    "성별을 선택하세요.",
    ["남성", "여성"],
    horizontal=True
)


# =====================================
# 9. 실기 종목 선택
# =====================================

st.subheader("2️⃣ 실기 종목 선택")

events = [
    "10m 왕복달리기",
    "제자리멀리뛰기",
    "메디신볼 던지기"
]

selected_events = st.multiselect(
    "측정할 종목을 선택하세요. 여러 종목을 선택할 수 있습니다.",
    events,
    default=events
)


# =====================================
# 10. 만점 기준 안내
# =====================================

st.subheader("3️⃣ 종목별 만점 기준")

max_rows = []

for event in selected_events:
    max_rows.append({
        "실기 종목": event,
        "만점 기록": MAX_RECORD[gender][event]
    })

if max_rows:
    st.dataframe(
        pd.DataFrame(max_rows),
        use_container_width=True,
        hide_index=True
    )


# =====================================
# 11. 기록 입력
# =====================================

st.subheader("4️⃣ 나의 실기 기록 입력")

records = {}

if selected_events:

    with st.form("record_form"):

        for event in selected_events:

            st.markdown(f"**{event}**")

            standard_df = make_standard_table(event, gender)

            st.dataframe(
                standard_df,
                use_container_width=True,
                hide_index=True
            )

            if event == "10m 왕복달리기":
                records[event] = st.number_input(
                    "기록 (초)",
                    min_value=0.0,
                    max_value=30.0,
                    value=10.0,
                    step=0.01,
                    format="%.2f",
                    key=f"time_{gender}"
                )

            elif event == "제자리멀리뛰기":
                records[event] = st.number_input(
                    "기록 (cm)",
                    min_value=0,
                    max_value=500,
                    value=200,
                    step=1,
                    key=f"jump_{gender}"
                )

            elif event == "메디신볼 던지기":
                records[event] = st.number_input(
                    "기록 (m)",
                    min_value=0.0,
                    max_value=30.0,
                    value=8.0,
                    step=0.1,
                    format="%.1f",
                    key=f"ball_{gender}"
                )

            st.divider()

        submitted = st.form_submit_button(
            "실기 점수 계산하기",
            use_container_width=True
        )

else:
    st.info("먼저 실기 종목을 하나 이상 선택하세요.")
    submitted = False


# =====================================
# 12. 점수 계산 및 결과 출력
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
            "획득 점수": score
        })

    st.session_state["results"] = results


# =====================================
# 13. 결과 분석
# =====================================

if "results" in st.session_state:

    results = st.session_state["results"]

    st.divider()
    st.subheader("🏆 실기 측정 결과")

    result_df = pd.DataFrame(results)

    st.dataframe(
        result_df,
        use_container_width=True,
        hide_index=True
    )

    total_score = sum(
        item["획득 점수"] for item in results
    )

    max_score = 38 * len(results)

    average_score = total_score / len(results)

    # 앱 자체 참고용 환산 점수
    converted_score = (
        (average_score - 19) / 19
    ) * 100

    converted_score = max(
        0,
        min(100, converted_score)
    )

    col1, col2 = st.columns(2)

    with col1:
        st.metric(
            "획득 점수 합계",
            f"{total_score} / {max_score}점"
        )

    with col2:
        st.metric(
            "앱 자체 참고 환산",
            f"{converted_score:.1f}점 / 100점"
        )

    st.caption(
        "100점 환산은 앱에서 비교하기 위한 참고용 계산입니다. "
        "한국체육대학교의 실제 입시 총점이나 합격 가능성을 뜻하지 않습니다."
    )

    # =================================
    # 14. 종목별 점수 그래프
    # =================================

    st.subheader("📊 종목별 점수 그래프")

    chart_df = pd.DataFrame({
        "종목": [item["종목"] for item in results],
        "점수": [item["획득 점수"] for item in results]
    })

    st.bar_chart(
        chart_df.set_index("종목")
    )

    # =================================
    # 15. 보강운동 분석
    # =================================

    st.divider()
    st.subheader("💪 보강운동 가이드")

    weak_events = []

    for item in results:

        if item["획득 점수"] <= 29:
            weak_events.append(item["종목"])

    if weak_events:

        st.warning(
            "보강운동을 참고하면 좋은 종목이 있습니다."
        )

        exercise_rows = []

        for event in weak_events:

            for exercise in EXERCISES[event]:

                exercise_rows.append({
                    "부족한 종목": event,
                    "보강운동": exercise["운동"],
                    "횟수": exercise["횟수"],
                    "세트": exercise["세트"],
                    "주기": exercise["주기"],
                    "운동 목적": exercise["목적"]
                })

        exercise_df = pd.DataFrame(exercise_rows)

        st.dataframe(
            exercise_df,
            use_container_width=True,
            hide_index=True
        )

    else:

        st.success(
            "현재 입력한 기록에서는 29점 이하인 종목이 없습니다."
        )

    # =================================
    # 16. 운동 안전 안내
    # =================================

    st.divider()

    st.subheader("⚠️ 운동할 때 주의할 점")

    st.write("""
    - 운동 전에는 가벼운 준비운동을 해주세요.
    - 처음부터 무리한 횟수나 강도로 운동하지 마세요.
    - 점프와 달리기는 충분한 휴식을 두고 진행하세요.
    - 통증이나 어지러움이 생기면 운동을 중단하세요.
    - 보강운동은 지도자와 상의해 본인에게 맞게 조절하세요.
    """)

    st.caption(
        "이 프로그램은 실기 기록을 바탕으로 점수와 보강운동을 "
        "참고할 수 있도록 만든 학습용 앱입니다."
    )

