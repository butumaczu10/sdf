import random
from typing import Dict, List
import streamlit as st

# ---------------------------------------------
# "괴담에서 살아남기" — 8장 전체, 어둡고 편한 UI
# ---------------------------------------------

st.set_page_config(
    page_title="괴담에서 살아남기",
    page_icon="🕯️",
    layout="centered",
    initial_sidebar_state="collapsed",
)

DARK_CSS = """
<style>
:root {
  --bg: #0b0c10;
  --card: #101218;
  --text: #e6e6e6;
  --muted: #a3a3a3;
  --accent: #ff334e;
  --btn-bg: #1b1c22;
  --btn-hover: #2a2b32;
  --btn-text: #e6e6e6;
}
html, body, [data-testid="stAppViewContainer"] {
  background: var(--bg);
  color: var(--text);
}
section.main > div { max-width: 760px; }
h1, h2, h3 { color: var(--text); }
.small { color: var(--muted); font-size: 0.9rem; }
.card {
  background: linear-gradient(180deg, rgba(255,51,78,0.07), rgba(0,0,0,0));
  border: 1px solid rgba(255,255,255,0.06);
  border-radius: 16px;
  padding: 18px 16px;
}
.radio-container { margin: 8px 0; }
button.stButton>button {
    border-radius: 999px;
    padding: 10px 16px;
    font-weight: 700;
    background-color: var(--btn-bg);
    color: var(--btn-text);
    border: 1px solid rgba(255,255,255,0.1);
}
button.stButton>button:hover {
    background-color: var(--btn-hover);
}
.hr { height: 1px; background: rgba(255,255,255,0.08); margin: 8px 0 16px; }
.rule { font-size: 0.95rem; line-height: 1.6; }
.note { font-size: 0.9rem; color: var(--muted); }
.tag { display: inline-block; border: 1px solid rgba(255,255,255,0.16); border-radius: 999px; padding: 2px 10px; font-size: 0.85rem; color: var(--muted); margin-right: 6px; }
</style>
"""
st.markdown(DARK_CSS, unsafe_allow_html=True)

# 세션 상태 초기화
if "step" not in st.session_state:
    st.session_state.step = 0
if "scores" not in st.session_state:
    st.session_state.scores = {k: 0 for k in list("EISNTFJP")}
if "answers" not in st.session_state:
    st.session_state.answers: List[int] = []
if "username" not in st.session_state:
    st.session_state.username = ""

# MBTI 유형
TYPEBOOK: Dict[str, Dict[str, str | int]] = {
    "ESTJ": {"name": "현실주의 지휘관", "desc": "상황을 빠르게 정리하고 지휘하려 한다." , "surv": 55},
    "ESTP": {"name": "위험한 행동파", "desc": "맞서 싸우는 걸 즐기지만, 계산 실수에 약하다.", "surv": 25},
    "ESFJ": {"name": "착한 보호자", "desc": "타인을 우선하다가 자신이 희생되기 쉽다.", "surv": 35},
    "ESFP": {"name": "호들갑 탐험가", "desc": "분위기에 휩쓸려 먼저 뛰어들곤 한다.", "surv": 20},
    "ENTJ": {"name": "야망 있는 전략가", "desc": "진실을 파헤치려 하나 호기심이 독이 되기도.", "surv": 40},
    "ENTP": {"name": "논리적 도전가", "desc": "위험을 퍼즐처럼 대하지만 변수가 치명적이다.", "surv": 30},
    "ENFJ": {"name": "이상한 예언자", "desc": "사람들을 이끌며 희미한 징조를 읽는다.", "surv": 45},
    "ENFP": {"name": "호기심 많은 방랑자", "desc": "새로운 흔적을 쫓다 뜻밖의 결말을 맞는다.", "surv": 25},
    "ISTJ": {"name": "조용한 생존자", "desc": "최대한 눈에 띄지 않고 오래 버틴다.", "surv": 75},
    "ISTP": {"name": "신중한 기술자", "desc": "손재주로 위기를 넘기고 감정 소모를 줄인다.", "surv": 65},
    "ISFJ": {"name": "희생적인 동료", "desc": "남을 살리려다 이름 없는 희생자가 되기도.", "surv": 30},
    "ISFP": {"name": "순한 도망자", "desc": "본능적으로 피하며 의외로 오래 산다.", "surv": 70},
    "INTJ": {"name": "고독한 추리자", "desc": "진실에 닿지만 세상에 전할 기회는 드물다.", "surv": 50},
    "INTP": {"name": "냉철한 분석가", "desc": "모든 걸 계산해보지만 괴담은 예외가 많다.", "surv": 45},
    "INFJ": {"name": "비극의 몽상가", "desc": "직감을 좇다 허무한 끝을 맞기도 한다.", "surv": 35},
    "INFP": {"name": "꿈꾸는 생존자", "desc": "상상을 따르지만 기묘하게 운이 따른다.", "surv": 60},
}

