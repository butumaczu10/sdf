# survival_quiz_app.py
# --------------------------------------------
# "재난에서 살아남기" - Streamlit 앱 (완성본)
# - 6가지 상황을 단계별로 진행
# - 숫자(1~8) 기반 성향 로직 (MBTI 노출 없음)
# - 결과: 생존자 유형 + 강점/약점/생존 팁
# - '다른 유형 보기'로 16유형 상세를 expander로 제공
# - 딥그린(조난) 테마 적용
import streamlit as st

# ----------------- 기본 세팅 -----------------
st.set_page_config(page_title="재난에서 살아남기", page_icon="🌍", layout="centered")

# ----------------- CSS (딥그린 테마) -----------------
st.markdown(
    """
    <style>
    .stApp { background-color: #1b4332; color: #ffffff; }
    h1, h2, h3, h4 { color: #d8f3dc; }
    /* 버튼 스타일 (신/구 버전 동시 대응) */
    div.stButton > button, button[kind="primary"] {
        background-color: #2d6a4f !important;
        color: #ffffff !important;
        border-radius: 12px !important;
        border: 1px solid #95d5b2 !important;
    }
    div.stButton > button:hover, button[kind="primary"]:hover {
        background-color: #40916c !important;
        border: 1px solid #b7e4c7 !important;
    }
    /* 라디오/체크 라벨 색상 */
    .stRadio label, .stCheckbox label { color: #f0f0f0 !important; }

    /* 결과 카드 */
    .result-box {
        background-color: #2d6a4f;
        padding: 20px;
        border-radius: 16px;
        margin-top: 16px;
        box-shadow: 0 0 10px rgba(0,0,0,0.35);
    }
    /* 구분선 색 */
    hr { border: none; height: 1px; background: #95d5b2; opacity: 0.4; }
    </style>
    """,
    unsafe_allow_html=True
)

# ----------------- 상태 초기화 (안전) -----------------
def ensure_state():
    if "step" not in st.session_state:
        st.session_state.step = 0
    if "scores" not in st.session_state:
        # 1(E),2(I),3(N),4(S),5(T),6(F),7(P),8(J)
        st.session_state.scores = {str(k): 0 for k in range(1, 9)}
    else:
        # 필요한 키가 빠져있어도 안전
        for k in map(str, range(1, 9)):
            st.session_state.scores.setdefault(k, 0)
    if "answers" not in st.session_state:
        st.session_state.answers = {}
    if "show_all_types" not in st.session_state:
        st.session_state.show_all_types = False

ensure_state()

# ----------------- 질문 데이터 -----------------
questions = [
    {
        "situation": "🔥 화재 발생",
        "question": "빌딩에서 화재가 발생했다! 가장 먼저 어떻게 할까?",
        "options": {
            "1": "사람들을 모아 함께 대피 경로를 찾는다",
            "2": "혼자 신속하게 가장 가까운 비상구로 이동한다",
            "4": "불과 연기를 확인하고 안전한 계단을 이용한다",
            "3": "창문이나 다른 비상 루트를 즉석에서 찾아본다",
        },
        "tip": "화재 시에는 절대 엘리베이터를 이용하지 말고, 계단으로 이동하세요.",
    },
    {
        "situation": "🌏 지진 발생",
        "question": "강한 지진이 발생했다! 당신의 행동은?",
        "options": {
            "4": "책상이나 탁자 아래에 들어가 머리를 보호한다",
            "3": "바로 건물 밖으로 뛰쳐나간다",
            "8": "비상용품을 챙기고 질서 있게 대피한다",
            "7": "상황을 보며 즉흥적으로 판단한다",
        },
        "tip": "지진 시에는 머리를 보호하고, 진동이 멈춘 후 안전하게 대피하세요.",
    },
    {
        "situation": "🌋 화산 폭발",
        "question": "화산이 폭발했다! 당신은?",
        "options": {
            "5": "먼저 가장 합리적인 탈출 경로를 계산한다",
            "6": "가족/친구가 다 같이 대피할 수 있도록 돕는다",
            "8": "대피 계획에 따라 침착하게 움직인다",
            "7": "주변 상황을 보고 빠른 길을 즉석에서 찾는다",
        },
        "tip": "화산재는 호흡기를 막을 수 있
