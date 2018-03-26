import itertools
import csv,re,json,sys
import os.path
import timecalc as t
import datetime,time
import zlib

"""
Todo
*Handle error if index column is somehow not present
"""
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
	return re.sub('[^A-Za-z0-9]+', '', (keyword.lower()).replace(" ",""))

def get_index(keyword):	
	"""
	Process:Index calculation
	*index is a sum of ascii of all charcters in keyword, It's modulo used to map to filename
	*index2 is a sum of ascii multiplied by ptr ranging from 1 to len(keyword), Its's modulo
		 used to map to odd/even row inside a file     
	Input: keyword extracted from given file
	Return Value:index value, mod with Prime number that yields number in range (0, mod-1), value of index2
	"""
	index,index2,ptr=0,0,1
	for c in "".join(keyword):
		index=index+ord(c)
		index2=index2+ord(c)*ptr
		ptr+=1	
	return index,index%mod,index2	


def get_basename(filename):
	"""
	Input:Filename
	Output:Basename
	Example: 
		Input:data/data.txt
		Output:data
	"""
	basename,extension=os.path.splitext(os.path.basename(filename))
	return basename

def make_list(row,offset,length):
	"""
	Returns a list
	"""
	return ([str(row), str(offset), str(length)])

def process_key(t):
	"""
	Input:List of key(s)
	Output:Convert into string by joining with separator '#$|$#'
	"""
	return "#$|$#".join(str(i) for i in t)
	#below return can be used, if key compression is also required. Although that doesn't makes much difference,
	#    only the overhead increases.
	#return zlib.compress("#$|$#".join(str(i) for i in t)).replace("\n","|#$#|")

	
def process_list(l):
	"""
	Process:List of lists is converted into string, using comma as separator between lists 
			and whitespace as separator between individual elements inside a list, then it is 
			compressed using zlib and finally if any '\n' is generated as a result of compression
			then it is replaced by '|#$#|' to avoid faculty reading and corresponding decompression. 
	Input: List of lists
	Output:Compressed string with zlib
	Library used:zlib (inbuild with python 2.7)
	"""
	s=""
	fool=0
	for info in l:
		if(fool!=0):
			s=s+","
		s=s+" ".join(info)
		fool=1
	return zlib.compress(s).replace("\n","|#$#|")


def insert_o_e_to_file(base,even,odd):
	"""
	Process:'mod' number of file is created and written like odd-even-odd-even format, residual dataset is sent to 
			'insert_residual' procedure. Separetor '$#|#$' is used between key-value.
	Input:base name of file, 2 data structures namely odd and even of 
			type [{0:{key1:[[],[],[]],key2:[[],[],[]]},1:{key1:[[],[],[]],key2:[[],[],[]]},...}]
	Output:NA        
	"""
	for i in range (0,mod):
		index_file="data/oe/base_index_"+str(i)+".txt"
		fo=open(index_file,"w")		
		ptr=1		
		for e, o in zip(even[i][i], odd[i][i]):
			fo.write(process_key(e)+"$#|#$"+process_list(even[i][i][e])+"\n")
			fo.write(process_key(o)+"$#|#$"+process_list(odd[i][i][o])+"\n")

		if(len(even[i][i])>len(odd[i][i])):	
			residue=len(odd[i][i])
			eo=0
			insert_residual(fo,even[i][i],list(even[i][i])[residue:],eo)
		else:	
			residue=len(even[i][i])
			eo=1
			insert_residual(fo,odd[i][i],list(odd[i][i])[residue:],eo)	
		fo.close()	         	
			

def insert_residual(fo,d,oe_list,oe):
	"""
	Process: Inserting residual odd or even data structure to file in format: odd/even - '\n'
	Input:File pointer, dictionary of residual key and values, list of residual keys, decision parameter oe i.e. used 
		   to distinguish weather residue data strcuture is odd or even
	"""
	if(oe==0):
		for keys in oe_list:
		   fo.write(process_key(keys)+"$#|#$"+process_list(d.get(keys))+"\n")	
		   fo.write("\n")		 
	else:
		for keys in oe_list:		   
		   fo.write("\n") 	
		   fo.write(process_key(keys)+"$#|#$"+process_list(d.get(keys))+"\n")		
					   

def init_odd_even_var():
	"""
	Input:NA
	Output:even, odd data-stucture of type [{0:{}},{1:{}},{}...]
	"""
	odd=[0]*mod
	even=[0]*mod
	for i in range(0,mod):
		odd[i]={}
		odd[i][i]={}
		even[i]={}
		even[i][i]={}
	return even, odd	

