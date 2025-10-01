import streamlit as st
from src.pages import dashBoardPage, loginPage, processingPage

st.set_page_config(
    page_title = "autoTracc",
)

if "page" not in st.session_state:
    st.session_state.page = "login_page"
    loginPage.initializeSessionState()


#Remove anchor from h1 titles
st.markdown("""
            <style>
                [data-testid='stHeaderActionElements'] {display: none;}
                body {text-align: center;}
            </style>""",unsafe_allow_html=True)
    
#Call the corresponding function according to session_state
if st.session_state.page == "login_page":
    loginPage.loginPage()

if st.session_state.page == "processing":
    processingPage.processingPage()

if st.session_state.page == "dashboard":
    dashBoardPage.dashBoardPage()
    dashBoardPage.dashBoardFooter()