#!/usr/local/bin/python

from enum import Enum
from datetime import date

class Semester(Enum):
    """
    A Semester at SFU: one of spring, summer, or fall. Enum numbers correlate with DB column numbers
    """
    spring = 6
    summer = 7
    fall = 8

def currentSemester() -> Enum:
    """
    Gets the current semester for todays date

    Arguments:
        - None
    Returns:
        - A semester enum
    """
    today = date.today()
    if today.month < 5:
        return Semester.spring
    elif 5 <today.month < 9 :
        return Semester.summer
    else:
        return Semester.fall

def nextSemester() -> Enum:
    """
    Gets the next semester for todays date

    Arguments:
        - None
    Returns:
        - A semester enum
    """
    today = date.today()
    if today.month < 5:
        return Semester.summer
    elif 5 <today.month < 9 :
        return Semester.fall
    else:
        return Semester.spring