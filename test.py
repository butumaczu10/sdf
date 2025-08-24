# survival_quiz_app_stable.py
# ============================================
# "재난에서 살아남기" 스트림릿 앱
# ✅ 선택지 흰색, 버튼 1회 클릭 즉시 진행, rerun 오류 제거

import streamlit as st

# ----------------- 페이지 세팅 -----------------
st.set_page_config(page_title="재난에서 살아남기", page_icon="🌍", layout="centered")

# ----------------- CSS 통합 -----------------
st.markdown(
    """
    <style>
    .stApp { background-color: #1b4332; color: #ffffff; }
    h1, h2, h3, h4 { color: #d8f3dc; }
    div.stButton > button, button[kind="primary"] {
        background-color: #2d6a4f !important;
        color: #ffffff !important;
        border-radius: 12px !important;
        border: 1px solid #95d5b2 !important;
        padding: 10px 20px !important;
        margin: 5px 0 !important;
        text-align: left !important;
    }
    div.stButton > button:hover, button[kind="primary"]:hover {
        background-color: #40916c !important;
        border: 1px solid #b7e4c7 !important;
    }
    .result-box {
        background-color: #2d6a4f;
        padding: 20px;
        border-radius: 16px;
        margin-top: 16px;
        box-shadow: 0 0 10px rgba(0,0,0,0.35);
    }
    hr { border: none; height: 1px; background: #95d5b2; opacity: 0.4; }
    </style>
    """,
    unsafe_allow_html=True
)

# ----------------- 상태 초기화 -----------------
def ensure_state():
    if "step" not in st.session_state: st.session_state.step = 0
    if "scores" not in st.session_state: st.session_state.scores = {str(k): 0 for k in range(1,9)}
    else:
        for k in map(str, range(1,9)): st.session_state.scores.setdefault(k,0)
    if "answers" not in st.session_state: st.session_state.answers = {}
    if "show_all_types" not in st.session_state: st.session_state.show_all_types = False
    if "clicked_option" not in st.session_state: st.session_state.clicked_option = None
ensure_state()

# ----------------- 질문 데이터 -----------------
questions = [
    {"situation":"🔥 화재 발생",
     "question":"빌딩에서 화재가 발생했다! 가장 먼저 어떻게 할까?",
     "options":{"1":"사람들을 모아 함께 대피 경로를 찾는다",
                "2":"혼자 신속하게 가장 가까운 비상구로 이동한다",
                "4":"불과 연기를 확인하고 안전한 계단을 이용한다",
                "3":"창문이나 다른 비상 루트를 즉석에서 찾아본다"},
     "tip":"화재 시에는 절대 엘리베이터를 이용하지 말고, 계단으로 이동하세요." \n '함께 보면 좋을 영상: https://youtu.be/bWCZ3UeqDOw?si=7-5mOYfzu8HvJRJo'},
    {"situation":"🌏 지진 발생",
     "question":"강한 지진이 발생했다! 당신의 행동은?",
     "options":{"4":"책상이나 탁자 아래에 들어가 머리를 보호한다",
                "3":"건물 밖으로 뛰쳐나간다",
                "8":"비상용품을 챙기고 질서 있게 대피한다",
                "7":"일단 문부터 열어두고 생각한다"},
     "tip":"지진 시에는 머리를 보호하고, 진동이 멈춘 후 안전하게 대피하세요." \n '함께 보면 좋을 영상: https://youtu.be/lO7AZIhi5mo?si=_y-aVvakWIqV8SMd'},
    {"situation":"🌋 화산 폭발",
     "question":"화산이 폭발했다! 당신은?",
     "options":{"5":"먼저 가장 합리적인 대피 경로를 계산한다",
                "6":"가족/친구가 다 같이 대피할 수 있도록 돕는다",
                "8":"대피 계획에 따라 침착하게 움직인다",
                "7":"주변 상황을 보고 빠른 길을 즉석에서 찾는다"},
     "tip":"화산재는 호흡기를 막을 수 있으니 마스크나 천으로 코와 입을 막으세요." \n '함께 보면 좋을 영상: https://youtu.be/RKp8FGY-1jA?si=Wx0IWXm3xp6sxAI7'},
    {"situation":"⚔️ 전쟁 상황",
     "question":"전쟁이 발발했다! 당신의 대피 방법은?",
     "options":{"1":"이웃과 함께 대피하며 정보를 공유한다",
                "2":"최소한의 노출로 조용히 움직인다",
                "5":"지도와 경로를 분석해 가장 안전한 길을 찾는다",
                "6":"다른 사람들을 챙기며 함께 피난한다"},
     "tip":"전쟁 상황에서는 눈에 띄지 않게 이동하고, 라디오 등으로 정보를 확인하세요." \n '함께 보면 좋을 영상: https://youtu.be/JPOghGgs-lo?si=wTmUprDK_l8Zj962'},
    {"situation":"🌊 폭우와 홍수",
     "question":"폭우로 도로가 잠겼다! 당신은?",
     "options":{"4":"높은 지대로 이동한다",
                "3":"물살을 가로질러 다른 길을 찾는다",
                "8":"예상된 대피 경로를 따른다",
                "7":"상황에 맞춰 목적지를 그때그때 바꾸어 나아간다"},
     "tip":"홍수 시에는 절대 물살을 건너지 말고 높은 지대로 이동하세요." \n '함께 보면 좋을 영상: https://youtu.be/cOQEdUBpLjg?si=Tpuxs1aeoLierBM-'},
    {"situation":"❄️ 눈보라 속 조난",
     "question":"산에서 눈보라를 만나 고립됐다! 당신은?",
     "options":{"2":"한 곳에 머무르며 체력을 아낀다",
                "1":"움직이며 구조 신호를 찾는다",
                "5":"불을 피워 체온을 유지한다",
                "6":"동료들과 서로 의지하며 대기한다"},
     "tip":"조난 시에는 체력을 아끼고, 구조 신호를 보내며 체온을 유지하세요." \n '함께 보면 좋을 영상: https://youtu.be/gePzFtRdGbs?si=6ArBg2dZ8TY5s0bz'}
]

