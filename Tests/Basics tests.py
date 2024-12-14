a=[[0, 1, 2], [3, 4, 5], [6, 7, 8]]

for i in a: c=(i if not "c" in vars() else c+i)

print(c)