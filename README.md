<h1> Sample Roombooking Program to Reserve a Study Room</h1>

This is a python program that allows students to book study rooms available at Sheridan College using the terminal. This program creates the necessary requests to book study rooms wihtout having to use the website.

DISCLAMER: This is NOT an offical Sheridan program, use at own risk and within the School's Roombooking policy.

<h2> Requirements </h2>

- Python 3
- pip
- make (to install required packages or can be manually done)

<h2> Setup </h2>

- 'make create' to install requirements on global python install
- 'make createvirt' to create virtual environment and install requirements
- create the 'config.yml' file and enter your credentials

<h2> Execution </h2>

To execute program run 'python -m BookRoom' in the same directory as the README.md

<b>-h, --help</b>           show this help message and exit </br>
<b>--room ROOM, -r ROOM</b>  The room you want to book. Optional </br>
<b>--date DATE, -d DATE</b>  Pass the date of the room booking either as an absolute date 'YYYY/MM/DD' or relative date specified by python's dateparser package</br>
<b>--starttime STARTTIME, -t STARTTIME</b> start time of room book. valid format is hh:mm[am,pm] </br>
<b>--duration {30,60,90,120}, -period {30,60,90,120}, -p {30,60,90,120}</b> Duration to reserve the room. </br>
<b>--config CONFIG, -c CONFIG</b> path to load conifiguration file. default is config.yaml </br>
<b>-l {DEBUG,INFO,WARNING,ERROR,CRITICAL}, --log {DEBUG,INFO,WARNING,ERROR,CRITICAL}  </b> Set the logging level  </br>

<h2> Examples </h2>
  - command passing room to book for the next day
  python -m BookRoom -r 'C138A' -d tomorrow -t '2:00pm' -p 30
  
  - command to return available rooms for next week
  python -m BookRoom -d 'in 1 week' -t '2:00pm' -p 30
  
  - command to return available rooms for specific date
  python -m BookRoom -r 'C138A' -d '2020/01/16' -t '2:00pm' -p 30
  
