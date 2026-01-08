import streamlit as st
from src.feedback import *
from src.logger import logEvent


def feedbackTab():
    st.write("##### Autofill your feedback forms with just one click!")
    
    white_space_left, button1, button2, white_space_right = st.columns([2,2,2,2])
    with button1:
        intermediate_form = st.button("Intermediate")
    with button2:
        endsem_form       = st.button("End-Semester")
    
    if endsem_form:
        try:
            logEvent("/feedback/endsem")
            autoFeedback(0,st.session_state.rollno,st.session_state.password)
            logEvent("/feedback/endsem/success")
        except:
            st.warning("End semester feedback form not found! Try again if autofill interrupted!")
            logEvent("/feedback/endsem/failure")
    
    if intermediate_form:
        try:
            logEvent("/feedback/intermediate")
            autoFeedback(1,st.session_state.rollno,st.session_state.password)
            logEvent("/feedback/intermediate/success")
        except:
            st.warning("Intermediate feedback form not found! Try again if autofill interrupted!")
            logEvent("/feedback/intermediate/failure")