# global useful vars

import numpy as np


class Mesh:
	def __init__(this, Format_, Ns,Nodes , Nt, Triangles):
		this.Format = Format_
		this.Nodes = Nodes
		this.Triangles = Triangles
		this.Ns = Ns
		this.Nt = Nt
		this.grad_phi_ref = np.array([[-1, -1], [1, 0], [0, 1]])


	def aire_element(this, id):
		if this.Triangles[id-1].typeElem == 15 or this.Triangles[id-1].typeElem == 1:
			return 0
		p1 = this.Nodes[this.Triangles[id-1].sommets[0]- 1]
		p2 = this.Nodes[this.Triangles[id-1].sommets[1]- 1]
		p3 = this.Nodes[this.Triangles[id-1].sommets[2]- 1]

		return abs(((p2.x - p1.x)*(p3.y - p1.y) - (p3.x - p1.x)*(p2.y - p1.y)) /2.0)

	def matrice_B(this, p):

		this.B = np.zeros((2, 2), dtype = complex)

		p1 = this.Nodes[this.Triangles[p].sommets[0]- 1]
		p2 = this.Nodes[this.Triangles[p].sommets[1]- 1]
		p3 = this.Nodes[this.Triangles[p].sommets[2]- 1]

		jac = (p2.x - p1.x)*(p3.y - p1.y) - (p3.x - p1.x)*(p2.y - p1.y)

		this.B[0][0] = (p3.y - p1.y)*(1.0/jac)
		this.B[0][1] = (p1.y - p2.y)*(1.0/jac)
		this.B[1][0] = (p1.x - p3.x)*(1.0/jac)
		this.B[1][1] = (p2.x - p1.x)*(1.0/jac)

		return this.B

	def matrice_mass(this):
		this.M = np.zeros((this.Ns, this.Ns), dtype = np.complex)

		for p in range(0, this.Nt):
			for i in range(0, 3):
				I = this.Triangles[p].sommets[i]
				for j in range(0, 3):
					J = this.Triangles[p].sommets[j]
					if i == j :
						this.M[I-1][J-1] += this.aire_element(p)/6.0
					else:
						this.M[I-1][J-1] += this.aire_element(p)/12.0
		return this.M

	def matrice_rigidite(this ):
		this.D = np.zeros((this.Ns, this.Ns), dtype = np.complex)

		for p in range(0, this.Nt):
			B = this.matrice_B(p)
			bTb = np.matmul(B, np.transpose(B))

			for i in range(0, 3):
				I = this.Triangles[p].sommets[i]
				for j in range(0, 3):
					J = this.Triangles[p].sommets[j]
					this.D[I-1][J-1] += this.aire_element(p) * np.matmul( np.transpose(this.grad_phi_ref[j]) ,np.matmul(bTb, this.grad_phi_ref[i]))


		return this.D




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


class Triangle:
	def __init__(this, id, tags, sommets ):
		this.id = id
		this.tags = tags
		this.sommets = sommets

class Segment:
	def __init__(this, id, sommets):
		this.id = id
		this.sommets = sommets


def read_file(filename):
	Nodes = np.empty((100, 4), dtype = np.float)
	MeshFormat = np.empty(3, dtype = int) #[None] * 3
	Number0fNodes = 0
	NumberOfTr = 0
	NumberOfSeg = 0

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

				Number0fElems = (int)(content[i][0:-1].split(" ")[0])

				i += 1;
				lent = content[i][0:-1].split(" ")
				Elems = list()#np.empty((Number0fElems ,0 ), dtype = list)

				print(len(Elems))
				cnt = 0;
				for j in range(i, i + Number0fElems): # todo i doesnt change

					print("merde:")
					print(content[i][0:-1].split(" "))
					type = (int)(content[i][0:-1].split(" ")[1])
					bntg = (int)(content[i][0:-1].split(" ")[2])

					print("nbtg")
					print(bntg)
					print("type")
					print(type)


					vertice_n = 4;

					if type == 2: # triangle
						vertice_n = 3;
						NumberOfTr += 1
						print("dans if triangle")
					elif type == 1:
						vertice_n = 2;
						NumberOfSeg +=1
						print("dans if segment")

					print("cnt:" + str(cnt))
					Elems.append(np.asarray([content[j][0:-1].split(" ")[2: ( vertice_n +bntg + 3)]]))  #[cnt] = np.asarray([content[j][0:-1].split(" ")[1:(vertice_n * 2 + 2)]])
					print("elems : ")
					print(Elems[cnt])
					cnt = cnt +1
			else:
				a = 2
	
	print("nbTr:")
	print(NumberOfTr)
	print("nbsg:")
	print(NumberOfSeg)

	# filling the object stuff:
	Nodes_ = np.empty(Number0fNodes, dtype = Node) #[Node]* (Number0fNodes+1);
	Elems_ = np.empty(Number0fElems, dtype = Element)
	Trs_ = np.empty(NumberOfTr, dtype = Triangle)
	
	segs_ext = np.empty(1, dtype = Segment)
	segs_int = np.empty(1, dtype = Segment)

	cnt = 0
	for i in range(0, Number0fNodes):
		Nodes_[ i ] = Node(i,Nodes[i][1], Nodes[i][2], Nodes[i][3])

	print("shape:")
	print(np.shape(Elems))
	#Elems = np.reshape(Elems, (Number0fElems, 7))
	#Elems = Elems.astype(int)
	print("shape:")
	print(np.shape(Elems))


	print("-----------------------------Elems:-------------------------")
	print(Elems)


	cntT = 0
	for i in range(0, Number0fElems):

		Elems_i = Elems[i][0].astype(int)

		print(Elems_i)

		nbTag = int(Elems[i][0][1])
		Elems[i] = Elems[i].astype( int)
		
		Elems_[ i ] = Element(i, Elems_i[0], Elems_i[2:2+nbTag], Elems_i[2+nbTag:] ) #id type tags sommets

		# Elems_[ i ] = Element(i, Elems[i][0][0], Elems[i][0][2:2+nbTag], Elems[i][0][2+nbTag:] ) #id type tags sommets

		if Elems_i[0] == 2:
			Trs_[cntT] = Triangle(i, Elems_i[0:nbTag],  Elems_i[nbTag:])
			cntT +=1
		elif Elems_i[0] == 1:
			seg_s = Segment(i, Elems_[i].sommets) 
			if Elems_[i].tags[0] == 1: #ext
				np.append(segs_ext, seg_s)
			else:
				if Elems_[i].tags[0] == 1: #int
					segs_int.append(seg_s)

	print("ext:")
	for i in segs_ext:
		print(i.sommets)
	
	print("ext:")
	for i in segs_int:
		print(i.sommets)

	princeMesh = Mesh(MeshFormat, Number0fNodes, Nodes_, Number0fElems , Elems_)

	return princeMesh



our_mesh = read_file("input_simple2.msh")

U = np.ones(13)

A=np.matmul(np.transpose(U),np.matmul(our_mesh.matrice_mass(),U))

A2=np.matmul(our_mesh.matrice_rigidite(),np.transpose(U))

print("aire de premier element")
print( our_mesh.aire_element(1)  )

print(our_mesh.Format) #todo

#print(our_mesh.matrice_rigidite())

#print("verification M")
#print(A)
print("\n--------------------verification D----------------------\n")
print(A2)