from requests import Session
from bs4 import BeautifulSoup

def getUserInput():
    rollno = input("Enter Roll No : ")
    password = input("Enter Password : ")
    return rollno,password


def getHomePage():
    #Start a session
    login_url = "https://ecampus.psgtech.ac.in/studzone"
    session = Session()

    #Get the login page
    login_page = session.get(login_url)

    #Extract the html from the page using lxml parser
    login_soup = BeautifulSoup(login_page.text , 'lxml')

    #Get the dynamic token used for login
    token = login_soup.find("input",{"name":"__RequestVerificationToken"})["value"]

    #Get the user input
    rollno, password = getUserInput()

    #Create a payload to POST to the login form
    payload = {
    "rollno" : rollno,
    "password" : password,
    "chkterms" : "on",
    "__RequestVerificationToken" : token
    }

    #Get the response from POST
    response = session.post(login_url, data=payload)