import itertools

f=open("test3.txt","r")
update=2
for l in f:
	print(l)
	next(f)
	next(f)