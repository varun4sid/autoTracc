import pandas as pd
import streamlit as st
from pages.processingPage import processCGPA
from decimal import Decimal, ROUND_HALF_UP

def cgpaTab():
    if not st.session_state.processing_cgpa:
        #Get the cgpa data and handle exceptions 
        processCGPA()
    if st.session_state.cgpa_available:
        cgpaUI()
    else:
        st.warning("""
            Courses data unavailable at the moment. This is likely to be a server issue.
            Try again after some time.
        """)


def cgpaUI():
    tab1,tab2,tab3 = st.tabs(["CGPA", "Course List", "Target"])
    
    df_columns = ["SEMESTER","GPA","CGPA"]
    df = pd.DataFrame(st.session_state.cgpa_data["result"], columns=df_columns)
    
    def roundHalfUp(x):
        return Decimal(x).quantize(Decimal('0.01'), rounding=ROUND_HALF_UP)
    
    df_rounded = df.copy()
    df_rounded["CGPA"] = df_rounded["CGPA"].astype(float).apply(roundHalfUp).astype(str)
    df_rounded["GPA"] = df_rounded["GPA"].astype(float).apply(roundHalfUp).astype(str)
    
    def toggleCGPAValues():
        st.session_state.marksheet_value = not st.session_state.marksheet_value
    
    with tab1:
        st.toggle(label="Marksheet Values",value=st.session_state.marksheet_value,on_change=toggleCGPAValues)
        if st.session_state.marksheet_value:
            st.dataframe(df_rounded, hide_index = True)
        else:
            st.dataframe(df, hide_index = True)
        st.info("NOTE : '-' denotes existing backlogs in the corresponding semester!\n")
    with tab2:
        st.write("Swipe left on table if you're on mobile to see credits and grade columns")
        st.dataframe(st.session_state.completed_courses_list, hide_index=True)
    with tab3:
        if st.session_state.current_courses is not None:
            targetGPA()
        else:
            st.warning("No current courses data available to compute target CGPA!")
            
            
def targetGPA():
    current_courses = st.session_state.current_courses
    
    current_semester = max([int(course[4]) for course in current_courses])
    current_credits = sum([int(course[6]) for course in current_courses])
    
    contents = [
        {
            "COURSE" : course[2],
            "CREDITS" : int(course[6]),
            "GRADE" : 10
        } for course in current_courses
    ]
    
    df = pd.DataFrame(contents)
    
    st.info("Edit the expected grades for your current courses and submit to compute expected CGPA.")
    
    edited_df = st.data_editor(
        df,
        column_config={
            "GRADE": st.column_config.NumberColumn(
                label="GRADE",
                min_value=5,
                max_value=10,
                step=1,
                disabled=None,
                help="Enter expected grade for the course"
            ),
        },
        disabled=["COURSE","CREDITS"],
        hide_index=True,
    )
    
    pstyle = "font-size:20px; font-weight:bold; margin-left:0px; position: relative; left:10px;"
    st.write(f"<p style={pstyle}>Total credits for {current_semester}th semester: {current_credits}</p>", unsafe_allow_html=True)
    submit_button = st.button("Submit")
    
    if submit_button:
        grade_credit_product = 0
        for index in range(len(current_courses)):
            grade = int(edited_df.at[index, "GRADE"])
            credits = int(edited_df.at[index, "CREDITS"])
            grade_credit_product += grade * credits
        
        st.write(f"#### Expected GPA for {current_semester}th semester: {grade_credit_product / current_credits :.4f}")
        overall_product = st.session_state.cgpa_data["overall_product"] + grade_credit_product
        overall_credits = st.session_state.cgpa_data["overall_credits"] + current_credits
        st.write(f"#### Expected CGPA after {current_semester}th semester: {overall_product / overall_credits :.4f}")