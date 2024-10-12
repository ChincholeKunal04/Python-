import pandas as pd
import numpy as np

data = pd.read_csv("findS.csv")
print(data)

print()

d = np.array(data)[:,:-1]
print("The attributes are: ")
print(d)

print()

target = np.array(data)[:,-1]
print("The target is: ")
print(target)


def train(d, target):
    for i, val in enumerate(target):
        if val == "Yes":
            specific_hypo = d[i].copy()
            break

    for i, val in enumerate(d):
        if target[i] == "Yes":
            for x in range(len(specific_hypo)):
                if val[x] != specific_hypo[x]:
                    specific_hypo[x] = "?"
                else:
                    pass
    
    return specific_hypo

print()
print("The final hypothesis is:",train(d,target))