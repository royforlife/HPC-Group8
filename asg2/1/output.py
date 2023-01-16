import os
filepath = "./"
path_list = os.listdir(filepath)
for path in path_list:
    if '.out' in path:
        file = open("./"+path, mode='r')
        lines = file.readlines()
        print(path)
        res = []
        for line in lines:
            if 'obtained' in line:
                data = line.split(' ')
                res.append(float(data[-2]))
        print(res)
