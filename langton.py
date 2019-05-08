import math
import sys
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.animation as animation



class LangtonsAnt:
    """
    This Object represents the entire cellular automata

    Args:
        N (int): Size of square grid

    Attibutes:
        N (int): Size and width of grid
        grid (np.ndarray): The whole board which the ant can travel over
        whiteVal (int): value representing "on" square
        blackVal (int): value representing "off" square
        ant (Ant): ant object
        fastMode (bool): whether to do 3 steps at a time or not
        steps (int): number of steps taken so far
    """
    
    def __init__(self, N:int, fastMode=False):
        self.N = N
        self.grid = np.ones((N, N), np.uint)
        self.whiteVal = 1
        self.blackVal = 0
        self.ant = Ant(N)
        self.fastMode = fastMode
        self.steps = 0

    def getGrid(self):
        return self.grid
    
    def step(self):
        """Makes a step, if fastmode is on, make another 50"""
        self.makeMove()
        if self.fastMode:
            for i in range(50):
                self.makeMove()

    def makeMove(self):
        """Makes one move based on following rules:
            1) If ant's current square is black, toggle to white and move ant
               to cell to the left of ant's direction (ant.direction).
            2) If ant's current square is white, toggle to black and move ant
               to cell to the right of ant's direction (ant.direction).

            Increments self.steps.
        """
               
        
        self.steps += 1
        loc = self.ant.getLocation()
        if self.grid[loc[0]][loc[1]] == self.blackVal:
            self.grid[loc[0]][loc[1]] = self.whiteVal
            self.ant.updateLocationAndDirection("left")
        else:
            self.grid[loc[0]][loc[1]] = self.blackVal
            self.ant.updateLocationAndDirection("right")

    def getSteps(self):
        return self.steps

class Ant:
    """
    The ant that is to roam around the grid

    Args:
        N (int): Size of square grid it will exist within

    Attributes:
        N (int): Size of square grid it will exist within
        location (list): Current coordinates
        direction (str): The direction of the ant
    """

    def __init__(self, N:int):
        self.N = N
        self.location = [math.ceil(N / 2), math.ceil(N / 2)] # Middle
        self.directionList = ["down", "left", "up", "right"]
        self.direction = "down" # facing down
        self.LEFTVAL = -1
        self.RIGHTVAL = 1

    def getLocation(self):
        return self.location

    def updateLocationAndDirection(self, direction:str):
        val = self.LEFTVAL if direction == "left" else self.RIGHTVAL
        if self.direction == "up":
            self.location = [self.location[0], self.location[1] + val]
        elif self.direction == "down":
            self.location = [self.location[0], self.location[1] - val]
        elif self.direction == "left":
            self.location = [self.location[0] - val, self.location[1]]
        elif self.direction == "right":
            self.location = [self.location[0] + val, self.location[1]]
        
        newDirectionIndex = (self.directionList.index(self.direction) \
                            + val) % 4
        self.direction = self.directionList[newDirectionIndex]

N = 500

lang = LangtonsAnt(N, fastMode=True)
lang.step()
grid = lang.getGrid()
fig = plt.figure()

"""
ax = fig.add_subplot(111, aspect='equal', autoscale_on=False,
                     xlim=(0, N), ylim=(0, N))
ax.grid()

line, = ax.plot([], [], 'o-', lw=2)
stepText = ax.text(0.02, 0.95, '', transform=ax.transAxes)
"""

plt.gray()
img = plt.imshow(grid, animated=True)

def init():
    """initialize animation"""
    line.set_data([], [])
    stepText.set_text('')
    return stepText

def animate(i):
    global lang
    lang.step()
    """
    line.set_data((0,0))
    stepText.set_text("Steps = %d" % lang.getSteps())
    """
    newGrid = lang.getGrid()
    img.set_array(newGrid)
    return img, #line, stepText

interval = 1


ani = animation.FuncAnimation(fig, animate, frames=sys.maxsize, \
        interval=interval)#, init_func=init)
plt.show()


