import random
import copy

from enum import Enum

class Direction(Enum):
    left = 1
    right = 2
    up = 3
    down = 4


class Point :
    def __init__ (self, x,y):
        self.x = x
        self.y = y

    @classmethod
    def random (cls,max) :
        x = random.randint(0,max)
        y = random.randint(0,max)
        return cls(x,y)


class Game :

    def __init__ (self, size):
        self.size = size
        self.grid = [[0]*size for j in range(size)]
        r1 = Point.random(size-1)
        r2 = Point.random(size-1)
        self.addPoint(r1,2)
        self.addPoint(r2,2)


    def dropLine(self,line):
        # remove all zeros
        res = list(filter(lambda x : x != 0, line))
        res2 = []
        # flatten numbers left to right
        i = 0
        while i < len(res) :
            if i < len(res) -1 and res[i] == res[i+1] :
                res2.append(res[i] * 2)
                i+=2
            else:
                res2.append(res[i])
                i+=1
        return res2

    def addPoint(self,p,v):
       if self.grid[p.x][p.y] == 0:
           self.grid[p.x][p.y] = v
           return True
       else :
           return False

    def printNumber(self,v):
        color = { 0 : "\u001b[37m",
                  2 : "\u001b[33m",
                  4 : "\u001b[31m",
                  8 : "\u001b[32m",
                  16 : "\u001b[35m",
                  32 : "\u001b[34m",
                  64 : "\u001b[36m",
                  128 : "\u001b[31m",
                  256 : "\u001b[32m",
                  512 : "\u001b[33m",
                  1024 : "\u001b[34m",
                  2048 : "\u001b[35m" }
        txt = color[v]+str(v)+"\u001b[0m"
        sp =  " "*(4-(len(str(v))))

        print(txt+sp, end = ' ')

    def printGrid(self):
        print("_")
        for i in range(self.size):
            for j in range(self.size):
                self.printNumber(self.grid[i][j])
            print("")

    def left(self):
        for i in range(0,self.size):
            line = self.dropLine(self.grid[i])
            self.grid[i] = line + [0] * (self.size - len(line))

    def right(self):
        for i in range(0,self.size):
            line = self.grid[i] = self.dropLine(self.grid[i][::-1])
            line = list(reversed(line))
            self.grid[i] =  [0] * (self.size - len(line)) + line

    def column(self,i):
        res = []
        for j in range(0,self.size):
            res.append(self.grid[j][i])
        return res

    def columns(self):
        res = []
        for i in range(0,self.size):
            res.append(self.column(i))
        return res

    def up(self):
        cols = self.columns()
        for i in range(0,self.size):
            c = cols[i]
            col = self.dropLine(c)
            col = col + [0] * (self.size - len(col))
            for j in range(0,self.size):
                self.grid[j][i] = col[j]

    def down(self):
        cols = self.columns()
        for i in range(0,self.size):
            c = cols[i]
            col = self.dropLine(c[::-1])
            col = list(reversed(col))
            col =  [0] * (self.size - len(col)) + col
            for j in range(0,self.size):
                self.grid[j][i] = col[j]


    def oneStep(self,d):
       g_copy = copy.deepcopy(self.grid)
       moves = { Direction.left : self.left ,
                 Direction.right : self.right ,
                 Direction.up : self.up ,
                 Direction.down : self.down }
       moves[d]()
       b = g_copy == self.grid
       while not b :
          b =  self.addPoint(Point.random(self.size-1),2)
       self.printGrid()

    def win(self):
        for line in self.grid:
            for cell in line:
                if cell == 2048 :
                    print("You win!")
                    return True
        return False

    def canMove(self):
        lines = self.grid
        cols = self.columns()
        can = False
        for l in lines:
            for i in range(0,self.size):
                can = can or l[i] == 0 or (i < self.size - 1 and l[i] == l[i+1])
        for c in cols :
            for i in range(0,self.size-1):
                can = can or c[i] == 0 or (i < self.size - 1 and c[i] == c[i+1])
        if not can :
            print("You lose")
        return can

    def gameLoop(self):
        dir = { "a" : Direction.left ,
                "d" : Direction.right ,
                "w" : Direction.up ,
                "s" : Direction.down }
        while not self.win() and self.canMove() :
            try:
                val = input("Please enter a direction (a,w,s,d)\n")
                self.oneStep(dir[val])
            except KeyError:
                continue


def main():
    print("2048")
    g = Game(4)
    g.printGrid()
    g.gameLoop()

if __name__ == "__main__":
    main()
