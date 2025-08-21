# survival_quiz_app.py
# --------------------------------------------
# "재난에서 살아남기" - 스트림릿 앱 (완성본)
# 6가지 상황에 대한 선택 → 생존자 유형 결과 + 강점/약점/생존 팁
# MBTI 문자가 아닌 숫자 기반 로직 사용 (1~8)

import streamlit as st

# ----------------- 페이지 세팅 -----------------
st.set_page_config(page_title="재난에서 살아남기", page_icon="🌍", layout="centered")

# ----------------- CSS 디자인 -----------------
st.markdown(
    """
    <style>
    /* 전체 배경색 */
    .stApp {
        background-color: #1b4332; /* 딥그린 */
        color: white;
    }
    /* 제목 */
    h1, h2, h3, h4 {
        color: #d8f3dc;
    }
    /* 버튼 */
    button[kind="primary"] {
        background-color: #2d6a4f !important;
        color: white !important;
        border-radius: 10px !important;
        border: 1px solid #95d5b2 !important;
    }
    button[kind="primary"]:hover {
        background-color: #40916c !important;
        border: 1px solid #b7e4c7 !important;
    }
    /* 라디오 라벨 */
    .stRadio label {
        color: #f0f0f0 !important;
    }
    /* 결과 카드 */
    .result-box {
        background-color: #2d6a4f;
        padding: 20px;
        border-radius: 15px;
        margin-top: 20px;
        box-shadow: 0px 0px 10px rgba(0,0,0,0.4);
    }
    </style>
    """,
    unsafe_allow_html=True
)

st.title("🌍 재난 상황에서 나는 어떤 생존자일까?")
st.markdown("6가지 재난 상황에서 선택지를 고르고, 당신의 생존 성향을 확인해 보세요!")
st.markdown("---")

# ----------------- 점수 관리 -----------------
if "scores" not in st.session_state:
    st.session_state.scores = {"1":0, "2":0, "3":0, "4":0, "5":0, "6":0, "7":0, "8":0}
if "step" not in st.session_state:
    st.session_state.step = 0
if "answers" not in st.session_state:
    st.session_state.answers = {}

# ----------------- 질문 데이터 -----------------
questions = [
    {
        "situation": "🔥 화재 발생",
        "question": "빌딩에서 화재가 발생했다! 가장 먼저 어떻게 할까?",
        "options": {
            "1": "사람들을 모아 함께 대피 경로를 찾는다",
            "2": "혼자 신속하게 가장 가까운 비상구로 이동한다",
            "4": "불과 연기를 확인하고 안전한 계단을 이용한다",
            "3": "창문이나 다른 비상 루트를 즉석에서 찾아본다"
        },
        "tip": "화재 시에는 절대 엘리베이터를 이용하지 말고, 계단으로 이동하세요."
    },
    {
        "situation": "🌏 지진 발생",
        "question": "강한 지진이 발생했다! 당신의 행동은?",
        "options": {
            "4": "책상이나 탁자 아래에 들어가 머리를 보호한다",
            "3": "바로 건물 밖으로 뛰쳐나간다",
            "8": "비상용품을 챙기고 질서 있게 대피한다",
            "7": "상황을 보며 즉흥적으로 판단한다"
        },
        "tip": "지진 시에는 머리를 보호하고, 진동이 멈춘 후 안전하게 대피하세요."
    },
    {
        "situation": "🌋 화산 폭발",
        "question": "화산이 폭발했다! 당신은?",
        "options": {
            "5": "먼저 가장 합리적인 탈출 경로를 계산한다",
            "6": "가족/친구가 다 같이 대피할 수 있도록 돕는다",
            "8": "대피 계획에 따라 침착하게 움직인다",
            "7": "주변 상황을 보고 빠른 길을 즉석에서 찾는다"
        },
        "tip": "화산재는 호흡기를 막을 수 있으니 마스크나 천으로 코와 입을 막으세요."
    },
    {
        "situation": "⚔️ 전쟁 상황",
        "question": "전쟁이 발발했다! 당신의 대피 방법은?",
        "options": {
            "1": "이웃과 함께 대피하며 정보를 공유한다",
            "2": "최소한의 노출로 조용히 움직인다",
            "5": "지도와 경로를 분석해 가장 안전한 길을 찾는다",
            "6": "다른 사람들을 챙기며 함께 피난한다"
        },
        "tip": "전쟁 상황에서는 눈에 띄지 않게 이동하고, 라디오 등으로 정보를 확인하세요."
    },
    {
        "situation": "🌊 폭우와 홍수",
        "question": "폭우로 도로가 잠겼다! 당신은?",
        "options": {
            "4": "높은 지대로 바로 이동한다",
            "3": "물살을 가로질러 다른 길을 시도한다",
            "8": "예상된 대피 경로를 따른다",
            "7": "상황에 맞춰 즉시 다른 길을 찾는다"
        },
        "tip": "홍수 시에는 절대 물살을 건너지 말고 높은 지대로 이동하세요."
    },
    {
        "situation": "❄️ 눈보라 속 조난",
        "question": "산에서 눈보라를 만나 고립됐다! 당신은?",
        "options": {
            "2": "한 곳에 머무르며 체력을 아낀다",
            "1": "움직이며 구조 신호를 찾는다",
            "5": "불을 피워 체온을 유지한다",
            "6": "동료들과 서로 의지하며 대기한다"
        },
        "tip": "조난 시에는 체력을 아끼고, 구조 신호를 보내며 체온을 유지하세요."
    },
]

