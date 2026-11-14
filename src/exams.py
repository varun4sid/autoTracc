from bs4 import BeautifulSoup
import requests
import pandas as pd

from src.logger import logError
from src.utils import courseAcronym

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
    try:
        seating_data = getSeating(session)
        if seating_data.columns.tolist() == ["SESSION", "COURSE", "HALL", "SEAT"]:
            print("Got seating!")
            return seating_data
    except Exception as e:
        print("Seating page available but no content!")
        logError(str(e))
        
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
        
    for row in data:
        course_string = row[0]
        acronym = courseAcronym(course_string)
        row[0] = acronym
        row[1] += " - " + row[2][0] + "N" # shortened session AN/FN
        row.pop(2)
        
    df = pd.DataFrame(data, columns=["COURSE", "SESSION"])
    df = df[["SESSION", "COURSE"]]

    return df


def getSeating(session: requests.Session):
    seating_page_url = "https://ecampus.psgtech.ac.in/studzone2/EpsWfSeating.aspx"
    seating_page = session.get(seating_page_url)
    
    if seating_page.status_code not in [200,302]:
        return None # no need exception as fallback is available
    
    seating_page_soup = BeautifulSoup(seating_page.text , "lxml")

    seating_table = seating_page_soup.find("table",{"id":"DgSeat"})
    seating_table_rows = seating_table.find_all("tr")
    
    
    if len(seating_table_rows) < 2:
        return None
    
    seating_data = []
    for row in seating_table_rows[1:]:
        record = []
        for cell in row.find_all("td"):
            record.append(cell.text)
        seating_data.append(record)
        
    for row in seating_data:
        course_string = row[2]
        parts = course_string.split("-")
        acronym = courseAcronym(parts[1])
        row[2] = parts[0] + " - " + acronym
        row[0] += " - " + row[1]
        row.pop(1)
        
    df = pd.DataFrame(seating_data, columns=["SESSION", "COURSE", "HALL", "SEAT"])
    
    return df
