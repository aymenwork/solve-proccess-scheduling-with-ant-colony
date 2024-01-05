import random as rn
import numpy as np
from numpy.random import choice as np_choice

class AntColony(object):

    def __init__(self, jobs, n_ants, n_best, n_iterations, decay, alpha=1, beta=1):
        """
        Args:
            jobs (2D numpy.array): Square matrix where each line is a job and each column is the time of execution on each machine.
            n_ants (int): Number of ants running per iteration
            n_best (int): Number of best ants who deposit pheromone
            n_iteration (int): Number of iterations
            decay (float): Rate it which pheromone decays. The pheromone value is multiplied by decay, so 0.95 will lead to decay, 0.5 to much faster decay.
            alpha (int or float): exponenet on pheromone, higher alpha gives pheromone more weight. Default=1
            beta (int or float): exponent on distance, higher beta give distance more weight. Default=1

        Example:
            ant_colony = AntColony(german_distances, 100, 20, 2000, 0.95, alpha=1, beta=2)          
        """
        self.jobs  = jobs
        self.pheromone = np.ones((len(jobs)*len(jobs[0])))
        #cuple of association ex 1,1 => job 1 is associated to machine1..
        self.all_inds = [str(x+1)+','+str(y+1) for x in range(len(jobs)) for y in range(len(jobs[0]))]
        self.n_ants = n_ants
        self.n_best = n_best
        self.n_iterations = n_iterations
        self.decay = decay
        self.alpha = alpha
        self.beta = beta

    def run(self):
        shortest_path = None
        all_time_shortest = ("placeholder", np.inf)
        for i in range(self.n_iterations):
            all_paths = self.gen_all_possibilities()
            self.spread_pheronome(all_paths, self.n_best, shortest_path=shortest_path)
            shortest_path = min(all_paths, key=lambda x: x[1])
            if shortest_path[1] < all_time_shortest[1]:
                all_time_shortest = shortest_path            
            self.pheromone = self.pheromone * self.decay            
        return all_time_shortest

    def spread_pheronome(self, all_paths, n_best, shortest_path):
        sorted_paths = sorted(all_paths, key=lambda x: x[1])
        for path, dist in sorted_paths[:n_best]:
            for move in path:
                self.pheromone[(int(move.split(",")[0])-1)*len(self.jobs[0])+(int(move.split(",")[1])-1) ] += 1.0 / self.jobs[int(move.split(",")[0])-1][int(move.split(",")[1])-1]

	#get the time max that a machine took
    def gen_path(self, path):
        total_dist = 0
        max_value= 0
        for i in range(len(self.jobs[0])):
        	process = [x.split(',')[0] for x in path if x.split(',')[1] == str(i+1) ]
        	new_max = 0
        	for p in process:
        		new_max+=self.jobs[int(p)-1][i]
        		if(new_max > max_value):
        			max_value = new_max
        return max_value
        

    def gen_all_possibilities(self):
        all_possibilities = []
        for i in range(self.n_ants):
        	for j in range(len(self.jobs)):
        		for k in range(len(self.jobs[0])):
        			start=str(j+1)+","+str(k+1)
        			possibility = self.gen_posibility(start)
        			all_possibilities.append((possibility, self.gen_path(possibility)))
        return all_possibilities
        
    def gen_posibility(self,start):
        possibility = []
        visited = set()
        visited.add(start)
        possibility.append(start)
        prev = start
        while(len(possibility) < len(self.jobs)):
            move = self.pick_move(self.pheromone, self.jobs[int(prev.split(",")[0])-1][int(prev.split(",")[1])-1], visited)
            possibility.append(move)
            visited.add(move)
        return possibility
        
    def pick_move(self, pheromone, dist, visited):
        pheromone = np.copy(pheromone)
        for v in visited:
        	c=0
        	#if a job was assigned to a machine we put the propability to reassign the same job to another machine to 0 , in this path
        	for l in range(len(self.jobs[0])):
        		pheromone[(int(v.split(",")[0])-1)*len(self.jobs[0]) + c ] = 0
        		c+=1
        row = pheromone ** self.alpha * (( 1.0 / dist) ** self.beta)
        norm_row = row / row.sum()
        move = np_choice(self.all_inds, 1, p=norm_row)[0]
        return move