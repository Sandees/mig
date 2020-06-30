import os
import re
import json
import pprint
with open("cpu.txt") as cpu_file:
    text=cpu_string = cpu_file.read()
    #print(text)
    #split_cpu_string = (str(cpu_string[2]))
    text = os.linesep.join([s for s in text.splitlines() if s])
    #print(text)
    p1 = re.compile(r'^ *\d+( +\d+)* *$')

    #          0    5    0    5    0    5    0    5    0    5    0
    p2 = re.compile(r'^ *0( +5 +0){5,6} *$')

    # 80     * **#*#**   * *       *
    # 70  *  * **#*#**   * *       *           *
    p3 = re.compile(r'^ *(?P<num>[\d]+)(?P<line>.*#.*$)')

    # CPU% per second (last 60 seconds)
    p4 = re.compile(r'^ *CPU%.*$')

    # initialize max list & average list & return dictionary
    max_list = []
    average_list = []
    ret_dict = {}

    max_list = []
    for line in text.splitlines():
            #strip_line = line[6:]
        m = p1.match(line)
        if m:
            max_list.append(line)
            continue

        m1 = p3.match(line)
        m2 = p4.match(line)
        if m1 or m2:
            average_list.append(line)
            continue
    #print(max_list)
    #print(average_list)
    # parser max value
    tmp = [''] * 73
    # print((tmp[70]))
    count = 0
    for line in max_list:
        m = p2.match(line)
        if not m:
            for i, v in enumerate(line):

                if v == ' ':
                    pass
                else:
                    # print(i,v)
                    try:
                        tmp[i] += v
                    except:
                        pass

        else:
            if count == 0:
                sub_dict = ret_dict.setdefault('60s', {})
                for i in range(60):
                    sub_dict.setdefault(
                        i + 1, {}).update({'maximum': int(tmp[i]) if tmp[i] != '' else 0})

            elif count == 1:
                sub_dict = ret_dict.setdefault('60m', {})
                for i in range(60):
                    sub_dict.setdefault(
                        i + 1, {}).update({'maximum': int(tmp[i]) if tmp[i] != '' else 0})

            else:
                sub_dict = ret_dict.setdefault('72h', {})
                for i in range(72):
                    sub_dict.setdefault(
                        i + 1, {}).update({'maximum': int(tmp[i]) if tmp[i] != '' else 0})
            tmp = [''] * 72
            count += 1
        # parser average value
    
    count = 0
    for line in average_list:
        m = p3.match(line)
        if count == 0:
            sub_dict = ret_dict.setdefault('60s', {})
        elif count == 1:
            sub_dict = ret_dict.setdefault('60m', {})
        else:
            sub_dict = ret_dict.setdefault('72h', {})

        if m:
            num = int(m.groupdict()['num'])
            line = m.groupdict()['line']
            for i, char in enumerate(line):
                if char == '#':
                    t = sub_dict.setdefault(i, {})
                    if 'average' not in t:
                        t.update({'average': num})

        else:
            for value in sub_dict.values():
                if 'average' not in value:
                    value.update({'average': 0})

            count += 1

    #print(ret_dict['72h'])
    result=ret_dict['72h']
    #print(result)
    resultlol=["ACGBSRVR1"]
    for each in result.keys():
        #print(each)
        resultlol.append(result[each]['average'])
    #print(resultlol)

    lol = json.dumps(ret_dict['72h'])
    

    heading=['Device_name']
    keys=(list(ret_dict['72h'].keys()))
    heading=heading+keys

  
    #print(heading)
    #pprint.pprint(json.loads(lol))
    import csv
    with open('final.csv', 'w', newline='') as file:
        writer = csv.writer(file)
        writer.writerow(heading)
        writer.writerow(resultlol)


print("hello")
