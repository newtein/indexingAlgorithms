
def split_it(row):
	#print(row)
	un_r=row.split()
	return un_r[0],un_r[1]

def fetch_result(f,a):
	offset,length=split_it(a)
	f.seek(int(offset),0)
	s=f.read(int(length))
	#print("end",s)
	return s.strip()

def get_key(lp):
	row=lp.split('$#|$#')

	return row[0]
	
def init_check(b_file,start,middle,end,keyword):
	s_read=get_key(fetch_result(b_file,start))
	e_read=get_key(fetch_result(b_file,end))
	#print(s_read,end)
	if middle==None:		
		if s_read<=keyword<=e_read:
			if s_read==keyword:
				print(keyword,"Found")
				return 2
			if e_read==keyword:
				print(keyword,"Found")
				return 2
			return 0			
		else:
			#print("{}",s_read,e_read)
			#print(keyword,"Not Found")
			return -1
	else:
		m_read=get_key(fetch_result(b_file,middle))
		#print("Start",s_read,"Middle",m_read,"End",e_read)

		if s_read<=keyword<=m_read:
			if s_read==keyword:
				print(keyword,"Found")
				return 2
			if e_read==keyword:
				print(keyword,"Found")
				return 2
			if m_read==keyword:
				print(keyword,"Found")
				return 2
			return 0
		elif m_read<=keyword<=e_read:
			if s_read==keyword:
				print(keyword,"Found")
				return 2
			if e_read==keyword:
				print(keyword,"Found")
				return 2
			if m_read==keyword:
				print(keyword,"Found")
				return 2
			return 1
		else:
			#print(keyword,"-->Not Found")
			return -1




if __name__=="__main__":
	init=0
	result=0
	count=-1
	skip=2
	keyword="newdelhi"
	middle=None
	f=open("3ltest.txt","r")
	b_file=open("3level.txt","r")
	for l in f:
		count+=1
		row=l.split('$#|$#')
		row=[i.strip() for i in row]
		if init<2:
			if init==0:
				start=row[0]
				end=row[1]
				offset=init_check(b_file,start,middle,end,keyword)
				if offset==2 or offset==-1:
					break
				
			elif init==1:
				if end!=row[0]:
					print(end,row[0])
					print("Something went wrong")
				middle=row[1]

				
				offset=init_check(b_file,start,middle,end,keyword)
				#print(offset)
			#print("?",start,middle,end)

			
			#print(result)
			init+=1
		else:
				if offset==0 and row[0]==middle:
					print(result,count,skip)
					skip=skip*2-1
					result=0
					end=middle
					middle=row[1].split("#")[0]
					offset=init_check(b_file,start,middle,end,keyword)
					if offset==2 or offset==-1:
						break
				elif offset==1 and row[0]==middle:
					print("->",result,count,skip)
					skip=skip*2
					result=0
					start=middle
					middle=row[1].split("#")[1]
					offset=init_check(b_file,start,middle,end,keyword)
				if offset==2 or offset==-1:
					break
				#print(offset,"?",start,middle,end)
				result+=1
			

			


	b_file.close()
		