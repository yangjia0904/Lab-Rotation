import os
import numpy as np
from numpy.core.records import record

def simple_count(file_name):
    lines = 0
    for _ in open(file_name):
        lines = lines +1
    return lines

def find_center_point(file_name,length,id1,id2):
    lens = [-1]
    cen = int (length * 1000000 /2 )
    for line in open(file_name):
        entries = line. split()
        physFrom = int (entries [2])
        physTo = int(entries [3])
        if ( physFrom < cen and physTo > cen and id1 == entries[0] and id2 == entries[1]):
            # if the ibd covers the centeral point add the length
            lens.append(physTo-physFrom)
    return np.max(lens)



def simulation(arg1,arg2,arg3,arg4,id1,id2,path):
    """
    using different args to set different paramrters
    arg1 arg2 samples of pop
    arg3 population number
    arg4 chr length
    id1 target ibd id1
    id2 target ibd id2
    """

    cmd='java -jar ARGON.0.1.jar -pop '+str(arg1)+' '+str(arg2)+' -N '+str(arg3)+' -seq 0.0 -size '+str(arg4)+' -IBD 0.001 -quiet -out'+str(path)
    lines=[]
    # Monte Carlo method estimate the Mean
    for i in range(1000):
        tempCmd=cmd
        os.system(tempCmd)
        # read the idb result file ***.ibd
        if (id1 =="2" and id2 == "3"):
            len_count=[find_center_point(path,arg4,"1","3"),find_center_point(path,arg4,"2","3"),
            find_center_point(path,arg4,"1","4"),find_center_point(path,arg4,"2","4")]
        else:
            len_count=find_center_point(path,arg4,id1,id2)
        lines.append(len_count)
    return lines

def simulation_count_ibd_rate(arg1,arg2,arg3,arg4,id1,id2,ibd_length,path_of_ibd,path_of_file,path_of_file_folder):
    """
    using different args to set different paramrters
    arg1 arg2 samples of pop
    arg3 population number
    arg4 chr length
    id1 target ibd id1
    id2 target ibd id2
    ibd_length the thredhold of ibd
    """
    os.chdir(path_of_ibd)
    # First simulate enough samples according to the parametres
    cmd='java -jar ARGON.0.1.jar -pop '+str(arg1)+' '+str(arg2)+' -N '+str(arg3)+' -seq 0.0 -size '+str(arg4)+' -IBD '+str(ibd_length)+' -quiet '+str(path_of_file_folder)
    lines=[]
    # Monte Carlo method estimate the Mean
    for i in range(5000):
        tempCmd=cmd
        os.system(tempCmd)
        # read the idb result file ***.ibd
        # if (id1 =="2" and id2 == "3"):
        #     # then find the ibds satisfying the conditions and record
        #     len_count=[find_center_point(path,arg4,"1","3"),find_center_point(path,arg4,"2","3"),
        #     find_center_point(path,arg4,"1","4"),find_center_point(path,arg4,"2","4")]
        # else:
        len_count=find_center_point(path_of_file,arg4,id1,id2)
        lines.append(len_count)
    number_of_zero=0
    # count the record whose number is 0
    for item in lines:
        if item == -1:
            number_of_zero = number_of_zero+1
            
    return number_of_zero/len(lines)


dict={}


# #s1
# res=simulation(1,"2","1000",10,"1","2")
# # wrtie the samples into into the files
# f=open("testResult\\results1.txt","w")
# for item in res:
#     f.write(str(item/10000000)+'\n')
# #s2 2 0
# res=simulation(2,"2 2","pop.txt",10,"1","2")
# # wrtie the samples into into the files
# f=open("testResult\\results2_20.txt","w")
# for item in res:
#     f.write(str(item/10000000)+'\n')

# #s2 1 1
# res=simulation(2,"2 2","pop.txt",10,"2","3")
# # wrtie the samples into into the files
# f=open("testResult\\results2_11.txt","w")
# for item in res:
#     for iitem in item:
#         f.write(str(iitem/10000000)+'\n')

# #s2 0 2
# res=simulation(2,"2 2","pop.txt",10,"3","4")
# # wrtie the samples into into the files
# f=open("testResult\\results2_02.txt","w")
# for item in res:
#     f.write(str(item/10000000)+'\n')


#s3
# res=simulation_count_ibd_rate(2,"2 2","pop2.txt",10,"1","2")
# wrtie the samples into into the files
# f=open("testResult\\results3.txt","w")
# for item in res:
#     f.write(str(item/10000000)+'\n')

#s4
# res=simulation(2,"2 2","pop2.txt",10,"2","3")
# wrtie the samples into into the files
# f=open("testResult\\results4.txt","w")
# for item in res:
#     for iitem in item:
#         f.write(str(iitem/10000000)+'\n')

thred=[0.01,0.001,0.0001]
#s1
# s1_result=[]
# for item in thred:
#     s1_result.append(simulation_count_ibd_rate(1,"2","1000",10,"1","2",ibd_length=item))


# #s2 2 0
# s220_result=[]
# for item in thred:
#     s220_result.append(simulation_count_ibd_rate(2,"2 2","pop.txt",10,"1","2",ibd_length=item))

#s2 1 1
s211_result=[]
for item in thred:
    s211_result.append(simulation_count_ibd_rate(2,"2 2","pop.txt",10,"2","3",ibd_length=item))


# # s3
# s3_result=[]
# for item in thred:
#     s3_result.append(simulation_count_ibd_rate(2,"2 2","pop2.txt",10,"1","2",ibd_length=item))


# s4
s4_result=[]
for item in thred:
    s4_result.append(simulation_count_ibd_rate(2,"2 2","pop2.txt",10,"2","3",ibd_length=item))

print(s4_result)

