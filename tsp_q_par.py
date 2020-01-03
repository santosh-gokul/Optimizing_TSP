import numpy as np
import threading as td

class GA1(td.Thread):
	def __init__():
		td.Thread.__init__(self)
		self.d_mat = {}
		count = 0
		self.opt_d = 9352
		with open("lu980.txt") as file1:
			for line in file1:
				self.d_mat[count] = [float(x) for x in line.split()]
				count+=1
		init = self.heuristics(self.d_mat)
		init.pop()
		self.pop = []
		for i in range(0,193,14):
			for j in range(i+14,193,14):
				temp = init.copy()
				if(j+14>192):
					temp[j:],temp[i:(192-j+1)] = temp[i:(192-j+1)],temp[j:]
				else: 
					temp[j:j+14],temp[i:i+14] = temp[i:i+14],init[j:j+14]
				self.pop.append(np.array(temp))
#The size was 92, now making it 90
		pop.pop(0)
		pop.pop(1)

		print("Done reading the file: Check for sample",d_mat[count-1],euc_dist(d_mat[0],d_mat[1]))
	def run(self):
	while(True):
		fitness = {}
		freq = {}
		tot_fit = 0
		for i in pop:
			fit = euc_dist(d_mat[0],d_mat[i[0]])
			for j in range(1,len(i)):
				fit+=euc_dist(d_mat[i[j-1]],d_mat[i[j]])
			fit+=euc_dist(d_mat[0],d_mat[i[-1]])
			
			fitness[str(i)] = fitness.get(str(i),0)+(1/fit)
			freq[str(i)] = freq.get(str(i),0)+1
			tot_fit+=(1/fit)
		#Scaling FW between 0-1
		for i in fitness.keys():
			fitness[i]/=tot_fit
		
		pop = np.unique(pop,axis=0)
		print("Population Length:",len(pop))
		pool = []
		if(gen==1000):
			break
		for ctr in range(90):
			rand = np.random.uniform()
			cum_freq = 0
			for i in fitness.keys():
				cum_freq+=fitness[i]
				if(rand<=cum_freq):
					pool.append(np.fromstring(i[1:-1],dtype=int,sep=' '))
					break
		#CrossOver phase...
		#Using Generational Approach
		next_gen = []
		sorted_x = sorted(fitness.items(), key=lambda kv: (kv[1]*tot_fit)/freq[kv[0]],reverse=True)

		next_gen.extend([np.fromstring(i[0][1:-1],dtype=int,sep=' ') for i in sorted_x[:10]])

		for i in range(1,90,2):
			child1 = []
			child2 = []
			rang = get_best_range(pool[i])
			#print(rang,"For C1")
			for j in pool[i-1]:
				if(j not in pool[i][rang[0]:rang[1]]):
					child1.append(j)
			
			if(len(child1[rang[0]:])!=0 and len(child1[:rang[0]])!=0):
				child1 = np.concatenate((child1[:rang[0]],pool[i][rang[0]:rang[1]],child1[rang[0]:]))
			elif(len(child1[:rang[0]])==0):
			
				child1 = np.concatenate((pool[i][rang[0]:rang[1]],child1))
			else:
				child1 = np.concatenate((child1[:rang[0]],pool[i][rang[0]:rang[1]]))
			
			rang = get_best_range(pool[i-1])
			#print(rang,"For C2")
			for j in pool[i]:
				if(j not in pool[i-1][rang[0]:rang[1]]):
					child2.append(j)
			if(len(child2[rang[0]:])!=0 and len(child2[:rang[0]])!=0):
				child2 = np.concatenate((child2[:rang[0]],pool[i-1][rang[0]:rang[1]],child2[rang[0]:]))
			elif(len(child2[:rang[0]])==0):
				child2 = np.concatenate((pool[i-1][rang[0]:rang[1]],child2))
			else:
				child2 = np.concatenate((child2[:rang[0]],pool[i-1][rang[0]:rang[1]]))
	
			next_gen.extend([child1,child2])
		#I have some doubts in Genrational aspect after crossover phase. But assuming all the children become the next gen.
		ct = 0
		while(ct<10):
			next_gen.pop()
			ct+=1
		print("Next Gen length:",len(next_gen))
		for i in range(1,int(0.1*len(next_gen))):
			next_gen[i] = mutate(next_gen[i])
		pop = list(next_gen)
		gen+=1
	max_fit = fitness[str(pop[0])]*tot_fit/freq[str(pop[0])]
	path=str(pop[0])
	for i in fitness.keys():
		if(((fitness[i]*tot_fit)/freq[i])>max_fit):
			max_fit = ((fitness[i]*tot_fit)/freq[i])
			path = i
			

	print("The path is:",path,"The Associated Cost=",1/max_fit)
	stats+=(1/max_fit)-opt_d
	exp+=1

