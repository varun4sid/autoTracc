from pandas import DataFrame
from bs4 import BeautifulSoup
from .attendance import getCourseNames

def getExamSchedule(session):
    #Get the exam schedule page
    schedule_page_url = "https://ecampus.psgtech.ac.in/studzone/ContinuousAssessment/CATestTimeTable"
    schedule_page = session.get(schedule_page_url)

    #Get the html of the page
    schedule_page_soup = BeautifulSoup(schedule_page.text , "lxml")

    #Check for presence of schedule content
    content_flag = schedule_page_soup.find("div",{"class":"Test-card"})

    if not content_flag:
        return False

    #Get the html of each exam's content
    exams_soup = schedule_page_soup.find_all("div",{"class":"text-left"})

    #Extract exam details and append the records to a list
    schedule_data = []

    #Map the course codes with course initials and store in list of records
    course_map = getCourseNames(session)

    #Set the indices for required data
    required_indices = [0,2,4]

    #Get the required details of each courses' exam
    for exam in exams_soup:
        #Get the html contents of each exam
        exam_contents = exam.find_all("span",{"class":"sol"})

        #Get the record of required details and append to schedule data
        row = []
        for index in required_indices:
            row.append(exam_contents[index].text[1:].strip())
        try:
            row[0] = ''.join( [ row[0], '   -   ', course_map[row[0]] ] )
        except KeyError:
            continue
        schedule_data.append(row)

    #Set the dataframe headers
    df_headers = ["COURSE_CODE","DATE","TIME"]

    #Create and return a dataframe
    df = DataFrame(schedule_data, columns = df_headers)
    
    return df