import streamlit as st
from src.pagerequests import getStudzoneModern


def loginPage():
    st.markdown("""<div>
            <h1 style = 'text-align:center;'>autoTracc</h1>
            <p style = 'opacity:0.7; text-align:center;'>Enter your studzone details</p>
            </div>""", unsafe_allow_html=True)
    
    form_widget = st.form(key="login_form", width=375)
    with form_widget:

        st.session_state.rollno   = st.text_input("RollNo:")
        st.session_state.password = st.text_input("Password:" ,type="password")

        submit_button = st.form_submit_button()

        if submit_button:
            #Check if all details are entered
            if not all( [st.session_state.rollno.strip(), st.session_state.password.strip()] ):
                st.warning("Please fill all the details!")
            
            else:
                form_widget.empty()
                st.session_state.rollno = st.session_state.rollno.strip().upper()

                try:
                    st.session_state.studzone1_session = getStudzoneModern(st.session_state.rollno,st.session_state.password)
                    st.session_state.page = "processing"
                    st.rerun()
                except Exception as e:
                    st.error(str(e))
                    return

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
    query_params = st.query_params
    show_demo  = query_params.get("demo") == "true"
    
    if show_demo:
        demo_button = st.button("Demo")
        
        if demo_button:
            st.session_state.rollno = st.secrets["DEMO_ROLL"].upper()
            st.session_state.password = st.secrets["DEMO_PASSWORD"]
            st.session_state.studzone1_session = getStudzoneModern(st.session_state.rollno,st.session_state.password)
            st.session_state.page = "processing"
            st.rerun()
        
        
def initializeSessionState():
    defaults = {
        "rollno": "",
        "password": "",
        "greeting": "",
        "attendance_slider": 75,
        "attendance_table": "",
        "exemption_table": "",
        "medical_table": "",
        "studzone1_session": None,
        "studzone2_session": None,
        "attendance_data": "",
        "attendance_available": False,
        "cgpa_data":"",
        "current_courses": None,
        "completed_courses_list":None,
        "custom_internals": 29,
        "custom_target": 50,
        "internals_data": None,
        "target_slider": "",
        "internals_table": None,
        "course_map": None,
        "is_cgpa_processed": False,
        "marksheet_value": False,
        "attendance_toggle": False,
        "attendance_percentage": "",
        "cgpa_error": None,
        "attendance_error": None
    }

    for key, value in defaults.items():
        if key not in st.session_state:
            st.session_state[key] = value