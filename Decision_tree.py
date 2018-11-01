##################################Not finish for describe variables

import pandas as pd
import numpy as np
import math

#################################################################################################
# Load data from file txt
data = np.array(pd.read_csv('data_tree3.txt', sep=',',header=None))

# Names of all columns
label=data[0,:]

# Draw data from data except labels
data=data[1:,:]

# list obtain all rules
rules=[]

#################################################################################################

# describe variables

#################################################################################################
# Draw all unique element in 1 column into list
def filteredVar(column, data):
    var = list(set(data[:, column].tolist()))
    return var

# Calculate H for each unique element in 1 column
def calH(unique_element, column, data):
    var=filteredVar(len(data[0])-1,data)
    size=len(data)
    decision1 = sum(unique_element == i[column] and i[len(i) - 1] == var[0] for i in data)
    decision2 = sum(unique_element == i[column] and i[len(i) - 1] == var[1] for i in data)
    if decision1 == 0:
        log_si_s_decision1 = 0
    else:
        log_si_s_decision1 = -(float(decision1) / float(decision1 + decision2)) * math.log2(float(decision1) / float(decision1 + decision2))
    if decision2 == 0:
        log_si_s_decision2 = 0
    else:
        log_si_s_decision2 = -(float(decision2) / float(decision1 + decision2)) * math.log2(float(decision2) / float(decision1 + decision2))
    si_s=float(decision1+decision2)/float(size)
    H = si_s*(log_si_s_decision1 + log_si_s_decision2)
    return H

# Calculate E for each column
def calE(column, data):
    E = sum(calH(i, column, data) for i in filteredVar(column, data))
    return E

# Get minimun E in all column in current data
def chooseMin(data):
    Es = {calE(i, data): i for i in range(len(data[0]) - 1)}
    return Es[min(val for val in Es)]

#################################################################################################
# Create rules via Decision_tree
def decision_tree(data,_rules,label,rules,stt):
    # check stop conditions
    temp_index=len(data[0])-1
    temp_element=filteredVar(temp_index,data)
    if len(temp_element)==1  or len(label)==1:
        rules.append(_rules.copy())
        rules[stt].append({label[temp_index]:temp_element[0]})
        return _rules

    # Not violated conditions
    else:
        index=chooseMin(data)
        _var=filteredVar(index,data)
        for v in _var:
            _rules.append({label[index]:v})
            _data=[i for i in data if i[index]==v]
            _data=np.delete(_data,np.s_[index],axis=1)
            _label=np.delete(label,index)
            _rules=decision_tree(_data,_rules,_label,rules,stt)
            stt=len(rules)
            _rules=np.delete(_rules,len(_rules)-1)
            _rules=_rules.tolist()
    return _rules


# Display rules
def printRules(data,label,rules):
    decision_tree(data,[],label,rules,0)
    for r in rules:
        _str=""
        for e in range(len(r)-2):
            _str+=str(list(r[e].keys())[0]) +" = "+str(list(r[e].values())[0])+" và "
        _str=_str+str(list(r[len(r)-2].keys())[0]) +" = "+str(list(r[len(r)-2].values())[0])+" --> "+str(list(r[len(r)-1].keys())[0]) +" = "+str(list(r[len(r)-1].values())[0])
        print(_str)

printRules(data,label,rules)
#################################################################################################
