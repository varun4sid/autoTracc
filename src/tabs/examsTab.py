import streamlit as st
import pandas as pd
from src.exams import getCATExamSchedule, getSemExamSchedule
from src.logger import logError, logEvent
from src.attendance import mapCodeWithName

@st.fragment
def examsTab():
    tabs = st.tabs(["CAT", "Semester"])
    
    with tabs[0]:
        fetch_button_cat = st.button("Fetch CAT schedule", key="cat_schedule_button")
        if fetch_button_cat:
            catTab()
        
    with tabs[1]:
        fetch_button_sem = st.button("Fetch Sem schedule", key="sem_schedule_button")
        if fetch_button_sem:
            semTab()
        

def catTab():
    try:
        cat_schedule = getCATExamSchedule(st.session_state.studzone1_session)
        cat_schedule = mapCodeWithName(cat_schedule, st.session_state.course_map)
    
        df_columns = ["COURSE_CODE","DATE","TIME"]
        df = pd.DataFrame(cat_schedule, columns=df_columns)
        st.dataframe(df, hide_index = True)
        logEvent("/schedule/cat/success")
    except Exception as e:
        logError(e)
        st.error(e)
        
        
def semTab():
    try:
        sem_schedule = getSemExamSchedule(st.session_state.studzone2_session)

        df_columns = ["TITLE","DATE","SLOT"]
        df = pd.DataFrame(sem_schedule, columns=df_columns)
        st.dataframe(df, hide_index = True)
        logEvent("/schedule/sem/success")
    except Exception as e:
        logError(e)
        st.error(e)