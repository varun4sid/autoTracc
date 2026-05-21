import streamlit as st
import pandas as pd

from src.attendance import getStudentAttendance, getCourseNames, mapCodeWithName
from src.cgpa import *
from src.logger import userLogger
from src.pagerequests import *

def processingPage():
    userLogger()
    with st.spinner("Fetching user data..."):
        #Compute the necessary details and store in session state
        try:
            st.session_state.greeting = greetUser(st.session_state.studzone1_session)
        except Exception as e:
            try:
                logError(str(e))
                st.session_state.greeting = fallbackGreeting(st.session_state.studzone1_session)
            except Exception as fallback_error:
                logError(str(fallback_error))
                st.session_state.greeting = {"message": "Welcome!", "balloons": False}
        
        try:
            processAttendance()
        except Exception as e:
            raise e
        
        st.session_state.page = "dashboard"
        st.rerun()
    

def processAttendance():
    try:
        st.session_state.course_map = getCourseNames(st.session_state.studzone1_session)
        attendance_data = getStudentAttendance(st.session_state.studzone1_session)
        attendance_data = mapCodeWithName(attendance_data, st.session_state.course_map)
        st.session_state.attendance_data = attendance_data
    except Exception as e:
        if st.secrets["LOG_ERROR"]:
            logError(str(e))
        st.session_state.attendance_error = str(e)
        raise e
    
    df_columns = ["COURSE_CODE","TOTAL","EXEMPT_HOURS","ABSENT","PRESENT","% PHYSICAL","'%' EXEMPTION","% MEDICAL", "START", "END"]
    st.session_state.attendance_percentage = pd.DataFrame(attendance_data, columns=df_columns)
    st.session_state.updated_date = st.session_state.attendance_data[1][9]


def processCGPA():
    try:
        studzone2_home_page = getStudzoneLegacy(st.session_state.rollno,st.session_state.password)
        st.session_state.studzone2_session = studzone2_home_page
        completed_courses, st.session_state.current_courses = getStudentCourses(studzone2_home_page)
        completed_semester = getCompletedSemester(studzone2_home_page)
    except Exception as e:
        if st.secrets["LOG_ERROR"]:
            logError(str(e))
        raise e
    finally:
        st.session_state.is_cgpa_processed = True
    
    st.session_state.cgpa_data = getCGPA(completed_courses, completed_semester)
    completed_courses_list = pd.DataFrame(completed_courses[1:],columns=completed_courses[0])
    columns_order = ["S.No","COURSE CODE","COURSE TITLE","CREDITS","GRADE"]
    st.session_state.completed_courses_list = completed_courses_list[columns_order]
    st.session_state.cgpa_error = None
    