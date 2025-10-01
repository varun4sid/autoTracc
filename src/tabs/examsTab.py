import streamlit as st
from src.exams import getExamSchedule 


def examsTab():
    schedule_data = getExamSchedule(st.session_state.studzone1_session)
    try:
        st.dataframe(schedule_data, hide_index = True)
    except:
        st.warning("Exam schedule not found!")