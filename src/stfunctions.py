import streamlit as st
import csv

from .pagerequests import *
from .attendance import *
from .cgpa import *
from .exams import *
from .internals import *

def initializeSessionState():
    defaults = {
        "rollno": "",
        "password": "",
        "greeting": "",
        "balloons":False,
        "attendance_slider": 75,
        "attendance_table": "",
        "attendance_session": 0,
        "attendance_data": "",
        "attendance_available": False,
        "cgpa_available": False,
        "courses_session": "",
        "updated_data": "",
        "custom_internals": 29,
        "custom_target": 50,
        "internals_data": "",
        "target_slider": "",
        "internals_table": "",
    }

    for key, value in defaults.items():
        if key not in st.session_state:
            st.session_state[key] = value


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
    #Use st.columns() to align the contents
    white_space_left, login_form, white_space_right = st.columns([1,4,1]) #List represents ratio of column widths

    #Use the middle column to center-justify our form
    with login_form:
        st.title("autoTracc")
        st.markdown("<p style = 'opacity:0.7'>Enter your studzone details</p>", unsafe_allow_html=True)

        form_widget = st.form(key="login_form")
        #Create a form
        with form_widget:

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
                    form_widget.empty()
                    #Check if credentials are correct by requesting user data from studzone website
                    attendance_home_page = getHomePageAttendance(st.session_state.rollno,st.session_state.password)

                    #If credentials are correct we get the homepage
                    if attendance_home_page:
                        #Store the studzone session
                        st.session_state.attendance_session = attendance_home_page

                        #Change session state and rerun to go to next page
                        st.session_state.page = "processing"
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
    

def processingPage():
    with st.spinner("Fetching user data..."):
        #Compute the necessary details and store in session state
        st.session_state.greeting = greetUser(st.session_state.attendance_session)      
        
        #Get the date when attendance was recently updated
        try:
            st.session_state.attendance_data = getStudentAttendance(st.session_state.attendance_session)
            st.session_state.updated_date = st.session_state.attendance_data[1][9]
            st.session_state.attendance_available = True
        except:
            st.session_state.attendance_available = False
            
        #Get the cgpa data and handle exceptions 
        try:
            courses_home_page = getHomePageCGPA(st.session_state.rollno,st.session_state.password)
            courses_data, completed_semester = getStudentCourses(courses_home_page)
            st.session_state.cgpa_data = getCGPA(courses_data, completed_semester)
            st.session_state.cgpa_available = True
        except:
            st.session_state.cgpa_available = False

        st.session_state.page = "dashboard"
        st.rerun()
        

def dashBoardPage():
    #Greet the user
    st.title(st.session_state.greeting)
    if st.session_state.balloons:
        st.balloons()
        st.session_state.balloons = False
        
    st.divider()

    #Separate the features with tabs
    attendance_tab, cgpa_tab, exams_tab, internals_tab = st.tabs(["Attendance","CGPA","Exams","Internals"])

    #Display attendance details
    with attendance_tab:
        if st.session_state.attendance_available:
            attendanceTab()
        else:
            st.warning("""
                Attendance data unavailable at the moment. Try :
                > Reloading the page and login again.\n
                > Check whether attendance is "On Process..."
            """)

    #Display tab for CGPA details
    with cgpa_tab:
        if st.session_state.cgpa_available:
            st.dataframe(st.session_state.cgpa_data, hide_index = True)
            st.warning("NOTE : '-' denotes existing backlogs in the corresponding semester!\n")
        else:
            st.warning("""
                Courses data unavailable at the moment. This is likely to be a server issue.
                Try again after some time.
            """)

    #Display tab for Exam schedule
    with exams_tab:
        schedule_data = getExamSchedule(st.session_state.attendance_session)
        try:
            st.dataframe(schedule_data, hide_index = True)
        except:
            st.warning("Exam schedule not found!")
            
    #Display tab for internal marks
    with internals_tab:
        table_tab,custom_tab = st.tabs(["CA Marks","Custom"])
        with table_tab:
            try:
                st.session_state.internals_data = getInternals(st.session_state.attendance_session)
                internalsTab()
            except:
                st.warning("Your internal marks are unavailable at the moment")
                
        with custom_tab:
            customScore()
             

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
    
    
def internalsTab():
    st.session_state.target_slider = st.slider(
        label = "Enter your target final marks (for 100): ",
        min_value = 50,
        max_value = 100,
        value = 50
    )
    
    st.write("You need a final score of atleast 50 and a semester exam score of atleast 45 to pass!")
    
    st.session_state.internals_table = getTargetScore(st.session_state.internals_data, st.session_state.target_slider)
    
    renderInternals()
    
    st.warning(""" '-' denotes you can't achieve target with your current internal marks                
                    * beside the internal marks denotes final mark entry is pending
                """)
        
        
def customScore():    
    st.session_state.custom_internals = st.slider(
        label = "Internal marks(for 50): ",
        min_value = 0,
        max_value = 50,
        value = 29
    )
    
    st.session_state.custom_target = st.slider(
        label = "Enter your target final marks (for 100): ",
        min_value = 50,
        max_value = 100,
        value = 50,
        key="custom"
    )
    
    target_score = calculateTarget(st.session_state.custom_internals,st.session_state.custom_target)
    if target_score != '-':
        result_string = "You need to score atleast "
        result_string += str(target_score)
        result_string += " in end-semester exam to get a final score of "
        result_string += str(st.session_state.custom_target)
        st.markdown(f"<h5 style='color:rgb(0, 255, 0);'><br><br>{result_string}<br><br></h5>", unsafe_allow_html=True)
    else:
        result_string = "You can't get a final score of "
        result_string += str(st.session_state.custom_target)
        result_string += " with an internals score of "
        result_string += str(st.session_state.custom_internals)
        st.markdown(f"<h5 style='color:rgb(255, 0, 0);'><br><br>{result_string}<br><br></h5>", unsafe_allow_html=True)
                 
    
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
        
    st.markdown("""<p>Join the <a href="https://github.com/varun4sid/autoTracc/discussions/new/choose">discussions</a>
                to share new feauture ideas and report bugs!</p>""",unsafe_allow_html=True)
        
        
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
        table_tab,custom_tab = st.tabs(["CA Marks","Custom"])
        
        with table_tab:
            st.warning("Your internal marks are unavailable at the moment")
            
        with custom_tab:
            customScore()
            

def renderInternals():
    table_header = f"""
        <table style='margin:auto;'>
            <tr>
                <th rowspan="2">Theory Course</th>
                <th rowspan="2">Internals (/50)</th>
                <th colspan="2">Required Semester Score</th>
            </tr>
            <tr>
                <th>To Pass (50)</th>
                <th>To Target ({st.session_state.target_slider})</th>
            </tr>
    """
    
    table_body = ""
    
    for course in st.session_state.internals_table:
        table_body += f"<tr><td style='text-align:left;'>{course[0]}</td><td style='text-align:right;'>{course[1]}</td>"
        table_body += f"<td>{course[2]}</td><td>{course[3]}</td></tr>"
        
    table_body += "</table><br>"
    
    table = table_header + table_body
    
    st.markdown(table, unsafe_allow_html=True)