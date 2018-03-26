import re
import os
import zlib

def process_keyword(keyword):
	return re.sub('[^A-Za-z0-9]+', '', (keyword.lower()).replace(" ",""))

def get_index(keyword):	
	index,index2,ptr=0,0,1
	for c in "".join(keyword):
		index=index+ord(c)
		index2=index2+ord(c)*ptr
		ptr+=1	
		
	#print(index%mod)
	return index,index%mod,index2	


def get_basename(filename):
	return os.path.splitext(os.path.basename(filename))[0]

def make_list(offset,length):
	return ([str(offset), str(length)])

def process_key(t):
	return "#$|$#".join(str(i) for i in t)

def process_list(l):
	s=""
	fool=0
	for info in l:
		if(fool!=0):
			s=s+","
		s=s+" ".join(info)
		fool=1
	return s
	#return zlib.compress(s).replace("\n","|#$#|")

def soul(line,sep,index_col,offset,m):
	global mod
	mod=m
	keyword=[]
	l=line.split(sep)
	for cols in index_col:
		#try:		

		keyword.append(process_keyword(l[int(cols)].strip()))	
		# except:
		# 	pass		
	index,init_hash,index2=get_index(keyword)
	length=len(str(line))			
	data_list=make_list(offset,length)
	offset=offset+length
	keyword=tuple(keyword)
	return keyword, data_list, index,init_hash,index2,offset	