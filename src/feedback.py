from bs4 import BeautifulSoup
import requests

def fillform_intermediate(session: requests.Session):
    intermediate_page_url = "https://ecampus.psgtech.ac.in/studzone/Feedback/Intermediate"
    response = session.get(intermediate_page_url)
    
    if response.status_code not in [200, 302]:
        raise Exception("Intermediate feedback form not found! /studzone/Feedback/Intermediate is unavailable!")
    
    soup = BeautifulSoup(response.text, "lxml")
    forms = soup.find_all("div", class_="intermediate-body")
    
    if not forms or len(forms) == 0:
        raise Exception("Intermediate feedback form not found! /studzone/Feedback/Intermediate has no content!")
    
    forms_data = []
    for form in forms:
        staffid = form.find_all("h5")[-1].text.strip()
        course_code = form.find_all("h6")[-2].text.strip()
        forms_data.append((staffid, course_code))
    
    endpoint = "https://ecampus.psgtech.ac.in/studzone/Feedback/Save_Intermediate"
    for form in forms_data:
        staffid, course_code = form
        for i in range(1, 13):
            payload = {
                "coursecode": course_code,
                "staffid": staffid,
                "questype": 1,
                "quesID": i,
                "ansid": 1,
            }
            response = session.post(endpoint, data=payload)

def getFeedbackDuration(session: requests.Session, mode: str):
    feedback_page = session.get("https://ecampus.psgtech.ac.in/studzone/Feedback/Index")
    
    if feedback_page.status_code not in [200,302]:
        return None 
    feedback_page_soup = BeautifulSoup(feedback_page.text , "lxml")
    feedback_cards = feedback_page_soup.find_all("div",{"class":"me-3"})
    
    if len(feedback_cards) != 2:
        return None
    
    card = None
    for feedback_card in feedback_cards:
        if mode in feedback_card.text:
            card = feedback_card
            
    end_date = card.find("span",{"id":"InterEndDate"}).text
    
    if not end_date:
        return None
    
    start_date = card.find("span",{"id":"InterStartDate"}).text
    
    if not start_date:
        return None
    
    return {
        "start" : start_date,
        "end" : end_date
    }
    
    
def checkIntermediateFeedbackFilled(session: requests.Session):
    intermediate_page = session.get("https://ecampus.psgtech.ac.in/studzone/Feedback/Intermediate")
    
    intermediate_page_soup = BeautifulSoup(intermediate_page.text , "lxml")
    
    total_courses = intermediate_page_soup.select("div.card.intermediate-card")
    feedback_filled = intermediate_page_soup.select("div.card.intermediate-card.bg-highlight")
    
    if len(total_courses) == 0:
        return False
    
    return len(total_courses) == len(feedback_filled)