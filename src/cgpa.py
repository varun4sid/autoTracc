from bs4 import BeautifulSoup

def getStudentCourses(session):
    #Get the courses page using the current session
    courses_page_url = "https://ecampus.psgtech.ac.in/studzone2/AttWfStudCourseSelection.aspx"
    courses_page = session.get(courses_page_url)

    #Get the html from the courses page
    courses_soup = BeautifulSoup(courses_page.text, "lxml")

    #Get the completed courses table element
    completed_courses_table = courses_soup.find("table",{"id":"PDGCourse"})

    #Get the table rows
    completed_table_rows = completed_courses_table.find_all("tr")
    
    #Extract the records and values and store in list of lists
    data = []

    for row in completed_table_rows:
        record=[]
        for cell in row.find_all("td"):
            record.append(cell.text)
        data.append(record)
    
    #Map the letter grades to their corresponding numeric values:
    letter_grade = {
        "O":10,
        "A+":9,
        "A":8,
        "B+":7,
        "B":6,
        "C":5,
    }

    #Convert required data to readable format
    completed_courses = []
    for row in data[1:]:
        completed_courses.append(row[1].strip())
        row[4] = int(row[4].strip())
        row[6] = letter_grade[row[6].strip()]
        row[7] = int(row[7].strip())

    return data


def getCompletedSemester(session):
    results_page_url = "https://ecampus.psgtech.ac.in/studzone2/FrmEpsStudResult.aspx"
    results_page     = session.get(results_page_url)
    
    results_page_soup = BeautifulSoup(results_page.text, "lxml")
    results_table = results_page_soup.find("table",{"id":"DgResult"})
    
    rows = results_table.find_all("tr")
    
    data = []
    for row in rows:
        record = []
        for cell in row.find_all("td"):
            record.append(cell.text)
        data.append(record)
    
    #Returns the least semester with RA or next semester if none
    for record in data[1:]:
        if record[0] != ' ':
            sem_index = int(record[0])
        if record[5] == "RA":
            return sem_index
        
    return sem_index+1

def getCGPA(data, completed_semester):
    from pandas import DataFrame

    #Get the most recent semester for iterating
    most_recent_semester = data[1][4]

    #Create a dataframe with required columns
    data[0][4]="COURSE_SEM"
    df = DataFrame(data[1:],columns=data[0])
    required_columns = ["COURSE_SEM","GRADE","CREDITS"]
    df = df[required_columns]

    #Declare an empty result table with header
    result_headers = ["SEMESTER","GPA","CGPA"]
    result = []
    
    #Initialize to calculate cgpa upto each semester
    overall_product = 0
    overall_credits = 0

    #Initialize backlogs flag to handle pending cgpa calculation
    backlogs = False
    for semester in range(1,most_recent_semester+1): #index from 1st to most recent semester
        if not backlogs:
            courses = df.loc[df["COURSE_SEM"] == semester] #get all courses of particular semester
            if semester >= completed_semester: #check for backlogs in particular semester
                backlogs = True
                record = [semester , "-", "-"]
                result.append(record)
            else:
                semester_product = sum(courses["GRADE"] * courses["CREDITS"])
                semester_credits = sum(courses["CREDITS"])

                overall_product += semester_product
                overall_credits += semester_credits

                semester_gpa  = float(semester_product / semester_credits)
                semester_cgpa = float(overall_product / overall_credits)
                
                semester_gpa = '{:.5f}'.format(semester_gpa)[:-1]
                semester_cgpa = '{:.5f}'.format(semester_cgpa)[:-1]
                
                record = [semester , semester_gpa , semester_cgpa]
                result.append(record)    
        else:
            record = [semester , "-", "-"]
            result.append(record)
    
    result = DataFrame(result, columns=result_headers)

    return result