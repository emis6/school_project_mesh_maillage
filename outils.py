# -*- coding: utf-8 -*-
"""
Mesh project script containing mesh class, read/write functions
Mahshid Khezri Nejad Paola Allegrini
Prof: Bertrand Thierry
"""

import numpy as np
from math import cos, sqrt, sin
from cmath import exp


"""
Class Mesh: Contains the essential information of a mesh: Triangles, Nodes, Exterieur Bord and interieur bord

It also aontains the necessery functions that calculate "Masse", "Rigidite" ->A matrices and the vector b 

The function vector_U calculates the solution to the given problem and puts it in the vector U

"""
class Mesh:
	def __init__(this, Format_, Ns,Nodes , Nt, Triangles, b_ext_size, Bord_exts, b_int_size, Bord_int, k, alpha):
		this.Format = Format_
		this.Nodes = Nodes
		this.Triangles = Triangles
		this.Ns = Ns
		this.Nt = Nt
		this.grad_phi_ref = np.array([[-1, -1], [1, 0], [0, 1]])

		this.k = k
		this.alpha = alpha
		
		this.b_ext_size = b_ext_size
		this.Bord_exts = Bord_exts

		this.b_int_size = b_int_size
		this.Bord_int = Bord_int

		this.Nodes_inter = []
		this.find_int_nodes()
		this.matrice_mass()
		this.matrice_rigidite()

		this.vector_b()
		this.matrice_A()
		#this.vector_U()

	"""
	finds internal bound's nodes' id_s
	"""
	def find_int_nodes(this):
		this.Nodes_inter = []
		
		for i in range(0, this.b_int_size):
			for s in this.Bord_int[i].sommets:
				if not(s in this.Nodes_inter ):
					this.Nodes_inter.append(s)


	"""
	calculates area of a triangle
	"""
	def aire_element(this, id):
		p1 = this.Nodes[this.Triangles[id-1].sommets[0]- 1]
		p2 = this.Nodes[this.Triangles[id-1].sommets[1]- 1]
		p3 = this.Nodes[this.Triangles[id-1].sommets[2]- 1]

		return abs(((p2.x - p1.x)*(p3.y - p1.y) - (p3.x - p1.x)*(p2.y - p1.y)) /2.0)

	"""
	calculates area of a line segment , 
	- id : id of segment to find it in segments arrays 
	- quoi = 1 indicates if this segemnts belongs to an exterieur bound / or else it belongs to an internal bound
	"""
	def aire_seg(this, id, quoi):
		if quoi == 1:
			p1 = this.Nodes[this.Bord_exts[id-1].sommets[0]- 1]
			p2 = this.Nodes[this.Bord_exts[id-1].sommets[1]- 1]
		else:
			p1 = this.Nodes[this.Bord_int[id-1].sommets[0]- 1]
			p2 = this.Nodes[this.Bord_int[id-1].sommets[1]- 1]

		return (np.sqrt( (p1.x - p2.x)**2 + (p1.y - p2.y)**2 ))

	"""
	u_inc function
	- x : first coordinate of a point
	- y : second coordinate of a point
	"""
	def u_inc(this, x, y):
		return exp(np.complex(0, 1)*this.k) * (x*np.cos(this.alpha) + y*np.sin(this.alpha))

	def vector_b(this):
		this.b = np.zeros(this.Ns, dtype = complex)

		for id_s in this.Nodes_inter:
			p = this.Nodes[id_s-1]
			this.b[id_s-1] = - this.u_inc(p.x, p.y)
		return this.b

	"""
	Matrix A's calculation: 
	"""
	def matrice_A(this):
		# this.A = this.M + this.D
		this.A = np.zeros((this.Ns, this.Ns), dtype = np.complex)

		for i in range(1, this.Ns):
			for j in range(1, this.Ns):
				this.A[i][j] = this.M[i][j] + this.D[i][j]

		for id_s in this.Nodes_inter:
			this.A[int(id_s) -1][:] = 0
			this.A[int(id_s) -1][int(id_s) -1] = 1
		return this.A
	
	"""
	Matrix B's calculation, this matrix is to be used in calculating matrix D
	"""
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
					if i == j : # 2
						this.M[I-1][J-1] += (this.k) * (this.k) * this.aire_element(p+1)/6.0
					else: # 1
						this.M[I-1][J-1] += (this.k) * (this.k) * this.aire_element(p+1)/12.0

		for p in range(0, this.b_ext_size):
			for i in range(0, 2):
				I = this.Bord_exts[p].sommets[i] 
				for j in range(0, 2):
					J = this.Bord_exts[p].sommets[j]
					if i == j : # 2 
						this.M[I-1][J-1] += np.complex(0, -1) * (this.k) * this.aire_seg( p+1, 1 ) /3.0 # * (this.k) * this.aire_element(p)/6.0
						
					else : # 1
						this.M[I-1][J-1] += np.complex(0, -1) * (this.k) * this.aire_seg( p+1, 1 )/6.0


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
					this.D[I-1][J-1] += (-1)*(this.aire_element(p+1) ) * np.matmul( np.transpose(this.grad_phi_ref[j]) ,np.matmul(bTb, this.grad_phi_ref[i]))
					this.D[I-1][J-1] = np.real(this.D[I-1][J-1])
		return this.D

	def vector_U(this):
		this.U = np.linalg.solve(this.A, this.b)
		print(this.U)
		for n in this.Nodes:
			this.U[n.id -1 ] = np.abs(this.U[n.id-1] + this.u_inc(n.x, n.y))

		return this.U


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

