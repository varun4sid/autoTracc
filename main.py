from src.userlogin import *
from src.attendance import *
from src.cgpa import *

while True:
    #Display Menu
    print("#====Welcome To autoTracc!====#\nMenu :\n 1. Caluculate Attendance \n 2. Calculate CGPA \n 3. Exit")

    #Get and validate user option
    while True:
        try:
            choice = input(">")
            choice = int(choice)
            if choice in [1,2,3]:
                break
            else:
                print("Invalid input! Try again!")
        except ValueError:
            print("Invalid input! Try again!")
        

    #Execute menu option
    if choice == 1:
        studentHomePage = getHomePageAttendance()
        studentData = getStudentPercentage(studentHomePage)
        getAttendance(studentData)
    elif choice == 2:
        studentHomePage = getHomePageCGPA()
        coursesData = getCourses(studentHomePage)
        getCGPA(coursesData)
    else:
        print("Thank You!")
        break