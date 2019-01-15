# global useful vars

import numpy as np

MeshFormat = [None] * 3
Number0fNodes = 0
Nodes = [[None] *4 ]*100

def read_file(filename):
	with open(filename) as f:
		content = f.readlines()

	for i in range(0, len(content)):
		line = content[i]

		if line[0] == '$': # reading a property
			
			property = line[1:-1]
			print("yay :" + property + ":\n")
			if property == "MeshFormat":
				print("property: " + property + "\n")
				i+= 1
				line = content[i][0:-1]

				formats = line.split(" ");
				MeshFormat = formats # check if it works 
				print("format:\n")
				print(formats)

			elif property == "Nodes":
				i+=1
				line = content[i]
				#print ("---------->" + content[i][1:-1].split(" ")[0] + "-----\n")
				
				Number0fNodes = (int)(content[i][0:-1].split(" ")[0])

				i += 1;
				
				for j in range(i, i + Number0fNodes):
					Nodes[j - Number0fNodes] = [content[j][0:-1].split(" ")[:4]] 
					print("nodes : ")
					print(Nodes[j - Number0fNodes])


			elif property == "Elements":
				i+=1
				line = content[i]
				#print ("---------->" + content[i][1:-1].split(" ")[0] + "-----\n")
				
				Number0fElems = (int)(content[i][0:-1].split(" ")[0])

				i += 1;
				type = (int)(content[i][0:-1].split(" ")[1])

				print("Number0fElems = ")
				print(Number0fElems)

				vertice_n = 4;

				if type == 2: # triangle
					vertice_n = 3;
				elif type == 1:
					vertice_n = 2;
				
				Elems = [[None] *( 1 + vertice_n * 2) ]*(Number0fElems + 1)

				print(len(Elems))
				cnt = 0;
				for j in range(i, i + Number0fElems):
					print("cnt:" + str(cnt))

					Elems[cnt] = [content[j][0:-1].split(" ")[1:(vertice_n * 2 + 2)]]
					print("elems : ")
					print(Elems[cnt])
					cnt = cnt +1
			else:
				a = 2



read_file("input_sample.msh")