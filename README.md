# SolarSorter
For our Robotics Minor, we have a project at a local company where we need to automate the sorting/grading of solar cells using vision, a robot, a plc and a hmi.

Solar cells will be present in plastic trays with a maximum of 12 cells per tray. These cells are very fragile, so we created an end-of-arm tool for the robot with two small suction cups connected to a compressed air connection via a vacuum generator, to be able to move the cells carefully while grading them.
Each cell has a data matrix on the back side containing the 11 digit serial number of that cell. Its grade/classification can be found in an Excel sheet and while combining that information, we can instruct the robot to move the cell to the output tray with only cells of the same grade.
The system follows a sequential flow and is able to display many safety different safety warnings, if applicable.

The project consists of the following devices:
- A FW03N Kawasaki robot
- Two Cognex 7200 series cameras
- A S7-1200 PLC controller
- A KTP700 HMI screen
- A computer with Python 3.8

In that, the PLC will control the following subdevices:
- LED RGB strip
- Orange flashing light
- Vacuum generator
- Red Klaxon Sonos Alarm/buzzer

The group consists of four students:
- David (linkedin)
- Dylan (linkedin)
- Frits (linkedin)
- Lex (linkedin)

Webpage robotics minor: https://www.robotminor.nl/<br>
Final demo video (1 min): *Expected nov 2020*
