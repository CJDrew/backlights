import numpy as np
import cv2

def processArea(area):
    #take average of pixels in the frame that are brighter than the cutoff.
    blackCutoff = 20
    averages = (0,0,0)
    count = 0
    for row in area:
        for pixel in row:
            if pixel[0] >= blackCutoff or pixel[1] >= blackCutoff or pixel[2] >= blackCutoff:
                averages += pixel
                count += 1
    
    return np.floor_divide(averages, (count,count,count))

def processFrame(frame, led_channelsX, led_channelsY):
    #Rescale the image to save processing
    scale_percent = 10 if len(frame) < 2000 else 5
    width = int(frame.shape[1] * scale_percent / 100)
    height = int(frame.shape[0] * scale_percent / 100)

    #Make the size a multiple of our LED channels to make life easier
    width -= (width % led_channelsX)
    height -= (height % led_channelsY)
    dim = (width, height)
    frame = cv2.resize(frame, dim, cv2.INTER_AREA)

    #take dimensions (after resizing)
    x, y = width, height

    #Divide the screen into a matrix MxN where M and N are the number of LEDs in the light strips
    #With agressive scaling there will likely be issues with rounding my steps
    #Consider switching to doubles and only rounding for display
    xStep, yStep = x // led_channelsX, y // led_channelsY
    topVals, bottomVals, leftVals, rightVals = [], [], [], []

    #Calculation and display are decoupled so I can specify larger chunks for analysis but still display the correct size
    #So below I can check deeper than 1 cell without changing my display
    cellDepth = 2

    #Do top and bottom at the same time
    i = 0
    while i <= x - xStep:
        top = processArea(frame[:yStep*cellDepth,i:i+xStep])
        bottom = processArea(frame[y-yStep*cellDepth:,i:i+xStep])
        topVals.append(top)
        bottomVals.append(bottom)
        i += xStep

    #Do left and right at the same time
    #First and last cells have already been calculated just doing them again for now to simplify
    i = 0
    while i <= y - yStep:
        left = processArea(frame[i:i+yStep,:xStep*cellDepth])
        right = processArea(frame[i:i+yStep,x-xStep*cellDepth:])
        leftVals.append(left)
        rightVals.append(right)
        i += yStep

    #Return all the calculated values as an array
    return [topVals, bottomVals, leftVals, rightVals]
    