# 8장 장면 샘플
SCENES = [
    {"title": "버려진 집 입구",
     "text": "어둡고 으스스한 집 앞에 서 있다. 들어갈까 말까?",
     "options":[{"label":"들어간다","effects":{"E":1,"S":1}},{"label":"돌아간다","effects":{"I":1,"N":1}}]},
    {"title": "복도에서 이상한 소리",
     "text": "복도에서 끼익거리는 소리가 난다. 어떻게 할까?",
     "options":[{"label":"직진한다","effects":{"E":1,"T":1}},{"label":"숨는다","effects":{"I":1,"F":1}}]},
    {"title": "계단 아래 그림자",
     "text": "계단 아래에서 누군가 움직이는 듯하다. 당신의 선택은?",
     "options":[{"label":"조심히 내려간다","effects":{"S":1,"T":1}},{"label":"올라간다","effects":{"N":1,"F":1}}]},
    {"title": "기묘한 방",
     "text": "방 안에 오래된 일기장이 있다. 읽어볼까?",
     "options":[{"label":"읽는다","effects":{"N":1,"I":1}},{"label":"무시한다","effects":{"S":1,"E":1}}]},
    {"title": "벽 뒤의 소리",
     "text": "벽 뒤에서 누군가 속삭인다. 어떻게 반응할까?",
     "options":[{"label":"응답한다","effects":{"E":1,"F":1}},{"label":"무시하고 지나간다","effects":{"I":1,"T":1}}]},
    {"title": "낡은 창고",
     "text": "창고 안에 반쯤 부서진 상자가 있다. 열어볼까?",
     "options":[{"label":"연다","effects":{"P":1,"N":1}},{"label":"닫는다","effects":{"J":1,"S":1}}]},
    {"title": "마지막 방",
     "text": "마지막 방에서 빛나는 문을 발견했다. 들어갈까?",
     "options":[{"label":"들어간다","effects":{"E":1,"P":1}},{"label":"돌아간다","effects":{"I":1,"J":1}}]},
    {"title": "탈출구",
     "text": "건물 밖으로 나갈 수 있는 길을 발견했다. 어떻게 할까?",
     "options":[{"label":"달려 나간다","effects":{"S":1,"E":1}},{"label":"조용히 나간다","effects":{"N":1,"I":1}}]},
]

# MBTI 계산
def calc_type(scores: Dict[str, int]) -> str:
    mbti = ""
    mbti += "E" if scores.get("E",0) >= scores.get("I",0) else "I"
    mbti += "S" if scores.get("S",0) >= scores.get("N",0) else "N"
    mbti += "T" if scores.get("T",0) >= scores.get("F",0) else "F"
    mbti += "J" if scores.get("J",0) >= scores.get("P",0) else "P"
    return mbti

# 이름 입력
if st.session_state.username == "":
    st.title("🕯️ 괴담에서 살아남기")
    st.text_input("당신의 이름을 입력하세요", key="username")
    st.stop()

# 진행 단계
step = st.session_state.step

# 장면 진행
if step < len(SCENES):
    scene = SCENES[step]
    st.header(f"장면 {step+1}: {scene['title']}")
    st.write(scene['text'])
    st.markdown("<div class='hr'></div>", unsafe_allow_html=True)

    # 선택지 radio
    choice = st.radio("선택지를 골라주세요", [opt["label"] for opt in scene["options"]], key=f"radio_{step}")
    if st.button("✔ 선택 완료"):
        idx = [opt["label"] for opt in scene["options"]].index(choice)
        for k,v in scene["options"][idx]["effects"].items():
            st.session_state.scores[k] += v
        st.session_state.answers.append(idx)
        st.session_state.step += 1
        st.experimental_rerun()

# 결과 화면
else:
    mbti = calc_type(st.session_state.scores)
    result = TYPEBOOK.get(mbti, {})
    st.title(f"🎉 {st.session_state.username}님의 생존 결과")
    st.subheader(f"{result.get('name','')} ({mbti})")
    st.write(result.get("desc",""))
    st.markdown(f"**생존 확률:** {result.get('surv','?')}%")

    st.markdown("<div class='hr'></div>", unsafe_allow_html=True)
    st.subheader("📜 당신의 선택 기록")
    for i, ans_idx in enumerate(st.session_state.answers):
        opt_text = SCENES[i]['options'][ans_idx]['label']
        st.write(f"장면 {i+1}: {opt_text}")

    if st.button("🔄 다시 시작"):
        st.session_state.step = 0
        st.session_state.scores = {k: 0 for k in list("EISNTFJP")}
        st.session_state.answers = []
        st.session_state.username = ""
        st.experimental_rerun()
