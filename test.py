# app.py
# ---------------------------------------------
# "괴담에서 살아남기" — 5분 발표용 스트림릿 웹앱
# - 스토리 껍데기를 씌운 퀴즈형 진행 (3~4개 상황)
# - 선택지에 따라 성향 점수 누적 → 16유형 결과
# - 각 유형별 생존 확률/이름/설명 표시 (MBTI 명시는 UI에서 안 함)
# - 발표 친화: 단계별 UI, 진행도 표시, 결과 공유 버튼, 리셋 버튼
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

# 다크 무드 CSS (가벼운 커스텀)
DARK_CSS = """
<style>
:root {
  --bg: #0b0c10;
  --card: #101218;
  --text: #e6e6e6;
  --muted: #a3a3a3;
  --accent: #ff334e;   /* 포인트 컬러 */
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
    st.session_state.step = 0  # 0=intro, 1..N=질문, N+1=결과
if "scores" not in st.session_state:
    st.session_state.scores = {k: 0 for k in list("EISNTFJP")}
if "answers" not in st.session_state:
    st.session_state.answers: List[int] = []
if "username" not in st.session_state:
    st.session_state.username = ""

# --------------- 유형 정의 (16가지) ---------------
# 내부 키는 편의상 E/I, S/N, T/F, J/P 조합을 사용하되, UI에는 노출하지 않음
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
# 각 옵션은 특정 성향 점수에 +1 (또는 복수 키)에 반영되도록 설계
SCENES = [
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
        ],
    },
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
        ],
    },
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
        ],
    },
    {
        "title": "옥상 출구",
        "text": (
            "옥상 문이 열려 있다. 안쪽에서는 바람 소리와 함께 낮은 훌쩍임이 들린다.\n"
            "하늘에는 번개가 멀리서 번쩍인다."
        ),
        "options": [
            {"label": "들어가기 전, 즉석으로 간단한 탈출 계획을 짠다.", "effects": {"J": 1, "T": 1, "I": 1}},
            {"label": "소리를 향해 천천히 다가가 말을 건넨다.", "effects": {"E": 1, "F": 1, "N": 1}},
            {"label": "문을 닫고 계단 쪽으로 빠르게 철수한다.", "effects": {"S": 1, "P": 1, "I": 1}},
        ],
    },
]

TOTAL_STEPS = len(SCENES)

# --------------- 유틸 함수 ---------------
def add_effects(effects: Dict[str, int]):
    for k, v in effects.items():
        st.session_state.scores[k] += v


def compute_type(scores: Dict[str, int]) -> str:
    # 각 축에서 높은 쪽을 선택, 동점이면 안정 애향(ESFJ 기준)으로 편향 없이 랜덤
    pairs = [("E", "I"), ("S", "N"), ("T", "F"), ("J", "P")]
    letters = []
    for a, b in pairs:
        if scores[a] > scores[b]:
            letters.append(a)
        elif scores[b] > scores[a]:
            letters.append(b)
        else:
            letters.append(random.choice([a, b]))
    return "".join(letters)


def reset_all():
    st.session_state.step = 0
    st.session_state.scores = {k: 0 for k in list("EISNTFJP")}
    st.session_state.answers = []
    st.session_state.username = ""


# --------------- 헤더 ---------------
st.markdown("""
# 🕯️ 괴담에서 살아남기

