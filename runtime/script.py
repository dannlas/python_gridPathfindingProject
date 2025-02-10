###################################################
# Grid generation, modification implementation and path finding algorithm integration for a web application, using Python via PyScript
###################################################
# type: ignore

from pyodide.ffi import create_proxy

# Directory inputs
imgDirectory = "img/"

# Initial output section
print(f"<div id='outputDiv'><div id='outputContentsDiv' style='min-width: 1500px;'></div><div id='outputDrawDiv' style='min-width: 1500px;'></div></div>")
gridCells = ["1", "1", "1", "1", "1", "1", "1", "1", "1", "1", "1", "1",
            "1", "S", "0", "1", "x", "0", "0", "0", "0", "0", "0", "1",
            "1", "0", "0", "1", "1", "1", "1", "1", "1", "1", "0", "1",
            "1", "1", "0", "0", "0", "1", "1", "0", "0", "1", "0", "1",
            "1", "1", "0", "0", "0", "1", "1", "0", "0", "1", "0", "1",
            "1", "1", "0", "0", "0", "1", "1", "0", "0", "1", "0", "1",
            "1", "1", "0", "0", "0", "0", "0", "0", "0", "0", "0", "1",
            "1", "1", "1", "1", "1", "1", "1", "1", "1", "1", "1", "1"]
nonDiagonalNavGridValues = [] # Values to store for a pathfinding algorithm that does not allow diagonal movement between traversible cells (TO IMPLEMENT)
diagonalNavGridValues = [] # Values to store for a pathfinding algorithm that allows diagonal movement between traversible cells
cellIntersections = [] # Intersection type logging, C = no intersection, H = horizontal intersection, V = vertical intersection, D = diagonal intersection
navigationRoute = []

# Important and reusable global values
startPosition = -1
endPosition = -1
width = 12
diagonalNavigation = True

# Button event function for executing the pathfinding function
def executePathfindingAlgorithm(e):
    global navigationRoute

    disperseNonDiagonalNavigationAlgorithmValues()
    disperseDiagonalNavigationAlgorithmValues()
    pathfindToEndPoint()
    drawPath()
    navigationRoute = []
    console.log("diagonalNavGridValues: " + str(diagonalNavGridValues))

# Any event listeners that are not generated dynamically
def addStaticEventListeners():
    proxy_func = create_proxy(executePathfindingAlgorithm)
    document.getElementById("runApplic").addEventListener("click", proxy_func)

