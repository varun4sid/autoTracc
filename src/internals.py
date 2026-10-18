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

    if len(content_tables) == 0:
        raise Exception("No internals data found in /studzone/ContinuousAssessment/CAMarksView")

    elif len(content_tables) == 1:
        # Project/Lab semester: single combined table; internals are out of 60
        theory_table_body = content_tables[0].find("tbody")
        is_lab = True

    elif len(content_tables) == 2:
        # Theory semester: first table is a header/summary, second is the theory marks table
        theory_table_body = content_tables[1].find("tbody")
        is_lab = False

    else:
        """
        Internal marks schema varies drastically for different courses. It is hard to process them without knowing the exact schema.
        So currently this script will support only schemas with 1 or 2 table-responsive divs.
        """
        raise Exception("Unsupported internals page layout — unexpected number of tables found.")
    
    theory_table_rows = theory_table_body.find_all("tr")
    
    theory_table = []
    for row in theory_table_rows:
        record = []
        cells = row.find_all("td")
        for cell in cells:
            record.append(cell.text)
        theory_table.append(record)

    return theory_table, is_lab
    
    
def getTargetScore(theory_table, target, is_lab=False):
    result = []
    for record in theory_table:
        row = []
        row.append(record[0])
        if record[-2] in ['',' ','*']:
            row.extend([0.0,'*','*'])
        else:
            if is_lab:
                pass_score = calculateTargetLab(record[-2], 50)
                sem_score  = calculateTargetLab(record[-2], target)
            else:
                pass_score = calculateTarget(record[-2], 50)
                sem_score  = calculateTarget(record[-2], target)
            row.extend([record[-2], pass_score, sem_score])
            row[1] = float(row[1])
            row[1] = f'{row[1]:.2f}'
        result.append(row)
        
    return result
    

def calculateTarget(internal, final):
    """ Theory: internal /50 contributes 40%, end sem /100 contributes 60%
     0.8 = 0.4 (internals weightage) × 2 (convert /50 to /100)
     0.6 = end semester exam weightage"""
    internal = float(internal)
    final    = float(final)
    
    target = (final - 0.8 * internal) / 0.6
    
    if target > 100:
        return '-'
    elif target > 45:
        return math.ceil(target)
    else:
        return 45


def calculateTargetLab(internal_60, final):
    """Lab/Project: Conv. Total /60 already contributes 60 marks directly;
    end sem /100 contributes the remaining 40 marks
    final = internal_60 + end_sem × 0.4  →  end_sem = (final - internal_60) / 0.4"""
    internal_60 = float(internal_60)
    final       = float(final)
    
    target = (final - internal_60) / 0.4
    
    if target > 100:
        return '-'
    elif target > 40:  # min end-sem passing threshold for lab/project
        return math.ceil(target)
    else:
        return 40