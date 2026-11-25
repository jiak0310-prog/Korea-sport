
# ==========================================
# 한국체육대학교 실기 가이드 프로그램
# 2027학년도 일반 실기고사 기준
# ==========================================

# 1. 공식 실기 기준표
# 시간: 낮을수록 높은 점수
# 거리: 높을수록 높은 점수

score_table = {
    "남성": {
        "10m 왕복달리기": [
            (8.27, 38), (8.45, 37), (8.63, 35),
            (8.81, 33), (8.99, 31), (9.18, 29),
            (9.36, 27), (9.54, 25), (9.72, 23),
            (9.90, 21), (float("inf"), 19)
        ],
        "제자리멀리뛰기": [
            (284, 38), (276, 37), (269, 35),
            (261, 33), (253, 31), (246, 29),
            (238, 27), (230, 25), (223, 23),
            (215, 21), (float("-inf"), 19)
        ],
        "메디신볼 던지기": [
            (12.4, 38), (12.0, 37), (11.6, 35),
            (11.2, 33), (10.8, 31), (10.4, 29),
            (10.0, 27), (9.6, 25), (9.2, 23),
            (8.8, 21), (float("-inf"), 19)
        ]
    },

    "여성": {
        "10m 왕복달리기": [
            (9.19, 38), (9.44, 37), (9.70, 35),
            (9.95, 33), (10.21, 31), (10.46, 29),
            (10.72, 27), (10.97, 25), (11.23, 23),
            (11.48, 21), (float("inf"), 19)
        ],
        "제자리멀리뛰기": [
            (231, 38), (222, 37), (212, 35),
            (203, 33), (193, 31), (184, 29),
            (174, 27), (165, 25), (155, 23),
            (146, 21), (float("-inf"), 19)
        ],
        "메디신볼 던지기": [
            (10.0, 38), (9.7, 37), (9.4, 35),
            (9.1, 33), (8.7, 31), (8.4, 29),
            (8.1, 27), (7.8, 25), (7.5, 23),
            (7.1, 21), (float("-inf"), 19)
        ]
    }
}


# 2. 보강운동 리스트

exercise_list = {
    "10m 왕복달리기": [
        ["사이드 스텝", "20회", "3세트", "주 2회"],
        ["방향전환 연습", "5회", "3세트", "주 2회"],
        ["짧은 거리 가속 달리기", "10m 4회", "2세트", "주 2회"]
    ],

    "제자리멀리뛰기": [
        ["스쿼트", "10회", "2세트", "주 2회"],
        ["글루트 브릿지", "12회", "2세트", "주 2회"],
        ["제자리 점프", "5회", "2세트", "주 1~2회"]
    ],

    "메디신볼 던지기": [
        ["무릎 대고 푸시업", "8회", "2세트", "주 2회"],
        ["밴드 로우", "12회", "2세트", "주 2회"],
        ["가벼운 메디신볼 연습", "5회", "2세트", "주 1~2회"]
    ]
}


# 3. 성별 선택

def select_gender():

    print("\n===== 성별 선택 =====")
    print("1. 남성")
    print("2. 여성")

    while True:

        choice = input("선택하세요: ")

        if choice == "1":
            return "남성"

        elif choice == "2":
            return "여성"

        else:
            print("다시 입력해주세요.")


# 4. 실기 종목 선택

def select_events():

    events = list(score_table["남성"].keys())
    selected = []

    print("\n===== 한체대 공식 실기 종목 =====")

    for i, event in enumerate(events, 1):
        print(f"{i}. {event}")

    print("0. 선택 완료")

    while True:

        choice = input("종목 번호: ")

        if choice == "0":
            break

        elif choice.isdigit() and 1 <= int(choice) <= 3:

            event = events[int(choice) - 1]

            if event not in selected:
                selected.append(event)
                print(event, "선택 완료!")

            else:
                print("이미 선택한 종목입니다.")

        else:
            print("올바른 번호를 입력하세요.")

    return selected


# 5. 기록 입력

def input_records(selected):

    records = {}

    for event in selected:

        while True:

            try:

                record = float(
                    input(f"{event} 기록 입력: ")
                )

                if record <= 0:
                    print("0보다 큰 숫자를 입력하세요.")
                    continue

                records[event] = record
                break

            except ValueError:
                print("숫자로 입력해주세요.")

    return records


# 6. 공식 점수 계산

def calculate_score(event, record, gender):

    standards = score_table[gender][event]

    # 시간 종목
    if event == "10m 왕복달리기":

        for standard, score in standards:

            if record <= standard:
                return score

    # 거리 종목
    else:

        for standard, score in standards:

            if record >= standard:
                return score

    return 19


# 7. 종목별 점수 계산

def analyze_scores(records, gender):

    results = {}

    for event, record in records.items():

        results[event] = calculate_score(
            event, record, gender
        )

    return results


# 8. 결과 출력

def print_results(records, results):

    print("\n========== 실기 측정 결과 ==========")

    total = 0

    for event, score in results.items():

        print(f"\n종목: {event}")
        print(f"기록: {records[event]}")
        print(f"점수: {score}점 / 38점")

        total += score

    print("\n================================")

    print(f"총 취득 점수: {total}점")

    if len(results) == 3:

        converted = total / 114 * 100

        print(f"100점 환산 점수: {converted:.2f}점")

    else:

        print("전체 3종목을 입력하지 않았습니다.")
        print("선택 종목 점수만 표시합니다.")


# 9. 보강운동 필요 여부 분석

def analyze_weakness(results):

    weak_events = []

    print("\n========== 보강운동 분석 ==========")

    for event, score in results.items():

        if score <= 29:

            weak_events.append(event)

            print(event, ": 보강운동 권장")

        else:

            print(event, ": 현재 기록 유지 및 기술 연습 권장")

    return weak_events


# 10. 보강운동 표 출력

def print_exercises(weak_events):

    if len(weak_events) == 0:

        print("\n현재 점수 기준 보강운동 권장 종목이 없습니다.")
        return

    print("\n========== 맞춤형 보강운동 ==========")

    for event in weak_events:

        print(f"\n[{event}]")

        print("-" * 70)

        print(
            f"{'운동명':<25}"
            f"{'횟수':<12}"
            f"{'세트':<12}"
            f"{'주기':<12}"
        )

        print("-" * 70)

        for exercise in exercise_list[event]:

            print(
                f"{exercise[0]:<25}"
                f"{exercise[1]:<12}"
                f"{exercise[2]:<12}"
                f"{exercise[3]:<12}"
            )

        print("-" * 70)


# 11. 메인 함수

def main():

    gender = select_gender()

    selected = select_events()

    if len(selected) == 0:

        print("선택한 종목이 없습니다.")
        return

    records = input_records(selected)

    results = analyze_scores(records, gender)

    print_results(records, results)

    weak_events = analyze_weakness(results)

    print_exercises(weak_events)

    print("\n===== 프로그램 종료 =====")


# 프로그램 실행

if __name__ == "__main__":
    main()
