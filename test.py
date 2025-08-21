# survival_quiz_step.py (업데이트: 유형별 강점/약점/팁 + expander)
import streamlit as st

st.set_page_config(page_title="재난에서 살아남기", page_icon="🌍", layout="centered")

st.title("🌍 재난 상황에서 나는 어떤 생존자일까?")
st.markdown("상황별 질문에 답하고, 마지막에 당신의 생존 성향을 확인하세요!")
st.markdown("---")

# 초기화
if "step" not in st.session_state:
    st.session_state.step = 0
if "scores" not in st.session_state:
    st.session_state.scores = {"E":0, "I":0, "S":0, "N":0, "T":0, "F":0, "J":0, "P":0}
if "answers" not in st.session_state:
    st.session_state.answers = {}
if "show_all_types" not in st.session_state:
    st.session_state.show_all_types = False

# 질문 데이터
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

# 생존자 유형 데이터 (강점/약점/팁 포함)
survivor_types = {
    "ISTJ": {
        "name": "신중한 분석가형 생존자",
        "strengths": "계획적이고 현실적. 위기에서 침착하게 행동.",
        "weaknesses": "융통성이 부족해 돌발 상황에 약할 수 있음.",
        "advice": "재난 계획을 철저히 세우되, 변화에도 적응하세요."
    },
    "ISFJ": {
        "name": "헌신적인 수호자형 생존자",
        "strengths": "타인을 잘 챙기고 안정감을 줌.",
        "weaknesses": "자신을 희생해 위험에 빠질 수 있음.",
        "advice": "다른 사람을 돌보면서도 자기 안전을 우선하세요."
    },
    "INFJ": {
        "name": "통찰력 있는 조언자형 생존자",
        "strengths": "상황을 예리하게 읽고 전략적 사고.",
        "weaknesses": "실행력이 부족할 수 있음.",
        "advice": "통찰을 행동으로 옮기는 용기가 필요합니다."
    },
    "INTJ": {
        "name": "전략적인 설계자형 생존자",
        "strengths": "계획과 전략에 강함.",
        "weaknesses": "협력보다는 독단적으로 움직일 수 있음.",
        "advice": "혼자만의 판단이 아니라 팀워크를 고려하세요."
    },
    "ISTP": {
        "name": "실용적인 해결사형 생존자",
        "strengths": "문제 해결 능력 뛰어나고 즉각적 행동 가능.",
        "weaknesses": "계획을 무시하고 충동적일 수 있음.",
        "advice": "즉흥성에 계획성을 보완하세요."
    },
    "ISFP": {
        "name": "온화한 적응가형 생존자",
        "strengths": "차분하고 조화롭게 상황 적응.",
        "weaknesses": "소극적이어서 위기 리더십 부족.",
        "advice": "자신의 목소리를 낼 때 더 안전해질 수 있습니다."
    },
    "INFP": {
        "name": "이상적인 탐색자형 생존자",
        "strengths": "창의적이고 의미를 찾음.",
        "weaknesses": "현실적 문제 해결이 느릴 수 있음.",
        "advice": "이상과 현실의 균형을 맞추세요."
    },
    "INTP": {
        "name": "호기심 많은 사색가형 생존자",
        "strengths": "논리적이고 새로운 해결책 탐구.",
        "weaknesses": "실행력 부족, 망설임.",
        "advice": "분석을 끝내고 행동으로 옮기세요."
    },
    "ESTP": {
        "name": "대담한 행동가형 생존자",
        "strengths": "위험 속에서도 침착하고 빠르게 대응.",
        "weaknesses": "너무 무모해 사고로 이어질 수 있음.",
        "advice": "대담함에 신중함을 더하세요."
    },
    "ESFP": {
        "name": "활기찬 즉흥가형 생존자",
        "strengths": "주변을 활기차게 하고 상황에 잘 적응.",
        "weaknesses": "계획이 부족하고 쉽게 주의 산만.",
        "advice": "즉흥성과 함께 기초적인 안전 지침은 지키세요."
    },
    "ENFP": {
        "name": "열정적인 탐험가형 생존자",
        "strengths": "창의적이고 주변을 고무함.",
        "weaknesses": "우왕좌왕할 수 있음.",
        "advice": "열정을 전략과 결합하세요."
    },
    "ENTP": {
        "name": "도전적인 전략가형 생존자",
        "strengths": "재치 있고 기발한 해결책을 냄.",
        "weaknesses": "규칙 무시와 충동적 행동.",
        "advice": "도전을 하되 기본 원칙은 따르세요."
    },
    "ESTJ": {
        "name": "체계적인 지휘관형 생존자",
        "strengths": "조직력과 실행력이 뛰어남.",
        "weaknesses": "융통성 부족, 고집스러움.",
        "advice": "리더십에 유연성을 더하세요."
    },
    "ESFJ": {
        "name": "사교적인 보호자형 생존자",
        "strengths": "타인을 돌보고 협력 잘함.",
        "weaknesses": "자신을 잊고 남만 챙길 수 있음.",
        "advice": "자기 돌봄도 중요합니다."
    },
    "ENFJ": {
        "name": "따뜻한 지도자형 생존자",
        "strengths": "이타적이고 리더십 발휘.",
        "weaknesses": "과도한 책임감.",
        "advice": "책임을 분담하고 균형을 찾으세요."
    },
    "ENTJ": {
        "name": "결단력 있는 통솔자형 생존자",
        "strengths": "빠른 결단과 실행.",
        "weaknesses": "독단적일 수 있음.",
        "advice": "결단력에 배려심을 더하세요."
    },
}