# TO IMPLEMENT: Display an intersection for the path taken when trying to reach the end point
def drawPath():
    global width
    global navigationRoute
    global cellIntersections
    intersectionElements = document.getElementsByClassName("cellIntersection")
    for intersectedElement in intersectionElements:
        intersectedElement.style.visibility = "hidden"

    horizontalIntersectionElements = document.getElementsByClassName("intersectionHorizontal")
    verticalIntersectionElements = document.getElementsByClassName("intersectionVertical")
    diagonalIntersectionElements1 = document.getElementsByClassName("intersectionDiagonal1")
    diagonalIntersectionElements2 = document.getElementsByClassName("intersectionDiagonal2")

    currentCellIndex = 0
    pathfindConditions = []
    for navigatedCell in navigationRoute:
        if(currentCellIndex +1 < len(navigationRoute)):
            if(abs(navigationRoute[currentCellIndex] - navigationRoute[currentCellIndex +1]) == 1 and navigationRoute[currentCellIndex] < navigationRoute[currentCellIndex +1]):
                horizontalIntersectionElements[navigationRoute[currentCellIndex]].style.visibility = "visible"
                pathfindConditions.append("H1")

            elif(abs(navigationRoute[currentCellIndex] - navigationRoute[currentCellIndex +1]) == 1 and navigationRoute[currentCellIndex] > navigationRoute[currentCellIndex +1]):
                horizontalIntersectionElements[navigationRoute[currentCellIndex +1]].style.visibility = "visible"
                pathfindConditions.append("H2")

            elif(abs(navigationRoute[currentCellIndex] - navigationRoute[currentCellIndex +1]) == width and navigationRoute[currentCellIndex] < navigationRoute[currentCellIndex +1]):
                verticalIntersectionElements[navigationRoute[currentCellIndex]].style.visibility = "visible"
                pathfindConditions.append("V1")

            elif(abs(navigationRoute[currentCellIndex] - navigationRoute[currentCellIndex +1]) == width and navigationRoute[currentCellIndex] > navigationRoute[currentCellIndex +1]):
                verticalIntersectionElements[navigationRoute[currentCellIndex +1]].style.visibility = "visible"
                pathfindConditions.append("V2")

            elif(abs(navigationRoute[currentCellIndex] - navigationRoute[currentCellIndex +1]) == (width -1) and navigationRoute[currentCellIndex] > navigationRoute[currentCellIndex +1]):
                diagonalIntersectionElements1[(navigationRoute[currentCellIndex +1] -1)].style.visibility = "visible"
                pathfindConditions.append("D1")

            elif(abs(navigationRoute[currentCellIndex] - navigationRoute[currentCellIndex +1]) == (width -1) and navigationRoute[currentCellIndex] < navigationRoute[currentCellIndex +1]):
                diagonalIntersectionElements1[(navigationRoute[currentCellIndex] -1)].style.visibility = "visible"
                pathfindConditions.append("D2")

            elif(abs(navigationRoute[currentCellIndex] - navigationRoute[currentCellIndex +1]) == (width +1) and navigationRoute[currentCellIndex] > navigationRoute[currentCellIndex +1]):
                diagonalIntersectionElements2[navigationRoute[currentCellIndex +1]].style.visibility = "visible"
                pathfindConditions.append("D3")

            elif(abs(navigationRoute[currentCellIndex] - navigationRoute[currentCellIndex +1]) == (width +1) and navigationRoute[currentCellIndex] < navigationRoute[currentCellIndex +1]):
                diagonalIntersectionElements2[navigationRoute[currentCellIndex]].style.visibility = "visible"
                pathfindConditions.append("D4")

        currentCellIndex += 1


    console.log("pathfindConditions: " + str(pathfindConditions))
    console.log("path drawn!")

# TO IMPLEMENT: Method for hiding the drawn path elements
def resetPathDraw():
    imageElements = document.getElementById("outputDrawDiv").getElementsByTagName("img")
    for imageElement in imageElements:
        imageElement.style.visibility = "hidden"
    console.log("drawn path reset!")

# Cell type change on clicking it
# Priority being given to the start position ("S") in YELLOW, which will override the cell if not present
# Then the same for the end position ("x" or "X") in RED
# And finally Inverting between a blocked off (1 or "I") in GRAY and a traversible cell (0 or "O") in WHITE

# Not entirely sure how to pass arguments to an addEvenetListener function with pyscript
# Luckily in this scenario the default event object parameter provides a way to access the clicked buton's id through event.target.id
def gridButtonClick(e): #, *args, **kwargs
    resetPathDraw()
    
    global startPosition
    global endPosition
    global navigationRoute

    navigationRoute = []

    elementID = str(e.target.id)
    element = document.getElementById(elementID)

    idNumber = elementID
    idNumber = idNumber.replace("cell", "", -1)

    if(startPosition < 0):
        element.innerHTML = "S"
        element.style.backgroundColor = "yellow"
        endPositionButtons = document.getElementsByClassName("endPositionButton")
        if endPositionButtons and endPositionButtons[0].id == element.id:
            endPositionButtons[0].classList.remove("endPositionButton")
        element.classList.add("startPositionButton")
        startPosition = int(idNumber)
        if(startPosition == endPosition):
            endPosition = -1
        gridCells[int(idNumber)] = "S"
    elif(endPosition < 0):
        element.innerHTML = "X"
        element.style.backgroundColor = "red"
        startPositionButtons = document.getElementsByClassName("startPositionButton")
        if startPositionButtons and startPositionButtons[0].id == element.id:
            startPositionButtons[0].classList.remove("startPositionButton")
        element.classList.add("endPositionButton")
        endPosition = int(idNumber)
        if(endPosition == startPosition):
            startPosition = -1
        gridCells[int(idNumber)] = "x"
    elif(element.innerHTML == "O"):
        element.innerHTML = "I"
        element.style.backgroundColor = "gray"
        gridCells[int(idNumber)] = "1"
    elif(element.innerHTML == "S"):
        element.classList.remove("startPositionButton")
        element.innerHTML = "O"
        element.style.backgroundColor = "white"
        startPosition = -1
        gridCells[int(idNumber)] = "0"
    elif(element.innerHTML == "X"):
        element.classList.remove("endPositionButton")
        element.innerHTML = "O"
        element.style.backgroundColor = "white"
        endPosition = -1
        gridCells[int(idNumber)] = "0"
    else:
        element.innerHTML = "O"
        element.style.backgroundColor = "white"
        gridCells[int(idNumber)] = "0"


