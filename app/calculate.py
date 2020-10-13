#!/usr/local/bin/python

from Graph import Graph
import db_handle
from ast import literal_eval
from semester import nextSemester

# [x] TODO: Comment all Functions and clean up useless code
# [x] TODO: Make Print all courses input that have taken - infer if some are missing but have
# a higher level course taken
# [x] TODO: Print all courses that are taken/not taken that are required
# [x] TODO: Print list of all courses that you can take next semester
# [x] TODO: Print list of all courses that you cannot take and list missing prereqs
# [] TODO: BONUS add credits taken -> need to add to DB

# Taken from: https://stackoverflow.com/questions/287871/how-to-print-colored-text-in-python
class bcolors:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'



def StringToList(string: str) -> list:
    """
    Converts a list [] as type string and converts it to a list

    Arguments:
        - string: A list as a string
    returns:
        - A list parsed from a string
    """
    if string is not None:
        return literal_eval(string)
    else:
        return None

def GetCoursePath(graph: Graph(), course: str) -> list:
    """
    Takes in a graph and course and calculates the prerequirements courses to take it.

    Arguments:
        - graph: a Graph object
        - course: a course as a string. EX: "CMPT 120"

    returns:
        - The list of prerequisites to that course
    """
    lst = []
    for item in graph.getAllPaths("CMPT 120", course):
        lst += item['path']
    for item in graph.getAllPaths("MATH 151", course):
        lst += item['path']
    for item in graph.getAllPaths("MACM 101", course):
        lst += item['path']

    lst = sorted(list(set(lst)))
    lst.remove(course)
    return lst

# Build and return course graph
def CreateGraph(conn) -> Graph():
    """
    Creates a graph of all courses in SFU CS Degree

    Arguemnts:
        - conn: A DB connection
    
    Returns:
        - A Graph() object with SFU CS courses
     """
    graph = Graph()
    with conn:
        print("Adding Vertices\n")
        for row in db_handle.select_all_prereqs(conn):
            course = row[0] + " " + str(row[1])
            print(course)
            graph.add(course, course)
        print("\nAdding Edges\n")
        for row in db_handle.select_all_prereqs(conn):
            course = row[0] + " " + str(row[1])
            print(course)

            r = StringToList(row[2])
            if r is not None:
                for item in r:
                    print("\t" + item + " -> " + course)
                    graph.addEdge(item, course, 1)
            else:
                continue
    return graph

def UserCourses() -> list:
    """
    Gets courses of the user from input

    Arguments:
        - None

    Returns:
        - A list of all courses [str()] ignoring all whitespace inputs
    
    """
    courses = []
    course =''
    while course != ':q':
        course = input("Enter a course or :q to quit: ")
        

        if course != ':q':
            courses.append(course)
    return list(filter(None, courses))

def CourseMatch(conn) -> list:
    """
    Verify courses from the user input that they are in the DB

    Arguments:
        - conn: A DB connection

    Returns:
        - a list of matched courses
    """
    matched = []

    print("Matched courses: ")
    for item in UserCourses():
        courses = item.split(" ")

        row = db_handle.select_course(conn, courses[0], courses[1])
        if row is not None:
            matched.append(item)
            print("Matched: " + item)
        else:

            print("Not Matched: " + item)
    return matched

def taken_courses(courses: dict) -> list:
    lst = []
    for item in courses:
        lst.append(item)
        lst = lst + courses[item]
    return sorted(list(set(lst)))
    # print(lst)

def print_required(conn, taken: list) -> None:
    """
    Helper function to print the required courses that the user has taken or not taken

    Arguments:
        - conn: sqlite3.Connection object to a sqlite3 database
        - taken: List of taken courses by the user that are required
    Returns:
        - None
    """
    required = db_handle.select_by_category(conn, "required")
    required_list = []
    for item in required:
        required_list.append(item[1] + " " + str(item[2]))
    # Print the courses taken by the user
    print(f"\n{bcolors.HEADER}Required: Taken{bcolors.OKGREEN}")
    required_taken = list(set(taken) & set(required_list))
    for item in required_taken:
        print(item)
    # Print the courses not taken by the user
    print(f"\n{bcolors.HEADER}Required: Not Taken{bcolors.FAIL}")
    requried_not_taken = list(set(required_list) - set(taken))
    for item in requried_not_taken:
        print(item)

def next_semester_courses(conn, taken: list) -> None:
    """
    Finds and prints to stdout what courses the user can take next semester

    Arguments:
        - conn: a sqlite3.Connection object
        - taken: a list of taken courses (str)

    Returns:
        - None
    """
    course_type = ['ai', 'computingSys', 'informationSys', 'languages', 'multimedia', 'required', 'other', 'theoretical']
    course_header = ['Artificial Intelligence', 'Computing Systems', 'Information Systems', 'Languages', 'Multimedia', 'Required', 'Other', 'Theoretical']
    nSemester = nextSemester()
    print(f"\n{bcolors.HEADER}COURSES AVAILABLE IN THE {bcolors.OKBLUE}" + nSemester.name.upper() + f"{bcolors.HEADER} SEMESTER")
    for t in course_type:
        courses = db_handle.select_by_category(conn, t)
        print(f"\n{bcolors.HEADER}" + course_header[course_type.index(t)])
        for course in courses:
            
            if bool(course[nSemester.value]):

                if (course[1] + " " + str(course[2])) not in taken:
                    try:
                        missing = list(set(StringToList(course[3])) - set(taken))
                    except:
                        missing = None
                    # print(missing)
                    if not missing:
                        print(f"{bcolors.OKGREEN} \u2713 " + course[1] + " " + str(course[2]) + f"{bcolors.ENDC}")
                    else:
                        
                        print(f"{bcolors.WARNING} \u2717 " + course[1] + " " + str(course[2]) + " Prerequisite missing: " + str(missing) + f"{bcolors.ENDC}")
                else:
                    continue
            else:
                continue

def main():
    """
    The main function
    """
    conn = db_handle.create_connection(db_handle.database)
    if conn is not None:
        graph = CreateGraph(conn)
        courses = CourseMatch(conn)
        d = {}
        
        for item in courses:
            d[item] = GetCoursePath(graph, item)

        taken = taken_courses(d)

        print_required(conn, taken)
        next_semester_courses(conn, taken)


    else:
        print("Error: DB connection failed")



if __name__ == "__main__":

    # 1) user enters courses
    # 2) computer gives:
        # a) List of current courses completed
        # b) Total credits taken (need to add credits to DB)
        # c) list of required courses to take and when to take them
        # d) What courses students can take and what semester they can take them in
        # e) What courses students cannot take and what prereqs they are missing

    # a) User inputs list of courses, print out courses found in DB and Not Found
    
    main()