# ----------------- 16유형 데이터 -----------------
TYPES = {
    "2458":{"name":"신중한 분석가형 생존자","strengths":"계획적이고, 현실적이다. 위기에서도 침착하다.","weaknesses":"융통성 부족으로 돌발 변수에 약할 수 있다.","advice":"세운 계획을 기본으로 하되 예외 시나리오를 준비하세요."},
    "2468":{"name":"헌신적인 수호자형 생존자","strengths":"타인을 잘 돌보고 신뢰감을 준다.","weaknesses":"자기 안전을 뒤로 미루는 경향이 있다.","advice":"도움과 자기보호의 균형을 지키세요."},
    "2368":{"name":"통찰력 있는 조언자형 생존자","strengths":"상황을 넓게 읽고 장기 전략에 강하다.","weaknesses":"과도한 고민으로 실행이 늦어질 수 있다.","advice":"핵심 결정을 정해두고 바로 행동하세요."},
    "2358":{"name":"전략적인 설계자형 생존자","strengths":"체계적 판단과 전략 구상 능력이 탁월하다.","weaknesses":"독단적으로 보일 수 있으니 주의하자.","advice":"전략 공유로 팀의 신뢰와 속도를 높이세요."},
    "2457":{"name":"실용적인 해결사형 생존자","strengths":"손재주와 즉시 해결 능력이 뛰어나다.","weaknesses":"장기 계획을 소홀히 할 위험이 있다.","advice":"즉흥력에 최소한의 계획을 더하세요."},
    "2467":{"name":"온화한 적응가형 생존자","strengths":"차분하고 조화롭게 협력한다.","weaknesses":"소극적 판단으로 기회를 놓칠 수 있다.","advice":"필요할 때는 명확하게 주도하세요."},
    "2367":{"name":"이상적인 탐색자형 생존자","strengths":"창의적이고 의미 중심의 동기.","weaknesses":"현실적 제약에 취약할 수 있음.","advice":"창의적 아이디어를 실행 체크리스트로 구체화하세요."},
    "2357":{"name":"호기심 많은 사색가형 생존자","strengths":"논리 분석과 대안 탐색이 빠르다.","weaknesses":"과분석으로 행동이 지연될 수 있다.","advice":"분석 마감시간을 정하고 실행하세요."},
    "1457":{"name":"대담한 행동가형 생존자","strengths":"위기에도 침착하고, 즉각적 행동에 능하다.","weaknesses":"무모함으로 리스크를 키울 수 있으니 주의하자.","advice":"행동 전 핵심 금지사항만 점검!"},
    "1467":{"name":"활기찬 즉흥가형 생존자","strengths":"적응력·사기 진작 능력이 우수하다.","weaknesses":"주의 산만·계획 부족의 가능성이 있다.","advice":"기본 안전수칙을 체크리스트로 고정하세요."},
    "1367":{"name":"열정적인 탐험가형 생존자","strengths":"창의·동기 부여, 다양한 시도.","weaknesses":"우왕좌왕으로 에너지 소모.","advice":"우선순위 3가지를 정하고 거기에 집중하세요."},
    "1357":{"name":"도전적인 전략가형 생존자","strengths":"재치 있는 문제 해결, 기민한 판단.","weaknesses":"규칙 무시·충동 위험.","advice":"도전하되 ‘금지·필수’ 규칙은 반드시 준수하세요."},
    "1458":{"name":"체계적인 지휘관형 생존자","strengths":"조직·실행력이 탁월, 신속한 지휘.","weaknesses":"융통성 부족·고집 위험.","advice":"대안 경로를 항상 1개 이상 준비하세요."},
    "1468":{"name":"사교적인 보호자형 생존자","strengths":"협력·유대 강화에 강함.","weaknesses":"자기 소모와 피로 누적.","advice":"역할 분담과 휴식 스케줄을 명확히."},
    "1368":{"name":"따뜻한 지도자형 생존자","strengths":"이타적 리더십, 팀 결속 ↑.","weaknesses":"과책임·번아웃 위험.","advice":"책임을 위임하고 팀의 자율을 신뢰하세요."},
    "1358":{"name":"결단력 있는 통솔자형 생존자","strengths":"강한 결단·실행 속도.","weaknesses":"독단·갈등 유발 위험.","advice":"핵심 결정 공유·피드백 루프를 운영하세요."}
}

