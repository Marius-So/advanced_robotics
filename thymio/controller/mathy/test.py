from controller import clean_map
from pathfinding import pathfinder

a = [[0, 0, 0, 1,1,0], [], None, [1,0,1,1,0,0,0],[1,0,1,1,1,1,1,1,1,1], [0,0,0,0,0,0], [1,0,1,0,1,0], [1,0,0,0,1,1,0]]
b = clean_map(a)
test = pathfinder(b, 0,0,8,5)
print(test)
test.solve()
l = test.get_list_of_indices(test.xtarget, test.ytarget)
print(test.get_list_of_moove(l))
print(test)
