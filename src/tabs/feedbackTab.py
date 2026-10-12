import streamlit as st
from src.feedback import *
from src.logger import logError, logEvent

import time


@st.fragment
def feedbackTab():
    st.write("<h5 style='text-align:center;'>Autofill your feedback forms with just one click!</h5>", unsafe_allow_html=True)
    
    white_space_left, button1, button2, white_space_right = st.columns([2,2,2,2])
    with button1:
        intermediate_form = st.button(
            "Intermediate",
            disabled=(
                st.session_state.available_feedback != "Intermediate"
                or st.session_state.is_feedback_processed
            ),
        )
    with button2:
        endsem_form = st.button(
            "End-Semester",
            disabled=(
                st.session_state.available_feedback != "End Semester"
                or st.session_state.is_feedback_processed
            ),
        )
    
    if endsem_form:
        autofill_form("endsem")
    
    if intermediate_form:
        autofill_form("intermediate")
            
            
def autofill_form(mode):
    try:
        logEvent(f"/feedback/{mode}")
        start = time.time()
        wait = st.empty()
        wait.write("Please wait...")
        if mode == "endsem":
            fillform_endsem(st.session_state.studzone1_session)
        elif mode == "intermediate":
            fillform_intermediate(st.session_state.studzone1_session)
        end = time.time()
        duration = end - start
        logEvent(f"/feedback/{mode}/success duration {duration:.2f} seconds")
        wait.empty()
        st.write(f"Time taken: {duration:.2f} seconds")
        st.markdown("##### Done! Check your [studzone](https://ecampus.psgtech.ac.in/studzone)!")
    except Exception as e:
        st.error(str(e))
        logEvent(f"/feedback/{mode}/failure")
        logError(str(e))
    finally:
        st.session_state.is_feedback_processed = True