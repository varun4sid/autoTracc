import streamlit as st

from src.pagerequests import *
from src.attendance import *
from src.cgpa import *
from src.exams import *

def initializeSessionState():
    if "page" not in st.session_state:
        st.session_state.page = "login_page"

    if "credentials" not in st.session_state:
        st.session_state.rollno   = ""
        st.session_state.password = ""

    if "custom_percentage" not in st.session_state:
        st.session_state.custom_percentage = 75

    if "attendance_result" not in st.session_state:
        st.session_state.attendance_table = []

    if "attendance_session" not in st.session_state:
        st.session_state.attendance_session = []

    if "attendance_data" not in st.session_state:
        st.session_state.attendance_data = []

    if "courses_session" not in st.session_state:
        st.session_state.courses_session = []


def displayLoginNote():
    st.markdown(
    """
        <div>
            <link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Material+Symbols+Outlined:opsz,wght,FILL,GRAD@24,400,0,0&icon_names=encrypted"/>
            <p style = 'text-align:center;opacity:0.7;'>
                    <span style='display:inline-block;margin:4px 0 0 0;'class="material-symbols-outlined">encrypted</span>
                    <span style='display:inline-block;margin:0px 0px 0px 0px;'>Your credentials and data are not stored!<span>
            </p>
        </div>
    """,
    unsafe_allow_html=True)
    

def loginPage():
    st.markdown("<h1 style = ' text-align : center; '>autoTracc</h1>", unsafe_allow_html=True)
    st.markdown("<p style = 'text-align:center;opacity:0.7'>Enter your studzone details</p>", unsafe_allow_html=True)

    #Use st.columns() to align the contents
    white_space_left, login_form, white_space_right = st.columns([1,4,1]) #List represents ratio of column widths

    #Use the middle column to center-justify our form
    with login_form:

        #Create a form
        with st.form(key="login_form"):

            #Get user input
            st.session_state.rollno   = st.text_input("RollNo:")
            st.session_state.password = st.text_input("Password:" ,type="password")

            #Center justify submit button
            white_space_right, submit_button, white_space_right = st.columns([4,3,3])
            with submit_button:
                submit_button = st.form_submit_button()

            #Following code is executed when button is clicked
            if submit_button:

                #Check if all details are entered
                if not all( [st.session_state.rollno.strip(), st.session_state.password.strip()] ):
                    st.warning("Please fill all the details!")
                
                else:
                    #Check if credentials are correct by requesting user data from studzone website
                    attendance_home_page = getHomePageAttendance(st.session_state.rollno,st.session_state.password)

                    #If credentials are correct we get the homepage
                    if attendance_home_page:

                        #Change session state and store the session
                        st.session_state.page = "dashboard"
                        st.session_state.attendance_session = attendance_home_page

                        courses_home_page = getHomePageCGPA(st.session_state.rollno,st.session_state.password)
                        st.session_state.courses_session = courses_home_page

                        #Rerun the script with updated session state to go to the next page
                        st.rerun()
                    
                    #If credentials incorrect then warn the user without leaving login page
                    else:
                        st.warning("Invalid Credentials! Try again!")

    #Display the disclaimer
    displayLoginNote()
    

def updateTable():
    #Update the session state variables when called after required event
    st.session_state.attendance_table = getAffordableLeaves(st.session_state.attendance_data,st.session_state.custom_percentage)

def dashBoardPage():
    #Greet the user
    user_name = getUsername(st.session_state.attendance_session)
    st.markdown(f"<h1 style='text-align: center;'>Welcome {user_name}!</h1>", unsafe_allow_html=True)
    st.divider()

    white_space_left, tabs, white_space_right = st.columns([1,60,1])
    with tabs:

        #Separate attendance and CGPA details using tabs
        attendance_tab, cgpa_tab, exams_tab = st.tabs(["Attendance","CGPA","Exams"])

        #Compute the necessary details and store in session state
        st.session_state.attendance_data = getStudentAttendance(st.session_state.attendance_session)
        
        #Get the date when attendance when recently updated
        try:
            updated_date = st.session_state.attendance_data[1][9]
            attendance_available = True
        except:
            attendance_available = False

        #Get the cgpa data and handle exceptions 
        try:
            courses_data, completed_semester = getStudentCourses(st.session_state.courses_session)
            cgpa_data = getCGPA(courses_data, completed_semester)
            cgpa_available = True
        except:
            cgpa_available = False

        schedule_data = getExamSchedule(st.session_state.attendance_session)

        #Display attendance details
        with attendance_tab:
            if attendance_available:
                #Create a slider
                st.session_state.custom_percentage = st.slider(
                    label = "Percentage you would like to maintain:",
                    min_value = 50,
                    max_value = 99,
                    value = 75,
                    on_change=updateTable()
                )

                #Update the table after slider event
                updateTable()

                #Display the table after latest update
                white_space_left, table, white_space_right = st.columns([1,2,1])
                with table:
                    st.dataframe(st.session_state.attendance_table, hide_index = True)
                    st.markdown(f"<h5 style='color:rgb(255, 75, 75);'>LAST UPDATED : {updated_date}<br><br></h5>", unsafe_allow_html=True)

                #Display notes for the user
                st.write("NOTE : '-' next to number denotes number of classes that must be attended to meet the respective percentage\n")
            
            else:
                st.warning("""
                    Attendance data unavailable at the moment. Try :
                    > Reloading the page and login again.\n
                    > Check whether attendance is "On Process..."
                """)

        #Display tab for CGPA details
        with cgpa_tab:
            if cgpa_available:
                white_space_left, table, white_space_right = st.columns([1,2,1])
                
                #Display the table
                with table:
                    st.dataframe(cgpa_data, hide_index = True)

                st.write("NOTE : '-' denotes existing backlogs in the corresponding semester!\n")
            else:
                st.warning("""
                    Courses data unavailable at the moment. This is likely to be a server issue.
                    Try again after some time.
                """)

        #Display tab for Exam schedule
        with exams_tab:
            try:
                white_space_left, table, white_space_right = st.columns([1,4,1])
                
                #Display the table
                with table:
                    st.dataframe(schedule_data, hide_index = True)

            except:
                st.warning("Exam schedule not found!")
    
    st.divider()

    #Add a logout button
    white_space_right, logout, star, white_space_right = st.columns([5,2,2,5])
    with logout:
        logout_button = st.button("Logout")

    #Link to github page
    with star:
        star_button = st.link_button("Star :star:","https://github.com/varun4sid/autoTracc")
    
    #On clicking logout button session state is reset to login page and script is rerun
    if logout_button:
        st.session_state.page = "login_page"
        st.rerun()