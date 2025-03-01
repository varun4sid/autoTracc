import streamlit as st
import csv

from src.pagerequests import *
from src.attendance import *
from src.cgpa import *
from src.exams import *
from src.internals import *
from src.feedback import *

def initializeSessionState():
    if "page" not in st.session_state:
        st.session_state.page = "login_page"

    if "rollno" not in st.session_state:
        st.session_state.rollno   = ""
    
    if "password" not in st.session_state:
        st.session_state.password = ""

    if "attendance_slider" not in st.session_state:
        st.session_state.attendance_slider = 75

    if "attendance_result" not in st.session_state:
        st.session_state.attendance_table = ""

    if "attendance_session" not in st.session_state:
        st.session_state.attendance_session = 0

    if "attendance_data" not in st.session_state:
        st.session_state.attendance_data = ""

    if "courses_session" not in st.session_state:
        st.session_state.courses_session = ""
        
    if "updated_date" not in st.session_state:
        st.session_state.updated_data = ""
        
    if "internals_slider" not in st.session_state:
        st.session_state.internals_slider = 29
        
    if "target_slider" not in st.session_state:
        st.session_state.target_slider = 50


def displayLoginNote():
    st.markdown(
    """
        <div>
            <link rel="stylesheet" 
            href="https://fonts.googleapis.com/css2?family=Material+Symbols+Outlined:opsz,wght,FILL,GRAD@24,400,0,0&icon_names=encrypted"/>
            <p style = 'text-align:center;opacity:0.7;display:flex;align-items:center;justify-content:center;'>
                    <span class="material-symbols-outlined">encrypted</span>
                    <span>Your credentials and data are not stored!</span>
            </p>
        </div>
    """,
    unsafe_allow_html=True)
    

def loginPage():
    st.title("autoTracc")
    st.markdown("<p style = 'opacity:0.7'>Enter your studzone details</p>", unsafe_allow_html=True)

    #Use st.columns() to align the contents
    white_space_left, login_form, white_space_right = st.columns([1,4,1]) #List represents ratio of column widths

    #Use the middle column to center-justify our form
    with login_form:

        #Create a form
        with st.form(key="login_form"):

            #Get user input
            st.session_state.rollno   = st.text_input("RollNo:")
            st.session_state.password = st.text_input("Password:" ,type="password")

            submit_button = st.form_submit_button()

            #Following code is executed when button is clicked
            if submit_button:

                #Check if all details are entered
                if not all( [st.session_state.rollno.strip(), st.session_state.password.strip()] ):
                    st.warning("Please fill all the details!")
                
                else:
                    with st.spinner("Fetching user data..."):
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

        demo_button = st.button("Demo")
        
        if demo_button:
            st.session_state.page = "demo"
            st.rerun()
    

def dashBoardPage():
    #Greet the user
    user_name = getUsername(st.session_state.attendance_session)
    st.title(f"Welcome {user_name}!")
    st.divider()

    #Separate the features with tabs
    attendance_tab, cgpa_tab, exams_tab, internals_tab,feedback_tab = st.tabs(["Attendance","CGPA","Exams","Internals","Feedback"])

    #Compute the necessary details and store in session state
    st.session_state.attendance_data = getStudentAttendance(st.session_state.attendance_session)
    
    #Get the date when attendance was recently updated
    try:
        st.session_state.updated_date = st.session_state.attendance_data[1][9]
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
            attendanceTab()
        else:
            st.warning("""
                Attendance data unavailable at the moment. Try :
                > Reloading the page and login again.\n
                > Check whether attendance is "On Process..."
            """)

    #Display tab for CGPA details
    with cgpa_tab:
        if cgpa_available:
            st.dataframe(cgpa_data, hide_index = True)
            st.warning("NOTE : '-' denotes existing backlogs in the corresponding semester!\n")
        else:
            st.warning("""
                Courses data unavailable at the moment. This is likely to be a server issue.
                Try again after some time.
            """)

    #Display tab for Exam schedule
    with exams_tab:
        try:
            st.dataframe(schedule_data, hide_index = True)
        except:
            st.warning("Exam schedule not found!")
            
    #Display tab for internal marks
    with internals_tab:
        targetScore()
        
    with feedback_tab:
        st.write("Autofill your feedback forms with just one click!")
        intermediate_form = st.button("Intermediate")
        
        if intermediate_form:
            with st.spinner("Filling the form... This takes a few minutes... Do not close the tab"):
                intermediateForm(st.session_state.rollno,st.session_state.password)
            st.write("Done!")
                
    dashBoardFooter()
        
        
