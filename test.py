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
