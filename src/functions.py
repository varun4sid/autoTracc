from requests import Session
from bs4 import BeautifulSoup
from csv import writer


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

    #Check if we have landed on student home page
    #and the pass the current session for the next function
    response_soup = BeautifulSoup(response.text , "lxml")
    check = response_soup.find("nav",{"class":"navbar navbar-expand-lg navbar-light"})
    if check:
        return session
    else:
        return None


def getStudentPercentage(session):
    #Get the student attendance page using the current session
    student_percentage_url = "https://ecampus.psgtech.ac.in/studzone/Attendance/StudentPercentage"
    student_percentage_page = session.get(student_percentage_url)

    #Get the html from the student attendance page
    attendance_soup = BeautifulSoup(student_percentage_page.text,"lxml")

    #Get the table element from the html
    attendance_table = attendance_soup.find("table",{"class":"table table-bordered"})

    #Get the list of table rows
    table_rows = attendance_table.find_all("tr")

    #Extract the values and append it to a list of records/rows
    data = []
    
    #Get the first row which is a header
    header = table_rows.pop(0)
    row=[]
    for cell in header.find_all("th"):
        row.append(cell.text)
    data.append(row)
    
    #Get the remaining rows
    for row in table_rows:
        record = []
        for cell in row.find_all("td"):
            record.append(cell.text)
        data.append(record)
    
    #Create a csv file
    with open("attendance.csv","w") as file:
        file_writer = writer(file)
        file_writer.writerows(data)