print("Average deviation from results: ",stats/1)
#Optimal Tour Length:
pop = []
		
#Number of Iterations
exp = 0
#Stats Count
stats = 0
init = heuristics(d_mat)
init.pop()

for i in range(0,193,14):
	for j in range(i+14,193,14):
		temp = init.copy()
		if(j+14>192):
			temp[j:],temp[i:(192-j+1)] = temp[i:(192-j+1)],temp[j:]
		else: 
			temp[j:j+14],temp[i:i+14] = temp[i:i+14],init[j:j+14]
		pop.append(np.array(temp))

pop.append(np.array(init))
#The size was 92, now making it 90
pop.pop(0)
pop.pop(1)



def mutate(chro):
	
	rand1 = np.random.randint(0,193)
	rand2 = np.random.randint(0,193)

	chro[rand1],chro[rand2] = chro[rand2],chro[rand1]
	
	return(chro)

def euc_dist(p1,p2):
	return np.sqrt((p1[1]-p2[1])**2 + (p1[2]-p2[2])**2)

def heuristics(d_mat):
	visit = {0:1}
	s_node = 0
	init = []
	ctr = 0
	while(ctr<194):
		min_d = 10**10
		for i in range(1,194):
			if(i not in visit):
				if(min_d>euc_dist(d_mat[s_node],d_mat[i])):
					mid_d = euc_dist(d_mat[s_node],d_mat[i])
					new_node = i
		#print(new_node)	
		s_node = new_node
		init.append(s_node)
		visit[s_node] = 1
		ctr+=1

	return(init)

def get_best_range(pooli):
	ctr = 0
	dist = []
	while(ctr<193):
		if((193-ctr)<13):
			break
		tmp_d = 0
		for i in range(ctr+1,ctr+20):
			if(i==193):
				break
			tmp_d+=euc_dist(d_mat[pooli[i]],d_mat[pooli[i-1]])	
		dist.append(tmp_d)
		ctr+=1
	min_d = min(dist)
	#print(len(dist))Work on programming & keen to learn technologies

	if(dist.index(min_d)+20>192):
		#return((20,40))
		return((dist.index(min_d),193))
	else:
		#return((20,40))
		return ((dist.index(min_d),dist.index(min_d)+20))
#Initial population of 25.'list' object cannot be interpreted as an integer
#Mutation rate: 0.15
#CrossOver probablity: 1.0
#Using uniform distribution for roulette wheel selection

#Reading the file and filling the distance matrix

d_mat = {}
count = 0
opt_d = 9352
with open("lu980.txt") as file1:
	for line in file1:
		d_mat[count] = [float(x) for x in line.split()]
		count+=1

print("Done reading the file: Check for sample",d_mat[count-1],euc_dist(d_mat[0],d_mat[1]))
#Number of Iterations
exp = 0
#Stats Count
stats = 0
init = heuristics(d_mat)
init.pop()

pop = []
for i in range(0,193,14):
	for j in range(i+14,193,14):
		temp = init.copy()
		if(j+14>192):
			temp[j:],temp[i:(192-j+1)] = temp[i:(192-j+1)],temp[j:]
		else: 
			temp[j:j+14],temp[i:i+14] = temp[i:i+14],init[j:j+14]
		pop.append(np.array(temp))

pop.append(np.array(init))
#The size was 92, now making it 90
pop.pop(0)
pop.pop(1)