def generateGridAssembly(new_grid_list):
    cellButtons = document.getElementsByClassName("cellButton")
    for cellButton in cellButtons:
        cellButtonID = cellButton.id
        document.getElementById(cellButtonID).removeEventListener("click", create_proxy(gridButtonClick(cellButtonID)))
        document.getElementById(cellbuttonID).removeEventListener("click", gridButtonClick(cellButtonID))

    outputContentsDiv = document.querySelector("#outputContentsDiv")
    outputContentsDiv.innerHTML = ""

    gridList = new_grid_list

    startPositionSet = False
    endPositionSet = False

    global startPosition
    global endPosition
    global width
    startPosition = 0
    endPosition = 0

    readWidth = 0
    gridString = ''

    # Allocation of inserted grid elements
    divCellBlockStart = "<div style='display: inline;'>"
    cellBlock = ""
    divCellBlockEnd = "</div>"
    cellIndex = 0
    for cell in gridList:
        gridString += divCellBlockStart
        match(cell):
            case "0":
                cellBlock = "<button id='cell" + str(cellIndex) + "' class='cellButton' style='min-width: 100px; min-height: 100px; background-color: white; color: black;'>"
                cellBlock += "O"
                cellBlock += "</button>"
            case "1":
                cellBlock = "<button id='cell" + str(cellIndex) + "' class='cellButton' style='min-width: 100px; min-height: 100px; background-color: gray; color: black;'>"
                cellBlock += "I"
                cellBlock += "</button>"
            case "S":
                cellBlock = "<button id='cell" + str(cellIndex) + "' class='cellButton startPositionButton' style='min-width: 100px; min-height: 100px; background-color: yellow; color: black;'>"
                cellBlock += "S"
                cellBlock += "</button>"
                startPositionSet = True
            case "x":
                cellBlock = "<button id='cell" + str(cellIndex) + "' class='cellButton endPositionButton' style='min-width: 100px; min-height: 100px; background-color: red; color: black;'>"
                cellBlock += "X"
                cellBlock += "</button>"
                endPositionSet = True
            case __:
                cellBlock = "<button id='cell" + str(cellIndex) + "' class='cellButton' style='min-width: 100px; min-height: 100px; background-color: black; color: black;'>"
                cellBlock += "Q"
                cellBlock += "</button>"
                
        gridString += cellBlock
        gridString += divCellBlockEnd
        readWidth += 1

        if(readWidth >= width):
            gridString += "<br>" #"\n"
            readWidth = 0

        if(startPositionSet != True):
            startPosition += 1
        
        if(endPositionSet != True):
            endPosition += 1

        cellIndex += 1

    outputContentsDiv.innerHTML = gridString

    cellButtons = document.getElementsByClassName("cellButton")
    for cellButton in cellButtons:
        cellButtonID = cellButton.id
        proxy_func = create_proxy(gridButtonClick)
        document.getElementById(cellButtonID).addEventListener("click", proxy_func)

    console.log("startPosition: " + str(startPosition))
    console.log("endPosition: " + str(endPosition))


