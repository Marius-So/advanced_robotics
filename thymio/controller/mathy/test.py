from controller import generate_map

a = [[False, False,False, True, True, False, False], [], [False, False, False, True, True], [False, False, False, False, False, False], [True, False, False, False, False, False], [False, False, False, False, False, False, False, False], None]

b = generate_map(a)
print(b)
