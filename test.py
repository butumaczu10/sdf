# survival_quiz.py
# --------------------------------------------
# "재난에서 살아남기" - 스트림릿 앱
# 6가지 상황에 대한 선택 → 생존자 유형 결과 + 대처 팁
# MBTI 로직 기반이지만 MBTI라는 단어는 전혀 노출 안 함

import streamlit as st

st.set_page_config(page_title="재난에서 살아남기", page_icon="🌍", layout="centered")

st.title("🌍 재난 상황에서 나는 어떤 생존자일까?")

st.markdown("6가지 재난 상황에서 선택지를 고르고, 당신의 생존 성향을 확인해 보세요!")
st.markdown("---")

# MBTI 점수 누적용
scores = {"E":0, "I":0, "S":0, "N":0, "T":0, "F":0, "J":0, "P":0}

# 질문/선택지 데이터
questions = [
    {
        "situation": "🔥 화재 발생",
        "question": "빌딩에서 화재가 발생했다! 가장 먼저 어떻게 할까?",
        "options": {
            "E": "사람들을 모아 함께 대피 경로를 찾는다",
            "I": "혼자 신속하게 가장 가까운 비상구로 이동한다",
            "S": "불과 연기를 확인하고 안전한 계단을 이용한다",
            "N": "창문이나 다른 비상 루트를 즉석에서 찾아본다"
        },
        "tip": "화재 시에는 절대 엘리베이터를 이용하지 말고, 계단으로 이동하세요."
    },
    {
        "situation": "🌏 지진 발생",
        "question": "강한 지진이 발생했다! 당신의 행동은?",
        "options": {
            "S": "책상이나 탁자 아래에 들어가 머리를 보호한다",
            "N": "바로 건물 밖으로 뛰쳐나간다",
            "J": "비상용품을 챙기고 질서 있게 대피한다",
            "P": "상황을 보며 즉흥적으로 판단한다"
        },
        "tip": "지진 시에는 머리를 보호하고, 진동이 멈춘 후 안전하게 대피하세요."
    },
    {
        "situation": "🌋 화산 폭발",
        "question": "화산이 폭발했다! 당신은?",
        "options": {
            "T": "먼저 가장 합리적인 탈출 경로를 계산한다",
            "F": "가족/친구가 다 같이 대피할 수 있도록 돕는다",
            "J": "대피 계획에 따라 침착하게 움직인다",
            "P": "주변 상황을 보고 빠른 길을 즉석에서 찾는다"
        },
        "tip": "화산재는 호흡기를 막을 수 있으니 마스크나 천으로 코와 입을 막으세요."
    },
    {
        "situation": "⚔️ 전쟁 상황",
        "question": "전쟁이 발발했다! 당신의 대피 방법은?",
        "options": {
            "E": "이웃과 함께 대피하며 정보를 공유한다",
            "I": "최소한의 노출로 조용히 움직인다",
            "T": "지도와 경로를 분석해 가장 안전한 길을 찾는다",
            "F": "다른 사람들을 챙기며 함께 피난한다"
        },
        "tip": "전쟁 상황에서는 눈에 띄지 않게 이동하고, 라디오 등으로 정보를 확인하세요."
    },
    {
        "situation": "🌊 폭우와 홍수",
        "question": "폭우로 도로가 잠겼다! 당신은?",
        "options": {
            "S": "높은 지대로 바로 이동한다",
            "N": "물살을 가로질러 다른 길을 시도한다",
            "J": "예상된 대피 경로를 따른다",
            "P": "상황에 맞춰 즉시 다른 길을 찾는다"
        },
        "tip": "홍수 시에는 절대 물살을 건너지 말고 높은 지대로 이동하세요."
    },
    {
        "situation": "❄️ 눈보라 속 조난",
        "question": "산에서 눈보라를 만나 고립됐다! 당신은?",
        "options": {
            "I": "한 곳에 머무르며 체력을 아낀다",
            "E": "움직이며 구조 신호를 찾는다",
            "T": "불을 피워 체온을 유지한다",
            "F": "동료들과 서로 의지하며 대기한다"
        },
        "tip": "조난 시에는 체력을 아끼고, 구조 신호를 보내며 체온을 유지하세요."
    },
]

answers = {}

# 질문 표시
for i, q in enumerate(questions):
    st.subheader(f"상황 {i+1}) {q['situation']}")
    choice = st.radio(q["question"], list(q["options"].values()), key=f"q{i}")
    if choice:
        # 선택에 해당하는 MBTI 알파벳을 찾아서 점수 +1
        for k, v in q["options"].items():
            if v == choice:
                scores[k] += 1
                answers[q['situation']] = (choice, q["tip"])

st.markdown("---")

# 결과 버튼
if st.button("내 생존자 유형 보기 🧭"):
    # MBTI 코드 계산
    mbti = ""
    mbti += "E" if scores["E"] >= scores["I"] else "I"
    mbti += "S" if scores["S"] >= scores["N"] else "N"
    mbti += "T" if scores["T"] >= scores["F"] else "F"
    mbti += "J" if scores["J"] >= scores["P"] else "P"

    # 생존자 유형 이름 (MBTI 단어는 안 씀)
    survivor_types = {
        "ISTJ": "신중한 분석가형 생존자",
        "ISFJ": "헌신적인 수호자형 생존자",
        "INFJ": "통찰력 있는 조언자형 생존자",
        "INTJ": "전략적인 설계자형 생존자",
        "ISTP": "실용적인 해결사형 생존자",
        "ISFP": "온화한 적응가형 생존자",
        "INFP": "이상적인 탐색자형 생존자",
        "INTP": "호기심 많은 사색가형 생존자",
        "ESTP": "대담한 행동가형 생존자",
        "ESFP": "활기찬 즉흥가형 생존자",
        "ENFP": "열정적인 탐험가형 생존자",
        "ENTP": "도전적인 전략가형 생존자",
        "ESTJ": "체계적인 지휘관형 생존자",
        "ESFJ": "사교적인 보호자형 생존자",
        "ENFJ": "따뜻한 지도자형 생존자",
        "ENTJ": "결단력 있는 통솔자형 생존자",
    }

    st.header(f"당신의 생존 성향: {survivor_types[mbti]}")

    st.write("### 🧩 당신의 특징")
    st.markdown(f"- 당신은 **{survivor_types[mbti]}** 성향을 가지고 있습니다.")
    st.markdown("- 이 유형은 위기 속에서 고유한 방식으로 생존 전략을 세웁니다.")

    st.write("### 📘 상황별 대처 팁")
    for sit, (ans, tip) in answers.items():
        st.markdown(f"**{sit}**  \n선택: {ans}  \n✅ 올바른 팁: {tip}")

    st.success("생존 지식은 언제나 실제 상황에 큰 도움이 됩니다. 기억해 두세요!")
