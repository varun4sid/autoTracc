from functions import *
import pandas as pd

studentHomePage = getHomePage()
studentData = getStudentPercentage(studentHomePage)
getAttendance(studentData)
