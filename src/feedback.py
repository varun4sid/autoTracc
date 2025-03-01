from selenium import webdriver
import os
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import StaleElementReferenceException
from webdriver_manager.chrome import ChromeDriverManager
import streamlit as st


def intermediateForm(rollno,password):
    #Initiate a headless browser session
    option = webdriver.ChromeOptions()
    option.add_argument("--headless=new")
    option.add_argument("--window-size=1920,1080")
    option.add_argument("--disable-gpu")
    option.add_argument("--no-sandbox")
    option.add_argument("--disable-dev-shm-usage")
    
    service = Service(ChromeDriverManager().install())
    browser = webdriver.Chrome(service=service,options=option)
    
    browser.get("https://ecampus.psgtech.ac.in/studzone")
    
    #Instantiate a wait sequence for page rendering
    wait = WebDriverWait(browser,10)
    wait.until(EC.presence_of_element_located((By.TAG_NAME, "body")))
    
    #Fill out the credentials
    rollno_field = browser.find_element(By.ID,"rollno")
    rollno_field.send_keys(rollno)

    password_field = browser.find_element(By.ID,"password")
    password_field.send_keys(password)

    checkbox = browser.find_element(By.ID,"terms")
    checkbox.click()

    login_button = browser.find_element(By.ID,"btnLogin")
    login_button.click()
    
    #Get the feedback index page
    browser.get("https://ecampus.psgtech.ac.in/studzone/Feedback/Intermediate")
    feedbacks_index = browser.find_elements(By.CLASS_NAME,"card-body")
    
    #Click the intermediate feedback 
    feedbacks_index[1].click()
    
    st.write("Progress : ")
    #Get the courses
    courses = browser.find_elements(By.CLASS_NAME,"intermediate-body")
    
    #Iterate through the courses
    for course in range(len(courses)):
        courses = browser.find_elements(By.CLASS_NAME,"intermediate-body")
        course_names = browser.find_elements(By.CSS_SELECTOR,"h6.course")
        courses[course].click()
        
        clicks = 0
        while clicks < 12:
            try:
                radio_button = wait.until(EC.element_to_be_clickable((By.XPATH,f"//label[@for='radio-{clicks+1}-1']")))
                radio_button.click()
                clicks += 1
                next = wait.until(EC.element_to_be_clickable((By.XPATH,"//button[@class='carousel-control-next']")))
                next.click()
            except StaleElementReferenceException:
                continue
           
        st.write(course_names[course].text) 
        back = browser.find_element(By.CLASS_NAME,"overlay")
        browser.execute_script("arguments[0].click();",back)