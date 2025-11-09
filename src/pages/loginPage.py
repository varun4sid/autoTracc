import streamlit as st
from src.pagerequests import getHomePageAttendance


def loginPage():
    st.title("autoTracc")
    st.markdown("<p style = 'opacity:0.7'>Enter your studzone details</p>", unsafe_allow_html=True)

    form_widget = st.form(key="login_form", width=375)
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
                    st.session_state.studzone1_session = attendance_home_page

                    #Change session state and rerun to go to next page
                    st.session_state.page = "processing"
                    st.rerun()
                    
                #If credentials incorrect then warn the user without leaving login page
                else:
                    st.warning("Invalid Credentials! Try again!")

    #Display the disclaimer
    displayLoginNote()
    displayDemoButton()

   
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
    
    
def displayDemoButton():
    demo_button = st.button("Demo")
        
    if demo_button:
        st.session_state.rollno = st.secrets["DEMO_ROLL"]
        st.session_state.password = st.secrets["DEMO_PASSWORD"]
        st.session_state.studzone1_session = getHomePageAttendance(st.session_state.rollno,st.session_state.password)
        st.session_state.page = "processing"
        st.rerun()
        
        
def initializeSessionState():
    defaults = {
        "rollno": "",
        "password": "",
        "greeting": "",
        "balloons":False,
        "attendance_slider": 75,
        "attendance_table": "",
        "exemption_table": "",
        "medical_table": "",
        "studzone1_session": 0,
        "attendance_data": "",
        "attendance_available": False,
        "cgpa_data":"",
        "courses_list":"",
        "cgpa_available": False,
        "custom_internals": 29,
        "custom_target": 50,
        "internals_data": "",
        "target_slider": "",
        "internals_table": "",
        "course_map": ""
    }

    for key, value in defaults.items():
        if key not in st.session_state:
            st.session_state[key] = value