# 현재 질문
if st.session_state.step < len(questions):
    q = questions[st.session_state.step]
    st.subheader(f"상황 {st.session_state.step+1}) {q['situation']}")
    choice = st.radio(q["question"], list(q["options"].values()), key=f"q{st.session_state.step}")

    if st.button("다음 ➡️"):
        if choice:
            for k, v in q["options"].items():
                if v == choice:
                    st.session_state.scores[k] += 1
                    st.session_state.answers[q['situation']] = (choice, q["tip"])
            st.session_state.step += 1
            st.rerun()

else:
    # MBTI 코드 계산
    scores = st.session_state.scores
    mbti = ""
    mbti += "E" if scores["E"] >= scores["I"] else "I"
    mbti += "S" if scores["S"] >= scores["N"] else "N"
    mbti += "T" if scores["T"] >= scores["F"] else "F"
    mbti += "J" if scores["J"] >= scores["P"] else "P"

    result = survivor_types[mbti]

    st.header(f"당신의 생존 성향: {result['name']}")

    st.write("### 🧩 당신의 특징")
    st.markdown(f"- **강점**: {result['strengths']}")
    st.markdown(f"- **약점**: {result['weaknesses']}")
    st.markdown(f"- **생존 팁**: {result['advice']}")

    st.write("### 📘 상황별 대처 팁")
    for sit, (ans, tip) in st.session_state.answers.items():
        st.markdown(f"**{sit}**  \n선택: {ans}  \n✅ 올바른 팁: {tip}")

    st.success("생존 지식은 언제나 실제 상황에 큰 도움이 됩니다. 기억해 두세요!")

    # 버튼 2개
    col1, col2 = st.columns(2)
    with col1:
        if st.button("🔄 다시 시작하기"):
            st.session_state.step = 0
            st.session_state.scores = {"E":0,"I":0,"S":0,"N":0,"T":0,"F":0,"J":0,"P":0}
            st.session_state.answers = {}
            st.session_state.show_all_types = False
            st.rerun()
    with col2:
        if st.button("📖 다른 유형 보기"):
            st.session_state.show_all_types = not st.session_state.show_all_types

    # 다른 유형 전체 보기
    if st.session_state.show_all_types:
        st.write("### 🔍 다른 생존자 유형들")
        for code, data in survivor_types.items():
            with st.expander(f"{data['name']} ({code})"):
                st.markdown(f"- **강점**: {data['strengths']}")
                st.markdown(f"- **약점**: {data['weaknesses']}")
                st.markdown(f"- **생존 팁**: {data['advice']}")
