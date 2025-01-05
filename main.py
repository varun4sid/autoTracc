from src.userlogin import *
from src.attendance import *
from src.cgpa import *

def main():
    #Get valid credentials and required student home pages
    rollno, password, attendance_home_page = checkUserInput()
    courses_home_page = getHomePageCGPA(rollno, password)
    
    #Extract the required data from the homepages
    attendance_data = getStudentAttendance(attendance_home_page)
    courses_data, completed_semester = getStudentCourses(courses_home_page)
    cgpa_data = getCGPA(courses_data, completed_semester)

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
            getAffordableLeaves(attendance_data)
        elif choice == 2:
            print(cgpa_data)
            print("NOTE : '-' denotes existing backlogs in the corresponding semester!\n")
        else:
            print("Thank You!")
            break


if __name__ == "__main__":
    main()