import streamlit as st

# 페이지 설정
st.set_page_config(page_title="MBTI 생존 테스트", layout="centered")
st.title("🌍 재난 생존 MBTI 테스트")
st.markdown("**당신의 선택으로 MBTI를 추정하고, 생존 시나리오에서의 역할을 분석해드립니다!**")

# 질문 리스트
questions = [
    {
        "question": "재난 상황 발생! 당신은?",
        "options": [("사람들을 모아 리더 역할을 한다", "E"), ("조용히 주변을 분석하고 계획을 짠다", "I")]
    },
    {
        "question": "구조될 가능성이 낮다면?",
        "options": [("일단 눈앞에 있는 물자를 챙긴다", "S"), ("상상력을 발휘해 탈출 루트를 구상한다", "N")]
    },
    {
        "question": "누군가 다쳤다면?",
        "options": [("일단 상황을 분석하고 행동한다", "T"), ("감정적으로 도와주며 안심시킨다", "F")]
    },
    {
        "question": "위기 상황에서 당신의 스타일은?",
        "options": [("플랜을 짜고 그에 따라 움직인다", "J"), ("상황 따라 유연하게 움직인다", "P")]
    },
    {
        "question": "다른 생존자와의 갈등 상황!",
        "options": [("감정 배제하고 전략적으로 결정", "T"), ("감정을 존중하며 중재", "F")]
    },
    {
        "question": "먹을 게 부족하다면?",
        "options": [("실질적인 분배 기준을 만든다", "S"), ("공동체 분위기를 고려해 분배한다", "N")]
    },
    {
        "question": "낯선 사람과 협동해야 한다면?",
        "options": [("먼저 말을 걸어본다", "E"), ("상대가 다가오기를 기다린다", "I")]
    },
    {
        "question": "위기 탈출 루트를 짠다면?",
        "options": [("지도, 경로, 물자 체크리스트로 구성", "J"), ("그때그때 떠오르는 아이디어로 대응", "P")]
    },
]

# 성향 점수 저장
scores = {
    "E": 0, "I": 0,
    "S": 0, "N": 0,
    "T": 0, "F": 0,
    "J": 0, "P": 0
}

# 사용자 응답 저장
responses = []

st.subheader("🧪 질문에 답해주세요:")

for i, q in enumerate(questions):
    answer = st.radio(f"{i+1}. {q['question']}", [opt[0] for opt in q['options']], key=i)
    # 선택된 옵션에 따라 점수 추가
    for opt in q['options']:
        if answer == opt[0]:
            scores[opt[1]] += 1
            break

if st.button("🔍 결과 확인하기"):
    # MBTI 계산
    mbti = ""
    mbti += "E" if scores["E"] >= scores["I"] else "I"
    mbti += "S" if scores["S"] >= scores["N"] else "N"
    mbti += "T" if scores["T"] >= scores["F"] else "F"
    mbti += "J" if scores["J"] >= scores["P"] else "P"

    # MBTI 역할 매핑 (예시)
    roles = {
        "INTJ": "🎯 전략가 - 생존 시나리오의 두뇌",
        "ENTP": "🔥 혁신가 - 창의적으로 탈출법을 설계",
        "ISFJ": "🛡️ 보호자 - 공동체의 안정을 책임",
        "ESFP": "🎉 생존가 - 분위기 메이커이자 즉흥적 해결사",
        "ISTP": "🧰 기술자 - 도구를 활용한 생존의 달인",
        "ENFJ": "🤝 리더 - 팀워크와 조율의 마스터",
        # ... 등 모든 MBTI 유형 커스터마이즈 가능
    }

    role = roles.get(mbti, "🧭 생존자 - 고유한 방식으로 생존을 추구하는 당신!")

    st.subheader("🧬 당신의 생존 MBTI는:")
    st.markdown(f"## **{mbti}**")
    st.markdown(f"**역할:** {role}")
