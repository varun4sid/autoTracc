from requests import Session
from bs4 import BeautifulSoup

def getUserInput():
    #check rollno input
    while True:
        rollno = input("Enter Roll No : ")
        if not rollno.strip():
            print("Invalid ID! Try again!")
        else:
            break
    
    #check password input
    while True:
        password = input("Enter Password : ")
        if not password.strip():
            print("Empty password detected! Try again!")
        else:
            break

    return rollno,password


def getHomePageAttendance():
    #Start a session
    login_url = "https://ecampus.psgtech.ac.in/studzone"
    session = Session()

    #Get the login page
    login_page = session.get(login_url)

    #Extract the html from the page using lxml parser
    login_soup = BeautifulSoup(login_page.text , "lxml")

    #Get the dynamic token used for login
    token = login_soup.find("input",{"name":"__RequestVerificationToken"})["value"]

    #Get the user input
    rollno, password = getUserInput()

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
        return None


def getHomePageCGPA():
    #Start a session
    login_url = "https://ecampus.psgtech.ac.in/studzone2/"
    session = Session()

    #Get the login page
    login_page = session.get(login_url)

    #Extract the html from the page using lxml parser
    login_soup = BeautifulSoup(login_page.text , "lxml")

    #Get the user input
    rollno, password = getUserInput()

    #Get the dynamic tokens used for login
    # event_target        = login_soup.find("input",{"name" : "__EVENTTARGET"})["value"]
    # event_argument      = login_soup.find("input",{"name" : "__EVENTARGUMENT"})["value"]
    # last_focus          = login_soup.find("input",{"name" : "__LASTFOCUS"})["value"]
    viewstate           = login_soup.find("input",{"name":"__VIEWSTATE"})["value"]
    viewstate_generator = login_soup.find("input",{"name":"__VIEWSTATEGENERATOR"})["value"]
    event_validation    = login_soup.find("input",{"name" : "__EVENTVALIDATION"})["value"]
    abcd3    = login_soup.find("input",{"name" : "abcd3"})["value"]

    #
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

    #Get the response from POST method
    response = session.post(login_url, data=payload)
    
    #Check if we have landed on student home page
    #and the pass the current session for the next function
    response_soup = BeautifulSoup(response.text , "lxml")
    check = response_soup.find("table",{"id":"Title1_Menu1"})
    if check:
        return session
    else:
        return None