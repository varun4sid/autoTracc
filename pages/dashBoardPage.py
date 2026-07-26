import streamlit as st
from src.logger import logEvent
from src.tabs import attendanceTab, cgpaTab, feedbackTab, internalsTab, examsTab

from datetime import datetime
import pytz


def dashBoardPage():
    #Greet the user
    st.title(st.session_state.greeting["message"], text_alignment="center")
    if st.session_state.greeting["balloons"]:
        logEvent("/birthday")
        st.balloons()
        st.session_state.greeting["balloons"] = False


    pstyle = "opacity:0.7; font-weight:bold; font-style:italic; text-align:center;"
    if st.session_state.feedback_duration is not None: 
        duration = st.session_state.feedback_duration
        start_date = datetime.strptime(duration["start"], "%d/%b/%y").date()
        if datetime.now(pytz.timezone('Asia/Calcutta')).date() >= start_date:
            st.markdown(f"<p style = '{pstyle}'>{st.session_state.available_feedback} Feedback form is available! Fill it before {duration['end']}!</p>", unsafe_allow_html=True)
    # st.markdown(f"<p style = '{pstyle}'>Latest CGPA data is available :D</p>", unsafe_allow_html=True)
        
    st.divider()

    #Separate the features with tabs
    attendance_tab, cgpa_tab, exams_tab, internals_tab,feedback_tab = st.tabs(["Attendance","CGPA","Exams","Internals","Feedback"])

    with attendance_tab:
        attendanceTab.attendanceTab()

    with cgpa_tab:
        cgpaTab.cgpaTab()
        
    with exams_tab:
        examsTab.examsTab()
            
    with internals_tab:
        internalsTab.internalsTab()

    with feedback_tab:
        feedbackTab.feedbackTab()


def dashBoardFooter():
    st.divider()

    #Add a logout button
    white_space_left, logout, star, white_space_right = st.columns([5,2,2,5])
    with logout:
        logout_button = st.button("Logout")
        
        if logout_button:
            st.session_state.page = "login_page"
            st.session_state.cgpa_available = False
            st.rerun()

    #Link to github page
    with star:
        st.link_button("Star :star:","https://github.com/varun4sid/autoTracc")
        
    st.markdown("""<p style = 'text-align:center;'>Join the <a href="https://github.com/varun4sid/autoTracc/discussions/new/choose">discussions</a>
                to share new feauture ideas and report bugs!</p>""",unsafe_allow_html=True)