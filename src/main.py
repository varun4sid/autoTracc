from userlogin import *
from attendance import *

studentHomePage = getHomePageAttendance()
studentData = getStudentPercentage(studentHomePage)
getAttendance(studentData)