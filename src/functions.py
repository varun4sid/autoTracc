from requests import Session
from bs4 import BeautifulSoup
from csv import writer
from pandas import DataFrame

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

    print("Extracting attendance data...")
    return data
    


def getAttendance(data):
    #Get custom percentage that user wants to maintain
    while True:
        custom_percentage = int(input("Enter attendance percentage you would like to maintain : "))
        if custom_percentage<0 or custom_percentage>100:
            print("Invalid input! Try again!")
        else:
            break

    #Declare an empty result table with header
    result = []
    result_header = ["COURSE_ID","RECOMMENDED_LEAVES(75%)",f"AFFORDABLE_LEAVES({custom_percentage}%)"]

    #Calculate affordable leaves for each course and update result
    for i in range(1, len(data)): #index from 1 as we exclude header
        row=[data[i][0]]          #initialize row with course id
        classes_total = int(data[i][1])  #typecast attendance values to int
        classes_present = int(data[i][4])

        #Calculate the recommended(75%) and customized leaves for the user and update row
        recommended_leaves = calculateAttendance(classes_present,classes_total,75)
        custom_leaves = calculateAttendance(classes_present,classes_total,custom_percentage)

        row.extend([recommended_leaves , custom_leaves])
        result.append(row)

    df = DataFrame(result,columns=result_header)
    print(df.to_string())

        
def calculateAttendance(classes_present , classes_total , maintenance_percentage):
    affordable_leaves = 0
    i=1

    #First check whether or not current attendance meets maintenance and then proceed
    if float(classes_present/classes_total)*100 < maintenance_percentage:
        while float((classes_present + i)/(classes_total + i))*100 <= maintenance_percentage:
            affordable_leaves -=1 #negative leaves denote number of unskippable classes to meet maintenance
            i+=1
    #Else block is run if maintenance is met
    else:
        while float(classes_present/(classes_total + i))*100 >= maintenance_percentage:
            affordable_leaves +=1
            i+=1

    return affordable_leaves