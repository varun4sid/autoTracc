import streamlit as st
import logging
import datetime
import pytz
import pandas as pd

from src.attendance import getStudentAttendance
from src.cgpa import *
from src.pagerequests import *

def processingPage():
    logger()
    with st.spinner("Fetching user data..."):
        #Compute the necessary details and store in session state
        try:
            st.session_state.greeting = greetUser(st.session_state.studzone1_session)      
        except:
            st.session_state.greeting = fallbackGreeting(st.session_state.studzone1_session)
            
        #Get the date when attendance was recently updated
        try:
            st.session_state.attendance_data = getStudentAttendance(st.session_state.studzone1_session)
            st.session_state.updated_date = st.session_state.attendance_data[1][9]
            st.session_state.attendance_available = True
        except:
            st.session_state.attendance_available = False
            
        #Get the cgpa data and handle exceptions 
        try:
            # Reuse studzone2 session if already created, otherwise create new one
            if "studzone2_session" not in st.session_state:
                st.session_state.studzone2_session = getHomePageCGPA(st.session_state.rollno,st.session_state.password)
            
            courses_home_page = st.session_state.studzone2_session
            courses_data = getStudentCourses(courses_home_page)
            completed_semester = getCompletedSemester(courses_home_page)
            st.session_state.cgpa_data = getCGPA(courses_data, completed_semester)
            course_list = pd.DataFrame(courses_data[1:],columns=courses_data[0])
            columns_order = ["S.No","COURSE CODE","COURSE TITLE","CREDITS","GRADE"]
            st.session_state.courses_list = course_list[columns_order]
            st.session_state.cgpa_available = True
        except:
            st.session_state.cgpa_available = False

        st.session_state.page = "dashboard"
        st.rerun()


def logger():
    logging.basicConfig()
    logtime = datetime.now(pytz.timezone('Asia/Calcutta')).replace(second=0,microsecond=0,tzinfo=None)
    logging.warning(f'{logtime} USER : {str.upper(st.session_state.rollno)}')