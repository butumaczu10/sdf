# app.py
# ---------------------------------------------
# "괴담에서 살아남기" — 5분 발표용 스트림릿 웹앱 (8장면, 선택지 4개)
# ---------------------------------------------

import random
from typing import Dict, List
import streamlit as st

# --------------- 기본 세팅 ---------------
st.set_page_config(
    page_title="괴담에서 살아남기",
    page_icon="🕯️",
    layout="centered",
    initial_sidebar_state="collapsed",
)

# 다크 무드 CSS
DARK_CSS = """
<style>
:root {
  --bg: #0b0c10;
  --card: #101218;
  --text: #e6e6e6;
  --muted: #a3a3a3;
  --accent: #ff334e;
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
.btn { border-radius: 999px; padding: 10px 16px; font-weight: 700; }
.hr { height: 1px; background: rgba(255,255,255,0.08); margin: 8px 0 16px; }
.rule { font-size: 0.95rem; line-height: 1.6; }
.option { padding: 10px 12px; border-radius: 12px; border: 1px solid rgba(255,255,255,0.1); }
.note { font-size: 0.9rem; color: var(--muted); }
.tag { display: inline-block; border: 1px solid rgba(255,255,255,0.16); border-radius: 999px; padding: 2px 10px; font-size: 0.85rem; color: var(--muted); margin-right: 6px; }
</style>
"""
st.markdown(DARK_CSS, unsafe_allow_html=True)

# --------------- 세션 상태 초기화 ---------------
if "step" not in st.session_state:
    st.session_state.step = 0
if "scores" not in st.session_state:
    st.session_state.scores = {k: 0 for k in list("EISNTFJP")}
if "answers" not in st.session_state:
    st.session_state.answers: List[int] = []
if "username" not in st.session_state:
    st.session_state.username = ""

# --------------- 유형 정의 ---------------
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

# --------------- 스토리 상황 정의 ---------------
SCENES = [
    # 장면 1
    {
        "title": "교실의 발자국",
        "text": (
            "불 꺼진 교실. 창문은 닫혀 있고, 바닥에 젖은 발자국이 하나둘 이어진다.\n"
            "멀리서 규칙적인 발소리가 가까워진다."
        ),
        "options": [
            {"label": "불을 켜고 주변을 빠르게 탐색한다.", "effects": {"S": 1, "J": 1, "E": 1}},
            {"label": "책상 아래로 숨어 소리를 가늠한다.", "effects": {"I": 1, "S": 1, "T": 1}},
            {"label": "발자국을 따라 조심스레 이동한다.", "effects": {"N": 1, "P": 1, "F": 1}},
            {"label": "창문 밖으로 탈출구를 찾는다.", "effects": {"S": 1, "P": 1, "E": 1}},
        ],
    },
    # 장면 2
    {
        "title": "복도의 그림자",
        "text": (
            "긴 복도 끝, 형체를 알 수 없는 그림자가 서 있다.\n"
            "휴대폰이 미약하게 진동한다."
        ),
        "options": [
            {"label": "그림자에게 말을 걸어 반응을 본다.", "effects": {"E": 1, "N": 1, "F": 1}},
            {"label": "근처 소화기를 들어 대비한다.", "effects": {"S": 1, "T": 1, "J": 1}},
            {"label": "조용히 계단 쪽으로 우회 이동한다.", "effects": {"I": 1, "S": 1, "P": 1}},
            {"label": "그림자를 피해 벽을 따라 달린다.", "effects": {"E": 1, "S": 1, "P": 1}},
        ],
    },
    # 장면 3
    {
        "title": "울리는 전화",
        "text": (
            "잠겨 있는 준비실에서 전화벨이 울린다.\n"
            "문틈 사이로 서늘한 바람이 새어 나온다."
        ),
        "options": [
            {"label": "전화를 받으며 동시에 녹음을 시작한다.", "effects": {"E": 1, "T": 1, "J": 1}},
            {"label": "받지 않고, 소리를 기록하며 발신지를 추적한다.", "effects": {"I": 1, "N": 1, "T": 1}},
            {"label": "무시하고 다른 출구를 먼저 찾는다.", "effects": {"S": 1, "P": 1, "F": 1}},
            {"label": "전화기를 던져 소리를 끊는다.", "effects": {"S": 1, "J": 1, "E": 1}},
        ],
    },
    # 장면 4
    {
        "title": "옥상 출구",
        "text": (
            "옥상 문이 열려 있다. 안쪽에서는 바람 소리와 함께 낮은 훌쩍임이 들린다.\n"
            "하늘에는 번개가 멀리서 번쩍인다."
        ),
        "options": [
            {"label": "들어가기 전, 즉석으로 도구를 준비한다.", "effects": {"J": 1, "T": 1, "S": 1}},
            {"label": "조용히 옥상 끝으로 이동한다.", "effects": {"I": 1, "P": 1, "S": 1}},
            {"label": "용기를 내어 번쩍임 쪽으로 뛰어간다.", "effects": {"E": 1, "S": 1, "F": 1}},
            {"label": "바람을 이용해 그림자와 거리를 둔다.", "effects": {"N": 1, "P": 1, "T": 1}},
        ],
    },
    # 장면 5
    {
        "title": "비밀 통로 발견",
        "text": "교실 뒤쪽 벽이 살짝 움직이며 비밀 통로가 드러난다. 어둡고 좁다.",
        "options": [
            {"label": "조심스럽게 안으로 들어간다.", "effects": {"I": 1, "S": 1, "P": 1}},
            {"label": "벽을 두드려 위험 여부를 확인한다.", "effects": {"E": 1, "T": 1, "J": 1}},
            {"label": "통로를 외면하고 다른 길을 찾는다.", "effects": {"S": 1, "F": 1, "P": 1}},
            {"label": "즉시 기록하고 나중에 돌아올 계획을 세운다.", "effects": {"N": 1, "J": 1, "T": 1}},
        ],
    },
    # 장면 6
    {
        "title": "계단 난간의 균열",
        "text": "오래된 계단 난간에 금이 가 있다. 아래로 떨어질 위험이 크다.",
        "options": [
            {"label": "천천히 손으로 난간을 짚으며 내려간다.", "effects": {"S": 1, "J": 1, "I": 1}},
            {"label": "한 번에 뛰어 내려 빠르게 이동한다.", "effects": {"E": 1, "P": 1, "F": 1}},
            {"label": "난간을 피하고 벽을 따라 우회한다.", "effects": {"N": 1, "S": 1, "T": 1}},
            {"label": "사진과 기록을 남기며 관찰한다.", "effects": {"I": 1, "N": 1, "T": 1}},
        ],
    },
    # 장면 7
    {
        "title": "창고 안의 그림자",
        "text": "낡은 창고 안, 짐더미 사이에서 이상한 움직임이 느껴진다.",
        "options": [
            {"label": "손전등으로 비추며 직접 확인한다.", "effects": {"E": 1, "S": 1, "T": 1}},
            {"label": "소리로 반응을 유도해 위치를 파악한다.", "effects": {"N": 1, "F": 1, "P": 1}},
            {"label": "은밀하게 통로를 돌아 나간다.", "effects": {"I": 1, "S": 1, "P": 1}},
            {"label": "짐더미를 조사하며 흔적을 기록한다.", "effects": {"T": 1, "J": 1, "N": 1}},
        ],
    },
    # 장면 8
    {
        "title": "마지막 탈출",
        "text": "문이 잠겨 있다. 뒤에서 발소리가 점점 가까워진다.",
        "options": [
            {"label": "힘으로 문을 열고 도망친다.", "effects": {"E": 1, "S": 1, "P": 1}},
            {"label": "문 근처에 함정을 설치한다.", "effects": {"T": 1, "J": 1, "N": 1}},
            {"label": "문 틈으로 시야를 살피며 기회를 기다린다.", "effects": {"I": 1, "S": 1, "F": 1}},
            {"label": "뒤를 돌아 상황을 분석하고 최적 경로를 찾는다.", "effects": {"N": 1, "T": 1, "J": 1}},
        ],
    },
]