# Method for assigning non-diagonal navigation values (using end point as the anchor) - yet to implement algorithmically
# For non-diagonal navigation, distance values must be assigned radially as though diagonal navigation is permitted
def disperseNonDiagonalNavigationAlgorithmValues(): 
    resetPathDraw()
    
    global gridCells
    global nonDiagonalNavGridValues
    global endPosition
    global width

    nonDiagonalNavGridValues = []
    
    xEndPosition = (endPosition % width)
    yEndPosition = (endPosition / width)
    
    gridCellIndex = 0
    gridXIndex = 0
    gridYIndex = 0
    cellRingIndex = 0
    for gridCell in gridCells:
        xCurrentEndPosition = int(xEndPosition) - gridXIndex
        yCurrentEndPosition = int(yEndPosition) - gridYIndex

        if(xCurrentEndPosition < 0):
            xCurrentEndPosition = abs(xCurrentEndPosition)
        if(yCurrentEndPosition < 0):
            yCurrentEndPosition = abs(yCurrentEndPosition)

        cellRingIndex = xCurrentEndPosition + yCurrentEndPosition
        diagonalNavGridValues.append(cellRingIndex)
        gridCellIndex += 1

        gridXIndex += 1
        if(gridXIndex >= width):
            gridXIndex = 0
            gridYIndex += 1
        
    console.log("nonDiagonalNavGridValues: " + str(nonDiagonalNavGridValues))


# Method for assigning diagonal navigation values (using end point as the anchor)
# For diagonal navigation, distance values must be assigned radially as though diagonal navigation is not permitted
def disperseDiagonalNavigationAlgorithmValues():
    global gridCells
    global diagonalNavGridValues
    global endPosition
    global width

    diagonalNavGridValues = []

    xEndPosition = (endPosition % width)
    yEndPosition = (endPosition / width)

    gridCellIndex = 0
    gridXIndex = 0
    gridYIndex = 0
    cellRingIndex = 0
    for gridCell in gridCells:
        xCurrentEndPosition = int(xEndPosition) - gridXIndex
        yCurrentEndPosition = int(yEndPosition) - gridYIndex

        if(xCurrentEndPosition < 0):
            xCurrentEndPosition = abs(xCurrentEndPosition)
        if(yCurrentEndPosition < 0):
            yCurrentEndPosition = abs(yCurrentEndPosition)

        cellRingIndex = yCurrentEndPosition
        if(xCurrentEndPosition > yCurrentEndPosition):
            cellRingIndex = xCurrentEndPosition
        diagonalNavGridValues.append(cellRingIndex)
        gridCellIndex += 1

        gridXIndex += 1
        if(gridXIndex >= width):
            gridXIndex = 0
            gridYIndex += 1
        
    console.log("diagonalNavGridValues: " + str(diagonalNavGridValues))

    