# ----------------- 생존자 유형 데이터 -----------------
survivor_types = {
    "2148": {
        "name": "신중한 분석가형 생존자",
        "strength": "위험 속에서도 침착하며 세부사항에 강하다.",
        "weakness": "융통성이 부족할 수 있다.",
        "tip": "계획을 세우되, 예외 상황에도 대비하세요."
    },
    "2648": {
        "name": "헌신적인 수호자형 생존자",
        "strength": "타인을 잘 돌보고 협동심이 강하다.",
        "weakness": "자신을 뒤로 미루는 경향이 있다.",
        "tip": "다른 사람도 중요하지만 본인 안전도 챙기세요."
    },
    # ... (모든 조합에 대해 추가 가능, 여기서는 예시만)
}

# ----------------- 진행 -----------------
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
    # 점수 기반 생존자 코드 만들기
    code = ""
    code += "1" if st.session_state.scores["1"] >= st.session_state.scores["2"] else "2"
    code += "4" if st.session_state.scores["4"] >= st.session_state.scores["3"] else "3"
    code += "5" if st.session_state.scores["5"] >= st.session_state.scores["6"] else "6"
    code += "8" if st.session_state.scores["8"] >= st.session_state.scores["7"] else "7"

    st.markdown('<div class="result-box">', unsafe_allow_html=True)
    if code in survivor_types:
        st.header(f"당신의 생존 성향: {survivor_types[code]['name']}")
        st.write("### 🟢 강점")
        st.markdown(f"- {survivor_types[code]['strength']}")
        st.write("### 🔴 약점")
        st.markdown(f"- {survivor_types[code]['weakness']}")
        st.write("### 📘 생존 팁")
        st.markdown(f"- {survivor_types[code]['tip']}")
    else:
        st.header("당신만의 독특한 생존자 유형이네요!")
        st.write("아직 데이터에 없는 조합입니다. 😉")

    st.write("### 상황별 대처 요약")
    for sit, (ans, tip) in st.session_state.answers.items():
        st.markdown(f"**{sit}**  \n선택: {ans}  \n✅ 팁: {tip}")

    st.markdown("</div>", unsafe_allow_html=True)

    if st.button("🔄 다시 시작하기"):
        st.session_state.scores = {"1":0, "2":0, "3":0, "4":0, "5":0, "6":0, "7":0, "8":0}
        st.session_state.step = 0
        st.session_state.answers = {}
        st.rerun()
