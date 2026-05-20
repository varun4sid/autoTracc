from requests import Session
from bs4 import BeautifulSoup
from datetime import datetime
import pytz

from requests.adapters import HTTPAdapter
from urllib3.util.retry import Retry

from src.logger import logError

def make_session():
    s = Session()
    retry = Retry(
        total=5,
        connect=5,
        read=3,
        backoff_factor=0.5,
        status_forcelist=(429, 500, 502, 503, 504),
        allowed_methods=("GET", "POST"),
        raise_on_status=False,
    )
    adapter = HTTPAdapter(max_retries=retry)
    s.mount("https://", adapter)
    s.mount("http://", adapter)
    return s


def getStudzoneModern(rollno, password):
    login_url = "https://ecampus.psgtech.ac.in/studzone"
    session = make_session()

    response = session.get(login_url)
    if response.status_code != 200:
        raise Exception("Failed to connect to /studzone")
    
    #Extract the html from the page using lxml parser
    login_soup = BeautifulSoup(response.text , "lxml")

    #Get the dynamic token used for login
    try:
        token = login_soup.find("input",{"name":"__RequestVerificationToken"})["value"]
    except:
        raise Exception("Failed to retrieve /studzone1 __RequestVerificationToken")

    #Create a payload to POST to the login form
    payload = {
    "rollno"                     : rollno,
    "password"                   : password,
    "chkterms"                   : "on",
    "__RequestVerificationToken" : token
    }

    #Get the response from POST
    response = session.post(login_url, data=payload)
    
    if response.status_code != 200:
        raise Exception("Failed to connect to /studzone")
    if response.url == login_url:
        raise Exception("Invalid credentials! Try again!")

    return session


def getStudzoneLegacy(rollno, password):
    #Start a session
    login_url = "https://ecampus.psgtech.ac.in/studzone2/"
    session = make_session()

    #Get the login page
    login_page = session.get(login_url)

    #Extract the html from the page using lxml parser
    login_soup = BeautifulSoup(login_page.text , "lxml")

    #Get the dynamic tokens used for login
    try:
        viewstate           = login_soup.find("input",{"name":"__VIEWSTATE"})["value"]
        viewstate_generator = login_soup.find("input",{"name":"__VIEWSTATEGENERATOR"})["value"]
        event_validation    = login_soup.find("input",{"name" : "__EVENTVALIDATION"})["value"]
        abcd3               = login_soup.find("input",{"name" : "abcd3"})["value"]
    except:
        err_message = "Failed to retrieve /studzone2 ASP.NET tokens"
        logError(err_message)
        raise Exception(err_message)

    #Create a payload to POST to the login form
    payload = {
        "__EVENTTARGET"        : "",
        "__EVENTARGUMENT"      : "",
        "__LASTFOCUS"          : "",
        "__VIEWSTATE"          : viewstate,
        "__VIEWSTATEGENERATOR" : viewstate_generator,
        "__EVENTVALIDATION"    : event_validation,
        "rdolst"               : "S",
        "txtusercheck"         : rollno,
        "txtpwdcheck"          : password,
        "abcd3"                : abcd3
    }

    #Send a POST request from current session
    session.post(login_url, data=payload)

    return session
    

def greetUser(session):
    scholarship_url = "https://ecampus.psgtech.ac.in/studzone/Scholar/VallalarScholarship"
    response = session.get(scholarship_url)
    
    if response.status_code != 200:
        raise Exception("Failed to connect to /studzone/Scholar/VallalarScholarship")
    
    page_soup = BeautifulSoup(response.text, "lxml")
    
    #Get the personal info table
    personal_info_table = page_soup.find("td",{"class":"personal-info"})
    personal_info = personal_info_table.find_all("td")
        
    #Get the username
    username = personal_info[0].string.strip()
    
    #Get the birthday
    birthdate = personal_info[2].string.strip()
    birthdate = datetime.strptime(birthdate, "%d/%m/%Y").date()
    
    #Get current date
    IST = pytz.timezone('Asia/Kolkata') 
    today = datetime.now(IST).date()
    
    if birthdate.month == today.month and birthdate.day == today.day:
        greeting = "Happy Birthday " + username + "!"
        balloons = True
    else:
        greeting = "Welcome " + username + "!"
        balloons = False

    return { "message" : greeting, "balloons": balloons }


def fallbackGreeting(session):
    profile_url = "https://ecampus.psgtech.ac.in/studzone/Home/Profile"
    profile_page = session.get(profile_url)
    
    if profile_page.status_code != 200:
        raise Exception("Failed to connect to /studzone/Home/Profile")
    
    profile_soup = BeautifulSoup(profile_page.text, "lxml")
    profile_name = profile_soup.find("h2", {"class":"profile-name"}).text
    greeting = "Welcome " + profile_name + "!"
    return greeting