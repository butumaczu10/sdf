import streamlit as st
import random

st.set_page_config(page_title="괴담 생존 게임", layout="wide")
st.markdown(
    """
    <style>
    body {background-color: #0a0a0a; color: #ffffff;}
    .stButton>button {background-color: #333333; color: #ffffff;}
    .stRadio>div>label {color: #ffffff;}
    </style>
    """, unsafe_allow_html=True
)

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

# 상황과 선택지 (원래 느낌 살린 길이 있는 선택지)
situations = [
    {
        "text": "폐허가 된 학교에서 으스스한 발자국 소리가 들린다. 당신은 어떻게 할까?",
        "options": [
            "숨을 곳을 찾아 몸을 낮춘다.",
            "심장이 터질 듯 뛰면서 복도를 달린다.",
            "호기심이 동해 소리의 근원을 찾아가 본다.",
            "문을 잠그고 안에서 상황을 지켜본다."
        ]
    },
    {
        "text": "복도에 검게 일그러진 그림자가 천천히 움직인다.",
        "options": [
            "그림자를 무시하고 지나간다.",
            "휴대폰으로 사진을 찍어 기록한다.",
            "두려움을 억누르고 도망친다.",
            "그림자와 눈을 마주치며 대화를 시도한다."
        ]
    },
    {
        "text": "어두운 지하실 문이 삐걱거리며 열리고 있다.",
        "options": [
            "호기심을 참지 못하고 들어간다.",
            "뒤돌아가 안전한 곳으로 도망친다.",
            "소리를 크게 내 상황을 확인해 본다.",
            "조심스럽게 문 앞에서 기다린다."
        ]
    },
    {
        "text": "벽에 이상한 글씨가 피처럼 적혀 있다.",
        "options": [
            "조심스럽게 글씨를 읽어본다.",
            "손으로 글씨를 지운다.",
            "무시하고 계속 걸어간다.",
            "사진을 찍어 나중에 분석한다."
        ]
    },
    {
        "text": "복도 끝에서 낮게 속삭이는 목소리가 들린다.",
        "options": [
            "뒤돌아보고 확인한다.",
            "심장을 부여잡고 달린다.",
            "속삭임을 따라가 본다.",
            "무시하고 복도를 걷는다."
        ]
    },
    {
        "text": "전등이 깜빡거리며 불길한 그림자를 만든다.",
        "options": [
            "멈춰서 상황을 관찰한다.",
            "빠르게 걸어서 지나간다.",
            "전등을 직접 확인해본다.",
            "깜빡거리는 전등을 피해 뛰어 나간다."
        ]
    },
    {
        "text": "책장에서 책이 스스로 떨어진다.",
        "options": [
            "떨어진 책을 주워 살펴본다.",
            "겁에 질려 도망친다.",
            "무시하고 지나간다.",
            "책이 떨어진 원인을 관찰한다."
        ]
    },
    {
        "text": "복도 끝에서 손이 천천히 튀어나온다.",
        "options": [
            "도망치며 복도를 벗어난다.",
            "손을 잡아보며 반응을 확인한다.",
            "소리를 지른다.",
            "그림자 속으로 몸을 숨긴다."
        ]
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
