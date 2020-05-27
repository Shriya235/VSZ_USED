import re
import matplotlib
import matplotlib.pyplot as plt
import matplotlib.dates as md
from  datetime import datetime

def Data_Plotting(x,y,title):                               #plots the data over difference in time
    ax=plt.gca()
    xfmt = md.DateFormatter('%Y-%m-%d %H:%M:%S')
    ax.xaxis.set_major_formatter(xfmt)
    plt.xticks( rotation=30, horizontalalignment='right' )
    plt.plot(x,y)
    plt.title(title)
    plt.xlabel('Time')
    plt.ylabel('Consecutive difference')
    plt.show()                                                             
    plt.savefig('utilisation.png')

def tocalsum(list1):                                    #calculates the sum of all vsz values of one part of accessed data and calculates for all portions of data
    single_ps=[]
    vsz=[]
    sum1=0
    for b in list1:
        single_ps.append(re.split(r'[|\s]\s*', b))
    for x in single_ps:
        for y in range(len(x)):
            if x[y]=='root' and x[y+2]=='S':
                vsz.append(x[y+1])
    for a in vsz:
        sum1=sum1+int(a)
    return sum1
        
def process_sum(logfile,catch_start,catch_end):          #logfile=input data file,access the part of data start at=catch_start and end at=catch_end  
    results = []
    t=0
    pstime=[]
    vsz_sum=[]
    diffvsz=[]
    tim=[]
    used=[]
    bufcach=[]
    diff_used=[]
    with open(logfile, 'r') as f1:
        lines = f1.readlines()
    i = 0
    while i < len(lines):
        if '-/+ buffers/cache:' in lines[i]:                #access the used memory values under "free" command
           bufcach.append(re.split(r'[|\s]\s*',lines[i])) 
        if catch_start in lines[i]:
            pstime.append(re.split(r'[|\s]\s*',lines[i]))
            for j in range(i + 1, len(lines)):
                if catch_end in lines[j] or j == len(lines)-1:
                    results.append(lines[i:j])
                    i = j
                    break
        else:
            i += 1
    k=0
    for a in results:
        vsztot = tocalsum(a)                                #function call
        vsz_sum.insert(k,vsztot)                            #vsz_sum: sum of all vsz values of all parts of data under each catch_start and catch_end
        k=k+1
    for d in range(len(vsz_sum)-1):
        diffvsz.append(abs(vsz_sum[d]-vsz_sum[d+1]))        #finds the adjacent difference of sum of vsz values
    for e in bufcach:
        used.append(e[2])
    for d in range(len(used)-1):
        diff_used.append(abs(int(used[d])-int(used[d+1])))  #finds the adjacent difference of sum of used values
    for m in pstime:
           tim.append(m[2]+" "+m[3])
    tim.remove(tim[0])
    date_obj = []
    for temp in tim:
        date_obj.append(datetime.strptime(temp, '%Y-%m-%d %H:%M:%S.%f'))
    dates = md.date2num(date_obj)

    Data_Plotting(dates,diffvsz,'Difference in sum of VSZ values')
    Data_Plotting(dates,diff_used,'Difference in Used values')
   



