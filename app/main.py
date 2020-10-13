
import os
import json
from time import sleep
from datetime import date
#!/usr/bin/env python

from enum import Enum
from semester import Semester 
import subprocess

import db_handle
import parsing

# Adapted from: http://www.wgilpin.com/howto/howto_cython.html
def test_db():
	'''
	Verifies the DB using C++
	'''
	## Shell=False helps the process terminate
	process = subprocess.Popen("./a.out", shell=False)
	
	## Get exit codes
	out, err = process.communicate()
	errcode = process.returncode
	print(errcode)

	process.kill() 
	process.terminate()

def findCategory(course: str) -> [str]:
    """
    Parses the 'upperDivision' folder .json files and returns the categories for each file
    
    Arguments:
        - course: A course (str). Ex: CMPT 300

    Returns:
        - One of the 7 course categories (str). Ex: 'ai'
    """

    path_to_json = 'upperDivision/'
    categories = []

    # Iterate through each file in the direcotry
    for file in [file for file in os.listdir(path_to_json) if file.endswith('.json')]:

        with open(path_to_json + file) as f:
            data = json.load(f)

        # Get the header
        for courses in data:
            if courses == course:

                categories.append(file.replace('.json', ""))

                break
        
        f.close()
    if not categories:
        return None
    else:
        return categories

def main():
    """
    The main function. Creates an sqlite3 DB with course information

    Arguments:
        - None
    Returns:
        - None
    """
    # USAGE:
    # response = courseSFUAPI(2020, "summer", "101", "macm")
    # print(json.dumps(response, indent=4))

    # How to iterate through several courses
    # for courseNum in range(100, 200):
    # for i in range(100, 500):
    #     try:
    #         response = courseSFUAPI(2020, "summer", i, "cmpt")
    #         print(response["number"])
    #     except:
    #         continue

    # Check if DB already exits
    if not os.path.isfile(db_handle.database):
        # Create a db
        conn = db_handle.create_connection(db_handle.database)

        # Build the table with courses
        if conn is not None:
            db_handle.create_table(conn, db_handle.create_db)

            
        else:
            print("Error: Cannot create the database connection.")
        
        # Get courses from json file. This would normally be scraped from
        # the SFU public API but there are so many inconsistencies that it
        # was impossible to scrape automatically
        with open('courses.json') as f:
            data = json.load(f)
        
        # Populate the table
        for _, val in data.items():
            # Insert a course
            print(val['department'] + " " + val['courseNum'])

            # Need to handle prereq, coreq, and equivalent specially
            prereq = str(val['prereq'])
            if not val['prereq'] :
                prereq = None
            coreq = str(val['coreq'])
            if not val['coreq'] :
                coreq = None
            equivalent = str(val['equivalent'])
            if not val['equivalent'] :
                equivalent = None
            
            # Check what semester each course is available
            sems = {}
            for item in Semester:
                response = parsing.courseSFUAPI(2020, item.name, str(val['courseNum']), (val['department']).lower())
                try:
                    sems[item.name] = int(bool(response['sections']))
                except:
                    sems[item.name] = 0
            
            # Add value to table
            course = (val['department'], val['courseNum'], prereq, coreq, equivalent, sems[Semester.spring.name], sems[Semester.summer.name], sems[Semester.fall.name], str(findCategory(val['department'] + " " + val['courseNum'])))
            
            db_handle.create_course(conn, course)

        
    else:
        print("DB already exists")
    test_db()
        

if __name__ == "__main__":
    
    main()