@t.timeit
def init_hash_odd_even(filename,sep,index_col,mod,base):
		"""
		Process:Initiates variables and commence file-reading by most simplest method, then split row with given separator
				process_each keyword, if multiple index col is given, eventually find its index value, then calculate 
				offset value of row i.e. size of row and length i.e. the extension of offset. The system then creates 
				a data structure, append all duplicate entry under the key, creating a list of list of values and then finally 
				writing it in mod files in programatic method.
		Input:Complete path of file, separator used in file, 
			  Col(s) to index, prime number to modulo with, basename of file.
		Output:Returns 1 on success else throws an error      
		"""	
		even, odd=init_odd_even_var()
		f=open(filename,"r")
		offset=0
		row=0			
		for line in f:	
				keyword=[]
				l=line.split(sep)
				for cols in index_col:
					try:		
						keyword.append(process_keyword(l[int(cols)].strip()))	
					except:
						pass		
				index,init_hash,index2=get_index(keyword)
				length=len(str(line))			
				data_list=make_list(row,offset,length)
				offset=offset+length
				keyword=tuple(keyword)				
				if index2%2!=0:
				  #print(keyword)	
				  if keyword not in odd[init_hash][init_hash]:
							 odd[init_hash][init_hash][keyword]=[]
				  odd[init_hash][init_hash][keyword].append(data_list)
				else:  
				  if keyword not in even[init_hash][init_hash]:
							 even[init_hash][init_hash][keyword]=[]
				  even[init_hash][init_hash][keyword].append(data_list)
				row+=1
		print("Data structure created successfully. File writing started...")		
		insert_o_e_to_file(base,even,odd)	
		del even
		del odd				  
		return 1

def create_meta_data(index_col,mod,filename,basename):
	f=open(basename+"_META_.txt","w")
	t=datetime.datetime.fromtimestamp(time.time()).strftime('%Y-%m-%d %H:%M:%S')
	t=str(t)

	message0="Time: "+t+"\nFilename: "+basename+"\nFile-Path: "+filename+"\nColumn Indexed: "+str(index_col)+"\nKey-Value Separator:$#|#$\nWithin Key Separator:#$|$#\nValue separator:,\nEach field inside value: (WHITE_SPACE)\nOutput: "+str(mod)+" compressed txt files"
	f.write(message0+"\n--------------------------Description--------------------------\n\n")
	message1="Index of "+filename+" [column(s): "+",".join(index_col)+" ] has been successfully created on "+t+". Output is "+str(mod)+" files."
	f.write(message1+"\n")
	message2="Data in stored in the form of key and values. Key denotes tuple of keywords from indexed column and value is a compressed list of list containing [row number, offset value, length of data segment]. To avoid mixing up of special charcters during compression using zlib '$#|#$' is used as a separater between key and values. '#$|$#' between multiple keywords inside each key, if any and value(s) are separated by 'commas'"
	f.write(message2+"\n")
	message3="Algorithm comprises of two level indexing using hashed approch. At first level every keyword is processed (converted in lower case and spaces and special charcters are eliminated), then, summation of ascii of each keyword is performed, followed by its modulos by "+str(mod)+". That generates index parameter ranging from 0 to "+str(mod-1)+". Example: Keyword 'XYZ' is convered to 'xyz' and its summation value is 363 and its index paramater is 363mod11 i.e. 0, it denotes that this keyword will be present in index file 0"
	f.write(message3+"\n")
	message4="Second level indexing uses binary odd, even inserting into respective index file. odd/even decision parameter is generated by following approch. Example: 'xyz' ascii(x)*1+ascii(y)*2+ascii(z)*3 then modulo of this value is performed by 2, resulting either 0 or 1. if output is zero then keyword is placed in even row and if one then odd row"
	f.write(message4+"\n")
	f.close()
if __name__=='__main__':
	try:
		sys.argv[1]
		sys.argv[2]
		sys.argv[3]		
	except:
		print("""Supply exactly 3 parameters file-path followed by Separator and index of to be indexed coloumn(s)\nExample:python2 python.py data/data.txt $pipe 1 2\nExplanation:python.py is filename to compile, data/data.txt is path of file to be indexed, $pipe is the separetor and 1,2 are indices of coloumns to be indexed\nAvalilable Separator $comma, $pipe, $tab.""")
	
	else:
		separ={'$pipe':"|","$tab":"\t","$comma":","}
		filename=sys.argv[1]
		sep=separ.get(sys.argv[2])
		index_col=sys.argv[3:]
		mod=11 
		base=get_basename(filename)
		success=init_hash_odd_even(filename,sep,index_col,mod,base)
		create_meta_data(index_col,mod,filename,base)
		if(success==1):
		   print("Hash generated successfully.")
		else:
		   print("Error")   

