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

    def printMap(self):
        s = "⊠ " * (self.columns + 2)
        print(s)
        for j in range(self.rows):
            row = "⊠ "
            for i in range(self.columns):
                row = str(row) + str(self.map[j][i]) + " "
            row = str(row) + "⊠"
            print(row)
            row = ""
        s = "⊠ " * (self.columns + 2)
        print(s)
        print("")

    def getCoordinates(self, p):
        i = int(self.columns/2 + p[0]/self.resolution)
        if(i == self.columns):
            i = i-1
        j = int(self.rows/2 - p[1]/self.resolution)
        if(j == self.rows):
            j = j-1
        return(j, i)

    def setDanger(self, p):
        danger = self.getCoordinates(p)
        self.map[danger[0]][danger[1]] = "X"

    def setCorpse(self, p):
        corpse = self.getCoordinates(p)
        self.map[corpse[0]][corpse[1]] = "C"
    def setCorpse(self, p):
        house = self.getCoordinates(p)
        self.map[house[0]][house[1]] = "H"

if __name__ == "__main__":
    W = 3  # width of arena
    H = 2  # height of arena
    res = 0.5  # in meters
    map = Map(H, W, res)
    danger = (0,0)
    map.setDanger(danger)
    map.printMap()
    corpse = (1,-0.45)
    map.setCorpse(corpse)
    map.printMap()