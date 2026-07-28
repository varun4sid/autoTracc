import streamlit as st
from src.feedback import *
from src.logger import logError, logEvent


@st.fragment
def feedbackTab():
    st.write("<h5 style='text-align:center;'>Autofill your feedback forms with just one click!</h5>", unsafe_allow_html=True)
    
    white_space_left, button1, button2, white_space_right = st.columns([2,2,2,2])
    with button1:
        intermediate_form = st.button("Intermediate", disabled = not st.session_state.available_feedback == "Intermediate")
    with button2:
        endsem_form       = st.button("End-Semester", disabled = not st.session_state.available_feedback == "End Semester")
    
    if endsem_form:
        try:
            logEvent("/feedback/endsem")
            autoFeedback(0,st.session_state.rollno,st.session_state.password)
            logEvent("/feedback/endsem/success")
        except Exception as e:
            st.warning("End semester feedback form not found! Try again if autofill interrupted!")
            logEvent("/feedback/endsem/failure")
            logError(str(e))
    
    if intermediate_form:
        try:
            logEvent("/feedback/intermediate")
            autoFeedback(1,st.session_state.rollno,st.session_state.password)
            logEvent("/feedback/intermediate/success")
        except Exception as e:
            print(str(e))
            st.warning("Intermediate feedback form not found! Try again if autofill interrupted!")
            logEvent("/feedback/intermediate/failure")
            logError(str(e))