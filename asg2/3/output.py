import os
filepath = "./"
path_list = os.listdir(filepath)
res = []
for path in path_list:
    if '.out' in path:
        file = open("./"+path, mode='r')
        lines = file.readlines()
        # print(path)
        # res = []
        for line in lines:
            if 'CPUS' in line:
                print(line[5:-1])
            if 'obtained' in line:
                data = line.split(' ')
                print(float(data[-2]))
                res.append(float(data[-2]))
        print(' ')
print(res)