# Method for the path finding algorithm, accounts for blocked off sections and whether the path to end point is possible
# Has a limit on possible navigation iterations before the algorithm stops (maxTraversalIterations variable)
# TO UPDATE: Add backtracking (important), investigate possible solutions for edge checking (optional)
def pathfindToEndPoint():
    global gridCells
    global startPosition
    global endPosition
    global width
    global diagonalNavigation
    global navigationRoute

    backtrack = False
    trackIndex = 0
    maxTrackIndex = 0
    navGridValues = []
    lowestNavGridValue = 100

    if(diagonalNavigation):
        navGridValues = diagonalNavGridValues
    else:
        navGridValues = nonDiagonalNavGridValues

    currentPosition = startPosition
    navigationRoute.append(currentPosition)

    maxTraversalIterations = 100
    
    if(diagonalNavigation):
        while(maxTraversalIterations > 0):
            if(currentPosition != endPosition):
                nextCell = currentPosition

                navigated = False
                checkCondition = currentPosition +1

                # Checks for whether the cells are actually present
                # And whether the position is not selecting a negative value, which would be out of bounds or create wrapping issues
                if(navGridValues[checkCondition] >= 0 and gridCells[checkCondition] and checkCondition >= 0):
                    #Checks a conditional that would allow wrapping around the grid otherwise
                    # It appears there are multiple of these conditions that would be difficult to account for
                    # So the better solution was to wrap the entire grid around with blocked cells
                    # This makes the following conditional check redundant
                    if(not (abs(currentPosition - checkCondition) < 8 and abs(currentPosition - checkCondition) > 1)): 
                        # Checks whether the next cell grid value is less than the lowest value found
                        # (their distrance from end position)
                        # And whether the cell value is not of wall type
                        if(navGridValues[checkCondition] < lowestNavGridValue and gridCells[checkCondition] != "1"):
                            # Checks whether the route has already been navigated before
                            for navigatedCell in navigationRoute:
                                if(navigatedCell == checkCondition):
                                    navigated = True

                            # Updates the lowest navigation grid value found and next cell to navigate to the current conditional
                            # If it has not already been navigated
                            if(navigated == False):
                                lowestNavGridValue = navGridValues[checkCondition]
                                nextCell = checkCondition

                navigated = False
                checkCondition = (currentPosition -width) +1
                if(navGridValues[checkCondition] >= 0 and gridCells[checkCondition] and checkCondition >= 0):
                    if(not (abs(currentPosition - checkCondition) < 8 and abs(currentPosition - checkCondition) > 1)):
                        if(navGridValues[checkCondition] < lowestNavGridValue and gridCells[checkCondition] != "1"):
                            for navigatedCell in navigationRoute:
                                if(navigatedCell == checkCondition):
                                    navigated = True

                            if(navigated == False):
                                lowestNavGridValue = navGridValues[checkCondition]
                                nextCell = checkCondition

                navigated = False
                checkCondition = currentPosition -width
                if(navGridValues[checkCondition] >= 0 and gridCells[checkCondition] and checkCondition >= 0):
                    if(not (abs(currentPosition - checkCondition) < 8 and abs(currentPosition - checkCondition) > 1)):
                        if(navGridValues[checkCondition] < lowestNavGridValue and gridCells[checkCondition] != "1"):
                            for navigatedCell in navigationRoute:
                                if(navigatedCell == checkCondition):
                                    navigated = True

                            if(navigated == False):
                                lowestNavGridValue = navGridValues[checkCondition]
                                nextCell = checkCondition

                navigated = False
                checkCondition = (currentPosition -width) -1
                if(navGridValues[checkCondition] >= 0 and gridCells[checkCondition] and checkCondition >= 0):
                    if(not (abs(currentPosition - checkCondition) < 8 and abs(currentPosition - checkCondition) > 1)):
                        if(navGridValues[checkCondition] < lowestNavGridValue and gridCells[checkCondition] != "1"):
                            for navigatedCell in navigationRoute:
                                if(navigatedCell == checkCondition):
                                    navigated = True

                            if(navigated == False):
                                lowestNavGridValue = navGridValues[checkCondition]
                                nextCell = checkCondition

                navigated = False
                checkCondition = currentPosition -1
                if(navGridValues[checkCondition] >= 0 and gridCells[checkCondition] and checkCondition >= 0):
                    if(not (abs(currentPosition - checkCondition) < 8 and abs(currentPosition - checkCondition) > 1)):
                        if(navGridValues[checkCondition] < lowestNavGridValue and gridCells[checkCondition] != "1"):
                            for navigatedCell in navigationRoute:
                                if(navigatedCell == checkCondition):
                                    navigated = True

                            if(navigated == False):
                                lowestNavGridValue = navGridValues[checkCondition]
                                nextCell = checkCondition

                navigated = False
                checkCondition = (currentPosition +width) -1
                if(navGridValues[checkCondition] >= 0 and gridCells[checkCondition] and checkCondition >= 0):
                    if(not (abs(currentPosition - checkCondition) < 8 and abs(currentPosition - checkCondition) > 1)):
                        if(navGridValues[checkCondition] < lowestNavGridValue and gridCells[checkCondition] != "1"):
                            for navigatedCell in navigationRoute:
                                if(navigatedCell == checkCondition):
                                    navigated = True

                            if(navigated == False):
                                lowestNavGridValue = navGridValues[checkCondition]
                                nextCell = checkCondition

                navigated = False
                checkCondition = currentPosition +width
                if(navGridValues[checkCondition] >= 0 and gridCells[checkCondition] and checkCondition >= 0):
                    if(not (abs(currentPosition - checkCondition) < 8 and abs(currentPosition - checkCondition) > 1)):
                        if(navGridValues[checkCondition] < lowestNavGridValue and gridCells[checkCondition] != "1"):
                            for navigatedCell in navigationRoute:
                                if(navigatedCell == checkCondition):
                                    navigated = True

                            if(navigated == False):
                                lowestNavGridValue = navGridValues[checkCondition]
                                nextCell = checkCondition
                    
                navigated = False
                checkCondition = (currentPosition +width) +1
                if(navGridValues[checkCondition] >= 0 and gridCells[checkCondition] and checkCondition >= 0):
                    if(not (abs(currentPosition - checkCondition) < 8 and abs(currentPosition - checkCondition) > 1)):
                        if(navGridValues[checkCondition] < lowestNavGridValue and gridCells[checkCondition] != "1"):
                            for navigatedCell in navigationRoute:
                                if(navigatedCell == checkCondition):
                                    navigated = True

                            if(navigated == False):
                                lowestNavGridValue = navGridValues[checkCondition]
                                nextCell = checkCondition

                # Checking whether the next cell is the last navigated cell, and if so, to enable backtracking, otherwise disable backtracking
                if(nextCell == navigationRoute[maxTrackIndex]):
                    backtrack = True
                    # If the next cell is also the cell before the last navigated one as well, the algorithm will end pathfinding
                    # By determining that the end point cannot be reached from the start point
                    if(nextCell == navigationRoute[maxTrackIndex-1]):
                        maxTraversalIterations = 0
                        console.log("END POINT UNREACHABLE FROM START POINT")
                else:
                    backtrack = False

                # Backtracking navigation check and update, otherwise continue the navigation path
                currentPosition = nextCell
                if(backtrack == True):
                    currentPosition = navigationRoute[trackIndex]
                    trackIndex -= 1
                else:
                    trackIndex = maxTrackIndex

                # Adding the newly navigated cell to the route and updating other parameters for the next loop run
                navigationRoute.append(currentPosition)
                maxTrackIndex += 1
                lowestNavGridValue = 100
                
                # Log if the end point is reached and the current position cell that should now be the end point
                if(currentPosition == endPosition):
                    console.log("END POINT REACHED AT CELL " + str(currentPosition))
            else:
                maxTraversalIterations = 0


            maxTraversalIterations -= 1
    else:
        while(maxTraversalIterations > 0):
            maxTraversalIterations -= 1

    console.log("navigationRoute: " + str(navigationRoute))


