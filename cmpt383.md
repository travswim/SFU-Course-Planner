# CMPT 383 Project

**Author**: Travis Booth <br>
**Course**: CMPT 383 - SFU <br>
**Term**: Summer 2020

---

## Project Goal

The goal of this project to allow CMPT students to find which courses are available next semester and which courses they have all the prerequisites for based on the courses they have taken.

---
## Languages

This console application uses 3 languages:

1. `python 3`: For populating the database ,doing backend calculations, and displaying information to the console
2. `bash script`: For setup, tare down, and getting user inputs
3. `C++`: For vefiying the database once it has been populated

---
## Language Communication

This console application uses 2 language communication methods:

1. Calling Functions in another language: The bash script `start.sh` calls 2 python functions. One to build the database (sqlite3), the other to calculate what courses the user can take
2. Calling an executable in another language: Once the database is built, it is verified using an executable created in C++. The C++ executable checks that the database is valid, has the appropriate columns, and has the correct number of rows. The executable is created in `start.sh`, and run in `main.py`.

---
## Setup and Running

This project is built using a docker container (Ubuntu 20.04 LTS). The `docker-compose` command must be installed beforehand.

1. Clone the repository and enter the main directory
```bash
$ git clone git@csil-git1.cs.surrey.sfu.ca:tmbooth/cmpt383-project.git
$ cd cmpt383-project
```

2. Build the docker image and run it
```bash
$ docker-compose build && docker-compose run find-course
```
3. Enter the `app/` directory
```bash
$ cd app/
```
4. Run the application
```
$ ./start.sh
```
**NOTE**: I ran into an issue where opening `start.sh` file in different OS (Going between Windows and Linux/WSL) caused the bash file to fail when executing it in the docker container. Somehow Windows changes the formating of bash scripts and which cause [this error](https://stackoverflow.com/questions/14219092/bash-script-and-bin-bashm-bad-interpreter-no-such-file-or-directory):
```bash
$ /bin/bash^M: bad interpreter: No such file or directory
```
The solution: You need to run this command before running the bash script:
```bash
$ sed -i -e 's/\r$//' start.sh
```
5. The script should automatically compile the `C++` file that verifies the database, create a new database, verify the database, then prompt the user to Find courses:
```bash
verfication information...
verfication information...
verfication information...

Operation OK!
0
Find courses you can take next semester? [y,n]
```

<a name="step6"></a>6. You can enter `n` to exit the program or `y` to build the course graph and get courses that you can take. Entering `y` will give the following output:
```bash
Adding Vertices
CMPT 102
...

Adding Edges
CMPT 102
...
CMPT 125
    CMPT 120 -> CMPT 125
...
Matched courses:
Enter a course or :q to quit:
```
7. You can then enter any `CMPT` course below the 500 level, and only `MATH` and `MACM` courses related to the SFU Computing Science undergrad degree. If you enter a course that is not in the database it will not match and won't count towards the list of taken courses. Courses need to be entered in the format `<4 letter department code (capitalized)>` + `[space]` + `<3 digit course number>`. Example: `CMPT 300`, `CMPT 225`, `MACM 101`, etc. I didn't spend too much time accounting for bad user inputs. If you enter newlines the application should disregard it. When you have entered all your courses you enter `:q` to print the results. So for example if I enter `CMPT 300` and `CMPT 225`:

```bash
Enter a course or :q to quit: CMPT 300
Enter a course or :q to quit: CMPT 225
Enter a course or :q to quit: :q
```

I should get:
```bash
Matched: CMPT 300
Matched: CMPT 225

Required: Taken

... (required courses I entered above and infered courses, see features)
...
Required: Not Taken

... (required courses I have not taken)
...

COURSES AVAILABLE IN THE FALL SEMESTER
...

```
You are then taken to [step 6](#step6) an you can run the application again or exit using `n`.

8. Teardown: You can close the docker container in another terminal using:
```bash
$ docker-compose down
```

---
## Features and Issues
Initially when scraping the [SFU Public API](http://www.sfu.ca/data-hub/api.html) I wanted to get all the course information from the API including:
1. course department
2. course number
3. credits
4. prerequisites
5. corequisites
6. equivalent courses
5. what semester the courses are offered
6. what category the courses fall under (`required`, `systems`, etc)

The main problem concerns scraping prerequisites, corequisites, and equivalent courses. There is no consistent or coherent way in which the data is posted from the API. Sometimes the corequisites are in the prerequisites field (despite having its own field!), equivalents does not have its own field, instead its shoved in with other random information in the `notes` field. It quickly became apparent that scraping all the information was futile for the amount of time I had to work on this project. I ended up partially scraping information from the API, and partially manually creating `JSON` files that would mimic a consistent API. The main `JSON` file is `cmpt383-project/app/courses.json`, and other categorical `JSON` data can be found in the `cmpt383-project/app/upperDivision/` folder. A lot of the used and attempted parsing functions can be found in `cmpt383-project/app/parsing.py`. So I guess the feature here is I use a mix of web scrapping skills and manually formating (A tasks heavily practiced in `CMPT 353` I took last year).

Other features...

1. Colour coded output:
    - Green checkmark: you can taken this course
    - Yellow X: you don't have all the prerequisites
    - Pink: header

2. Infered prerequisite courses

Suppose you are entering the courses you have taken (and are taking this semester) thus far, you don't necissarily need to input all the lower level courses. Suppose you have taken all courses up to and including `CMPT 300`. You don't need to input all of those courses:

- CMPT 120
- CMPT 125
- CMPT 127
- CMPT 225
- MACM 101

If you just input `CMPT 300`, it will infer all the prerequisites and add them to a list of taken courses.

3. Checks the next semester

The application searches for courses to take that are only available in the next semester. So if the current semester is `summer` it will look at courses only available int eh `fall`.



## External Resources
There are two main external resources I used to create this project for which I need to give a significant amount of credit:

1. [This guide](https://www.sqlitetutorial.net/sqlite-python/sqlite-python-select/) on how to connect to an `sqlite3` DB using python is mostly responsible for the code in `cmpt383-project/app/db_handle.py`.
2. [This brilliant article](https://programmingsoup.com/find-all-paths-between-two-nodes) on creating a graph in python and how to do depth first search. I created none of the code in `Vertex.py`, `Graph.py`, and `TestGraph.py` in the `cmpt383-project/app/` folder.

Everything else is my own work or mildly modified code with references commented in the file.

## Future Works

There were a lot of features that I wanted to implement, but quickly ran out of time partly due to the issues mentioned above for webscraping. The future plan to extend the work:

1. **Course Credits**<br>
Adding course credits to the database to print out the number of credits taken thus far, how many credits need to be taken towards the degree, and how many credits each course is (most are 3, but some are 4).

2. **Extending to other Departments**<br>
Adding the full list of courses for all departments, such as `ENSC`, `MEC`, `PSYC`, etc

3. **Equivalent Courses**<br>
Some courses have a lot of equivalents within and outside university departments. Being able to give credits for other courses would be useful

4. **Make it a Web Application**<br>
This seems obvious, but it I ran out of time

5. **Fix Edge Cases**
There are a few edge cases that are difficult to abstract logically, specifically related to prerequisites and corequrisites