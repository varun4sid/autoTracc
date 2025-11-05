from bs4 import BeautifulSoup
from .attendance import getCourseNames
import math

def getInternals(session):
    internals_url = "https://ecampus.psgtech.ac.in/studzone/ContinuousAssessment/CAMarksView"
    
    internals_page = session.get(internals_url)
    internals_soup = BeautifulSoup(internals_page.text, "lxml")
    
    content_tables = internals_soup.find_all("table")

    #Check for the presence of both the tables
    if len(content_tables) != 2:
        return False
    
    # lab_table = content_tables[0]
    theory_table_body = content_tables[1].find("tbody")
    
    theory_table_rows = theory_table_body.find_all("tr")
    
    course_map = getCourseNames(session)
    
    #Get the theory internal marks in the form of list
    theory_table = []
    for row in theory_table_rows:
        record = []
        cells = row.find_all("td")
        for cell in cells:
            record.append(cell.text)
        try:
            record[0] = ''.join( [ record[0], '   -   ', course_map[record[0]] ] )
        except KeyError:
            continue
        theory_table.append(record)

    return theory_table
    
    
def getTargetScore(theory_table, target):
    #Check for temporary/final mark entry
    final = True
    for record in theory_table:
        if record[-1] == '*':
            final = False
            break
    
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
            if not final:
                row[1] = f'{row[1]}*'
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