import json
import requests
import re
import boolean

def courseSFUAPI(year: int, semester: str, courseNum: int, department: str = "cmpt") -> str:
    """
    Calls the SFU API and returns a JSON object given the year, semester, courseNum, department.

    Args:
        year: The year of the course offering
        semester: One of: spring, summer, fall
        courseNm: The course number. Values between [100, 500)
        department: The 4 letter department code. For this project only cmpt is used

    Returns:
        A JSON object with all the course information. An example can be found in courseExample.json

    """
    
    url = "http://www.sfu.ca/bin/wcm/academic-calendar?{year}/{semester}/courses/{department}/{courseNum}"
    return json.loads(requests.get(
        url.format(year=year, semester=semester, courseNum=courseNum, department=department)).text)

def parseEquivalents(notes: str) -> tuple():
    """
    Takes the notes section of the SFU Public API, parses it, and returns
    all equivalent courses

    Arg:
        notes: The JSON attribute as a string that contains the equivalent courses

    Returns:
        A tupple, firt item is a string with the 4 letter course department (ex: CMPT, MATH, MACM)
        the second item is a list of course numbers

    """
    department = re.findall(r'[A-Z]{4}', notes)[0]
    courseNums = re.findall(r'[1-4]\d\d', notes)
    return department, courseNums

def parsePrerequisites(prerequisites: str) -> str:
    courseNums = re.findall(r'[1-4]\d\d', prerequisites)
    department = re.findall(r'[A-Z]{4}', prerequisites)
    courses = {}
    # for i in range(len(courseNums)):
    #     courses[ascii_lowercase[i]] = str(department[i] + " " + courseNums[i])
    
    # print(courses)
    prereq = str(((re.search(r'\((.*)\)', prerequisites).group()).split(courseNums[-1], 1))[0] + str(courseNums[-1]) + ")")
    # for key in courses:
    #     prereq = prereq.replace(str(courses[key]), key)
    #     print(key)

    return prereq
    # return ((re.search(r'\((.*)\)', prerequisites).group()).split(courseNums[-1], 1))[0] + str(courseNums[-1]) + ")"
    
    # courses = re.search(r'\((.*)\)', prerequisites).group()
    algebra = boolean.BooleanAlgebra()
    return algebra.parse(prereq).simplify()
  

def parseCorequisites(prerequisites: str) -> tuple:
    """
    Takes the 'prerequisites section of JSON and returns the department and course
    number of the corequisites

    Args:
        prerequisites: A string with the prerequisites and corequisites

    Returns:
        A tuple: the first item is the 4 letter department code. The second is the list of course numbers
    """
    
    if (prerequisites.find('Co-requisite') != -1):
        courses = re.findall(r'(?<=Co-requisite:).*', prerequisites)
        courses = courses[0].replace('.','')
        department = re.findall(r'[A-Z]{4}', courses)[0]
        courseNums = re.findall(r'[1-4]\d\d', courses)
        return department, courseNums

    elif (prerequisites.find('Corequisite') != -1):
        courses = re.findall(r'(?<=Corequisite).*', prerequisites)
        courses = courses[0].replace('.','')
        department = re.findall(r'[A-Z]{4}', courses)[0]
        courseNums = re.findall(r'[1-4]\d\d', courses)
        return department, courseNums
    else:
        return None, None