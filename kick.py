#排序
import ipaddress 
import re

#白名单B
with open('./resource/外网白名单B.txt') as f:
     list2 = [line.rstrip() for line in f.readlines()]

with open('./results/禁止IP(国外B段去重).txt') as f1:
     all_list = f1.readlines()

#国外取C段



no_repeat1 = set()
#遍历所有IP
for ip in all_list:
    ip = ip.strip() 
    numB = re.split('\.', ip)[0]+"."+re.split('\.', ip)[1]
    no_repeat1.add(numB)
  
list1=list(no_repeat1)

all_bb=list(filter(lambda x: x not in list2, list1))
print(list2)
print(all_bb)

Out_B_nums = []

for ab in all_bb:
    B = ab.strip()+'.0.0/16'
    Out_B_nums.append(B)


no_repeat2 = set()
for l in Out_B_nums:
    no_repeat2.add(l.strip())
with open('禁止IP(国外B段去重去白)_17.txt', 'w') as f:
    f.write('\n'.join(no_repeat2))


