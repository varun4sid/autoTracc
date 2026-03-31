import streamlit as st
import pandas as pd
from src.exams import getCATExamSchedule, getSemExamSchedule
from src.logger import logEvent

@st.fragment
def examsTab():
    tabs = st.tabs(["CAT", "Semester"])
    
    with tabs[0]:
        catTab()
        
    with tabs[1]:
        fetch_button = st.button("Click to fetch schedule")
        
        if fetch_button:
            semTab()
        

def catTab():
    cat_schedule = getCATExamSchedule(st.session_state.studzone1_session)
    
    try:
        df_columns = ["COURSE_CODE","DATE","TIME"]
        df = pd.DataFrame(cat_schedule, columns=df_columns)
        st.dataframe(df, hide_index = True)
    except:
        st.warning("CAT schedule not found!")
        
        
def semTab():
    sem_schedule = getSemExamSchedule(st.session_state.studzone2_session)
    
    try:
        df_columns = ["TITLE","DATE","SLOT"]
        df = pd.DataFrame(sem_schedule, columns=df_columns)
        st.dataframe(df, hide_index = True)
        logEvent("/exams/schedule/success")
    except:
        st.warning("Semester exam schedule not found!")
        logEvent("/exams/schedule/failure")