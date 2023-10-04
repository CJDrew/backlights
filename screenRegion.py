class ScreenRegion:
    def __init__(self):
        self.colorStep = 8
        self.curColor = None
        self.goalColor = None
        self.xMin = None
        self.xMax = None
        self.yMin = None
        self.yMax = None

    def iterateColor(self):
        c = self.curColor
        g = self.goalColor

        #The further apart the cur value is from goal the faster we should increment
        c[0] += (g[0] - c[0]) // self.colorStep
        c[1] += (g[1] - c[1]) // self.colorStep
        c[2] += (g[2] - c[2]) // self.colorStep


        #This might flicker with larger colorStep values
        # if c[0] != g[0]:
        #     c[0] += self.colorStep * 1 if c[0] < g[0] else -1
        # if c[1] != g[1]:
        #     c[1] += self.colorStep * 1 if c[1] < g[1] else -1
        # if c[2] != g[2]:
        #     c[2] += self.colorStep * 1 if c[2] < g[2] else -1

def createRegions(x, y, led_channelsX, led_channelsY):
    #Create lists to track my screenRegions
    topRegions, bottomRegions, leftRegions, rightRegions = [], [], [], []
    xStep = x // led_channelsX
    yStep = y // led_channelsY
    for i in range(led_channelsX):
        #Populate top
        top = ScreenRegion()
        top.curColor = [0,0,0]
        top.goalColor = [0,0,0]
        top.minY = 0
        top.maxY = yStep
        top.minX = i * xStep
        top.maxX = (i+1) * xStep
        topRegions.append(top)
        #populate bottom
        bottom = ScreenRegion()
        bottom.curColor = [0,0,0]
        bottom.goalColor = [0,0,0]
        bottom.minY = y - yStep
        bottom.maxY = y
        bottom.minX = i * xStep
        bottom.maxX = (i+1) * xStep
        bottomRegions.append(bottom)

    for i in range(led_channelsY):
        #populated left
        left = ScreenRegion()
        left.curColor = [0,0,0]
        left.goalColor = [0,0,0]
        left.minY = i * yStep
        left.maxY = (i+1) * yStep
        left.minX = 0
        left.maxX = yStep
        leftRegions.append(left)

        #populated right
        right = ScreenRegion()
        right.curColor = [0,0,0]
        right.goalColor = [0,0,0]
        right.minY = i * yStep
        right.maxY = (i+1) * yStep
        right.minX = x - xStep
        right.maxX = x
        rightRegions.append(right)
    
    return topRegions, bottomRegions, leftRegions, rightRegions