"""
Reading a gmsh file and filling a mesh object
"""
def read_file(filename):
	Nodes = np.empty((100000, 4), dtype = float)
	MeshFormat = np.empty(3, dtype = int) #[None] * 3
	Number0fNodes = 0
	NumberOfTr = 0
	NumberOfSeg = 0
	Number0fElems = 0

	cnt_ext = cnt_inter = 0

	with open(filename) as f:
		content = f.readlines()

	for i in range(0, len(content)):
		line = content[i]

		if line[0] == '$': # reading a property
			
			property = line[1:-1]
			if property == "MeshFormat":
				i+= 1
				line = content[i][0:-1]

				formats = np.asarray( line.split(" ") );
				MeshFormat = formats # check if it works 


			elif property == "Nodes":
				i+=1
				line = content[i]
			
				Number0fNodes = (int)(content[i][0:-1].split(" ")[0])

				i += 1;
				
				for j in range(i, i + Number0fNodes):
					Nodes[j - i] = np.asarray([content[j][0:-1].split(" ")[:4]] )

			elif property == "Elements":
				i+=1
				line = content[i]

				Number0fElems = (int)(content[i][0:-1].split(" ")[0])

				i += 1;
				lent = content[i][0:-1].split(" ")
				Elems = list()#np.empty((Number0fElems ,0 ), dtype = list)

				cnt = 0;
				for j in range(i, i + Number0fElems): # todo i doesnt change

					type = (int)(content[j][0:-1].split(" ")[1])
					bntg = (int)(content[j][0:-1].split(" ")[2])

					vertice_n = 4;

					if type == 2: # triangle
						vertice_n = 3;
						NumberOfTr += 1
						
					elif type == 1:
						vertice_n = 2;
						NumberOfSeg +=1

					Elems.append(np.asarray([content[j][0:-1].split(" ")[1: ( vertice_n +bntg + 3)]]))  #[cnt] = np.asarray([content[j][0:-1].split(" ")[1:(vertice_n * 2 + 2)]])

					if Elems[-1][0][0] == '1' and Elems[-1][0][2] == '1':
						cnt_ext += 1
					if Elems[-1][0][0] == '1' and Elems[-1][0][2] == '2':
						cnt_inter += 1

					cnt = cnt +1
			else:
				a = 2

	Nodes_ = np.empty(Number0fNodes, dtype = Node) #[Node]* (Number0fNodes+1);
	Elems_ = np.empty(Number0fElems, dtype = Element)
	Trs_ = np.empty(NumberOfTr, dtype = Triangle)
	

	segs_ext = np.empty(cnt_ext, dtype = Segment)
	segs_int = np.empty(cnt_inter, dtype = Segment)

	cnt = 0
	for i in range(0, Number0fNodes):
		Nodes_[ i ] = Node(i,Nodes[i][1], Nodes[i][2], Nodes[i][3])

	ide_ext = ide_int = 0


	cntT = 0
	for i in range(0, Number0fElems):

		Elems_i = Elems[i][0].astype(int)

		nbTag = int(Elems[i][0][1])
		Elems[i] = Elems[i].astype( int)
		
		Elems_[ i ] = Element(i, Elems_i[0], Elems_i[2:2+nbTag], Elems_i[2+nbTag:] ) #id type tags sommets


		if Elems_i[0] == 2:
			Trs_[cntT] = Triangle(i, Elems_i[2:nbTag],  Elems_i[2+nbTag:])
			cntT +=1


		elif Elems_i[0] == 1:

			if int(Elems_i[2]) == 1: #ext
				segs_ext[ide_ext] = Segment(i, Elems_i[2+nbTag:]) #seg_s;
				ide_ext += 1
				
			else:
				if Elems_i[2] == 2: #int
					segs_int[ide_int] = Segment(i, Elems_i[2+nbTag:])#seg_s
					ide_int +=  1

	princeMesh = Mesh(MeshFormat, Number0fNodes, Nodes_, NumberOfTr , Trs_, cnt_ext, segs_ext , cnt_inter, segs_int,(2*np.pi)/(1.2), 0) #def __init__(this, Format_, Ns,Nodes , Nt, Triangles):
	return princeMesh