def demoPage():
    st.title("Welcome, Demo!")
    st.divider()
    
    attendance_tab, cgpa_tab, exams_tab, internals_tab = st.tabs(["Attendance","CGPA","Exams","Internals"])
    
    with open("./demo/attendance.csv","r") as file:
        csv_reader = csv.reader(file)
        st.session_state.attendance_data = list(csv_reader)
        st.session_state.updated_date = st.session_state.attendance_data[1][9]
        
    with open("./demo/cgpa.csv","r") as file:
        csv_reader = csv.reader(file)
        cgpa_data = list(csv_reader)
        df_headers = ["SEMESTER","GPA","CGPA"]
        cgpa_df = DataFrame(cgpa_data, columns=df_headers)
        
    with open("./demo/exams.csv","r") as file:
        csv_reader = csv.reader(file)
        schedule_data = list(csv_reader)
        df_headers = ["COURSE_CODE","DATE","TIME"]
        schedule_df = DataFrame(schedule_data, columns=df_headers)
        
    with attendance_tab:
        attendanceTab()
            
    with cgpa_tab:
        st.dataframe(cgpa_df, hide_index = True)
        st.warning("NOTE : '-' denotes existing backlogs in the corresponding semester!\n")
        
    with exams_tab:
        st.dataframe(schedule_df, hide_index = True)
        
    with internals_tab:
        targetScore()
        
    dashBoardFooter()
    

def attendanceTab():
    #Create a slider
    st.session_state.attendance_slider = st.slider(
        label = "Percentage you would like to maintain:",
        min_value = 50,
        max_value = 99,
        value = 75,
    )

    #Update the table after slider event
    st.session_state.attendance_table = getAffordableLeaves(st.session_state.attendance_data, st.session_state.attendance_slider)

    #Display the table after latest update
    st.dataframe(st.session_state.attendance_table, hide_index = True)
    st.markdown(f"<h5 style='color:rgb(255, 75, 75);'>LAST UPDATED : {st.session_state.updated_date}<br><br></h5>", unsafe_allow_html=True)

    #Display notes for the user
    st.warning("""NOTE : '-' next to number of leaves denotes classes must be attended
                to meet the corresponding percentage without skipping classes""")


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
        st.session_state.page = "login_page"
        st.rerun()
        
        
def targetScore():
    #st.warning("Automated tracking for your courses coming soon...")
    st.warning("Your internal marks are unavailable at the moment...")
    
    st.session_state.internals_slider = st.slider(
        label = "Internal marks(for 50): ",
        min_value = 0,
        max_value = 50,
        value = 29
    )
    
    st.session_state.target_slider = st.slider(
        label = "Enter your target final marks(for 100): ",
        min_value = 50,
        max_value = 100,
        value = 50
    )
    
    target_score = calculateTarget(st.session_state.internals_slider,st.session_state.target_slider)
    if target_score != '-':
        result_string = "You need to score atleast "
        result_string += str(target_score)
        result_string += " in end-semester exam to get a final score of "
        result_string += str(st.session_state.target_slider)
        st.markdown(f"<h5 style='color:rgb(0, 255, 0);'><br><br>{result_string}<br><br></h5>", unsafe_allow_html=True)
    else:
        result_string = "You can't get a final score of "
        result_string += str(st.session_state.target_slider)
        result_string += " with an internals score of "
        result_string += str(st.session_state.internals_slider)
        st.markdown(f"<h5 style='color:rgb(255, 0, 0);'><br><br>{result_string}<br><br></h5>", unsafe_allow_html=True)