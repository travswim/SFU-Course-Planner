# SFU Course Planner

**Author**: Travis Booth <br>
**Course**: CMPT 383 - SFU <br>
**Term**: Summer 2020

---

## Project Description: CMPT Course Scheduler

This console application is used to help undergrad computing science students plan courses to take in the next semester. The full details of this project including setup and running can be found in [cmpt383.md](cmpt383.md).

## TLDR

Run the following series of commands to get up and running:

```bash
$ git clone git@csil-git1.cs.surrey.sfu.ca:tmbooth/cmpt383-project.git
$ cd cmpt383-project
$ docker-compose build && docker-compose run find-course
$ cd app/
$ sed -i -e 's/\r$//' start.sh
$ ./start.sh
```

