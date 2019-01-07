# global useful vars

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
				#print(formats)

			elif property == "Nodes":
				i+=1
				line = content[i]
				#print ("---------->" + content[i][1:-1].split(" ")[0] + "-----\n")
				Number0fNodes = (int)(content[i][1:-1].split(" ")[0])
				i += 1;

				for j in range(i, i + Number0fNodes):
					print("j; "+ str(j) + "\n");
					print(content[j][0:-1].split(" "))
					Nodes[j - Number0fNodes] = content[j][0:-1].split(" ")[:4]
					print(Nodes)


			elif property == "Elements":
				q = 2
			else:
				a = 2



read_file("input_sample.msh")