import pandas as pd
import numpy as np
import math

data = np.array(pd.read_csv('data_tree3.txt', sep=',',header=None))
label=data[0,:]
data=data[1:,:]
#size=len(data)
rules = []
# tinh H cua 1 cot
def calH(element_row, element_column, data):
    var=filteredVar(len(data[0])-1,data)
    size=len(data)
    y = sum(element_row == i[element_column] and i[len(i) - 1] == var[0] for i in data)
    z = sum(element_row == i[element_column] and i[len(i) - 1] == var[1] for i in data)
    if y == 0:
        br = 0
    else:
        br = -(float(y) / float(y + z)) * math.log2(float(y) / float(y + z))
    if z == 0:
        k = 0
    else:
        k = -(float(z) / float(y + z)) * math.log2(float(z) / float(y + z))
    s=float(y+z)/float(size)
    H = s*(br + k)
    return H


# ten cac thuoc tinh cua cot
def filteredVar(element_row, data):
    x = list(set(data[:, element_row].tolist()))
    return x

# tinh E
def calE(element_row, data):
    # print('calE',element_row)
    E = sum(calH(i, element_row, data) for i in filteredVar(element_row, data))
    return E


# Chon E nho nhat
def chooseMin(data):
    X = {calE(i, data): i for i in range(len(data[0]) - 1)}
    return X[min(val for val in X)]
kq=[]
# tao luat
def decision_tree(data,rules,label,kq,stt):
    temp_index=len(data[0])-1
    temp=filteredVar(temp_index,data)
    if len(temp)==1  or len(label)==1:
        a=[]
        for r in rules:
            a.append(r)
        kq.append(a)
        kq[stt].append({label[temp_index]:temp[0]})
        return rules
    else:
        index=chooseMin(data)
        _var=filteredVar(index,data)
        for v in _var:
            rules.append({label[index]:v})
            _data=[]
            for i in data:
                if i[index]==v:
                    _data.append(i)
            _data=np.delete(_data,np.s_[index],axis=1)
            _label=np.delete(label,index)
            rules=decision_tree(_data,rules,_label,kq,stt)
            stt=len(kq)
            rules=np.delete(rules,len(rules)-1)
            rules=rules.tolist()
    return rules


decision_tree(data,rules,label,kq,0)
for k in kq:
    _str=""
    for e in range(len(k)-2):
        _str=str(list(k[e].keys())[0]) +" = "+str(list(k[e].values())[0])+" và "
    _str=_str+str(list(k[len(k)-2].keys())[0]) +" = "+str(list(k[len(k)-2].values())[0])+" --> "+str(list(k[len(k)-1].keys())[0]) +" = "+str(list(k[len(k)-1].values())[0])
    print(_str)