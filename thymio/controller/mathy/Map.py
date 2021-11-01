class Map:
    def __init__(self, H, W, resolution) -> None:
        self.H = H  # vertical
        self.W = W  # horizontal
        self.resolution = resolution
        self.columns = int(W/resolution)
        self.rows = int(H/resolution)
        self.map = [[" " for i in range(self.columns)]
                    for j in range(self.rows)]
        #print("map")
        #print(self.map)

    def __str__(self):
        s = "⊠ " * (self.columns + 2)  +'\n'
        for j in range(self.rows):
            row = "⊠ "
            for i in range(self.columns):
                row += str(self.map[j][i]) + " "
            row += "⊠"
            s += (row) + '\n'
            row = ""
        s += "⊠ " * (self.columns + 2) + '\n'
        return(s)

    def getCoordinates(self, p):
        i = int(self.columns/2 + p[0]/self.resolution)
        if(i == self.columns):
            i = i-1
        j = int(self.rows/2 - p[1]/self.resolution)
        if(j == self.rows):
            j = j-1
        return(j, i)

    def setDanger(self, p):
        try:
            danger = self.getCoordinates(p)
            self.map[danger[0]][danger[1]] = "B"
        except IndexError:
            print("index error")
            pass

    def setSafe(self, p):
        try:
            safe = self.getCoordinates(p)
            self.map[safe[0]][safe[1]] = "W"
        except IndexError:
            pass

    def setCorpse(self, p):
        try:
            corpse = self.getCoordinates(p)
            self.map[corpse[0]][corpse[1]] = "C"
        except IndexError:
            pass

    def setHouse(self, p):
        try:
            house = self.getCoordinates(p)
            self.map[house[0]][house[1]] = "H"
        except IndexError:
            pass

if __name__ == "__main__":
    W = 1.92  # width of arena
    H = 1.13  # height of arena
    res = 0.05  # in meters
    map = Map(H, W, res)
    danger = (-0.5,-0.2)
    map.setDanger(danger)
    danger = (-0.6,0.2)
    map.setDanger(danger)
    print(map)
