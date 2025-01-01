from userlogin import *
from attendance import *

while True:
    #Display Menu
    print("#====Welcome To autoTracc!====#\nMenu :\n 1. Caluculate Attendance \n 2. Calculate CGPA \n 3. Exit")

    #Get and validate user option
    while True:
        choice = int(input(">"))
        if choice not in [1,2,3]:
            print("Invalid option! Try again!")
        else:
            break

    #Execute menu option
    if choice == 1:
        studentHomePage = getHomePageAttendance()
        studentData = getStudentPercentage(studentHomePage)
        getAttendance(studentData)
    if choice == 2:
        getHomePageCGPA()
    else:
        print("Thank You!")
        break