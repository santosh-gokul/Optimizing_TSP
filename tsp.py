d_mat = [[0,10,15,20],[10,0,35,25],[15,35,0,30],[20,25,30,0]]

def tsp(visit):
	#Base case
	if(len(visit)==4):
		return(d_mat[visit[-1]][0])
	min_dist = []
	for i in range(4):
		if(i not in visit):
			v = visit.copy()
			v.append(i)
			min_dist.append(d_mat[visit[-1]][i]+tsp(v))
	return(min(min_dist))	
val = tsp([0])
print(val)