<div class="small">선택으로 드러나는 당신의 생존 성향 — 3~4개의 상황을 지나 최종 결과를 확인하세요.</div>
""", unsafe_allow_html=True)

# 진행도 바
if st.session_state.step > 0 and st.session_state.step <= TOTAL_STEPS:
    st.progress(st.session_state.step / TOTAL_STEPS, text=f"진행 {st.session_state.step}/{TOTAL_STEPS}")

# --------------- 화면 분기 ---------------
if st.session_state.step == 0:
    with st.container():
        st.markdown('<div class="card">', unsafe_allow_html=True)
        st.subheader("시작하기 전에")
        st.session_state.username = st.text_input("닉네임(선택)", placeholder="예: 어둠을걷는학생")
        st.markdown("<div class='hr'></div>", unsafe_allow_html=True)
        st.markdown(
            """
            <div class="rule">
            - 너무 자극적인 묘사는 없습니다. 가볍게 오싹한 톤으로 즐겨요.<br/>
            - 각 상황에서 본능적으로 떠오르는 선택을 골라보세요.<br/>
            - 마지막 화면에서 **당신의 생존 유형**과 **생존 확률**이 공개됩니다.
            </div>
            """,
            unsafe_allow_html=True,
        )
        start = st.button("시작하기 ▶", type="primary")
        st.markdown('</div>', unsafe_allow_html=True)
        if start:
            st.session_state.step = 1
            st.rerun()

elif 1 <= st.session_state.step <= TOTAL_STEPS:
    idx = st.session_state.step - 1
    scene = SCENES[idx]

    st.subheader(f"장면 {st.session_state.step}. {scene['title']}")
    st.write(scene["text"])

    # 선택 라디오
    labels = [opt["label"] for opt in scene["options"]]
    choice = st.radio("당신의 선택은?", labels, index=None, label_visibility="visible")

    cols = st.columns([1,1])
    with cols[0]:
        back = st.button("◀ 이전", disabled=(st.session_state.step == 1))
    with cols[1]:
        next_clicked = st.button("다음 ▶", type="primary")

    if back:
        # 이전 질문으로 돌아갈 때 점수 롤백
        if st.session_state.answers:
            # 마지막 답변의 효과를 취소
            last_idx = st.session_state.step - 2  # 이전 씬 인덱스
            if 0 <= last_idx < len(SCENES):
                # 이전에 고른 라벨을 찾고 해당 효과를 반대로 적용
                chosen_label = st.session_state.answers.pop()
                for opt in SCENES[last_idx]["options"]:
                    if opt["label"] == chosen_label:
                        for k, v in opt["effects"].items():
                            st.session_state.scores[k] -= v
                        break
        st.session_state.step -= 1
        st.rerun()

    if next_clicked:
        if choice is None:
            st.warning("선택지를 골라주세요!")
        else:
            # 점수 반영
            for opt in scene["options"]:
                if opt["label"] == choice:
                    add_effects(opt["effects"])
                    st.session_state.answers.append(choice)
                    break
            # 다음 단계로
            st.session_state.step += 1
            st.rerun()

else:
    # 결과 페이지
    code = compute_type(st.session_state.scores)
    info = TYPEBOOK[code]

    st.subheader("최종 결과")
    user = st.session_state.username or "탐험가"
    st.markdown(
        f"""
        <div class="card">
        <div class="tag">선택 {TOTAL_STEPS}개 완료</div>
        <h3>🧩 {user}님의 생존 유형: <span style='color: var(--accent);'>{info['name']}</span></h3>
        <p class="small">{info['desc']}</p>
        </div>
        """,
        unsafe_allow_html=True,
    )

    st.write("")

    # 생존 확률 표시
    prob = int(info["surv"])  # 0~100
    st.write("**생존 확률**")
    st.progress(prob/100, text=f"{prob}%")

    # 요약 카드: 선택 로그(옵션 라벨만)
    with st.expander("내가 했던 선택 확인하기"):
        for i, label in enumerate(st.session_state.answers, start=1):
            st.markdown(f"**장면 {i}.** {label}")

    # 리셋/공유
    cols = st.columns([1,1])
    with cols[0]:
        if st.button("다시 해보기 🔁"):
            reset_all()
            st.rerun()
    with cols[1]:
        st.download_button(
            label="결과 저장하기 ⤓",
            file_name="my_result.txt",
            mime="text/plain",
            data=(
                f"[괴담에서 살아남기]\n"
                f"닉네임: {user}\n"
                f"생존 유형: {info['name']} ({code})\n"
                f"생존 확률: {prob}%\n"
                f"설명: {info['desc']}\n"
                f"선택 요약: {' | '.join(st.session_state.answers)}\n"
            ),
        )

    st.markdown("<div class='hr'></div>", unsafe_allow_html=True)
    st.caption("※ 본 테스트는 오락용으로 제작되었습니다. 너무 무섭지 않게 즐겨요 :)")
