# from bs4 import BeautifulSoup
# from pandas import DataFrame
# from .attendance import getCourseNames

# def getInternalsPage(session):
#     internals_url = "https://ecampus.psgtech.ac.in/studzone/ContinuousAssessment/CAMarksView"
    
#     internals_page = session.get(internals_url)
    
#     internals_soup = BeautifulSoup(internals_page.text, "lxml")
    
#     content_flag = internals_soup.find_all("table")
    
#     if content_flag != 2:
#         return False
    
#     #Get the rows of first table (lab courses)
    

def calculateTarget(internal,final):
    # 0.8 = 0.4(internals weightage) * 2(convert /50 to /100)
    # 0.6 = (end semester exam weightage)
    for target in range(45,101):
        if (float)(0.8 * internal) + (float)(0.6 * target) >= final:
            return target
        
    return '-'