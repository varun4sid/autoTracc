import streamlit as st


if "page" not in st.session_state:
    st.session_state.page = "login_page"

if "credentials" not in st.session_state:
    st.session_state.rollno   = None
    st.session_state.password = None

def loginPage():
    white_space_left, title, white_space_right = st.columns([5,5,4])

    with title:
        st.title("autoTracc")

    white_space_left, login_form, white_space_right = st.columns([1,4,1])

    with login_form:
        with st.form(key="login_form"):
            st.session_state.rollno   = st.text_input("RollNo:")
            st.session_state.password = st.text_input("Password:" ,type="password")

            white_space_right, submit_button, white_space_right = st.columns([4,3,3])
            with submit_button:
                submit_button = st.form_submit_button()

            if submit_button:
                if not all( [st.session_state.rollno.strip(), st.session_state.password.strip()] ):
                    st.warning("Please fill all the details!")
                else:
                    
                    st.session_state.page = "dashboard"
                    st.rerun()


def dashBoard():
    st.write("Hola")

if st.session_state.page == "login_page":
    loginPage()

elif st.session_state.page == "dashboard":
    dashBoard()