# Method for creating drawn path elements
def generateDrawPathElements():
    global width
    global gridCells
    global cellIntersections
    height = len(gridCells) / width
    rows = (height * 2) -1
    columns = (width * 2) -1
    cornerRow = False

    currentRow = rows

    # Filtering for image types to be placed between cells (cell intersections)
    # so that the travelled path could later be displayed accordingly

    # Some extra elements are generated which would never be used
    # (outside of allowing the algorithm to wrap-navigate around the borders of the grid)
    # so as to simplify the visibility draw filtering later

    while(currentRow > 0):
        if(cornerRow == True):
            rowCellIntersection = 0
            while(rowCellIntersection < width):
                cellIntersections.append("V")
                cellIntersections.append("D")
                rowCellIntersection += 1
            cornerRow = False
        else:
            rowCellIntersection = 0
            while(rowCellIntersection < width):
                cellIntersections.append("C")
                cellIntersections.append("H")
                rowCellIntersection += 1
            cornerRow = True

        currentRow -= 1

    # Generates a string of all image elements to be placed in the output draw element for displaying the path taken
    generatedString = ""
    lengthIndex = 0
    for cellIntersection in cellIntersections:
        match(cellIntersection):
            case "C":
                generatedString += "<img class='cellIntersection intersectionClear' src='" + imgDirectory + "connectionClear.png'>"
            case "H":
                generatedString += "<img class='cellIntersection intersectionHorizontal' src='" + imgDirectory + "connectionHorizontal.png'>" 
            case "V":
                generatedString += "<img class='cellIntersection intersectionVertical' src='" + imgDirectory + "connectionVertical.png'>" 
            case "D":
                generatedString += "<img class='cellIntersection intersectionDiagonal1' src='" + imgDirectory + "connectionDiagonal1.png'>"
                generatedString += "<img class='cellIntersection intersectionDiagonal2' src='" + imgDirectory + "connectionDiagonal2.png'>"
            case __:
                generatedString += "<img class='cellIntersection' src=''>" 

        
        lengthIndex += 1
        if (lengthIndex > columns):
            generatedString += "<br>"
            lengthIndex = 0

        document.getElementById("outputDrawDiv").innerHTML = generatedString

#######################################################
# Initial code execution
generateGridAssembly(gridCells)
addStaticEventListeners()
generateDrawPathElements()