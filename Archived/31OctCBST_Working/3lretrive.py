import itertools


def split_it(row):
	un_r=row.split()
	if len(un_r)==2:
		return un_r[0],un_r[1]
	else:
		return None,None


def fetch_result(f,a):
	offset,length=split_it(a)
	if offset is not None and length is not None:
		f.seek(int(offset),0)
		s=f.read(int(length))
		##print("end",s)
		return s.strip()
	else:
		return None

def get_key(lp):
	row=lp.split('$#|$#')

	return row[0]


def init_check(b_file,start,middle,end,keyword):
	s_read=get_key(fetch_result(b_file,start))
	e_read=get_key(fetch_result(b_file,end))
	#print("keys",s_read,e_read)
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
			##print("{}",s_read,e_read)
			print(keyword,"Not Found")
			return -1
	else:
		m_read=get_key(fetch_result(b_file,middle))
		#print("Start",s_read,"Middle",m_read,"End",e_read)

		if s_read<=keyword<=m_read:
			if s_read==keyword:
				#print(keyword,"Found")
				return 2
			if e_read==keyword:
				#print(keyword,"Found")
				return 2
			if m_read==keyword:
				#print(keyword,"Found")
				return 2
			return 0
		elif m_read<=keyword<=e_read:
			if s_read==keyword:
				#print(keyword,"Found")
				return 2
			if e_read==keyword:
				#print(keyword,"Found")
				return 2
			if m_read==keyword:
				#print(keyword,"Found")
				return 2
			return 1
		else:
			##print(keyword,"-->Not Found")
			return -1




if __name__=="__main__":
	# init is used to restrict to headers only
	# count is row count of entire file
	init=0
	ptr=0
	result=0
	count=0
	update=0
	keyword="8"
	middle=None
	prev_jump=[0]
	f=open("3ltest.txt","r")
	b_file=open("3level.txt","r")
	for l in f:
		

		row=l.split('$#|$#')
		row=[i.strip() for i in row]
		print("\n\nCount",count,"Data",row)
		count+=1
		
		
		if init<2:
			
			if init==0:
				start=row[0]
				end=row[1]
				offset=init_check(b_file,start,middle,end,keyword)
				if offset==2 or offset==-1:
					#print("offset",offset)
					break

			elif init==1:
				if end!=row[0]:
					#print(end,row[0])
					print("Something went wrong")
				middle=row[1]


				offset=init_check(b_file,start,middle,end,keyword)
				#print("offset",offset)
			##print("?",start,middle,end)


			##print(result)
			init+=1
		else:
				#print("\n\nCount",count,"Data",[fetch_result(f,row[0]),fetch_result(f,row[1].split("#")[0]),fetch_result(f,row[1].split("#")[1])])
			
				if offset==0 and row[0]==middle:
					#print("-->",result,"count",count,"update",update)
					#skip=skip*2-1
					update=update*2+1
					result=0
					end=middle
					middle=row[1].split("#")[0]
					offset=init_check(b_file,start,middle,end,keyword)
					if offset==2 or offset==-1:
						print(offset)
						break
				elif offset==1 and row[0]==middle:
					#print("---->",result,"count",count,"update",update)
					#skip=skip*2
					update=update*2+2
					result=0
					start=middle
					middle=row[1].split("#")[1]
					offset=init_check(b_file,start,middle,end,keyword)

				if offset==2 or offset==-1:
					print(offset)
					print("found")
					break
				for i in range(update-prev_jump[-1]-1):
					next(f)
					

				print(update,update-prev_jump[-1])
				prev_jump.append(update)

	  





	b_file.close()
