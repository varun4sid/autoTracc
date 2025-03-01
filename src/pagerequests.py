from requests import Session
from bs4 import BeautifulSoup


def getHomePageAttendance(rollno, password):
    #Start a session
    login_url = "https://ecampus.psgtech.ac.in/studzone"
    session = Session()

    #Get the login page
    login_page = session.get(login_url)

    #Extract the html from the page using lxml parser
    login_soup = BeautifulSoup(login_page.text , "lxml")

    #Get the dynamic token used for login
    token = login_soup.find("input",{"name":"__RequestVerificationToken"})["value"]

    #Create a payload to POST to the login form
    payload = {
    "rollno"                     : rollno,
    "password"                   : password,
    "chkterms"                   : "on",
    "__RequestVerificationToken" : token
    }

    #Get the response from POST
    response = session.post(login_url, data=payload)

    #Check if we have landed on student home page
    #and the pass the current session for the next function
    response_soup = BeautifulSoup(response.text , "lxml")
    check = response_soup.find("nav",{"class":"navbar navbar-expand-lg navbar-light"})
    if check:
        return session
    else:
        return False


def getHomePageCGPA(rollno, password):
    #Start a session
    login_url = "https://ecampus.psgtech.ac.in/studzone2/"
    session = Session()

    #Get the login page
    login_page = session.get(login_url)

    #Extract the html from the page using lxml parser
    login_soup = BeautifulSoup(login_page.text , "lxml")

    #Get the dynamic tokens used for login
    viewstate           = login_soup.find("input",{"name":"__VIEWSTATE"})["value"]
    viewstate_generator = login_soup.find("input",{"name":"__VIEWSTATEGENERATOR"})["value"]
    event_validation    = login_soup.find("input",{"name" : "__EVENTVALIDATION"})["value"]
    abcd3               = login_soup.find("input",{"name" : "abcd3"})["value"]

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
    

def getUsername(session):
    #Get a page with username
    name_page_url = "https://ecampus.psgtech.ac.in/studzone/Attendance/AttendanceMenu" 
    name_page = session.get(name_page_url)

    #Get the html of the page
    name_page_soup = BeautifulSoup(name_page.text, "lxml")

    #Get the username
    username = name_page_soup.find("span",{"class":"name"})

    return username.string