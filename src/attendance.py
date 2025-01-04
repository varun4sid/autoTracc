def getStudentAttendance(session):
    from bs4 import BeautifulSoup

    #Get the student attendance page using the current session
    student_percentage_url = "https://ecampus.psgtech.ac.in/studzone/Attendance/StudentPercentage"
    student_percentage_page = session.get(student_percentage_url)

    #Get the html from the student attendance page
    attendance_soup = BeautifulSoup(student_percentage_page.text,"lxml")

    #Get the table element from the html
    attendance_table = attendance_soup.find("table",{"class":"table table-bordered"})

    #Get the list of table rows
    table_rows = attendance_table.find_all("tr")

    #Extract the values and append it to a list of records/rows
    data = []
    
    #Get the first row which is a header
    header = table_rows.pop(0)
    row=[]
    for cell in header.find_all("th"):
        row.append(cell.text)
    data.append(row)
    
    #Get the remaining rows
    for row in table_rows:
        record = []
        for cell in row.find_all("td"):
            record.append(cell.text)
        data.append(record)

    return data
    

def getAffordableLeaves(data):
    from pandas import DataFrame
    
    #Get custom percentage that user wants to maintain
    while True:
        try:
            custom_percentage = int(input("Enter attendance percentage you would like to maintain : "))
            if custom_percentage<0 or custom_percentage>100:
                print("Invalid input! Try again!")
            else:
                break
        except ValueError:
            print("Invalid input! Try again!")

    #Declare an empty result table with header
    result = []
    result_header = ["COURSE_ID","RECOMMENDED_LEAVES(75%)",f"AFFORDABLE_LEAVES({custom_percentage}%)"]

    #Calculate affordable leaves for each course and update result
    for i in range(1, len(data)): #index from 1 as we exclude header
        row=[data[i][0]]          #initialize row with course id
        classes_total = int(data[i][1])  #typecast attendance values to int
        classes_present = int(data[i][4])

        #Calculate the recommended(75%) and customized leaves for the user and update row
        recommended_leaves = calculateLeaves(classes_present,classes_total,75)
        custom_leaves = calculateLeaves(classes_present,classes_total,custom_percentage)

        row.extend([recommended_leaves , custom_leaves])
        result.append(row)

    df = DataFrame(result,columns=result_header)
    print(df.to_string())
    print("NOTE : '-' next to number denotes number of classes that must be attended to meet the respective percentage\n")
    

def calculateLeaves(classes_present , classes_total , maintenance_percentage):
    affordable_leaves = 0
    i=1

    #First check whether or not current attendance meets maintenance and then proceed
    if float(classes_present/classes_total)*100 < maintenance_percentage:
        while float((classes_present + i)/(classes_total + i))*100 <= maintenance_percentage:
            affordable_leaves -=1 #negative leaves denote number of unskippable classes to meet maintenance
            i+=1
    #Else block is run if maintenance is met
    else:
        while float(classes_present/(classes_total + i))*100 >= maintenance_percentage:
            affordable_leaves +=1
            i+=1

    return affordable_leaves