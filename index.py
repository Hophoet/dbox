
file = open('data/data.txt', 'r')
data = eval(file.read())
data[8] = ('Olivier', 23)
data[7] = ('François', 25)
file = open('data/data.txt', 'w')
file.write(str(data))
