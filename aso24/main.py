import numpy as np
import sys
from ant_colony import AntColony
import matplotlib
import matplotlib.pyplot as plt
import random


def draw_gant(nb_machines,the_best_solution,arg1,colors,processing_times):
	# Declaring a figure "gnt"
	fig, gnt = plt.subplots()
	 
	# Setting Y-axis limits
	gnt.set_ylim(0, nb_machines*2*10)
	 
	# Setting X-axis limits
	gnt.set_xlim(0, the_best_solution[1])
	 
	# Setting labels for x-axis and y-axis
	gnt.set_xlabel('jobs')
	gnt.set_ylabel('machines')

	# Setting graph attribute
	gnt.grid(True)
	times  = {}
	yticklabels = []
	yticks = []
	for m in range(nb_machines):
		times[m] = 0
		yticklabels.append("machine "+str(m+1))
		yticks.append((m+1)*10+(5*m))
	# Setting ticks on y-axis
	gnt.set_yticks(yticks)
	# Labelling tickes of y-axis
	gnt.set_yticklabels(yticklabels)
	data = the_best_solution[0]
	patches = []
	for d in data:
		job=int(d.split(",")[0])-1
		machine=int(d.split(",")[1])-1
		time_of_process = processing_times[job][machine]
		patches.append(matplotlib.patches.Patch(color=colors["job"+str(job+1)]))
		gnt.broken_barh([(times[machine], time_of_process)], ( machine *10 + ((machine+1) * 5 ), 10), facecolors =colors["job"+str(job+1)], label = 'job'+str(job+1))
		times[machine]+=time_of_process
	plt.legend(handles=patches, labels=colors.keys(), fontsize=11)
	plt.show()
	plt.savefig(arg1.replace(".txt",".png"))
get_colors = lambda n: ["#%01x" % random.randint(0, 0xFFFFFF) for _ in range(n)]


def main(arg1):
	with open(arg1) as file:
		lines = [line.rstrip() for line in file]
	nb_jobs = int(lines[0])
	nb_machines = int(lines[1])
	processing_times=np.zeros((nb_jobs,nb_machines),dtype=int)
	print("nb_jobs : ",nb_jobs)
	print("nb_machines : ",nb_machines)
	i=0
	colors = plt.cm.rainbow(np.linspace(0, 1, nb_jobs))
	process_colors = {}
	for j in range(nb_jobs):
		process_colors["job"+str(j+1)] = colors[j]
	print("processing_times :")
	for line in lines[2:]:
		print(" | ".join(line.split(" ")))
		line_splited = line.split(" ")
		#print(line_splited)
		processing_times[i] = [int(x) for x in line_splited ]
		i+=1
		

	ant_colony = AntColony(processing_times, 10, 100, 20, 0.95, alpha=1, beta=1)
	the_best_solution = ant_colony.run()
	print("the_best_solution :")
	print("\n".join(["job " + b.split(",")[0] +" in machine "+ b.split(",")[1] for b in the_best_solution[0]]))
	print("the maximum time :",the_best_solution[1])
	draw_gant(nb_machines,the_best_solution,arg1,process_colors,processing_times)
	
if __name__ == "__main__":
    main(sys.argv[1])