# ----------------- 진행 -----------------
st.title("🌍 재난 상황에서 나는 어떤 생존자일까?")
st.markdown("6가지 재난 상황에서 선택지를 고르고, 당신의 생존 성향을 확인해 보세요!")
st.markdown("<hr/>", unsafe_allow_html=True)
progress = st.session_state.step / len(questions)
st.progress(progress)

if st.session_state.step < len(questions):
    q = questions[st.session_state.step]
    st.subheader(f"상황 {st.session_state.step+1}) {q['situation']}")

    # ----------------- 버튼 선택지 -----------------
    for k,v in q["options"].items():
        btn_id = f"btn_{st.session_state.step}_{k}"
        if st.button(v, key=btn_id):
            st.session_state.clicked_option = (k,v)

    # 클릭 후 상태 업데이트만, rerun 없이 처리
    if st.session_state.clicked_option:
        k,v = st.session_state.clicked_option
        st.session_state.scores[k] += 1
        st.session_state.answers[q["situation"]] = (v, q["tip"])
        st.session_state.step += 1
        st.session_state.clicked_option = None

    if st.button("처음으로 ⏮️"):
        st.session_state.step = 0
        st.session_state.scores = {str(k):0 for k in range(1,9)}
        st.session_state.answers = {}
        st.session_state.show_all_types = False
        st.session_state.clicked_option = None

else:
    # ----------------- 결과 계산 -----------------
    s = {k: st.session_state.scores.get(k,0) for k in map(str, range(1,9))}
    code = ""
    code += "1" if s["1"] >= s["2"] else "2"
    code += "4" if s["4"] >= s["3"] else "3"
    code += "5" if s["5"] >= s["6"] else "6"
    code += "8" if s["8"] >= s["7"] else "7"

    st.markdown('<div class="result-box">', unsafe_allow_html=True)
    data = TYPES.get(code)
    if data:
        st.header(f"당신의 생존 성향: {data['name']}")
        st.write("### 🧩 특징")
        st.markdown(f"- **강점**: {data['strengths']}")
        st.markdown(f"- **약점**: {data['weaknesses']}")
        st.markdown(f"- **생존 팁**: {data['advice']}")
    else:
        st.header("당신만의 독특한 생존자 유형!")
        st.markdown("아직 데이터에 없는 조합입니다. 😉 기본 안전수칙을 우선하세요.")
    st.markdown("</div>", unsafe_allow_html=True)

    st.write("### 📘 상황별 대처 요약")
    for sit, (ans, tip) in st.session_state.answers.items():
        st.markdown(f"**{sit}**  \n- 선택: {ans}  \n- ✅ 팁: {tip}")

    col1, col2 = st.columns(2)
    with col1:
        if st.button("🔄 다시 시작하기"):
            st.session_state.step = 0
            st.session_state.scores = {str(k):0 for k in range(1,9)}
            st.session_state.answers = {}
            st.session_state.show_all_types = False
            st.session_state.clicked_option = None
    with col2:
        if st.button("📖 다른 유형 보기"):
            st.session_state.show_all_types = not st.session_state.show_all_types

    if st.session_state.show_all_types:
        st.write("### 🔍 다른 생존자 유형들")
        ordered_items = [(code, TYPES[code])] + [(k,v) for k,v in TYPES.items() if k!=code]
        seen = set()
        for k,v in ordered_items:
            if k in seen: continue
            seen.add(k)
            with st.expander(v["name"]):
                st.markdown(f"- **강점**: {v['strengths']}")
                st.markdown(f"- **약점**: {v['weaknesses']}")
                st.markdown(f"- **생존 팁**: {v['advice']}")
