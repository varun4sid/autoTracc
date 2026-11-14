import string


def courseAcronym(course: string):
    """
    Returns the acronym of a course name.
    Example: "Computer Networks" -> "CN"
    """
    acronym = ''
    for word in course.split():
        if word[0] in string.ascii_letters and len(word) > 2:
            acronym += word[0].upper()
    
    return acronym
