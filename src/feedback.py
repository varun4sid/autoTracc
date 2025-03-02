import os
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import StaleElementReferenceException
from webdriver_manager.chrome import ChromeDriverManager
import streamlit as st


def createDriver():
    #Set up Selenium Chrome options
    options = webdriver.ChromeOptions()
    options.binary_location = "/usr/bin/chromium"
    options.add_argument("--headless=new")
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")
    options.add_argument("--window-size=1920,1080")
    options.add_argument("--disable-gpu")

    #Start WebDriver
    service = service = Service("/usr/bin/chromedriver")
    driver = webdriver.Chrome(service=service, options=options)
    
    return driver


def intermediateForm(rollno,password):
    #Create a webdriver
    progress_bar = st.progress(0,text = "Fetching feedback page...")
    browser = createDriver()
    
    browser.get("https://ecampus.psgtech.ac.in/studzone")
    
    #Instantiate a wait sequence for page rendering
    wait = WebDriverWait(browser,10)
    
    #Fill out the credentials
    rollno_field = browser.find_element(By.ID,"rollno")
    rollno_field.send_keys(rollno)

    password_field = browser.find_element(By.ID,"password")
    password_field.send_keys(password)

    checkbox = browser.find_element(By.ID,"terms")
    browser.execute_script("arguments[0].click();",checkbox)

    login_button = browser.find_element(By.ID,"btnLogin")
    browser.execute_script("arguments[0].click();",login_button)
    
    #Get the feedback index page
    browser.get("https://ecampus.psgtech.ac.in/studzone/Feedback/Intermediate")
    feedbacks_index = browser.find_elements(By.CLASS_NAME,"card-body")
    
    #Click the intermediate feedback 
    browser.execute_script("arguments[0].click();",feedbacks_index[1])
    
    #Get the courses
    courses = browser.find_elements(By.CLASS_NAME,"intermediate-body")
    
    #Iterate through the courses
    for course in range(len(courses)):
        courses = browser.find_elements(By.CLASS_NAME,"intermediate-body")
        course_names = browser.find_elements(By.CSS_SELECTOR,"h6.course")
        progress_bar.progress((course)/len(courses),text=course_names[course].text+"...")  
        browser.execute_script("arguments[0].click();",courses[course])
        
        clicks = 0
        while clicks < 12:
            try:
                radio_button = wait.until(EC.element_to_be_clickable((By.XPATH,f"//label[@for='radio-{clicks+1}-1']")))
                browser.execute_script("arguments[0].click();",radio_button)
                clicks += 1
                next = wait.until(EC.element_to_be_clickable((By.XPATH,"//button[@class='carousel-control-next']")))
                browser.execute_script("arguments[0].click();",next)
            except StaleElementReferenceException:
                continue
            
        back = browser.find_element(By.CLASS_NAME,"overlay")
        progress_bar.progress((course+1)/len(courses),text=course_names[course].text+"...")
        browser.execute_script("arguments[0].click();",back)
    
    browser.quit()