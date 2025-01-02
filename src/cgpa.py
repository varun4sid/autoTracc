def getCourses(session):
    from bs4 import BeautifulSoup

    #Get the courses page using the current session
    courses_page_url = "https://ecampus.psgtech.ac.in/studzone2/AttWfStudCourseSelection.aspx"
    courses_page = session.get(courses_page_url)

    #Get the html from the courses page
    courses_soup = BeautifulSoup(courses_page.text, "lxml")

    #Get the completed courses table element
    courses_table = courses_soup.find("table",{"id":"PDGCourse"})

    #Get the table rows
    table_rows = courses_table.find_all("tr")
    
    #Extract the records and values and store in list of lists
    data = []

    for row in table_rows:
        record=[]
        for cell in row.find_all("td"):
            record.append(cell.text)
        data.append(record)
    
    return data
