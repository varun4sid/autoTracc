import streamlit as st
import pandas as pd
from src.exams import getExamSchedule 


def examsTab():
    schedule_data = getExamSchedule(st.session_state.studzone1_session)
    
    try:
        df_columns = ["COURSE_CODE","DATE","TIME"]
        df = pd.DataFrame(schedule_data, columns=df_columns)
        st.dataframe(df, hide_index = True)
    except:
        st.warning("Exam schedule not found!")