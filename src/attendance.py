from bs4 import BeautifulSoup
from pandas import DataFrame


def getStudentAttendance(session):
    #Get the student attendance page using the current session
    student_percentage_url = "https://ecampus.psgtech.ac.in/studzone/Attendance/StudentPercentage"
    student_percentage_page = session.get(student_percentage_url)

    #Get the html from the student attendance page
    attendance_soup = BeautifulSoup(student_percentage_page.text,"lxml")

    #Get the table element from the html
    attendance_table = attendance_soup.find("table",{"id":"example"}).find("tbody")

    #Get the list of table rows
    table_rows = attendance_table.find_all("tr")

    #Get the mapping of course code to course name's initials
    course_map = getCourseNames(session)

    #Extract the values and append it to a list of records/rows
    data = []

    for row in table_rows:
        record = []
        for cell in row.find_all("td"):
            record.append(cell.text)
        try:
            record[0] = ''.join( [ record[0], '   -   ', course_map[record[0]] ] )
        except KeyError:
            continue
        data.append(record)
        
    return data


def getCourseNames(session):
    #Find the course details page url
    courses_url = "https://ecampus.psgtech.ac.in/studzone/Attendance/courseplan"

    #Get the course details page
    courses_page = session.get(courses_url)

    #Get the html of the course details page
    courses_soup = BeautifulSoup(courses_page.text, "lxml")

    #Get the list of div elements containing course details of each course
    courses = courses_soup.find_all("div",{"class":"col-md-8"})

    #Create an empty dictionary
    course_map = {}

    #Iterate through the list of divs to get the contents
    for course in courses:
        course_code = course.find("h5")
        course_name = course.find("h6")

        #Initialize an empty list
        course_initials = []
        for words in course_name.text.split():
            #Check for special characters
            if ord(words[0]) in list(range(65,91)):
                #Append the first letter of each word in course name
                course_initials.append(words[0])

        #Convert the list of initials to string and map it to the course code
        course_map[course_code.text] = ''.join(course_initials)

    return course_map


def getAffordableLeaves(data,custom_percentage):
    #Declare an empty result table
    result = []

    #Calculate affordable leaves for each course and update result
    for i in range(len(data)):
        row=[data[i][0]]                #initialize row with course id
        classes_total = int(data[i][1])  #typecast attendance values to int
        classes_present = int(data[i][4])

        #Calculate the customized leaves for the user and update row
        custom_leaves = calculateLeaves(classes_present,classes_total,custom_percentage)

        #Update the row with calculated leaves
        row.append(custom_leaves)
        result.append(row)

    #Create a dataframe from the result list with headers
    result_header = ["COURSE_CODE",f"AFFORDABLE_LEAVES({custom_percentage}%)"]
    df = DataFrame(result,columns=result_header)

    return df
    

def calculateLeaves(classes_present , classes_total , maintenance_percentage):
    #Initialize leaves with 0
    affordable_leaves = 0
    #Let i represent the ith class from last updated date
    i=1

    #First check whether or not current attendance meets maintenance and then proceed
    if float(classes_present/classes_total)*100 < maintenance_percentage:
        #Simulate attendance after attending i classes while also checking if attendance met at each i
        while float((classes_present + i)/(classes_total + i))*100 <= maintenance_percentage:
            affordable_leaves -=1 #negative leaves denote number of unskippable classes to meet maintenance
            i+=1
    #Else block is run if maintenance is met
    else:
        while float(classes_present/(classes_total + i))*100 >= maintenance_percentage:
            affordable_leaves +=1
            i+=1

    return affordable_leaves