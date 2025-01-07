import streamlit as st
from src.pagerequests import *
from src.attendance import *
from src.cgpa import *

st.set_page_config(
    page_title = "autoTracc",
)

if "page" not in st.session_state:
    st.session_state.page = "login_page"

if "credentials" not in st.session_state:
    st.session_state.rollno   = None
    st.session_state.password = None

def loginPage():
    st.markdown(f"<h1 style='text-align: center;'>autoTracc</h1>", unsafe_allow_html=True)

    white_space_left, login_form, white_space_right = st.columns([1,4,1])

    with login_form:
        with st.form(key="login_form"):
            st.session_state.rollno   = st.text_input("RollNo:")
            st.session_state.password = st.text_input("Password:" ,type="password")

            white_space_right, submit_button, white_space_right = st.columns([4,3,3])
            with submit_button:
                submit_button = st.form_submit_button()

            if submit_button:
                if not all( [st.session_state.rollno.strip(), st.session_state.password.strip()] ):
                    st.warning("Please fill all the details!")
                else:
                    attendance_home_page = getHomePageAttendance(st.session_state.rollno,st.session_state.password)
                    if attendance_home_page:
                        st.session_state.page = "dashboard"
                        st.session_state.attendance_session = attendance_home_page

                        courses_home_page = getHomePageCGPA(st.session_state.rollno,st.session_state.password)
                        st.session_state.courses_session = courses_home_page
                        st.rerun()
                    else:
                        st.warning("Invalid Credentials! Try again!")


def dashBoardPage():
    user_name = getUsername(st.session_state.attendance_session)
    st.markdown(f"<h1 style='text-align: center;'>Welcome {user_name}!</h1>", unsafe_allow_html=True)
    st.divider()

    attendance_tab, cgpa_tab = st.tabs(["Attendance","CGPA"])

    attendance_data = getStudentAttendance(st.session_state.attendance_session)

    courses_data, completed_semester = getStudentCourses(st.session_state.courses_session)
    cgpa_data = getCGPA(courses_data, completed_semester)

    with attendance_tab:
        st.dataframe(getAffordableLeaves(attendance_data))
        st.write("NOTE : '-' next to number denotes number of classes that must be attended to meet the respective percentage\n")
            
    with cgpa_tab:
        st.dataframe(cgpa_data)
        st.write("NOTE : '-' denotes existing backlogs in the corresponding semester!\n")
    


if st.session_state.page == "login_page":
    loginPage()

if st.session_state.page == "dashboard":
    dashBoardPage()