while(exp<1):
	#Dataset ready with d_mat.
	#Numpy array dict problem many ways exists to make the hashing faster.
	"""
	init_sol = np.arange(1,194)
	chr_ind = {}
	pop = []
	while(len(pop)<90):
		chro = np.random.permutation(init_sol)
		if(chr_ind.get(str(chro),0)==0):
			pop.append(chro)
			chr_ind[str(chro)] = 1
	#Selection Procedure...
	#Implemented RW selection, many more to try
	gen = 0
	#pop.pop()
	#By default 0 is the starting city 
	#pop.append(np.array([12,14,1,4,8,2,6,11,13,9,7,5,3,10]))
	pop.pop()
	pop.append(np.array(init))
	"""
	while(True):
		fitness = {}
		freq = {}
		tot_fit = 0
		for i in pop:
			fit = euc_dist(d_mat[0],d_mat[i[0]])
			for j in range(1,len(i)):
				fit+=euc_dist(d_mat[i[j-1]],d_mat[i[j]])
			fit+=euc_dist(d_mat[0],d_mat[i[-1]])
			
			fitness[str(i)] = fitness.get(str(i),0)+(1/fit)
			freq[str(i)] = freq.get(str(i),0)+1
			tot_fit+=(1/fit)
		#Scaling FW between 0-1
		for i in fitness.keys():
			fitness[i]/=tot_fit
		
		pop = np.unique(pop,axis=0)
		print("Population Length:",len(pop))
		pool = []
		if(gen==1000):
			break
		for ctr in range(90):
			rand = np.random.uniform()
			cum_freq = 0
			for i in fitness.keys():
				cum_freq+=fitness[i]
				if(rand<=cum_freq):
					pool.append(np.fromstring(i[1:-1],dtype=int,sep=' '))
					break
		#CrossOver phase...
		#Using Generational Approach
		next_gen = []
		sorted_x = sorted(fitness.items(), key=lambda kv: (kv[1]*tot_fit)/freq[kv[0]],reverse=True)

		next_gen.extend([np.fromstring(i[0][1:-1],dtype=int,sep=' ') for i in sorted_x[:10]])

		for i in range(1,90,2):
			child1 = []
			child2 = []
			rang = get_best_range(pool[i])
			#print(rang,"For C1")
			for j in pool[i-1]:
				if(j not in pool[i][rang[0]:rang[1]]):
					child1.append(j)
			
			if(len(child1[rang[0]:])!=0 and len(child1[:rang[0]])!=0):
				child1 = np.concatenate((child1[:rang[0]],pool[i][rang[0]:rang[1]],child1[rang[0]:]))
			elif(len(child1[:rang[0]])==0):
			
				child1 = np.concatenate((pool[i][rang[0]:rang[1]],child1))
			else:
				child1 = np.concatenate((child1[:rang[0]],pool[i][rang[0]:rang[1]]))
			
			rang = get_best_range(pool[i-1])
			#print(rang,"For C2")
			for j in pool[i]:
				if(j not in pool[i-1][rang[0]:rang[1]]):
					child2.append(j)
			if(len(child2[rang[0]:])!=0 and len(child2[:rang[0]])!=0):
				child2 = np.concatenate((child2[:rang[0]],pool[i-1][rang[0]:rang[1]],child2[rang[0]:]))
			elif(len(child2[:rang[0]])==0):
				child2 = np.concatenate((pool[i-1][rang[0]:rang[1]],child2))
			else:
				child2 = np.concatenate((child2[:rang[0]],pool[i-1][rang[0]:rang[1]]))
	
			next_gen.extend([child1,child2])
		#I have some doubts in Genrational aspect after crossover phase. But assuming all the children become the next gen.
		ct = 0
		while(ct<10):
			next_gen.pop()
			ct+=1
		print("Next Gen length:",len(next_gen))
		for i in range(1,int(0.1*len(next_gen))):
			next_gen[i] = mutate(next_gen[i])
		pop = list(next_gen)
		gen+=1
	max_fit = fitness[str(pop[0])]*tot_fit/freq[str(pop[0])]
	path=str(pop[0])
	for i in fitness.keys():
		if(((fitness[i]*tot_fit)/freq[i])>max_fit):
			max_fit = ((fitness[i]*tot_fit)/freq[i])
			path = i
			

	print("The path is:",path,"The Associated Cost=",1/max_fit)
	stats+=(1/max_fit)-opt_d
	exp+=1

print("Average deviation from results: ",stats/1)
#Optimal Tour Length:
pop = []
