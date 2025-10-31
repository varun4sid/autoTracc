from bs4 import BeautifulSoup
from pandas import DataFrame

# Cache for course names to avoid redundant API calls
_course_names_cache = {}

def clearCourseNamesCache():
    """
    Clear the course names cache. Useful for freeing memory after session ends.
    """
    global _course_names_cache
    _course_names_cache.clear()

def getStudentAttendance(session):
    #Get the student attendance page using the current session
    student_percentage_url = "https://ecampus.psgtech.ac.in/studzone/Attendance/StudentPercentage"
    student_percentage_page = session.get(student_percentage_url)

    #Get the html from the student attendance page
    attendance_soup = BeautifulSoup(student_percentage_page.text,"lxml")

    #Get the table element from the html
    attendance_table = attendance_soup.find("table",{"id":"example"}).find("tbody")

    #Get the list of table rows
    table_rows = attendance_table.find_all("tr")

    #Get the mapping of course code to course name's initials
    course_map = getCourseNames(session)

    #Extract the values and append it to a list of records/rows
    data = []

    for row in table_rows:
        record = []
        for cell in row.find_all("td"):
            record.append(cell.text)
        try:
            # Use f-string for more efficient string formatting
            record[0] = f"{record[0]}   -   {course_map[record[0]]}"
        except KeyError:
            continue
        data.append(record)
        
    return data


def getCourseNames(session):
    """
    Get course names with caching to avoid redundant API calls.
    Uses session object ID as cache key for session-specific caching.
    """
    # Use session ID as cache key to avoid cross-session contamination
    cache_key = id(session)
    
    # Return cached data if available
    if cache_key in _course_names_cache:
        return _course_names_cache[cache_key]
    
    #Find the course details page url
    courses_url = "https://ecampus.psgtech.ac.in/studzone/Attendance/courseplan"

    #Get the course details page
    courses_page = session.get(courses_url)

    #Get the html of the course details page
    courses_soup = BeautifulSoup(courses_page.text, "lxml")

    #Get the list of div elements containing course details of each course
    courses = courses_soup.find_all("div",{"class":"col-md-8"})

    #Create an empty dictionary
    course_map = {}

    #Iterate through the list of divs to get the contents
    for course in courses:
        course_code = course.find("h5")
        course_name = course.find("h6")

        #Build course initials more efficiently using list comprehension and direct range check
        course_initials = [
            word[0] for word in course_name.text.split() 
            if word and 65 <= ord(word[0]) <= 90  # 'A' to 'Z' range check without creating list
        ]

        #Convert the list of initials to string and map it to the course code
        course_map[course_code.text] = ''.join(course_initials)

    # Cache the result for future use
    _course_names_cache[cache_key] = course_map
    
    return course_map


def getAffordableLeaves(data,custom_percentage):
    #Declare an empty result table
    result = []

    #Calculate affordable leaves for each course and update result
    for i in range(len(data)):
        row=[data[i][0]]                #initialize row with course id
        classes_total = int(data[i][1])  #typecast attendance values to int
        classes_present = int(data[i][4])

        #Calculate the customized leaves for the user and update row
        custom_leaves = calculateLeaves(classes_present,classes_total,custom_percentage)

        #Update the row with calculated leaves
        row.append(custom_leaves)
        result.append(row)

    #Create a dataframe from the result list with headers
    result_header = ["COURSE_CODE",f"AFFORDABLE_LEAVES({custom_percentage}%)"]
    df = DataFrame(result,columns=result_header)

    return df
    

def calculateLeaves(classes_present , classes_total , maintenance_percentage):
    """
    Calculate affordable leaves using direct mathematical formula instead of simulation.
    This is significantly faster than iterative simulation, especially for large differences.
    """
    # Convert to percentage threshold (e.g., 75% -> 0.75)
    threshold = maintenance_percentage / 100.0
    
    # Current attendance percentage
    current_percentage = classes_present / classes_total if classes_total > 0 else 0
    
    # If current attendance is below maintenance
    if current_percentage < threshold:
        # Calculate classes needed to attend to meet maintenance
        # Formula: (present + x) / (total + x) >= threshold
        # Solving: present + x >= threshold * (total + x)
        # present + x >= threshold * total + threshold * x
        # x - threshold * x >= threshold * total - present
        # x * (1 - threshold) >= threshold * total - present
        # x >= (threshold * total - present) / (1 - threshold)
        if threshold < 1:
            classes_needed = (threshold * classes_total - classes_present) / (1 - threshold)
            return -int(classes_needed) if classes_needed > 0 else 0
        else:
            return 0
    else:
        # Calculate leaves that can be taken while maintaining threshold
        # Formula: present / (total + x) >= threshold
        # Solving: present >= threshold * (total + x)
        # present >= threshold * total + threshold * x
        # present - threshold * total >= threshold * x
        # x <= (present - threshold * total) / threshold
        if threshold > 0:
            leaves = (classes_present - threshold * classes_total) / threshold
            return int(leaves)
        else:
            return classes_total  # Can skip all if no maintenance required
    
    return 0