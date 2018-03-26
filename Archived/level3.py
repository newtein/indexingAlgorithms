from collections import OrderedDict
import operator,re
from math import ceil

def process_keyword(keyword):
	return re.sub('[^A-Za-z0-9]+', '', (keyword.lower()).replace(" ",""))
def check(a,b,length):
	t=[]
	
	if(b>=0 and b<=length):
		t.append(int(b))
	if(a>=0 and a<=length):
		t.append(int(a))
		
	return t

def read_file():
	#f=open("data/city_list.csv","r")
	f=open("test3.txt","r")
	index_col=0
	offset=0
	data={}
	for g in f:
		flag=0
		row=g.split(",") 
		for i in range(len(row)):
			row[i]=process_keyword(row[i])
			if row[i]=='':
				flag=1 
		if flag==0:
			length=len(str(g))
			if row[0] not in data:
				 data[int(row[0])]=[]	 
			data[int(row[0])].append([offset,length])
			offset=offset+length
	f.close()
	

	return sorted(data.items(), key=operator.itemgetter(0))

def process_list(l):
	s=""
	fool=0
	for info in l:
		if(fool!=0):
			s=s+","
		s=s+" ".join([ str(c) for c in info])
		fool=1
	return s

def write_data(data):
	f=open("3level.txt","w")
	#print(data)
	for l in data:
		print(l,l[0],l[1])
		#l=[i.strip() for i in l]
		f.write(str(l[0]).strip()+"$#|$#"+process_list(l[1])+"\n")
		#f.write(str(l)+"$#|$#"+process_list(data[l])+"\n")
	f.close()	
	return 1

def make_list(fname):
	f=open(fname,"r")
	offset,length=0,0
	ds=[]
	for l in f:
		length=len(str(l))
		ds.append((offset,length))
		offset=offset+length
	f.close()
	print("level 3 list completed")	
	return ds

def process_val(val):
	s=""
	fool=0
	for l in val:
		if(fool!=0):
			s=s+"#"
		s=s+str(l[0])+" "+str(l[1])
		fool=1
	return s	





def write_in3l(data):
	f=open("3ltest.txt","w")
	#print(data)
	for key,val in data.items():
		#pass
		#print(l)
		f.write(" ".join(str(k) for k in key)+"$#|$#"+process_val(val)+"\n")
	f.close()
	print("done yo yo")	
	return 1


# data=read_file()

# print(data)

# success=write_data(data)
# if(success==1):
# 	print("File written")
# x=make_list("3level.txt")	
# print(len(x))
#x=[ i for i in range(0,11)]
#x=[(0,0),(1,0),(2,0),(3,0),(4,0),(5,0),(6,0),(7,0),(8,0),(9,0),(10,0),(11,0),(12,0)]
x=[(i,0) for i in range(0,13)]
l=len(x)-1
length=len(x)
data=OrderedDict()
i=0
q=[]
q.append(0)
past=[]
fool=True
ptr=1
while True:
	if len(q)==0:
		break
	i=q[0]
	#print(i,l)
	tl=check(i+l,i-l,length)	
	past.append(len(tl))
	try:
		if x[i] not in data:
			data[x[i]]=[ x[p] for p in tl]
	except:
		break		
	q.extend(tl)
	#print(ptr,fool)
	if(fool==True):
		l=ceil(l/2)
		fool=False
	if ptr in [pow(2,i) for i in range(0,50)]:
		 fool=True
	ptr+=1     	
	del q[0]  

#print(data)	
write_in3l(data)   	

0---8
1
2
3
4----2,6
5
6
7
8----4



