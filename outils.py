# global useful vars

import numpy as np


class Mesh:
	def __init__(this, Format_, Nodes,Elements):
		this.Format = Format_
		this.Nodes = Nodes
		this.Elements = Elements


class Node:
  def __init__(this, id, x,y, z):
    this.id = id
    this.x = x
    this.y = y
    this.z = z


class Element:
	def __init__(this, id, typeElem, tags, sommets ):
		this.id = id
		this.typeElem = typeElem
		this.tags = tags
		this.sommets = sommets


def read_file(filename):
	Nodes = np.empty((100, 4), dtype = np.float128)
	MeshFormat = np.empty(3, dtype = int) #[None] * 3
	Number0fNodes = 0

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

				formats = np.asarray( line.split(" ") );
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
					Nodes[j - i] = np.asarray([content[j][0:-1].split(" ")[:4]] )
					print("nodes : ")
					print(j -i)
					print(Nodes[j - i])


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
				
				#Elems = [[None] *( 1 + vertice_n * 2) ]*(Number0fElems + 1)

				Elems = np.empty((Number0fElems , 1 + vertice_n * 2 ), dtype = int)

				print(len(Elems))
				cnt = 0;
				for j in range(i, i + Number0fElems):
					print("cnt:" + str(cnt))
					Elems[cnt] = np.asarray([content[j][0:-1].split(" ")[1:(vertice_n * 2 + 2)]])
					print("elems : ")
					print(Elems[cnt])
					cnt = cnt +1
			else:
				a = 2
	
	# filling the object stuff:
	Nodes_ = np.empty(Number0fNodes, dtype = Node) #[Node]* (Number0fNodes+1);
	Elems_ = np.empty(Number0fElems, dtype = Element)

	cnt = 0
	for i in range(0, Number0fNodes):
		Nodes_[ i ] = Node(i,Nodes[i][1], Nodes[i][2], Nodes[i][3])


	for i in range(0, Number0fElems):
		Elems_[ i ] = Element(i, Elems[i][0], Elems[i][1:vertice_n], Elems[i][vertice_n+1:] ) #id type tags sommets

	princeMesh = Mesh(MeshFormat, Nodes_, Elems_)

	return princeMesh



our_mesh = read_file("input_sample.msh")
print(our_mesh.Format) #todo