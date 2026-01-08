import logging
from datetime import datetime
import pytz
import streamlit as st

def userLogger():
    logging.basicConfig(level=logging.INFO)
    logtime = datetime.now(pytz.timezone('Asia/Calcutta')).replace(second=0,microsecond=0,tzinfo=None)
    logging.info(f'{logtime} USER : {str.upper(st.session_state.rollno)}')
    
    
def logEvent(event_message):
    logging.basicConfig(level=logging.INFO)
    logging.info(f'USER : {str.upper(st.session_state.rollno)}{event_message}')