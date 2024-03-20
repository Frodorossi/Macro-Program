
import numpy as np
import json

def mood():
    print('it worked')

testlist = [['mood',2,3],['mood',3,4]]
print(testlist)
#np.savez('savetest.npz', testlist)
with open('jtest.json', 'w') as outfile:
    json.dump(testlist, outfile)
#list2 = np.load('savetest.npz')['arr_0']
list2 = json.load(open('jtest.json'))
print(list2)
#print(type(list2[0][1]))
#for i in range(len(list2)):
    #eval(list2[i][0]+'()')

