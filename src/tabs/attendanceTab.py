import streamlit as st
from src.attendance import getAffordableLeaves
import pandas as pd


def attendanceTab():
    if st.session_state.attendance_available:
        attendanceUI()
    else:
        st.warning("""
            Attendance data unavailable at the moment. Try :\n
            ● Reloading the page and login again.\n
            ● Check whether attendance is "On Process..."
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
    df_columns = ["COURSE_CODE",f"AFFORDABLE_LEAVES({st.session_state.attendance_slider}%)"]
    with tabs[0]:
        df = pd.DataFrame(st.session_state.attendance_table, columns=df_columns)
        st.dataframe(df, hide_index = True)
    with tabs[1]:
        df = pd.DataFrame(st.session_state.exemption_table, columns=df_columns)
        st.dataframe(df, hide_index = True)
    with tabs[2]:
        df = pd.DataFrame(st.session_state.medical_table, columns=df_columns)
        st.dataframe(df, hide_index = True)

    st.markdown(f"<h5 style='color:rgb(255, 75, 75);'>LAST UPDATED : {st.session_state.updated_date}<br><br></h5>", unsafe_allow_html=True)

    #Display notes for the user
    st.info("""NOTE : '-' next to number of leaves denotes classes must be attended
                to meet the corresponding percentage without skipping classes""")