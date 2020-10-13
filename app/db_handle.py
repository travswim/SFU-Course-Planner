#!/usr/local/bin/python
import sqlite3

# All functions adapted from: https://www.sqlitetutorial.net/sqlite-python/sqlite-python-select/

database = "courses.db"

create_db = """CREATE TABLE IF NOT EXISTS course (
                id integer PRIMARY KEY AUTOINCREMENT,
                department text NOT NULL,
                number integer NOT NULL,
                prerequisite text,
                corequisite text,
                equivalent text,
                spring bool,
                summer bool,
                fall bool,
                category text

                
            );"""

# Taken from: https://www.sqlitetutorial.net/sqlite-python/create-tables/
def create_connection(db_file: str) -> sqlite3.Connection:
    """ 
    Creates a database connection to the SQLite database

    Arguments:
        - db_file: A database file

    Return:
        - Connection object or None
    """
    conn = None
    try:
        conn = sqlite3.connect(db_file)
        return conn
    except RuntimeError as e:
        print(e)

    return conn


def create_table(conn: sqlite3.Connection, create_table_sql):
    """ Creates a table from the create_table_sql statement
    Arguments:
        - conn: A connection object
    :param create_table_sql: a CREATE TABLE statement
    :return:
    """
    try:
        c = conn.cursor()
        c.execute(create_table_sql)
    except RuntimeError as e:
        print(e)

def create_course(conn, project):
    """
    Create a new project into the projects table
    :param conn:
    :param project:
    :return: project id
    """
    sql = ''' INSERT INTO course(department,number,prerequisite,corequisite,equivalent,spring,summer,fall,category)
              VALUES(?,?,?,?,?,?,?,?,?) '''
    cur = conn.cursor()
    cur.execute(sql, project)
    conn.commit()
    return cur.lastrowid

def select_all_prereqs(conn: sqlite3.Connection):
    """
    Query the prerequisites
        
    Arguments:
        - conn: the Connection object
    
    Return:
        - All matching prerequisites for each course
    """
    cur = conn.cursor()
    cur.execute("SELECT department, number, prerequisite FROM course")

    rows = cur.fetchall()
    return rows
    # for row in rows:
    #     print(row[2])

def select_course(conn: sqlite3.Connection, department: str, number: int):
    """
    Queries the DB for a specific course

    Arguments:
        - conn: the Connection object
        - department: course department
        - number: course number

    Returns:
        - the first querry
    """
    cur = conn.cursor()
    select = "SELECT * FROM course WHERE department = '{0}' AND number = {1}".format(department, number)
    # print(select)
    cur.execute(select)
    rows = cur.fetchall()
    if rows:
        return rows[0]
    else:
        return None

def select_by_category(conn: sqlite3.Connection, category: str):
    """
    Select by courses by category

    Arguments:
         - conn: the Connection object
         - category: a category of course

    Returns:
        - Query information


    """
    cur = conn.cursor()
    select = "SELECT * FROM course WHERE category LIKE '%{0}%'".format(category)
    cur.execute(select)
    rows = cur.fetchall()
    if rows:
        return rows
    else:
        return None


