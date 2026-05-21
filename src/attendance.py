from bs4 import BeautifulSoup
import requests
import math

def getStudentAttendance(session: requests.Session):
    student_percentage_url = "https://ecampus.psgtech.ac.in/studzone/Attendance/StudentPercentage"
    response = session.get(student_percentage_url)

    if response.status_code != 200:
        raise Exception("Failed to connect to /studzone/Attendance/StudentPercentage")

    attendance_soup = BeautifulSoup(response.text,"lxml")

    #Get the table element from the html
    attendance_table = attendance_soup.find("table",{"id":"example"}).find("tbody")

    #Get the list of table rows
    table_rows = attendance_table.find_all("tr")
    
    if attendance_table is None or table_rows is None:
        raise Exception("/studzone/Attendance/StudentPercentage has no content!")
    
    if len(table_rows[-1].find_all("td")) == 1:
        raise Exception("Attendance data unavailable!")

    #Extract the values and append it to a list of records/rows
    data = []

    for row in table_rows:
        record = []
        for cell in row.find_all("td"):
            record.append(cell.text)
        # try:
        #     record[0] = f"{record[0]}   -   {course_map[record[0]]}"
        # except KeyError:
        #     continue
        data.append(record)
        
    return data


def getCourseNames(session: requests.Session):
    courses_url = "https://ecampus.psgtech.ac.in/studzone/Attendance/courseplan"

    response = session.get(courses_url)

    if response.status_code != 200:
        raise Exception("Failed to connect to /studzone/Attendance/courseplan")

    courses_soup = BeautifulSoup(response.text, "lxml")

    #Get the list of div elements containing course details of each course
    courses = courses_soup.find_all("div",{"class":"col-md-8"})
    course_map = {}

    #Iterate through the list of divs to get the contents
    for course in courses:
        course_code = course.find("h5").text.strip()
        course_name = course.find("h6").text.strip()

        #Check and append uppercase letters
        course_initials = [
            word[0] for word in course_name.split() 
            if word and ord('A') <= ord(word[0]) <= ord('Z')
        ]
                
        #Convert the list of initials to string and map it to the course code
        course_map[course_code] = ''.join(course_initials)

    return course_map


def getAffordableLeaves(data,custom_percentage, mode):
    result = []

    #Calculate affordable leaves for each course and update result
    for record in data:
        row=[record[0]]
        classes_total = int(record[1])
        if mode == 0:
            classes_present = int(record[4])
        elif mode == 1:
            classes_present = int(record[4]) + int(record[2])
        elif mode == 2:
            classes_present = math.floor(int(record[1]) * int(record[7]) / 100)

        #Calculate the customized leaves for the user and update row
        custom_leaves = calculateLeaves(classes_present,classes_total,custom_percentage)

        #Update the row with calculated leaves
        row.append(custom_leaves)
        result.append(row)

    return result


def calculateLeaves(classes_present , classes_total , maintenance_percentage):
    threshold = maintenance_percentage / 100.0
    
    current_percentage = classes_present / classes_total if classes_total > 0 else 0

    if current_percentage < threshold:
        if threshold < 1:
            classes_needed = (threshold * classes_total - classes_present) / (1 - threshold)
            classes_needed = math.ceil(classes_needed - 1e-12)
            if classes_needed > 0:
                return -classes_needed
            else:
                return 0
        else:
            return 0
    else:
        if threshold > 0:
            affordable_leaves = (classes_present - threshold * classes_total) /threshold
            return math.floor(affordable_leaves)
        else:
            return classes_total

def mapCodeWithName(data, course_map):
    for record in data:
        course_code = record[0]
        try:
            record[0] = f"{course_code}   -    {course_map[course_code]}"
        except KeyError:
            continue
        
    return data