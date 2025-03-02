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
    #Check for presence of stable chrome version in streamlit runtime
    CHROME_PATH = "/usr/bin/google-chrome-stable"
    if not os.path.exists(CHROME_PATH):
        os.system("wget https://dl.google.com/linux/direct/google-chrome-stable_current_amd64.deb")
        os.system("apt-get install -y ./google-chrome-stable_current_amd64.deb || apt-get install -fy")
        os.system("rm google-chrome-stable_current_amd64.deb")

    #Set up Selenium Chrome options
    options = webdriver.ChromeOptions()
    options.binary_location = CHROME_PATH
    options.add_argument("--headless=new")
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")
    options.add_argument("--window-size=1920,1080")
    options.add_argument("--disable-gpu")

    #Start WebDriver
    service = Service(ChromeDriverManager().install())
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
    checkbox.click()

    login_button = browser.find_element(By.ID,"btnLogin")
    login_button.click()
    
    #Get the feedback index page
    browser.get("https://ecampus.psgtech.ac.in/studzone/Feedback/Intermediate")
    feedbacks_index = browser.find_elements(By.CLASS_NAME,"card-body")
    
    #Click the intermediate feedback 
    feedbacks_index[1].click()
    
    #Get the courses
    courses = browser.find_elements(By.CLASS_NAME,"intermediate-body")
    
    #Iterate through the courses
    for course in range(len(courses)):
        courses = browser.find_elements(By.CLASS_NAME,"intermediate-body")
        course_names = browser.find_elements(By.CSS_SELECTOR,"h6.course")
        progress_bar.progress((course)/len(courses),text=course_names[course].text+"...")  
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
            
        back = browser.find_element(By.CLASS_NAME,"overlay")
        progress_bar.progress((course+1)/len(courses),text=course_names[course].text+"...")
        browser.execute_script("arguments[0].click();",back)
    
    browser.quit()