# --------------- 함수 정의 ---------------
def calc_type(scores: Dict[str, int]) -> str:
    """점수에서 MBTI 유형 결정"""
    mbti = ""
    mbti += "E" if scores.get("E", 0) >= scores.get("I", 0) else "I"
    mbti += "S" if scores.get("S", 0) >= scores.get("N", 0) else "N"
    mbti += "T" if scores.get("T", 0) >= scores.get("F", 0) else "F"
    mbti += "J" if scores.get("J", 0) >= scores.get("P", 0) else "P"
    return mbti

# --------------- UI ---------------

# 사용자 이름 입력
if st.session_state.username == "":
    st.title("🕯️ 괴담에서 살아남기")
    st.text_input("당신의 이름을 입력하세요", key="username")
    st.stop()

# 진행 단계
step = st.session_state.step

# 마지막 단계 전
if step < len(SCENES):
    scene = SCENES[step]
    st.header(f"장면 {step+1}: {scene['title']}")
    st.write(scene['text'])
    st.markdown("<div class='hr'></div>", unsafe_allow_html=True)

    # 선택지 버튼
    for idx, opt in enumerate(scene['options']):
        if st.button(opt['label'], key=f"{step}_{idx}"):
            # 점수 반영
            for k, v in opt['effects'].items():
                st.session_state.scores[k] += v
            st.session_state.answers.append(idx)
            st.session_state.step += 1
            st.experimental_rerun()

# 마지막 단계 도달
else:
    mbti = calc_type(st.session_state.scores)
    result = TYPEBOOK.get(mbti, {})
    st.title(f"🎉 {st.session_state.username}님의 생존 결과")
    st.subheader(f"{result.get('name', '')} ({mbti})")
    st.write(result.get("desc", ""))
    st.markdown(f"**생존 확률:** {result.get('surv', '?')}%")

    st.markdown("<div class='hr'></div>", unsafe_allow_html=True)
    st.subheader("📜 당신의 선택 기록")
    for i, ans_idx in enumerate(st.session_state.answers):
        opt_text = SCENES[i]['options'][ans_idx]['label']
        st.write(f"장면 {i+1}: {opt_text}")

    # 초기화 버튼
    if st.button("🔄 다시 시작"):
        for key in ["step", "scores", "answers", "username"]:
            st.session_state[key] = 0 if key == "step" else {} if key == "scores" else [] if key == "answers" else ""
        st.experimental_rerun()