"""
Writing the solution and the mesh into a file readable by paraview
"""
def write_file( mesh_, ):
	out_file="./out_put.vtu"
	file = open(out_file,"w")
	file.write('<VTKFile type="UnstructuredGrid" version="1.0" byte_order="LittleEndian" header_type="UInt64">\n')
	file.write("<UnstructuredGrid>\n")
	file.write('<Piece NumberOfPoints="' + str(mesh_.Ns)+'" NumberOfCells="'+str(mesh_.Nt )+'">\n')
	file.write("<Points>\n")
	file.write('<DataArray NumberOfComponents="3" type="Float64">\n')
	for i in mesh_.Nodes:
		file.write(str(i.x) + " " + str(i.y) + " " + str(i.z))
		file.write('\n')

	file.write('</DataArray>\n</Points>\n<Cells>\n<DataArray type="Int32" Name="connectivity">\n')

	for i in range(0, mesh_.Nt):
		file.write(str(mesh_.Triangles[i].sommets[0]-1)+ " " + str(mesh_.Triangles[i].sommets[1]-1)+ " " + str(mesh_.Triangles[i].sommets[2]-1))
		file.write('\n')

	file.write('</DataArray>\n<DataArray type="Int32" Name="offsets">\n')

	for i in range(mesh_.Nt):
		file.write(str((i+1)*3) + '\n')

	file.write('</DataArray>\n<DataArray type="UInt8" Name="types">\n')

	for i in range(mesh_.Nt):
		file.write('5\n')

	file.write('</DataArray>\n</Cells>\n<PointData Scalars="solution">\n<DataArray type="Float64" Name="Real part" format="ascii">\n')
	for u in mesh_.U:
		file.write(str(np.real(u)) + "\n")
	file.write('</DataArray>\n')
	file.write('<DataArray type="Float64" Name="Imag part" format="ascii">\n')
	for u in mesh_.U:
		file.write(str(np.imag(u)) + "\n")
	file.write('</DataArray>\n')

	file.write('</PointData>\n</Piece>\n</UnstructuredGrid>\n</VTKFile>\n')
	file.close()


# Mesh creation from msh file:
our_mesh = read_file("smarin.msh")


# calculationg matrix A:
A = our_mesh.matrice_A()
print("------------------A--------------")
print(A)


# calculating b:
b = our_mesh.vector_b()
print("---------------b----------------")
print(b)

U = our_mesh.vector_U()

print("--------------Solution Real Part---------------")

print(np.real(U))



write_file(our_mesh)