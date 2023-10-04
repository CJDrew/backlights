import cv2
import numpy as np
from scipy.cluster.vq import kmeans
from scipy import product

from frameUtilities import processFrame
import screenRegion

frameSkip = 3
frameCount = -1

led_channelsX = 100
led_channelsY = 50
x, y = 800, 300
topRegions, bottomRegions, leftRegions, rightRegions = screenRegion.createRegions(x, y, led_channelsX, led_channelsY)

cap = cv2.VideoCapture("media/natureLoop.mp4")
cap.set(cv2.CAP_PROP_POS_FRAMES, 30000)

while True:
    #Only process a subset of frames to reduce computations
    ret, frame = cap.read()
    frameCount += 1
    cv2.imshow("movie", frame)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break
    
    #To save processing only calculate new goal colors every n frames
    if frameCount % frameSkip == 0:

        #frameCount = 1
        
        #Get new goal colors
        goalColors = processFrame(frame, led_channelsX, led_channelsY)

        #Set new goal colors top/bottom
        for i in range(len(topRegions)):
            topRegions[i].goalColor = goalColors[0][i]
            bottomRegions[i].goalColor = goalColors[1][i]
        #Set new goal colors left/right
        for i in range(len(leftRegions)):
            leftRegions[i].goalColor = goalColors[2][i]
            rightRegions[i].goalColor = goalColors[3][i]
    #Move each bgr value closer to the goal and set the screen regions correclty
    allRegions = topRegions + bottomRegions + leftRegions + rightRegions
    for r in allRegions:
        r.iterateColor()        

    #make a sample color block so I can see
    image = np.zeros((y, x, 3), np.uint8)
    for r in allRegions:
        image[r.minY:r.maxY,r.minX:r.maxX] = r.curColor
    cv2.imshow("processed", image)

cap.release()
cv2.destroyAllWindows()