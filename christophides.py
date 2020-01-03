import heapq
import numpy as np

def get_path(root):
	path=[node[root].data]
	for i in node[root].child:
		path+=get_path(i)
	return(path)
class Node:
	def __init__(self,data,child):
		self.data = data
		self.child = child


def euc_dist(p1,p2):
	return np.sqrt((p1[1]-p2[1])**2 + (p1[2]-p2[2])**2)

d_mat = {}
count = 0
opt_d = 9352
with open("tspdata_two.txt") as file1:
	for line in file1:
		d_mat[count] = [float(x) for x in line.split()]
		count+=1
dist = {}
par = {}
child = {}
for i in range(count):
	dist[i] = 10**100
	par[i] = ''
dist[0] = 0
par[0] = -1
corresponding = {}
for i in range(count):
	corresponding[dist[i]] = corresponding.get(dist[i],[])+[i]

visit = {}
heap = []	
for i in range(count):
	heap.append(dist[i])

heapq.heapify(heap)
#print(len(heap))

while(len(heap)!=0):
	n_v = corresponding[heap[0]][0]
	#print(n_v)
	visit[n_v] = 1
	corresponding[heap[0]].pop(0)
	heapq.heappop(heap)
	
	for i in range(count):
		if((i not in visit) and dist[i]>euc_dist(d_mat[n_v],d_mat[i])):
			par[i] = n_v
			corresponding[euc_dist(d_mat[n_v],d_mat[i])] = corresponding.get(euc_dist(d_mat[n_v],d_mat[i]),[])+[i]
			heap.append(euc_dist(d_mat[n_v],d_mat[i]))
			heap.remove(dist[i])
			dist[i] = euc_dist(d_mat[n_v],d_mat[i])
	heapq.heapify(heap)

ans = 0
for i in dist.keys():
	ans+=dist[i]

for i in range(count):
	child[par[i]] = child.get(par[i],[])+[i]
	
node = {}
for i in range(count):
	li = child.get(i,[])
	n = Node(i,li)
	node[i] = n

path = get_path(0)
path_len = 0
print(path)
for i in range(1,len(path)):
	path_len+=(euc_dist(d_mat[path[i]],d_mat[path[i-1]]))
print(path_len+euc_dist(d_mat[path[-1]],d_mat[0]))

print(len(np.unique(np.array(path))))
