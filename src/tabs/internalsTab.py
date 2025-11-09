import streamlit as st
from src.internals import getInternals, calculateTarget
from src.state_manager import get_internals_table


def internalsTab():
    table_tab,custom_tab = st.tabs(["CA Marks","Custom"])
    with table_tab:
        try:
            st.session_state.internals_data = getInternals(st.session_state.studzone1_session)
            internalsUI()
        except:
            st.warning("Your internal marks are unavailable at the moment")
            
    with custom_tab:
        customScore()


def renderInternals(internals_table):
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
    
    for course in internals_table:
        table_body += f"<tr><td style='text-align:left;'>{course[0]}</td><td style='text-align:right;'>{course[1]}</td>"
        table_body += f"<td>{course[2]}</td><td>{course[3]}</td></tr>"
        
    table_body += "</table><br>"
    
    table = table_header + table_body
    
    st.markdown(table, unsafe_allow_html=True)
    
    
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


def internalsUI():
    st.session_state.target_slider = st.slider(
        label = "Enter your target final marks (for 100): ",
        min_value = 50,
        max_value = 100,
        value = 50
    )
    
    st.write("You need a final score of atleast 50 and a semester exam score of atleast 45 to pass!")
    
    # Get internals table using cached computation
    internals_table = get_internals_table(st.session_state.target_slider)
    
    if internals_table:
        renderInternals(internals_table)
    else:
        st.error("Unable to display internals table")
    
    st.warning(""" '-' denotes you can't achieve target with your current internal marks                
                    * beside the internal marks denotes final mark entry is pending
                """)