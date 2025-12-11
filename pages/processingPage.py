import streamlit as st
import logging
import datetime
import pytz
import pandas as pd

from src.attendance import getStudentAttendance, getCourseNames
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
            st.session_state.course_map = getCourseNames(st.session_state.studzone1_session)
            st.session_state.attendance_data = getStudentAttendance(st.session_state.studzone1_session)
            st.session_state.updated_date = st.session_state.attendance_data[1][9]
            st.session_state.attendance_available = True
        except:
            st.session_state.attendance_available = False
            
        #Get the cgpa data and handle exceptions 
        try:
            courses_home_page = getHomePageCGPA(st.session_state.rollno,st.session_state.password)
            completed_courses, st.session_state.current_courses = getStudentCourses(courses_home_page)
            completed_semester = getCompletedSemester(courses_home_page)
            st.session_state.cgpa_data = getCGPA(completed_courses, completed_semester)
            completed_courses_list = pd.DataFrame(completed_courses[1:],columns=completed_courses[0])
            columns_order = ["S.No","COURSE CODE","COURSE TITLE","CREDITS","GRADE"]
            st.session_state.completed_courses_list = completed_courses_list[columns_order]
            st.session_state.cgpa_available = True
        except:
            st.session_state.cgpa_available = False

        st.session_state.page = "dashboard"
        st.rerun()


def logger():
    logging.basicConfig()
    logtime = datetime.now(pytz.timezone('Asia/Calcutta')).replace(second=0,microsecond=0,tzinfo=None)
    logging.warning(f'{logtime} USER : {str.upper(st.session_state.rollno)}')