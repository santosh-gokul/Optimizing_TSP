import numpy as np

def mutate(chro):
	
	rand1 = np.random.randint(0,14)
	rand2 = np.random.randint(0,14)

	chro[rand1],chro[rand2] = chro[rand2],chro[rand1]
	
	return(chro)

#Initial population of 25.
#Mutation rate: 0.15
#CrossOver probablity: 1.0
#Using uniform distribution for roulette wheel selection

#Reading the file and filling the distance matrix

d_mat = {}
count = 0
with open("tspdata.txt") as file1:
	for line in file1:
		d_mat[count] = line.split()
		count+=1

#Optimal Tour Length..
OPT =  [0,12,1,14,8,4,6,2,11,13,9,7,5,3,10,0]
opt_d = 0
for i in range(1,len(OPT)):
	opt_d+=int(d_mat[OPT[i-1]][OPT[i]])
print("The Optimal Tour Length: ",opt_d)

#Number of Iterations
exp = 0
#Stats Count
stats = 0

while(exp<10):
	#Dataset ready with d_mat.
	#Numpy array dict problem many ways exists to make the hashing faster.
	init_sol = np.arange(1,15)
	chr_ind = {}
	pop = []
	while(len(pop)<48):
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
	while(True):

		fitness = {}
		freq = {}
		tot_fit = 0
		for i in pop:
			fit = int(d_mat[0][i[0]])
			for j in range(1,len(i)):
				fit+=int(d_mat[i[j-1]][i[j]])
			fit+=int(d_mat[i[-1]][0])
			
			fitness[str(i)] = fitness.get(str(i),0)+(1/fit)
			freq[str(i)] = freq.get(str(i),0)+1
			tot_fit+=(1/fit)
			#print(str(i),hash(str(i)),fit)
		#Scaling FW between 0-1
		for i in fitness.keys():
			fitness[i]/=tot_fit
		pop = np.unique(pop,axis=0)
		#print("Population Length:",len(pop))
		#print(fitness)
		#print("Total:",tot_fit)
		pop = np.unique(pop,axis=0)
		pool = []
		if(gen==1000):
			break
		for ctr in range(48):
			rand = np.random.uniform()
			#print(rand)
			cum_freq = 0
			for i in fitness.keys():
				cum_freq+=fitness[i]
				if(rand<=cum_freq):
					pool.append(np.fromstring(i[1:-1],dtype=int,sep=' '))
					break

		#CrossOver phase...
		#Using Generational Approach
		#print("Pool length:",len(pool))
		next_gen = []
		sorted_x = sorted(fitness.items(), key=lambda kv: (kv[1]*tot_fit)/freq[kv[0]],reverse=True)
		#print(sorted_x)
		next_gen.extend([np.fromstring(i[0][1:-1],dtype=int,sep=' ') for i in sorted_x[:3]])
		for i in range(1,48,2):
			child1 = []
			child2 = []
			for j in pool[i-1]:
				if(j not in pool[i][5:8]):
					child1.append(j)
			child1 = np.concatenate((child1[:5],pool[i][5:8],child1[5:]))
			for j in pool[i]:
				if(j not in pool[i-1][5:8]):
					child2.append(j)
			child2 = np.concatenate((child2[:5],pool[i-1][5:8],child2[5:]))
			
			next_gen.extend([child1,child2])
		#I have some doubts in Genrational aspect after crossover phase. But assuming all the children become the next gen.
		ct = 0
		while(ct<3):
			next_gen.pop()
			ct+=1
		for i in range(1,int(0.1*len(next_gen))):
			next_gen[i] = mutate(next_gen[i])
		pop = list(next_gen)
		gen+=1
		#print(pop)

	#print(fitness)
	max_fit = fitness[str(pop[0])]*tot_fit/freq[str(pop[0])]
	path=str(pop[0])
	for i in fitness.keys():
		if(((fitness[i]*tot_fit)/freq[i])>max_fit):
			max_fit = ((fitness[i]*tot_fit)/freq[i])
			path = i
			

	print("The path is:",path,"The Associated Cost=",1/max_fit)
	stats+=(1/max_fit)-opt_d
	exp+=1

print("Average deviation from results: ",stats/10)

"""
#Optimal Tour Length:

OPT =  [0,12,1,14,8,4,6,2,11,13,9,7,5,3,10,0]
opt_d = 0
for i in range(1,len(OPT)):
	opt_d+=int(d_mat[OPT[i-1]][OPT[i]])
print("The Optimal Tour Length: ",opt_d)
"""
