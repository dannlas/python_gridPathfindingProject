Grid generation, modification implementation and path finding algorithm integration for a web application, using Python via PyScript

This project requires a local PyScript library to run. You can download a copy of it from https://github.com/PFython/pyscript-local-runtime
You will also require VS Code and need to install Live Server and Python plugins if you have not yet already
And anything else to run python on your local machine

After that, follow the following instructions:
* Remove the popup.html file from the root directory of the pyscript library and replace it with index.html
* Replace the manifest.json file from the PyScript library with the one from this project
* Place the script.py file from the project's runtime folder directly into the PyScript runtime folder
* Remove popup.css from the PyScript project and paste this project's style.css in its place in the PyScript root directory
* Paste the image folder into the root directory of the PyScript project
* Launch the live server from the index.html file

What the project does:
* Generates a sequence of grid cells which can either represent blocked off cells, traversible cells or represent the start and end point for the navigation algorithm
* Each cell has a value asigned for it in the background to indicate how far it is from the end point which the navigation algorithm uses to find a path to it from the start point
* The pathfinding algorithm will run for up to 100 iterations to find the end point from the start point and will stop if it finds the end point or determines that there is no path to the end point

How you can interact with it:
* Clicking on individual cells will change them between traversible and being blocked off (NOTE: the outer layer of the grid must stay blocked off)
* Start position and end position can also be clicked and put elsewhere, which will be done sequentially if not start or end position cells are present right before clicking to change a cells
* Pressing the "Find" button (in the top left corner) will start the algorithm and change the displayed path to show roughly how the path finding algorithm reached its destination
* Console log information provides some more details about how the algorithm functions for finding the path

NOTE: Initially you will be able to see all possible paths overlayed, however this and any path generated later can be cleared by either:
* Clicking the "Find" button in the top left corner to restart the path finding algorithm again
* Clicking on a cell to change it
