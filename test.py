import streamlit as st
import random

st.set_page_config(page_title="괴담 생존 게임", layout="wide")

st.title("👻 괴담에서 살아남기")

# 캐릭터 유형 정의
types = {
    "겁 많은 도망자": 40,
    "호기심 많은 희생자": 30,
    "냉정한 생존자": 80,
    "계획적인 전략가": 75,
    "직감 있는 탐험가": 65,
    "충동적인 용감자": 50,
    "조심스러운 관찰자": 70,
    "현실적인 회피자": 55,
    "호기심+공포 혼합형": 35,
    "리더형 생존자": 85,
    "용맹한 보호자": 60,
    "분석적 판단자": 78,
    "불안한 회피자": 33,
    "과감한 탐험가": 68,
    "신중한 결단자": 72,
    "모험적 위험 감수자": 58
}

# 상황과 선택지
situations = [
    {
        "text": "폐허가 된 학교에서 소리가 들린다.",
        "options": ["숨는다", "달린다", "소리 쫓아간다", "문 잠근다"]
    },
    {
        "text": "복도에 그림자가 나타났다.",
        "options": ["무시한다", "사진 찍는다", "도망친다", "대화 시도"]
    },
    {
        "text": "어두운 지하실 문이 삐걱거린다.",
        "options": ["들어간다", "돌아간다", "소리낸다", "기다린다"]
    },
    {
        "text": "벽에 이상한 글씨가 적혀있다.",
        "options": ["읽는다", "지운다", "무시하고 걷는다", "사진 찍는다"]
    },
    {
        "text": "복도 끝에서 이상한 속삭임이 들린다.",
        "options": ["뒤돌아본다", "달린다", "따라간다", "무시한다"]
    },
    {
        "text": "복도에 갑자기 전등이 깜빡인다.",
        "options": ["멈춘다", "빠르게 걷는다", "전등 확인", "뛰어 나간다"]
    },
    {
        "text": "책장에서 책이 스스로 떨어진다.",
        "options": ["줍는다", "도망친다", "무시한다", "관찰한다"]
    },
    {
        "text": "복도 끝에서 손이 튀어나온다.",
        "options": ["도망간다", "잡아본다", "소리친다", "숨는다"]
    }
]

# 세션 상태 초기화
if "answers" not in st.session_state:
    st.session_state.answers = []

# 상황 진행
if len(st.session_state.answers) < len(situations):
    idx = len(st.session_state.answers)
    situation = situations[idx]
    st.subheader(f"상황 {idx + 1}")
    st.write(situation["text"])
    choice = st.radio("당신은 어떤 선택을 할래?", situation["options"])
    if st.button("결정", key=f"btn_{idx}"):
        st.session_state.answers.append(choice)
        st.experimental_rerun()
else:
    st.subheader("🎯 결과")
    # 선택 기반 임의 유형 선택
    result_type = random.choice(list(types.keys()))
    survival = types[result_type]

    st.markdown(f"### 🏷️ 당신의 선택 종합 결과: {result_type}")
    st.markdown(f"### 💀 생존 확률: {survival}%")

    st.markdown("**다른 유형도 보고 싶다면 선택하세요:**")
    other_type = st.selectbox("다른 유형 보기", list(types.keys()))
    st.write(f"### 🏷️ {other_type}")
    st.write(f"💀 생존 확률: {types[other_type]}%")
    st.write(f"설명: {other_type} 유형은 상황에 따라 다르게 행동하며 생존 전략이 달라집니다.")

    if st.button("다시하기"):
        st.session_state.answers = []
        st.experimental_rerun()
