# ------------------------- 추가 상황 예시 -------------------------
SCENES += [
    {
        "title": "지하실의 속삭임",
        "text": (
            "지하실 문틈에서 낮은 속삭임이 들린다.\n"
            "전등이 깜빡이고 있다."
        ),
        "options": [
            {"label": "조심스럽게 내려가 목소리의 출처를 찾는다.", "effects": {"N": 1, "F": 1, "I": 1}},
            {"label": "겁먹고 문을 닫고 돌아간다.", "effects": {"S": 1, "P": 1, "E": 1}},
            {"label": "기록 장비를 꺼내 소리를 녹음한다.", "effects": {"T": 1, "J": 1, "S": 1}},
        ],
    },
    {
        "title": "화장실의 그림자",
        "text": (
            "화장실 거울에 자신과는 다른 그림자가 비친다.\n"
            "물을 틀자 물이 이상하게 흐른다."
        ),
        "options": [
            {"label": "그림자에게 말을 걸어본다.", "effects": {"F": 1, "E": 1, "N": 1}},
            {"label": "거울을 가리고 화장실을 빠르게 벗어난다.", "effects": {"S": 1, "P": 1, "I": 1}},
            {"label": "상황을 사진으로 기록한다.", "effects": {"T": 1, "J": 1, "S": 1}},
        ],
    },
]
TOTAL_STEPS = len(SCENES)

# ------------------------- 결과창에서 다른 결과 보기 -------------------------
else:
    # 기존 최종 결과 계산
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

    # 생존 확률 표시
    prob = int(info["surv"])
    st.write("**생존 확률**")
    st.progress(prob/100, text=f"{prob}%")

    # 선택 기록
    with st.expander("내가 했던 선택 확인하기"):
        for i, label in enumerate(st.session_state.answers, start=1):
            st.markdown(f"**장면 {i}.** {label}")

    # ----------------- 다른 결과 보기 -----------------
    st.markdown("---")
    st.subheader("💡 다른 유형 결과 보기")
    other_type = st.selectbox(
        "다른 유형을 선택해서 결과 확인:",
        options=list(TYPEBOOK.keys()),
        format_func=lambda x: TYPEBOOK[x]["name"]
    )
    other_info = TYPEBOOK[other_type]
    st.markdown(
        f"""
        <div class="card">
        <h4>유형: <span style='color: var(--accent);'>{other_info['name']}</span></h4>
        <p class="small">{other_info['desc']}</p>
        <p>생존 확률: {other_info['surv']}%</p>
        </div>
        """,
        unsafe_allow_html=True,
    )

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
