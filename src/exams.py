from bs4 import BeautifulSoup
import requests

def getCATExamSchedule(session: requests.Session):
    schedule_page_url = "https://ecampus.psgtech.ac.in/studzone/ContinuousAssessment/CATestTimeTable"
    schedule_page = session.get(schedule_page_url)

    if schedule_page.status_code not in [200,302]:
        raise Exception("/studzone/ContinuousAssessment/CATestTimeTable is unavailable!")
    
    schedule_page_soup = BeautifulSoup(schedule_page.text , "lxml")

    content_flag = schedule_page_soup.find("div",{"class":"Test-card"})

    if not content_flag:
        raise Exception("CAT exam schedule not found! /studzone/ContinuousAssessment/CATestTimeTable has no content!")

    exams_soup = schedule_page_soup.find_all("div",{"class":"text-left"})

    required_indices = [0,2,4]

    schedule_data = []
    for exam in exams_soup:
        exam_contents = exam.find_all("span",{"class":"sol"})
        
        row = []
        for index in required_indices:
            row.append(exam_contents[index].text[1:].strip())

        schedule_data.append(row)
    
    return schedule_data


def getSemExamSchedule(session: requests.Session):
    sem_schedule_page_url = "https://ecampus.psgtech.ac.in/studzone2/FrmEpsTimetable.aspx"
    sem_schedule_page = session.get(sem_schedule_page_url)
    
    if sem_schedule_page.status_code not in [200,302]:
        raise Exception("Semester schedule not found! /studzone2/FrmEpsTimetable.aspx is unavailable!")
    
    sem_schedule_page_soup = BeautifulSoup(sem_schedule_page.text , "lxml")
    
    schedule_table = sem_schedule_page_soup.find("table",{"id":"DgResult"})
    
    if not schedule_table:
        raise Exception("Semester schedule not found!")
    
    schedule_table_rows = schedule_table.find_all("tr")
    
    data = []
    for row in schedule_table_rows[1:]:
        record = []
        for cell in row.find_all("td")[2:]:
            record.append(cell.text)
        data.append(record)

    return data