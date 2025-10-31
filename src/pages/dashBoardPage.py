import streamlit as st 
from src.tabs import attendanceTab, cgpaTab, feedbackTab, internalsTab, examsTab


def dashBoardPage():
    #Greet the user
    st.title(st.session_state.greeting)
    if st.session_state.balloons:
        st.balloons()
        st.session_state.balloons = False
    
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

    #Link to github page
    with star:
        st.link_button("Star :star:","https://github.com/varun4sid/autoTracc")
    
    #On clicking logout button session state is reset to login page and script is rerun
    if logout_button:
        # Clear cache to free memory before switching to login page
        from src.attendance import clearCourseNamesCache
        clearCourseNamesCache()
        st.session_state.page = "login_page"
        st.rerun()
        
    st.markdown("""<p>Join the <a href="https://github.com/varun4sid/autoTracc/discussions/new/choose">discussions</a>
                to share new feauture ideas and report bugs!</p>""",unsafe_allow_html=True)