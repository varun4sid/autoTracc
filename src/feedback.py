from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import StaleElementReferenceException
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


def autoFeedback(index,rollno,password):
    #Create a webdriver
    progress_bar = st.progress(0,text = "Fetching feedback page...")
    browser = createDriver()
    wait = WebDriverWait(browser,10)
    
    browser.get("https://ecampus.psgtech.ac.in/studzone")
    
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
    feedback_card = wait.until(EC.element_to_be_clickable((By.XPATH,f"//h5[text()='Feedback']")))
    browser.execute_script("arguments[0].scrollIntoView();arguments[0].click();",feedback_card)
    
    wait.until(EC.element_to_be_clickable((By.CLASS_NAME,"card-body")))
    feedbacks = browser.find_elements(By.CLASS_NAME,"card-body")
    
    #Click the desired feedback
    browser.execute_script("arguments[0].click();",feedbacks[index])
    
    progress_bar.empty()
    if index == 0:
        endsemForm(browser)
    else:
        intermediateForm(browser)
        
    
    
def intermediateForm(browser):
    progress_bar = st.progress(0,text = "Fetching feedback page...")
    
    #Get the courses
    courses = browser.find_elements(By.CLASS_NAME,"intermediate-body")

    if len(courses) == 0:
        progress_bar.empty()
        raise
    
    #Instantiate a wait sequence for page rendering
    wait = WebDriverWait(browser,10)
    
    #Iterate through the courses
    for course in range(len(courses)):
        courses = browser.find_elements(By.CLASS_NAME,"intermediate-body")
        course_names = browser.find_elements(By.CSS_SELECTOR,"h6.course")
        progress_bar.progress((course)/len(courses),text=course_names[course].text+"...")  
        browser.execute_script("arguments[0].scrollIntoView(); arguments[0].click();", courses[course])
        
        questions = browser.find_element(By.CSS_SELECTOR,"div.bottom-0").text
        questions = int(questions.split()[-1])
        
        clicks = 0
        while clicks < questions:
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
    progress_bar.empty()
    st.markdown("##### Done! Check your [studzone](https://ecampus.psgtech.ac.in/studzone)!")
    
    
def endsemForm(browser):
    progress_bar = st.progress(0,text = "Fetching feedback page...")
    
    wait = WebDriverWait(browser,10)
    try:
        wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR,"div.staff-item")))
    except:
        raise
        
    staffList = browser.find_elements(By.CSS_SELECTOR,"div.staff-item")
    
    for staff in range(len(staffList)):
        wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR,"div.staff-item")))
        staffList = browser.find_elements(By.CSS_SELECTOR,"div.staff-item")
        browser.execute_script("arguments[0].scrollIntoView();arguments[0].click()", staffList[staff])
        
        wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR,"span.ms-1")))
        course_name = browser.find_elements(By.CSS_SELECTOR,"span.ms-1")[1].text
        progress_bar.progress( (staff/len(staffList)), text = course_name+"...")
        wait.until(EC.element_to_be_clickable((By.XPATH,"//tbody[@id='feedbackTableBody']/tr[1]/td[@class='rating-cell']/div[@class='star-rating']/label[1]")))
        
        review_list = browser.find_elements(By.CSS_SELECTOR,"td.question-cell")
        for count in range(1,len(review_list)+1):
            star_button = browser.find_element(By.XPATH,f"//tbody[@id='feedbackTableBody']/tr[{count}]/td[@class='rating-cell']/div[@class='star-rating']/label[1]")
            browser.execute_script("arguments[0].scrollIntoView();arguments[0].click()",star_button)
        
        submit_button = browser.find_element(By.ID,"btnSave")
        browser.execute_script("arguments[0].scrollIntoView();arguments[0].click()", submit_button)
        wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR,"img.img-fluid")))
        progress_bar.progress( ((staff+1)/len(staffList)), text = course_name+"...")
        
    final_submit_button = browser.find_element(By.ID,"btnFinalSubmit")
    browser.execute_script("arguments[0].scrollIntoView();arguments[0].click()",final_submit_button)
    
    browser.quit()
    progress_bar.empty()
    st.markdown("##### Done! Check your [studzone](https://ecampus.psgtech.ac.in/studzone)!")