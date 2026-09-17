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
        try:
            logEvent("/feedback/endsem")
            st.write("In development...")
            logEvent("/feedback/endsem/success")
        except Exception as e:
            st.warning("End semester feedback form not found! Try again if autofill interrupted!")
            logEvent("/feedback/endsem/failure")
            logError(str(e))
        finally:
            st.session_state.is_feedback_processed = True
    
    if intermediate_form:
        try:
            logEvent("/feedback/intermediate")
            start = time.time()
            wait = st.empty()
            wait.write("Please wait...")
            fillform_intermediate(st.session_state.studzone1_session)
            end = time.time()
            logEvent("/feedback/intermediate/success")
            wait.empty()
            st.write(f"Time taken: {end - start:.2f} seconds")
            st.markdown("##### Done! Check your [studzone](https://ecampus.psgtech.ac.in/studzone)!")
        except Exception as e:
            print(str(e))
            st.warning("Intermediate feedback form not found! Try again if autofill interrupted!")
            logEvent("/feedback/intermediate/failure")
            logError(str(e))
        finally:
            st.session_state.is_feedback_processed = True