import streamlit as st
from src.attendance import getAffordableLeaves


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

    #Update the tables after slider event
    st.session_state.attendance_table = getAffordableLeaves(st.session_state.attendance_data, st.session_state.attendance_slider, 0)
    st.session_state.exemption_table = getAffordableLeaves(st.session_state.attendance_data, st.session_state.attendance_slider, 1)
    st.session_state.medical_table = getAffordableLeaves(st.session_state.attendance_data, st.session_state.attendance_slider, 2)

    #Display the tables after latest update
    
    tabs = st.tabs(["Physical", "Exemption", "Medical"])
    with tabs[0]:
        st.dataframe(st.session_state.attendance_table, hide_index = True)
    with tabs[1]:
        st.dataframe(st.session_state.exemption_table, hide_index = True)
    with tabs[2]:
        st.dataframe(st.session_state.medical_table, hide_index = True)
    
    st.markdown(f"<h5 style='color:rgb(255, 75, 75);'>LAST UPDATED : {st.session_state.updated_date}<br><br></h5>", unsafe_allow_html=True)

    #Display notes for the user
    st.warning("""NOTE : '-' next to number of leaves denotes classes must be attended
                to meet the corresponding percentage without skipping classes""")