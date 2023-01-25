import os
filepath = "./"
path_list = os.listdir(filepath)
for path in path_list:
    if '.err' in path:
        file = open("./"+path, mode='r')
        lines = file.readlines()
        print(path)
        res = []
        for line in lines:
            if 'real' in line:
                data = line.split('\t')
                tmp = data[-1].split('\n')[0]
                tmp = tmp.split('m')
                
                res_tmp = float(tmp[0])*60+float(tmp[1].split('s')[0])
                print(res_tmp)
                res.append(res_tmp)
        print(res)
