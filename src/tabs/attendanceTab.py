import streamlit as st
from src.state_manager import get_attendance_table, get_updated_date


def attendanceTab():
    if st.session_state.attendance_available:
        attendanceUI()
    else:
        st.warning("""
            Attendance data unavailable at the moment. Try :
            > Reloading the page and login again.\n
            > Check whether attendance is "On Process..."
        """)


def attendanceUI():
    #Create a slider
    st.session_state.attendance_slider = st.slider(
        label = "Percentage you would like to maintain:",
        min_value = 50,
        max_value = 99,
        value = 75,
    )

    #Get the table using cached computation
    attendance_table = get_attendance_table(st.session_state.attendance_slider)
    
    if attendance_table is not None:
        #Display the table after latest update
        st.dataframe(attendance_table, hide_index = True)
        
        #Get updated date using cached computation
        updated_date = get_updated_date()
        st.markdown(f"<h5 style='color:rgb(255, 75, 75);'>LAST UPDATED : {updated_date}<br><br></h5>", unsafe_allow_html=True)
    else:
        st.error("Unable to display attendance table")

    #Display notes for the user
    st.warning("""NOTE : '-' next to number of leaves denotes classes must be attended
                to meet the corresponding percentage without skipping classes""")