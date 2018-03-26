import sys
import os,re,csv,json,itertools
import timecalc as t
import zlib


def process_keyword(keyword):
	"""
	Process:2-Step process
	*Covert string into lower case
	*Remove white cases and special characters(if any)
	Library used:'re' i.e. regular expressions
	Inline procedure:
	Input: keyword extracted from given file
	Return Value:Processed Keyword
	"""
	keyword=str(keyword)	
	keyword=(keyword.lower()).replace(" ","")
	keyword=re.sub('[^A-Za-z0-9]+', '', keyword)
	return keyword

def get_index(keyword):
	"""
	Process:Index calculation
	*index is a sum of ascii of all charcters in keyword, It's modulo used to map to filename
	*index2 is a sum of ascii multiplied by ptr ranging from 1 to len(keyword), Its's modulo
		 used to map to odd/even row inside a file     
	Input: keyword extracted from given file
	Return Value:value of index mod with Prime number that yields number in range (0, mod-1), value of index2
	"""
	index=0
	index2=0
	ptr=1
	keyword="".join(keyword)
	for c in keyword:
		index=index+ord(c)
		index2=index2+ord(c)*ptr
		ptr+=1	
	return index%mod,index2	      


def get_basename(filename):
	"""
	Input:Filename
	Output:Basename
	Example: 
		Input:data/data.txt
		Output:data
	"""
	fname=os.path.basename(filename)
	basename,extension=os.path.splitext(fname)
	return basename
	

@t.timeit
def get_data_from_oe(index_file,keyword,index):	
	"""
	Process:Selective scanning of odd/even rows based ypon value of index%2.
	Input:index_file path, in which our keyword will be present, keyword(s) to search and index that after 
	modulo with two has values either 0 or 1 denoting even or odd row, in which keyword will be present.
	Output:entire row at which column value matches
	"""
	if(index%2==0):
		f=open(index_file,"r")
		for lines in itertools.islice(f,0,None,2):
			part=lines.split("$#|#$")
			row=part[0].split("#$|$#")
			flag=0
			#print(row)
			for i in range(0,len(keyword)):
				#print(keyword[i],row[i])
				if (keyword[i]!=row[i]):
					   flag=1
			if(flag==0):
				  return part		   
				
	else:
		f=open(index_file,"r")
		for lines in itertools.islice(f,1,None,2):
			part=lines.split("$#|#$")
			row=part[0].split("#$|$#")
			flag=0
			#print("-",row)
			for i in range(0,len(keyword)):
				#print(keyword[i],row[i])
				if (keyword[i]!=row[i]):
					   flag=1
			if(flag==0):
				  return part


def break_data(lines):
	   """
		Process:Open original data file, decompress value segement, replace back '|#$#|' with \n. Retrieve value and
				seek file pointer to retrived offset value and read data from file pointer from that offset to retrived
				length.
		Input:Row in which key value is matched
		Output: NA
	   """
	   f=os.open(filename,os.O_RDWR)
	   try:
		   w=zlib.decompress(lines[1].replace("|#$#|","\n"))
		   row=w.split(",")
		   for l in row:
			   d=l.split()
			   use_seek(f,d[1],d[2])

	   except:
		   print("Decompressing failed")
	   print("Total number of records feteched: "+str(len(row)))	
	   os.close(f)		   		 


@t.timeit
def use_seek(f,start,length):	
	os.lseek(f,int(start),0)
	str=os.read(f,int(length))
	print str.strip()				

@t.timeit
def high_seek(file,start,length):
	f=open(file,"r")
	f.seek(int(start),0)
	str=f.read(int(length))
	print str

@t.timeit
def raw_scan(filename,keyword):
	f=open(filename,"r")
	reader=csv.reader(f,delimiter="|")
	for lines in reader:
		#print(lines[0])
		if lines[0].lower()==keyword.lower():
			print(lines)
							
try: 
	sys.argv[1]
	

except:
	print("Only 1 parameter required to search.\nPlease enter Filename to search in")

else:
	mod=11
	filename=sys.argv[1]
	form="oe"
	keyword=[]
	index_col=[]
	x=input("Enter no. of columns: ")
	
	for i in range(0,x):
		index_col.append(input("Enter index of column: "))
		keyword.append(process_keyword(raw_input("Enter keyword to search in this index: ")))
		

	if not os.path.isfile(filename):
		print("File not found")
	else:
		
		init_hash,index2=get_index(keyword)
		base=get_basename(filename)
		
				
		if(form=="oe"):
				index_file="data/oe/base_index_"+str(init_hash)+".txt"
				#print(index_file)
				lines=get_data_from_oe(index_file,keyword,index2)
				
				break_data(lines)
				#high_seek(f,o,l)
				#print(type(row))

		elif(form=="raw"):
				raw_scan(filename,keyword[0])

					
						

					   
