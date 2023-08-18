#排序
import ipaddress 
import re

def ip2int(ip):
    return int(ipaddress.ip_address(ip))  

def sort_Ip(ipv4_ips):
    ipv4_ips = [ip.strip() for ip in ipv4_ips]
    #IP大小排序
    ipv4_ips.sort(key=ip2int)
    return ipv4_ips

#读取-历史ip集合
ips_set = set()
with open('./resource/历史所有ip集合.txt') as fi:
    for i in fi:
        ips_set.add(i.strip())

#读取-今日新增ip.txt
new_ips = set()
with open('今日新增ip.txt') as fil:
    for n in fil:
        new_ips.add(n.strip())

#“今日新增ip“和“历史ip集合“ 比较  得到“今日新增ip(去重)”
ips_unique = new_ips-ips_set

with open('./resource/今日新增ip(去重).txt','w') as f:
    for ip in ips_unique:
        f.write(ip + '\n')

#讲新增的ips_unique set集合放置到“历史所有ip集合.txt”，这样“历史所有ip集合.txt”会越来越多
ips_set=ips_set|ips_unique
with open('./resource/历史所有ip集合.txt','w') as f:
    for ip in ips_set:
        f.write(ip + '\n')


#今日新增ip(去重)拿去处理
with open('./resource/今日新增ip(去重).txt') as f:
    ips = f.readlines()
    

ipv4_ips = []
ipv6_ips = []

for ip in ips:
    ip = ip.strip()
    try:
        if ipaddress.ip_address(ip).version == 4:
            ipv4_ips.append(ip)
        else:
            ipv6_ips.append(ip)
    except:
        pass

with open('./results/IPV6地址.txt', 'w') as f:
    f.write('\n'.join(ipv6_ips))

#IP国内外分组
china_ips = []
out_ips = [] 

for ip in ipv4_ips:
    ip = ip.strip()
    if ipaddress.ip_address(ip).is_private:
        continue 
    if ip.startswith('10.') or ip.startswith('192.168.') or ip.startswith('172.'):
        continue
    if ip.startswith('1.') or ip.startswith('42.') or ip.startswith('49.'): 
        china_ips.append(ip)
        china_ips=sort_Ip(china_ips)
    else:
        out_ips.append(ip)

#set去重        
no_repeat = set()
for line in china_ips:
    no_repeat.add(line.strip())
#写入   
with open('./results/禁止IP(国内去重).txt', 'w') as f:
    f.write('\n'.join(no_repeat))



#白名单B
aa_list=[]
with open('./resource/外网白名单B.txt') as f1:
     bb_list = f1.readlines()

for haif_ip in bb_list:
    aa_list.append(re.split('\.', haif_ip)[0])

#国外取C段
Out_second_nums = []
Out_A_nums = []
Out_B_nums = []
out_ips=sort_Ip(out_ips)
for ip in out_ips:
    ip = ip.strip() 
    num = re.split('\.', ip)[0]+"."+re.split('\.', ip)[1]+"."+re.split('\.', ip)[2]+ '.0/24'
    numB = re.split('\.', ip)[0]+"."+re.split('\.', ip)[1]
    numA = re.split('\.', ip)[0]
    if numB not in bb_list:
        B = numB+'.0.0/16'
        Out_B_nums.append(B)
    if numA not in aa_list:
        A  = numA+'.0.0.0/8'
        Out_A_nums.append(A)
    Out_second_nums.append(num)
    


#set去重  
no_repeat1 = set()
for l in Out_second_nums:
    no_repeat1.add(l.strip())
with open('./results/禁止IP(国外C段去重).txt', 'w') as f:
    f.write('\n'.join(no_repeat1))

no_repeat2 = set()
for l in Out_B_nums:
    no_repeat2.add(l.strip())
with open('./results/禁止IP(国外B段去重).txt', 'w') as f:
    f.write('\n'.join(no_repeat2))

no_repeat3 = set()
for l3 in Out_A_nums:
    no_repeat3.add(l3.strip())
with open('./results/禁止IP(国外A段去重).txt', 'w') as f3:
    f3.write('\n'.join(no_repeat3))
