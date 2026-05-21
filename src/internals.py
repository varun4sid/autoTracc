from bs4 import BeautifulSoup
import requests
import math

def getInternals(session: requests.Session):
    internals_url = "https://ecampus.psgtech.ac.in/studzone/ContinuousAssessment/CAMarksView"
    internals_page = session.get(internals_url)
    
    if internals_page.status_code not in [200,302]:
        raise Exception("Failed to connect to /studzone/ContinuousAssessment/CAMarksView")
    
    internals_soup = BeautifulSoup(internals_page.text, "lxml")
    content_tables = internals_soup.find_all("div", {"class":"table-responsive"})
    
    if content_tables is None:
        raise Exception("/studzone/ContinuousAssessment/CAMarksView has no content!")

    if len(content_tables) != 2:
        """
        Internal marks schema varies drastically for different courses. It is hard to process them without knowing the exact schema.
        So currently this script will support only the internals schema with which this feature was built
        """
        raise Exception("This feature is currently only supported for non-project semesters of MSc Integrated courses!")
    
    theory_table_body = content_tables[1].find("tbody")
    
    theory_table_rows = theory_table_body.find_all("tr")
    
    theory_table = []
    for row in theory_table_rows:
        record = []
        cells = row.find_all("td")
        for cell in cells:
            record.append(cell.text)
        theory_table.append(record)

    return theory_table
    
    
def getTargetScore(theory_table, target):
    result = []
    for record in theory_table:
        row = []
        row.append(record[0])
        if record[-2] in ['',' ','*']:
            row.extend(['*','*'])
        else:
            pass_score = calculateTarget(record[-2],50)
            sem_score = calculateTarget(record[-2],target)
            row.extend([record[-2],pass_score,sem_score])
            row[1] = float(row[1])
            row[1] = f'{row[1]:.2f}'
        result.append(row)
        
    return result
    

def calculateTarget(internal,final):
    # 0.8 = 0.4(internals weightage) * 2(convert /50 to /100)
    # 0.6 = (end semester exam weightage)
    internal = (float)(internal)
    final    = (float)(final)
    
    target = (final - 0.8 * internal) / 0.6
    
    if target > 100:
        return '-'
    elif target > 45:
        return math.ceil(target)
    else:
        return 45