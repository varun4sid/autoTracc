import streamlit as st


def cgpaTab():
    if st.session_state.cgpa_available:
        cgpaUI()
    else:
        st.warning("""
            Courses data unavailable at the moment. This is likely to be a server issue.
            Try again after some time.
        """)


def cgpaUI():
    tab1,tab2 = st.tabs(["CGPA", "Course List"])
    
    with tab1:
        st.dataframe(st.session_state.cgpa_data, hide_index = True)
        st.warning("NOTE : '-' denotes existing backlogs in the corresponding semester!\n")
    with tab2:
        st.write("Swipe left on table if you're on mobile to see credits and grade columns")
        st.dataframe(st.session_state.courses_list, hide_index=True)