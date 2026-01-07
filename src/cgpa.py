from bs4 import BeautifulSoup

def getStudentCourses(session):
    #Get the courses page using the current session
    courses_page_url = "https://ecampus.psgtech.ac.in/studzone2/AttWfStudCourseSelection.aspx"
    courses_page = session.get(courses_page_url)

    #Get the html from the courses page
    courses_soup = BeautifulSoup(courses_page.text, "lxml")

    completed_courses = getCompletedCourses(courses_soup)
    current_courses = getCurrentCourses(courses_soup)
    
    return completed_courses, current_courses


def getCompletedCourses(soup):
    completed_courses_table = soup.find("table",{"id":"PDGCourse"})
    completed_table_rows = completed_courses_table.find_all("tr")
    
    #Extract the records and values and store in list of lists
    results = []

    for row in completed_table_rows:
        record=[]
        for cell in row.find_all("td"):
            record.append(cell.text)
        results.append(record)
    
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
    for row in results[1:]:
        row[4] = int(row[4].strip())
        row[6] = letter_grade[row[6].strip()]
        row[7] = int(row[7].strip())

    return results


def getCurrentCourses(soup):
    current_courses_table = soup.find("table",{"id":"Prettydatagrid3"})
    current_table_rows = current_courses_table.find_all("tr")
    
    records = []
    for row in current_table_rows[1:]:
        record = []
        for cell in row.find_all("td"):
            record.append(cell.text)
        records.append(record)
    
    return records


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

    #Get the semester range (lateral entry students start from sem 3, so handle explicitly)
    most_recent_semester = data[1][4]
    first_semester = data[-1][4]

    #Create a dataframe with required columns
    data[0][4]="COURSE_SEM"
    df = DataFrame(data[1:],columns=data[0])
    required_columns = ["COURSE_SEM","GRADE","CREDITS"]
    df = df[required_columns]

    #Declare an empty result table
    result = []
    
    #Initialize to calculate cgpa upto each semester
    overall_product = 0
    overall_credits = 0

    #Initialize backlogs flag to handle pending cgpa calculation
    backlogs = False
    for semester in range(first_semester, most_recent_semester+1):
        if not backlogs:
            courses = df.loc[df["COURSE_SEM"] == semester] #get all courses of particular semester
            if semester >= completed_semester: #check for backlogs in particular semester
                backlogs = True
                record = [semester , "-", "-"]
                result.append(record)
            else:
                semester_product = (courses["GRADE"] * courses["CREDITS"]).sum()
                semester_credits = courses["CREDITS"].sum()
                
                if not semester_credits:
                    semester_gpa = "Pending"
                    semester_cgpa = "Pending"
                else:
                    overall_product += semester_product
                    overall_credits += semester_credits

                    semester_gpa  = semester_product / semester_credits
                    semester_cgpa = overall_product / overall_credits
                    
                    marksheet_cgpa = '{:.2f}'.format(semester_cgpa)[:-1]
                    semester_gpa = '{:.5f}'.format(semester_gpa)[:-1]
                    semester_cgpa = '{:.5f}'.format(semester_cgpa)[:-1]
                
                record = [semester , semester_gpa , semester_cgpa, marksheet_cgpa]
                result.append(record)    
        else:
            record = [semester , "-", "-", "-"]
            result.append(record)
    
    response = {
        "result": result,
        "overall_product": overall_product,
        "overall_credits": overall_credits
    }
    
    return response
