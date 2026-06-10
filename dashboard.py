import streamlit as st

st.set_page_config(page_title="샴푸 대시보드", layout="wide")

st.markdown("""
<style>
[data-baseweb="tag"] { background-color: #888888 !important; }
[data-baseweb="tag"] span { color: #ffffff !important; }
</style>
""", unsafe_allow_html=True)

pg = st.navigation([
    st.Page("pages/대시보드.py",   title="Dashboard",   icon="🧴"),
    st.Page("pages/가이드라인.py", title="Guidelines",  icon="📋"),
])
pg.run()
