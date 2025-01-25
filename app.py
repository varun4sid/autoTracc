import streamlit as st
from src.stfunctions import *

st.set_page_config(
    page_title = "autoTracc",
)

if "init" not in st.session_state:
    st.session_state.init = 0
    initializeSessionState()


#Remove anchor from h1 titles
st.markdown("""
            <style>
                [data-testid='stHeaderActionElements'] {display: none;}
                html {text-align: center;}
            </style>""",unsafe_allow_html=True)
    
#Call the corresponding function according to session_state
if st.session_state.page == "login_page":
    loginPage()

if st.session_state.page == "dashboard":
    dashBoardPage()